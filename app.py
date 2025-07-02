# -*- coding: utf-8 -*-

# --- Built-in Imports ---
import os
import json

# --- Third-Party Imports ---
import streamlit as st
# SQLAlchemy Imports
from sqlalchemy import create_engine, Column, String, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError


# --- Database Configuration & Model ---
DATABASE_FILE = 'pubmed_articles.db'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, DATABASE_FILE)
DATABASE_URL = f'sqlite:///{DATABASE_PATH}'

# Create a base class for declarative models
Base = declarative_base()

# Define the Article model
class Article(Base):
    __tablename__ = 'articles'
    id = Column(String, primary_key=True) # PMID
    title = Column(String, nullable=False)
    abstract = Column(Text)
    pub_date = Column(String)
    keywords = Column(JSON) # Stored as JSON
    summary = Column(Text)

    def __repr__(self):
        return f"<Article(id='{self.id}', title='{self.title[:50]}...')>"

# --- Database Connection and Data Fetching Function ---

# Use Streamlit's caching for the database engine creation
@st.cache_resource
def get_database_engine():
    """Creates and returns the SQLAlchemy database engine."""
    print(f"Attempting to create database engine for: {DATABASE_URL}") # Terminal print
    # Check if the database file exists before creating engine
    if not os.path.exists(DATABASE_PATH):
         st.error(f"🚨 Database file not found at {DATABASE_PATH}. Please run pubmed_fetcher.py first.")
         print(f"Database file not found at {DATABASE_PATH}") # Print to terminal
         return None

    try:
        engine = create_engine(DATABASE_URL)
        print("Database engine created successfully.") # Terminal print
        return engine
    except Exception as e:
        st.error(f"🚨 Error creating database engine: {e}")
        print(f"Error creating database engine: {e}") # Also print to terminal
        return None

# Use Streamlit's caching for the data fetching function
@st.cache_data
def get_articles_from_db(_engine):
    """Fetches all articles from the database using the provided engine."""
    if _engine is None:
        return [] # Cannot fetch if engine failed to create

    try:
        # Create a session from the engine (using _engine)
        Session = sessionmaker(bind=_engine)
        session = Session()

        print("Fetching articles from the database using Streamlit cached function...") # Terminal print
        # Query all articles
        articles_from_db = session.query(Article).all()

        print(f"Successfully fetched {len(articles_from_db)} articles from DB.") # Terminal print

        # Convert SQLAlchemy objects to a list of dictionaries for easier handling/display in Streamlit
        articles_list_of_dicts = []
        for article in articles_from_db:
            keywords_data = article.keywords if article.keywords is not None else []
            # Ensure keywords are formatted as a string for simple display
            keywords_display = ", ".join(keywords_data) if isinstance(keywords_data, list) else str(keywords_data)

            articles_list_of_dicts.append({
                'id': article.id if article.id is not None else 'N/A',
                'title': article.title if article.title is not None else 'Untitled',
                'abstract': article.abstract if article.abstract is not None else 'No abstract.',
                'pub_date': article.pub_date if article.pub_date is not None else 'N/A',
                'keywords': keywords_display, # Display as joined string
                'summary': article.summary if article.summary is not None else 'No summary.',
            })

        session.close() # Close the session
        return articles_list_of_dicts

    except SQLAlchemyError as e:
        st.error(f"🚨 SQLAlchemy Error fetching data from database: {e}")
        print(f"SQLAlchemy Error fetching data from database: {e}") # Print to terminal
        return []
    except Exception as e:
        st.error(f"🚨 An unexpected error occurred while fetching data from the database: {e}")
        print(f"An unexpected error occurred while fetching data from the database: {e}") # Print to terminal
        return []


# --- Enhanced Streamlit App Layout ---

