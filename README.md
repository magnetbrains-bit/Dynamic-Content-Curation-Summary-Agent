
# 🧠 Dynamic Content Curation & Summary Agent: AI in Healthcare⚕️

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![requests](https://img.shields.io/badge/requests-1976D2?style=for-the-badge&logo=python&logoColor=white)](https://docs.python-requests.org/en/latest/)
[![NLTK](https://img.shields.io/badge/NLTK-30A14C?style=for-the-badge&logo=nltk&logoColor=white)](https://www.nltk.org/)
[![Sumy](https://img.shields.io/badge/Sumy-FF7043?style=for-the-badge&logoColor=white)](https://pypi.org/project/sumy/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-F37627?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)

An automated agent designed to intelligently discover, process, analyze, and present the latest content on Artificial Intelligence in Healthcare, transforming scattered information into curated, digestible insights.

---

## 📜 Table of Contents

*   [💡 The Idea: Navigating the Information Avalanche](#-the-idea-navigating-the-information-avalanche)
*   [💼 Why This Project Matters: Delivering Actionable Insights](#-why-this-project-matters-delivering-actionable-insights)
*   [🚀 Tech Stack](#-tech-stack--architecture)
*   [✨ Key Features](#-key-features)
*   [📂 Project Structure](#-project-structure)
*   [🏁 Getting Started](#-getting-started)
    *   [Prerequisites](#prerequisites)
    *   [Installation & Setup](#installation--setup)
*   [🔧 How It Works: Behind the Scenes](#-how-it-works-behind-the-scenes)
*   [🖼️ Visual Showcase: The Dashboard in Action](#-visual-showcase-the-dashboard-in-action)
*   [🔮 Future Improvements](#-future-improvements)
*   [📧 Contact](#-contact)
*   [⚖️ License](#️-license)

---

## 💡 The Idea: Navigating the Information Avalanche

Staying updated in a field as dynamic as AI in Healthcare means sifting through countless research papers, news articles, blogs, and reports daily. Traditional methods of manual browsing are inefficient and lead to information overload, making it hard to pinpoint crucial developments.

The core idea of this project is to build an **intelligent agent that cuts through the noise**. It automates the entire content pipeline, from discovering relevant information to processing it using Natural Language Processing (NLP) techniques to extract key insights, and finally presenting these insights in a clean, organized, and digestible format through a web dashboard. It transforms reactive searching and reading into a proactive system for knowledge acquisition.

## 💼 Why This Project Matters: Delivering Actionable Insights

This project addresses real-world needs for anyone (researchers, healthcare professionals, businesses) who needs to efficiently monitor advancements in AI in Healthcare.

*   **Saves Time & Effort:** Automates the laborious process of discovering and summarizing content, freeing up valuable time.
*   **Provides Quick Insights:** Delivers curated keywords and summaries, allowing users to grasp the main points of numerous articles at a glance.
*   **Enables Focused Exploration:** The dashboard provides basic search and filtering (with potential for more advanced options in future) to quickly find information on specific topics or entities.
*   **Demonstrates End-to-End Data Pipeline:** Showcases skills in data collection, cleaning, NLP, database management, and web visualization.
*   **Reduces Information Overload:** Presents information in a structured format rather than just a raw list of links.

---

## 🚀 Tech Stack & Architecture

The project is built using popular and powerful Python libraries, orchestrated through a logical data pipeline.

| Technology         | Role in Project                                                                                                |
| :----------------- | :------------------------------------------------------------------------------------------------------------- |
| **Python**         | 🐍 The main programming language for the entire pipeline logic.                                                |
| **Requests**       | 🌐 Used for making HTTP calls to interact with the PubMed E-utilities API for data retrieval.                  |
| **XML.etree.ElementTree** | 🌳 Python's built-in library for parsing the XML data received from the PubMed API response.                   |
| **Re**             | 🔍 Python's Regular Expressions module used within the data cleaning steps to remove patterns like HTML tags.   |
| **NLTK**           | 📚 (Natural Language Toolkit) Provides foundational tools like tokenizers and stopwords for NLP tasks. Requires downloading specific data. |
| **Rake-NLTK**      | ✨ A library utilizing NLTK for efficient, extractive Keyword Extraction based on phrase structure.            |
| **Sumy**           | 📝 A library for automatic text summarization, implementing various algorithms like LexRank (used here) for extractive summaries. |
| **SQLAlchemy**     | 🐘 A powerful SQL Toolkit and Object-Relational Mapper (ORM) used to interact with the database using Python objects. |
| **SQLite**         | 🗄️ A server-less, file-based SQL database engine used for easily storing the processed article data persistently. |
| **Streamlit**      | 📊 A framework to build interactive web applications (the dashboard) quickly using pure Python.                 |


## ✨ Key Features

*   **Targeted Data Fetching:** Gathers relevant data from the PubMed database based on a specific query.
*   **Robust Cleaning:** Handles XML parsing and cleans text from common noise and formatting issues.
*   **Intelligent Keyword Extraction:** Identifies crucial terms and phrases from article content.
*   **Concise Summarization:** Creates easy-to-read extractive summaries.
*   **Structured Persistent Storage:** Stores all article data and NLP results in a reliable SQLite database.
*   **Interactive Web Dashboard:** Allows users to browse and search the curated content via a web interface.
*   **Customizable Appearance:** Basic appearance customization via CSS injection in the Streamlit app.
*   **Efficient Data Loading:** Utilizes Streamlit's caching to load data from the database efficiently.

---

## 📂 Project Structure

The project is organized into a few key files:

```
dynamic-content-agent/
│
├── 🐍 pubmed_fetcher.py           # Script to fetch data, perform cleaning, NLP, and store in DB.
├── 📊 app.py                     # Streamlit web application script for the dashboard.
├── 🗄️ pubmed_articles.db        # The SQLite database file (created after running pubmed_fetcher.py).
├── 📄 requirements.txt          # List of Python dependencies (generated via `pip freeze > requirements.txt` after installing libs).
└── 📄 README.md                  # You are here!
```
*(Note: In the latest code shared, NLP functions are integrated into `pubmed_fetcher.py` for simplicity, instead of a separate `nlp_processor.py`)*

---

## 🏁 Getting Started

Follow these steps to set up and run the project on your local machine.

### Prerequisites

*   [Python 3.8+](https://www.python.org/downloads/)
*   A text editor

### Installation & Setup

1.  **Create Project Directory & Copy Files:**
    ```bash
    mkdir dynamic-content-agent
    cd dynamic-content-agent
    # Copy pubmed_fetcher.py, app.py (and optionally nlp_processor.py if keeping separate) here
    ```

2.  **Create and activate a Python Virtual Environment:**
    ```bash
    python -m venv venv
    # On Windows Command Prompt:
    # venv\Scripts\activate
    # On Windows PowerShell:
    .\venv\Scripts\activate
    # On macOS/Linux:
    # source venv/bin/activate
    ```
    *(Ensure `(venv)` appears on your terminal prompt)*

3.  **Install the required Python packages:**
    *   It's recommended to create a `requirements.txt` first:
        ```bash
        pip freeze > requirements.txt
        # Now, install all listed packages (or manually list: requests, beautifulsoup4, lxml, rake-nltk, nltk, sumy, SQLAlchemy, streamlit)
        pip install -r requirements.txt
        ```
    *   Alternatively, install manually:
        ```bash
        pip install requests beautifulsoup4 lxml rake-nltk nltk sumy SQLAlchemy streamlit
        ```


4.  **Download NLTK data:** Open a Python shell in your active venv and run the downloader. You specifically need `punkt` and `stopwords`.
    ```bash
    python
    >>> import nltk
    >>> nltk.download('punkt')
    >>> nltk.download('stopwords')
    >>> exit()
    ```
    *(The scripts also attempt downloads, but doing this manually first can prevent initial errors).*

5.  **Get your NCBI API Key:** Obtain a free API key from NCBI for higher request rates (recommended). Go to [NCBI Account](https://www.ncbi.nlm.nih.gov/account/) -> Settings -> API Key.
    *   Open `pubmed_fetcher.py` and update the `NCBI_API_KEY` variable near the top of the file with your generated key. **Do not share your API key publicly or commit it directly to public repositories in production code.**

## 🔧 How It Works: Behind the Scenes

### 💉 Data Acquisition from PubMed API

Instead of fragile web scraping, we leverage the official NCBI E-utilities API using the `requests` library. The `pubmed_fetcher.py` script:
1.  Uses the **`ESearch`** utility with a search query (`AI in healthcare`) to retrieve a list of unique article identifiers (PMIDs).
2.  Uses the **`EFetch`** utility with these PMIDs, requesting data in XML format with `rettype=abstract` to get titles, dates, and abstracts.
   *(This process adheres to NCBI rate limits using `time.sleep` and utilizes an API key for higher access limits).*

### 🧼 Data Cleaning and Preprocessing

The raw XML response is processed:
1.  **XML Parsing:** `xml.etree.ElementTree` is used to navigate the XML structure and extract text content from specific tags (PMID, ArticleTitle, AbstractText, PubDate).
2.  **Text Cleaning:** A custom `clean_text` function applies regular expressions (`re`) and string operations to remove HTML entities, stray tags, and standardize whitespace from the extracted text, making it ready for NLP.

### ✨ NLP Insights

The cleaned text (combined title and abstract) is processed to extract key insights:
1.  **Keyword Extraction:** The `rake-nltk` library identifies important terms and phrases by analyzing word frequency and relationships within the text. NLTK's `punkt` and `stopwords` data are utilized for this.
2.  **Text Summarization:** The `sumy` library, specifically the `LexRankSummarizer` (which also uses NLTK's `punkt` and `stopwords`), generates a concise extractive summary by selecting the most representative sentences from the abstract.

### 🗄️ Data Storage with SQLAlchemy & SQLite

The processed article data (including PMIDs, cleaned text, extracted keywords, and summaries) is stored persistently:
1.  **Database Choice:** SQLite is used for its zero-configuration, file-based nature, ideal for local development (`pubmed_articles.db`).
2.  **ORM:** `SQLAlchemy` maps a Python `Article` class to the database table structure, allowing interaction using Python objects.
3.  **Storage Process:** The script creates the database file and table (if they don't exist) and inserts each processed article as a row using SQLAlchemy sessions, checking for existing PMIDs to avoid duplicates.

### 📊 Interactive Dashboard with Streamlit

The `app.py` script powers the web interface:
1.  **Data Loading:** It uses SQLAlchemy to connect to `pubmed_articles.db` and fetch the stored articles.
2.  **Caching:** Streamlit's `@st.cache_resource` is used for the database engine, and `@st.cache_data` is used for fetching the data list, ensuring efficiency on app reruns (handling the unhashable engine parameter by prefixing with `_`).
3.  **UI:** Streamlit components like `st.title`, `st.text_input`, and `st.expander` structure the layout. Each article is displayed in an expandable section showing its summary, keywords, and abstract.
4.  **Interactivity:** User input in the `st.text_input` is used to filter the list of articles displayed on the fly (client-side filtering for moderate datasets).
5.  **Appearance:** Custom CSS injected via `st.markdown` is used to style the background and ensure text readability, adding a more polished look. Emojis are added to enhance visual intuition.

## 🖼️ Visual Showcase: The Dashboard in Action

See the agent's output come to life in the Streamlit dashboard.

1.  **Fetcher Output - Processed Sample (Keywords & Summary):** Verification of the data processed by the backend script before storage.
    <!-- Placeholder for screenshot: Terminal output showing sample data with keywords and summary from pubmed_fetcher.py -->
    a) **Searching**
    
    ![Screenshot 2025-07-01 065330](https://github.com/user-attachments/assets/bc5dc570-3d7a-4ee0-9b1a-62fbded0cca8)
    
    b) **Cleaning**
    
    ![Screenshot 2025-07-01 065342](https://github.com/user-attachments/assets/831e5058-8229-4a29-b17d-48ad8034874d)
    
    c) **Keyword Extraction**
    
    ![Screenshot 2025-07-01 065351](https://github.com/user-attachments/assets/885b41a7-9817-4dfa-ad24-082f613c06f1)
    
    d) **Summary**
    
    ![Screenshot 2025-07-01 065401](https://github.com/user-attachments/assets/56b813f6-daa3-43c2-a244-5f0afbbe8ec8)





3.  **Database Content Verification:** Confirming data is successfully stored in the SQLite database.
    <!-- Placeholder for screenshot: DB Browser for SQLite showing articles table content or sqlite3 terminal output -->
    ![Screenshot 2025-07-01 035532](https://github.com/user-attachments/assets/af391814-f3d5-4c52-a228-59f029c323cf)

    ![Screenshot 2025-07-01 065414](https://github.com/user-attachments/assets/7cf1ab0c-c4ca-4a7c-bc9e-be2c5ffe4bb7)


5.  **Streamlit Dashboard - Initial View:** The main dashboard with custom background and a list of article expanders.
    <!-- Placeholder for screenshot: Running Streamlit dashboard - initial view -->
    ![Screenshot 2025-07-01 065512](https://github.com/user-attachments/assets/f0a3b622-6bdc-446c-b4b1-435b7e32861c)

6.  **Streamlit Dashboard - Search Functionality:** Demonstrating the filtering capability by typing a query.
    <!-- Placeholder for screenshot: Streamlit dashboard with search query typed and filtered results shown -->
    ![Screenshot 2025-07-01 065547](https://github.com/user-attachments/assets/e3478b26-9561-4286-a3ef-e9a04642d91c)

7.  **Streamlit Dashboard - Expanded Article:** Viewing the detailed information (Summary, Keywords, Abstract) within an expanded article section.
    <!-- Placeholder for screenshot: Streamlit dashboard with one expander open -->
    ![Screenshot 2025-07-01 065613](https://github.com/user-attachments/assets/44563d99-2071-4d4c-9220-15eca7bd0831)

## 🔮 Future Improvements

This project provides a solid foundation for a content curation system. Here are exciting avenues for future development:

*   🔄 **Automated Scheduling:** Implement periodic execution of the data fetching/processing script (e.g., daily) using task schedulers (`cron`, Windows Task Scheduler) or workflow tools (Apache Airflow).
*   📊 **Advanced Dashboarding:** Add visualizations (e.g., article count over time, keyword frequency charts), multi-criteria filtering (date range, selecting keywords), and sorting options.
*   📚 **Expand Data Sources:** Integrate data from additional relevant APIs (e.g., health news APIs) or implement ethical web scraping for permissible news sites and blogs (using `Scrapy`).
*   🧠 **Advanced NLP:** Incorporate **Named Entity Recognition (NER)** to identify and extract mentions of organizations, people, technologies, diseases, etc., using libraries like `spaCy`. Explore **Topic Modeling (LDA)** using `gensim` to discover overarching themes. Investigate **Abstractive Summarization** with transformer models (e.g., Hugging Face `transformers`) for potentially higher quality summaries (may require GPU).
*   🔗 **Link Articles & Entities:** Create a more sophisticated database schema with relationships between articles, keywords, authors, journals, and entities identified by NER.
*   🐳 **Containerization:** Package the application using **Docker** for consistent environments and easier deployment.
*   ☁️ **Cloud Deployment:** Deploy the application (potentially containerized) to a cloud platform (e.g., AWS, Heroku) for public access and scalability, potentially migrating the database to a managed service (e.g., AWS RDS).
*   📈 **Monitoring & Logging:** Implement robust logging (`logging` module) and integrate with monitoring tools for better error tracking and application health checks.

---

## 📧 Contact

Feel free to reach out if you have questions or feedback!

*   Himanshu Raj
*   LinkedIn - https://www.linkedin.com/in/himanshu-raj-63a519287
*   GitHub - (https://github.com/magnetbrains-bit)
*   raj.himanshu8765@gmail.com

---
