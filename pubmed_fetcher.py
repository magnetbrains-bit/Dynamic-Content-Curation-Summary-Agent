# -*- coding: utf-8 -*-

# --- Imports ---
import time
import xml.etree.ElementTree as ET
import os
import re
import json

import requests
import nltk
from rake_nltk import Rake

SumyLexRankSummarizer = None
try:
    from sumy.summarizers.lexrank import LexRankSummarizer as SumyLexRankSummarizer
except ImportError:
    try:
        from sumy.summarizers.lex_rank import LexRankSummarizer as SumyLexRankSummarizer
    except ImportError as e:
        print(f"Error importing LexRankSummarizer: {e}")

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.utils import get_stop_words

from sqlalchemy import create_engine, Column, String, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError


# --- Configuration ---
# Replace with your actual NCBI API Key
NCBI_API_KEY = "Your_API_key"

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
REQUEST_DELAY = 0.15
SEARCH_TERM = "AI in healthcare"
MAX_RESULTS = 100

SUMMARY_SENTENCE_COUNT = 3
KEYWORD_COUNT = 15

DATABASE_FILE = 'pubmed_articles.db'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, DATABASE_FILE)
DATABASE_URL = f'sqlite:///{DATABASE_PATH}'


# --- Helper Function ---
def check_and_download_nltk_data(resource):
    try:
        nltk.data.find(resource)
        return True
    except LookupError:
        print(f"NLTK resource '{resource}' not found. Attempting download...")
        try:
            import ssl
            try: _create_unverified_https_context = ssl._create_unverified_context
            except AttributeError: pass
            else: ssl._create_default_https_context = _create_unverified_https_context
            nltk.download(resource, quiet=True, raise_on_error=False)
            try: return nltk.data.find(resource) is not None
            except LookupError: return False
        except Exception as e:
            print(f"Error downloading '{resource}': {e}")
            return False