# Set page configuration
st.set_page_config(
    page_title="🏥 AI Healthcare Research Hub",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS styling
st.markdown("""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Main app styling */
.stApp {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    font-family: 'Inter', sans-serif;
    min-height: 100vh;
}

/* Header styling */
.main-header {
    text-align: center;
    padding: 2rem 0;
    background: rgba(30, 30, 50, 0.9);
    border-radius: 20px;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.main-header h1 {
    color: #ffffff;
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.main-header p {
    color: #e0e6ed;
    font-size: 1.1rem;
    font-weight: 400;
    margin: 0;
}

/* Stats container */
.stats-container {
    display: flex;
    justify-content: center;
    gap: 2rem;
    margin: 1.5rem 0;
    flex-wrap: wrap;
}

.stat-card {
    background: rgba(20, 20, 35, 0.95);
    padding: 1.5rem;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    min-width: 150px;
}

.stat-number {
    font-size: 2rem;
    font-weight: 700;
    color: #64b5f6;
    display: block;
}

.stat-label {
    font-size: 0.9rem;
    color: #e0e6ed;
    margin-top: 0.5rem;
    font-weight: 500;
}

/* Search section styling */
.search-section {
    background: rgba(20, 20, 35, 0.95);
    padding: 2rem;
    border-radius: 20px;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

/* Search input styling */
.stTextInput > div > div > input {
    background: rgba(40, 40, 60, 0.9) !important;
    border: 2px solid #4a5568 !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
    font-size: 1rem !important;
    color: #ffffff !important;
    transition: all 0.3s ease !important;
}

.stTextInput > div > div > input:focus {
    border-color: #64b5f6 !important;
    box-shadow: 0 0 0 3px rgba(100, 181, 246, 0.2) !important;
}

.stTextInput > div > div > input::placeholder {
    color: #a0aec0 !important;
}

.stTextInput label {
    color: #ffffff !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
    margin-bottom: 0.5rem !important;
}

/* Article cards container */
.articles-container {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

/* Enhanced expander styling */
.stExpander {
    background: rgba(20, 20, 35, 0.95) !important;
    border-radius: 15px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
    backdrop-filter: blur(10px) !important;
    margin-bottom: 1rem !important;
    overflow: hidden !important;
}

.stExpander > div:first-child {
    background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%) !important;
    padding: 1.5rem !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
    margin: 0 !important;
}

.stExpander > div:first-child > div {
    color: #ffffff !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
    line-height: 1.4 !important;
}

.stExpander div[data-testid="stExpanderDetails"] {
    background: rgba(30, 30, 50, 0.98) !important;
    padding: 2rem !important;
    margin: 0 !important;
}

.stExpander div[data-testid="stExpanderDetails"] p {
    color: #e0e6ed !important;
    line-height: 1.6 !important;
    margin-bottom: 1rem !important;
}

.stExpander div[data-testid="stExpanderDetails"] strong {
    color: #ffffff !important;
    font-weight: 600 !important;
}

.stExpander div[data-testid="stExpanderDetails"] code {
    background: rgba(100, 181, 246, 0.2) !important;
    color: #64b5f6 !important;
    padding: 2px 6px !important;
    border-radius: 4px !important;
    font-size: 0.9rem !important;
}

/* Info sections within expanders */
.info-section {
    background: rgba(40, 40, 60, 0.8);
    padding: 1rem;
    border-radius: 10px;
    margin: 1rem 0;
    border-left: 4px solid #64b5f6;
}

/* Success and error message styling */
.stSuccess > div {
    background-color: rgba(34, 139, 34, 0.2) !important;
    color: #90EE90 !important;
    border: 1px solid rgba(34, 139, 34, 0.3) !important;
}

.stInfo > div {
    background-color: rgba(100, 181, 246, 0.2) !important;
    color: #87CEEB !important;
    border: 1px solid rgba(100, 181, 246, 0.3) !important;
}

.stWarning > div {
    background-color: rgba(255, 193, 7, 0.2) !important;
    color: #FFE55C !important;
    border: 1px solid rgba(255, 193, 7, 0.3) !important;
}

.stError > div {
    background-color: rgba(220, 53, 69, 0.2) !important;
    color: #FF6B8A !important;
    border: 1px solid rgba(220, 53, 69, 0.3) !important;
}

/* Separator styling */
hr {
    border: none !important;
    height: 2px !important;
    background: linear-gradient(90deg, transparent, #64b5f6, transparent) !important;
    margin: 2rem 0 !important;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
    .main-header h1 {
        font-size: 2rem;
    }
    
    .stats-container {
        flex-direction: column;
        align-items: center;
    }
    
    .stat-card {
        width: 100%;
        max-width: 200px;
    }
    
    .stExpander > div:first-child {
        padding: 1rem !important;
    }
    
    .stExpander div[data-testid="stExpanderDetails"] {
        padding: 1.5rem !important;
    }
}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 12px;
}

::-webkit-scrollbar-track {
    background: rgba(20, 20, 35, 0.5);
    border-radius: 6px;
}

::-webkit-scrollbar-thumb {
    background: rgba(100, 181, 246, 0.6);
    border-radius: 6px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(100, 181, 246, 0.8);
}

/* Additional dark theme fixes */
.stMarkdown {
    color: #e0e6ed !important;
}

.stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
    color: #ffffff !important;
}

/* Fix for column headers and other elements */
div[data-testid="column"] h3 {
    color: #ffffff !important;
}

/* Ensure all text in markdown is visible */
.stMarkdown p, .stMarkdown div, .stMarkdown span {
    color: #e0e6ed !important;
}

/* Style for code blocks and inline code */
.stMarkdown code {
    background: rgba(100, 181, 246, 0.2) !important;
    color: #64b5f6 !important;
    padding: 2px 6px !important;
    border-radius: 4px !important;
}

/* Center content styling for empty states */
div[style*="text-align: center"] {
    background: rgba(20, 20, 35, 0.95) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
}

div[style*="text-align: center"] h3 {
    color: #ffffff !important;
}

div[style*="text-align: center"] p {
    color: #e0e6ed !important;
}

div[style*="text-align: center"] code {
    background: rgba(100, 181, 246, 0.2) !important;
    color: #64b5f6 !important;
}
</style>
""", unsafe_allow_html=True)

# Main header with enhanced styling
st.markdown("""
<div class="main-header">
    <h1>🤖🏥 AI in Healthcare: Curated Content Dashboard 📈</h1>
    <p>🔬 Curated PubMed Articles & Research Insights</p>
</div>
""", unsafe_allow_html=True)

# Get the database engine (cached resource)
engine = get_database_engine()

# Check if the engine was successfully created before fetching data
if engine:
    # Fetch data using the cached function
    all_articles_data = get_articles_from_db(engine)

    if all_articles_data:
        # Display stats
        st.markdown(f"""
        <div class="stats-container">
            <div class="stat-card">
                <span class="stat-number">{len(all_articles_data)}</span>
                <div class="stat-label">📚 Total Articles</div>
            </div>
            <div class="stat-card">
                <span class="stat-number">{len(set(article.get('pub_date', 'N/A')[:4] for article in all_articles_data if article.get('pub_date') != 'N/A'))}</span>
                <div class="stat-label">📅 Publication Years</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Search section with enhanced styling
        st.markdown('<div class="search-section">', unsafe_allow_html=True)
        
        st.markdown("### 🔍 Search Articles")
        search_query = st.text_input(
            "Search across titles, abstracts, and keywords:",
            "",
            help="💡 Enter keywords to find relevant research articles",
            placeholder="e.g., machine learning, diagnosis, treatment..."
        )
        
        st.markdown('</div>', unsafe_allow_html=True)

        # Filter articles based on search query (case-insensitive)
        if search_query:
            search_query_lower = search_query.lower()
            filtered_articles = [
                article for article in all_articles_data
                if search_query_lower in article.get('title', '').lower()
                or search_query_lower in article.get('abstract', '').lower()
                or (article.get('keywords') and search_query_lower in article.get('keywords', '').lower())
            ]
            
            if filtered_articles:
                st.success(f"🎯 Found {len(filtered_articles)} articles matching your search!")
            else:
                st.warning(f"🔍 No articles found matching '{search_query}'. Try different keywords.")
        else:
            filtered_articles = all_articles_data

        # Display Articles
        if filtered_articles:
            st.markdown("### 📖 Research Articles")
            
            # Create articles container
            st.markdown('<div class="articles-container">', unsafe_allow_html=True)
            
            for i, article in enumerate(filtered_articles, 1):
                # Create unique expander title with emoji and numbering
                expander_title = f"📄 **{article.get('title', 'Untitled')}**"
                
                with st.expander(expander_title, expanded=False):
                    # Article metadata
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**🆔 PMID:** `{article.get('id', 'N/A')}`")
                    with col2:
                        st.markdown(f"**📅 Published:** {article.get('pub_date', 'N/A')}")
                    
                    st.markdown("---")
                    
                    # Summary section
                    st.markdown("**📋 Summary:**")
                    summary_text = article.get('summary', 'No summary available.')
                    if summary_text != 'No summary available.':
                        st.markdown(f"💡 {summary_text}")
                    else:
                        st.info("🤷‍♂️ No summary available for this article.")
                    
                    # Keywords section
                    st.markdown("**🏷️ Keywords:**")
                    keywords = article.get('keywords', 'No keywords available.')
                    if keywords and keywords != 'No keywords available.':
                        keyword_list = keywords.split(', ')
                        keyword_badges = ' '.join([f"`{keyword.strip()}`" for keyword in keyword_list if keyword.strip()])
                        st.markdown(f"🔖 {keyword_badges}")
                    else:
                        st.info("🤷‍♂️ No keywords available for this article.")
                    
                    # Abstract section
                    st.markdown("**📝 Abstract:**")
                    abstract = article.get('abstract', 'No abstract available.')
                    if abstract != 'No abstract available.':
                        st.markdown(f"📖 {abstract}")
                    else:
                        st.info("🤷‍♂️ No abstract available for this article.")
                
                # Add visual separator between articles
                if i < len(filtered_articles):
                    st.markdown("---")
            
            st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.markdown("""
            <div style="text-align: center; padding: 3rem; background: rgba(255, 255, 255, 0.9); border-radius: 20px; margin: 2rem 0;">
                <h3>🔍 No Articles Found</h3>
                <p>Try adjusting your search terms or clear the search to see all articles.</p>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: rgba(255, 255, 255, 0.9); border-radius: 20px; margin: 2rem 0;">
            <h3>📚 No Articles Available</h3>
            <p>🚀 Please run <code>pubmed_fetcher.py</code> first to populate the database with research articles.</p>
        </div>
        """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div style="text-align: center; padding: 3rem; background: rgba(255, 255, 255, 0.9); border-radius: 20px; margin: 2rem 0;">
        <h3>🚨 Database Connection Error</h3>
        <p>Unable to connect to the database. Please check if the database file exists and try again.</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; padding: 2rem; margin-top: 3rem; color: rgba(255, 255, 255, 0.9);">
    <p>🏥 AI Healthcare Research Hub | 🔬 Powered by PubMed & AI</p>
</div>
""", unsafe_allow_html=True)