import streamlit as st
import feedparser
from openai import OpenAI
import os

# --- Page Setup ---
st.set_page_config(page_title="AI Multi-Perspective News", layout="wide")
st.title("📰 AI Multi-Perspective News")
st.write("Fetches top headlines and generates a neutral summary plus an opposing perspective using AI.")

# --- OpenAI Setup ---
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

def summarize_and_opposing(text):
    """Generate a neutral summary + opposing view."""
    prompt = f"""
    Summarize this news in 2 sentences (Neutral Summary).
    Then provide an opposing or alternative perspective in 2 sentences (Opposing View).
    Article: {text}
    """
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )
    return resp.choices[0].message.content.strip()

# --- App Logic ---
articles = fetch_articles()

if articles:
    for art in articles:
        st.subheader(art["title"])
        st.markdown(f"[Read Full Article]({art['link']})")
        ai_output = summarize_and_opposing(art["summary"])
        st.write(ai_output)
        st.markdown("---")
else:
    st.warning("No articles found. Try again later.")