# --- Data Cleaning ---
def clean_text(text):
    if text is None: return ""
    text = str(text)
    text = text.replace('&', '&').replace('<', '<').replace('>', '>').replace('"', '"').replace('’', "'")
    clean = re.compile('<.*?>')
    text = re.sub(clean, '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# --- Data Fetching ---
def search_pubmed(term, max_results, api_key):
    print(f"Searching PubMed for: '{term}'...")
    esearch_url = f"{BASE_URL}esearch.fcgi?db=pubmed&term={term.replace(' ', '+')}&retmax={max_results}&usehistory=y&api_key={api_key}"
    try:
        response = requests.get(esearch_url)
        response.raise_for_status()
        root = ET.fromstring(response.text)
        pubmed_ids = [id_element.text for id_element in root.findall('.//IdList/Id')]
        webenv = root.findtext('WebEnv')
        query_key = root.findtext('QueryKey')
        print(f"Found {len(pubmed_ids)} articles.")
        return pubmed_ids, webenv, query_key
    except Exception as e:
        print(f"Error during ESearch: {e}")
        return [], None, None

def fetch_article_details_with_abstract(pubmed_ids, api_key):
    if not pubmed_ids: return []
    print(f"Fetching details for {len(pubmed_ids)} articles...")
    id_string = ",".join(pubmed_ids)
    efetch_url = f"{BASE_URL}efetch.fcgi?db=pubmed&id={id_string}&retmode=xml&rettype=abstract&api_key={api_key}"
    time.sleep(REQUEST_DELAY)
    article_details = []
    try:
        response = requests.get(efetch_url)
        response.raise_for_status()
        root = ET.fromstring(response.text)
        for pubmed_article in root.findall('.//PubmedArticle'):
            pmid = pubmed_article.findtext('.//MedlineCitation/PMID')
            article_title_element = pubmed_article.find('.//ArticleTitle')
            article_title = "".join(article_title_element.itertext()).strip() if article_title_element is not None else "N/A"
            abstract_text = ""
            abstract_elements = pubmed_article.findall('.//Abstract/AbstractText')
            for abs_elem in abstract_elements:
                label = abs_elem.get('Label')
                if label: abstract_text += f"**{label}:** "
                paragraph_text = "".join(abs_elem.itertext()).strip()
                abstract_text += paragraph_text + "\n" if paragraph_text else ""
            pub_date_element = pubmed_article.find('.//PubDate')
            year = pub_date_element.findtext('Year')
            month = pub_date_element.findtext('Month')
            day = pub_date_element.findtext('Day')
            medline_date = pub_date_element.findtext('MedlineDate')
            publication_date = f"{year}-{month}-{day}" if year and month and day else medline_date if medline_date else "N/A"
            article_details.append({'pmid': pmid, 'title': article_title, 'abstract': abstract_text.strip(), 'pub_date': publication_date})
        print(f"Successfully fetched details for {len(article_details)} articles.")
        return article_details
    except Exception as e:
        print(f"Error during EFetch: {e}")
        return []

# --- NLP Functions ---
def extract_keywords(text, num_keywords=10):
    if not text or not isinstance(text, str): return []
    if not check_and_download_nltk_data('tokenizers/punkt'): return []
    if not check_and_download_nltk_data('corpora/stopwords'): r = Rake()
    else:
         try: r = Rake(stopwords=nltk.corpus.stopwords.words('english'))
         except: r = Rake()
    try: r.extract_keywords_from_text(text)
    except: return []
    ranked_phrases = sorted(r.get_ranked_phrases_with_scores(), key=lambda item: item[0], reverse=True)
    return [phrase for score, phrase in ranked_phrases][:num_keywords]

def generate_summary(text, num_sentences=3):
    if not text or not isinstance(text, str): return ""
    if SumyLexRankSummarizer is None: return ""
    if not check_and_download_nltk_data('tokenizers/punkt'): return ""
    try: parser = PlaintextParser.from_string(text, Tokenizer("english"))
    except: return ""
    try:
        summarizer = SumyLexRankSummarizer()
        if check_and_download_nltk_data('corpora/stopwords'):
             summarizer.stop_words = get_stop_words("english")
    except: return ""
    try: summary_sentences = summarizer(parser.document, sentences_count=num_sentences)
    except: return ""
    return " ".join(str(sentence) for sentence in summary_sentences)

# --- Database Model ---
Base = declarative_base()
class Article(Base):
    __tablename__ = 'articles'
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    abstract = Column(Text)
    pub_date = Column(String)
    keywords = Column(JSON)
    summary = Column(Text)
    def __repr__(self): return f"<Article(id='{self.id}', title='{self.title[:50]}...')>"

# --- Database Operations ---
def create_database_tables(engine):
    print(f"Creating/checking tables in {DATABASE_FILE}...")
    try:
        db_exists = os.path.exists(DATABASE_PATH) and os.path.getsize(DATABASE_PATH) > 0
        if not db_exists:
             Base.metadata.create_all(engine)
             print("Database table(s) created.")
        else:
             print("Database file is not empty, assuming table exists.")
    except Exception as e:
        print(f"Error creating tables: {e}")

def store_articles(articles_data, engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    print(f"Attempting to store {len(articles_data)} articles...")
    stored_count, skipped_count, error_count = 0, 0, 0
    for article_data in articles_data:
        pmid = article_data.get('pmid')
        if not pmid: skipped_count += 1; continue
        try:
            existing = session.query(Article).filter_by(id=pmid).first()
            if existing: skipped_count += 1
            else:
                new_article = Article(id=pmid, title=article_data.get('title','N/A'), abstract=article_data.get('abstract','N/A'), pub_date=article_data.get('pub_date','N/A'), keywords=article_data.get('keywords',[]), summary=article_data.get('summary','N/A'))
                session.add(new_article)
                stored_count += 1
        except Exception as e: print(f"Error processing PMID {pmid}: {e}. Skipping."); error_count += 1
    try:
        session.commit()
        print(f"Storage committed. Stored: {stored_count}, Skipped: {skipped_count}, Errors: {error_count}")
    except Exception as e: print(f"Final commit error: {e}"); session.rollback()
    finally: session.close(); print("Session closed.")


# --- Main Execution ---
if __name__ == "__main__":
    if NCBI_API_KEY == "YOUR_GENERATED_API_KEY_HERE":
         print("Error: Please replace 'YOUR_GENERATED_API_KEY_HERE' with your actual NCBI API Key.")
    else:
        print("Checking NLTK resources...")
        punkt_available = check_and_download_nltk_data('tokenizers/punkt')
        stopwords_available = check_and_download_nltk_data('corpora/stopwords')
        if not (punkt_available and stopwords_available): print("\nWarning: Essential NLTK resources might be missing.")
        else: print("NLTK resources appear available.")
        if SumyLexRankSummarizer is None: print("\nWarning: Sumy LexRankSummarizer not imported. Skipping Summarization.")
        print("-" * 30)

        article_ids, webenv, query_key = search_pubmed(SEARCH_TERM, MAX_RESULTS, NCBI_API_KEY)

        if article_ids:
            articles_data = fetch_article_details_with_abstract(article_ids, NCBI_API_KEY)
            
            print("\n--- Sample Raw Data (First 2) ---")
            if articles_data: [print(json.dumps(a, indent=4)) for a in articles_data[:2]]

            print("\nCleaning data...")
            cleaned_articles_data = [ {'pmid':a.get("pmid"), 'title':clean_text(a.get("title")), 'abstract':clean_text(a.get("abstract")), 'pub_date':a.get("pub_date")} for a in articles_data ]
            print(f"Cleaning completed for {len(cleaned_articles_data)} articles.")

            print("\n--- Sample Cleaned Data (First 2) ---")
            if cleaned_articles_data: [print(json.dumps(a, indent=4)) for a in cleaned_articles_data[:2]]

            if punkt_available:
                 print(f"\nApplying Keyword Extraction ({KEYWORD_COUNT} keywords)...")
                 for article in cleaned_articles_data: article['keywords'] = extract_keywords(article.get("title","") + ". " + article.get("abstract",""), KEYWORD_COUNT)
                 print(f"Keyword extraction completed for {len(cleaned_articles_data)}.")
            else: print("\nSkipping Keyword Extraction.")

            if SumyLexRankSummarizer and punkt_available:
                 print(f"\nApplying Text Summarization ({SUMMARY_SENTENCE_COUNT} sentences)...")
                 for article in cleaned_articles_data: article['summary'] = generate_summary(article.get("abstract",""), SUMMARY_SENTENCE_COUNT)
                 print(f"Summarization completed for {len(cleaned_articles_data)}.")
            else: print("\nSkipping Text Summarization.")

            print("\n--- Sample Processed Data (First 2) ---")
            if cleaned_articles_data: [print(json.dumps(a, indent=4, ensure_ascii=False)) for a in cleaned_articles_data[:2]]

            print("\nStarting Data Storage...")
            if cleaned_articles_data:
                try:
                    engine = create_engine(DATABASE_URL)
                    create_database_tables(engine)
                    store_articles(cleaned_articles_data, engine)
                    print("Storage finished.")
                except Exception as e: print(f"Storage error: {e}")
            else: print("No data to store.")

            try:
                output_filename = "processed_pubmed_articles_full.json"
                with open(output_filename, "w", encoding="utf-8") as f: json.dump(cleaned_articles_data, f, indent=4, ensure_ascii=False)
                print(f"\nProcessed data saved to {output_filename}")
            except Exception as e: print(f"Error saving JSON: {e}")

            if DATABASE_FILE and os.path.exists(DATABASE_PATH):
                 print(f"\nFull pipeline completed. Data in: {DATABASE_FILE}")
            else: print(f"\nPipeline completed, but {DATABASE_FILE} might not exist or is empty.")

        else:
            print("No articles found or fetching failed.")