import streamlit as st
import feedparser
from openai import OpenAI
import os

# --- Page Setup ---
st.set_page_config(page_title="AI Multi-Perspective News", layout="wide")
st.title("📰 AI Multi-Perspective News (Fact-Based)")
st.write(
    "This app fetches top headlines and generates a structured summary with verifiable facts "
    "and two different fact-based perspectives."
)

# --- OpenAI Setup ---
api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
if not api_key:
    st.error("No OpenAI API key found. Add it in Streamlit Cloud → App → Settings → Secrets.")
    st.stop()

client = OpenAI(api_key=api_key)

# --- RSS Feeds ---
RSS_FEEDS = [
    "https://rss.cnn.com/rss/edition.rss",
    "https://feeds.bbci.co.uk/news/rss.xml"
]

def fetch_articles(max_articles=3):
    """Fetch a few top articles from RSS feeds."""
    articles = []
    for feed in RSS_FEEDS:
        parsed = feedparser.parse(feed)
        for entry in parsed.entries[:max_articles]:
            articles.append({
                "title": entry.title,
                "link": entry.link,
                "summary": entry.get("summary", "")
            })
    return articles

def generate_fact_based_perspectives(article_text):
    """Generate fact-based summary with two factual viewpoints."""
    prompt = f"""
    You are a fact-focused analyst creating a multi-perspective news summary.

    1. List ONLY verifiable facts from the article.
    2. Then provide two different fact-based viewpoints, each backed by supporting facts.
    3. Do not speculate or add opinions. Only use factual information.

    Output format:

    ### Facts
    - Fact 1
    - Fact 2

    ### Viewpoint A
    - Fact-based perspective
    - Supporting fact(s)

    ### Viewpoint B
    - Fact-based perspective
    - Supporting fact(s)

    Article:
    {article_text}
    """
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.choices[0].message.content.strip()

# --- App Logic ---
articles = fetch_articles()

if articles:
    for art in articles:
        st.subheader(art["title"])
        st.markdown(f"[Read Full Article]({art['link']})")

        with st.spinner("Analyzing article..."):
            fact_perspectives = generate_fact_based_perspectives(art["summary"])
        
        st.markdown(fact_perspectives)
        st.markdown("---")
else:
    st.warning("No articles found. Try again later.")
