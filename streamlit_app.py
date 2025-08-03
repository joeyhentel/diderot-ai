import streamlit as st
import feedparser
import os
import json
import time
from collections import defaultdict
from openai import OpenAI

# --- Streamlit Setup ---
st.set_page_config(page_title="Diderot AI: Democratizing News :)", layout="wide")
st.title("Diderot AI: Democratizing News")
st.write("Fact-based summaries with perspectives across multiple sources.")

# --- User Input Layer ---
st.sidebar.header("🔎 Search a Topic")
user_topic = st.sidebar.text_input("Enter a topic to focus on (optional):").strip().lower()

# --- OpenAI Setup ---
api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
if not api_key:
    st.error("No OpenAI API key found. Add it in Streamlit Cloud → App → Settings → Secrets.")
    st.stop()

client = OpenAI(api_key=api_key)

# --- RSS Feeds ---
RSS_FEEDS = [
    "https://rss.cnn.com/rss/edition.rss",
    "https://moxie.foxnews.com/google-publisher/latest.xml",
    "https://feeds.reuters.com/reuters/topNews"
]

CACHE_FILE = "article_cache.json"

# --- Simple JSON Cache ---
def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)

cache = load_cache()

# --- Step 1: Fetch Articles ---
def fetch_articles(max_per_feed=5):
    articles = []
    for feed in RSS_FEEDS:
        parsed = feedparser.parse(feed)
        for entry in parsed.entries[:max_per_feed]:
            articles.append({
                "title": entry.title,
                "link": entry.link,
                "summary": entry.get("summary", ""),
                "source": feed
            })
    return articles

# --- Step 2: Cluster Articles by Simple Keywords ---
def cluster_by_keyword(articles):
    clusters = defaultdict(list)
    for art in articles:
        keywords = [w.lower().strip(".,!?") for w in art["title"].split() if len(w) > 4]
        for kw in keywords:
            clusters[kw].append(art)
    filtered = {k: v for k, v in clusters.items() if len({a["source"] for a in v}) >= 2}
    return filtered

# --- Step 3: AI Fact-Based Multi-Perspective Summary ---
def generate_fact_perspectives(topic, articles):
    combined_text = "\n\n".join([f"{a['source']} - {a['title']}: {a['summary']}" for a in articles])
    prompt = f"""
    You are a fact-focused analyst.

    Articles on topic: {topic}

    1. Extract only verifiable facts across all sources.
    2. Provide two different fact-based perspectives, each supported by facts.
    3. Output in this format:

    ### Facts
    - Fact 1
    - Fact 2

    ### Viewpoint A
    - Fact-based perspective A
    - Supporting facts

    ### Viewpoint B
    - Fact-based perspective B
    - Supporting facts

    Articles:
    {combined_text}
    """
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.choices[0].message.content.strip()

# --- Step 4: Render ---
articles = fetch_articles()
clusters = cluster_by_keyword(articles)

displayed = False

if not clusters:
    st.warning("No overlapping topics found across sources right now.")
else:
    for topic, group in list(clusters.items())[:10]:  # allow more clusters to search through
        # If user entered a topic, filter by keyword match
        if user_topic and user_topic not in topic:
            continue

        displayed = True
        st.subheader(f"Topic: {topic}")
        for art in group:
            st.markdown(f"- [{art['title']}]({art['link']})")

        # Cache key = topic + date
        today = time.strftime("%Y-%m-%d")
        cache_key = f"{topic}-{today}"

        if cache_key in cache:
            summary = cache[cache_key]
        else:
            with st.spinner("Analyzing topic across sources..."):
                summary = generate_fact_perspectives(topic, group)
                cache[cache_key] = summary
                save_cache(cache)

        st.markdown(summary)
        st.markdown("---")

if not displayed:
    st.info("No clustered topics matched your search today.")
