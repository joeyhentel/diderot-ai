try:
    import autogen
except ImportError:
    import pyautogen as autogen

from typing import List, Dict, Any
import json
import feedparser
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import os
from config import Config

# Get LLM configuration from config
llm_config = Config.get_llm_config()

class NewsAgents:
    """Container for all news analysis agents"""
    
    def __init__(self):
        self.setup_agents()
    
    def setup_agents(self):
        """Initialize all agents with their specific roles and configurations"""
        
        # HeadlineFinderAgent - Finds top trending headlines
        self.headline_finder = autogen.AssistantAgent(
            name="HeadlineFinderAgent",
            system_message="""You are a specialized news headline finder. Your task is to:
1. Fetch the top 10 trending headlines from Google News RSS feeds
2. Categorize each headline as 'world', 'politics', or 'other'
3. Focus on major news outlets and trending topics
4. Return results in JSON format: [{"title": "...", "category": "world|politics|other"}]

Use RSS feeds from Google News for different categories:
- World: https://news.google.com/rss/sections/topic/WORLD
- Politics: https://news.google.com/rss/sections/topic/POLITICS
- Top Stories: https://news.google.com/rss

Ensure headlines are current and significant. Avoid entertainment, sports, and local news unless they have major political/world implications.""",
            llm_config=llm_config
        )
        
        # ArticleFinderAgent - Finds articles from different political perspectives
        self.article_finder = autogen.AssistantAgent(
            name="ArticleFinderAgent",
            system_message="""You are a specialized article finder that gathers news from across the political spectrum. For each headline, find 1-2 relevant articles from each perspective:

LEFT PERSPECTIVE:
- CNN (https://www.cnn.com/services/rss/)
- New York Times (https://rss.nytimes.com/services/xml/rss/)

CENTER PERSPECTIVE:
- Reuters (https://feeds.reuters.com/Reuters/worldNews)
- Associated Press (https://feeds.ap.org/ap/english)

RIGHT PERSPECTIVE:
- Fox News (https://feeds.foxnews.com/foxnews/latest)
- New York Post (https://nypost.com/feed/)

Return results in JSON format:
[{"source": "CNN", "title": "...", "url": "...", "perspective": "left"}, ...]

Focus on articles that directly address the headline topic. Ensure diversity of perspectives.""",
            llm_config=llm_config
        )
        
        # ResearchCompilerAgent - Compiles research from all articles
        self.research_compiler = autogen.AssistantAgent(
            name="ResearchCompilerAgent",
            system_message="""You are a research compiler that analyzes articles to extract facts and opinions. For each article:

1. Extract VERIFIABLE FACTS (dates, numbers, quotes, events)
2. Identify OPINIONS/INTERPRETATIONS (editorial content, analysis, commentary)
3. Note the source's perspective and potential bias
4. Cross-reference facts across sources

Return results in JSON format:
{
  "CNN": {"facts": ["fact1", "fact2"], "opinions": ["opinion1", "opinion2"]},
  "Fox News": {"facts": ["fact1", "fact2"], "opinions": ["opinion1", "opinion2"]},
  ...
}

Be objective and thorough. Distinguish clearly between facts and interpretations.""",
            llm_config=llm_config
        )
        
        # DeterminatorAgent - Identifies solid truths and perspectives
        self.determinator = autogen.AssistantAgent(
            name="DeterminatorAgent",
            system_message="""You are a determinator that identifies solid truths and maps perspectives. Your tasks:

1. Identify FACTS that are consistent across multiple sources
2. Map each source to its political perspective (Left/Right/Center)
3. Identify the justification/rationale behind each perspective
4. Note any inconsistencies or contradictions

Return results in JSON format:
{
  "solid_facts": ["fact1", "fact2"],
  "perspectives": {
    "left": {"sources": ["CNN", "NYT"], "justification": "..."},
    "right": {"sources": ["Fox", "NYPost"], "justification": "..."},
    "center": {"sources": ["Reuters", "AP"], "justification": "..."}
  }
}

Be analytical and objective. Focus on policy positions and ideological differences.""",
            llm_config=llm_config
        )
        
        # FlawsAgent - Identifies potential flaws in each perspective
        self.flaws_agent = autogen.AssistantAgent(
            name="FlawsAgent",
            system_message="""You are a flaws analyst that identifies potential issues with each perspective. For each perspective:

1. Identify potential logical fallacies
2. Note missing context or counterarguments
3. Point out potential bias or selective reporting
4. Suggest what information might be missing

Return results in JSON format:
{
  "left_perspective": {"flaws": ["flaw1", "flaw2"], "missing_context": "..."},
  "right_perspective": {"flaws": ["flaw1", "flaw2"], "missing_context": "..."},
  "center_perspective": {"flaws": ["flaw1", "flaw2"], "missing_context": "..."}
}

Be constructive and analytical. Focus on helping readers understand limitations.""",
            llm_config=llm_config
        )
        
        # BirdsEyeAgent - Consolidates all perspectives
        self.birds_eye = autogen.AssistantAgent(
            name="BirdsEyeAgent",
            system_message="""You are a birds-eye analyst that consolidates all perspectives into a comprehensive view. Your tasks:

1. Name perspectives based on actual ideological/policy stances (not generic labels)
2. Order perspectives from Left → Center → Right when political
3. Synthesize justifications and identify flaws
4. Create a balanced overview

Return results in JSON format:
{
  "perspectives": [
    {
      "name": "Progressive Reform Perspective",
      "justification": "...",
      "flaws": ["..."],
      "position": "left"
    },
    {
      "name": "Centrist Pragmatic Perspective", 
      "justification": "...",
      "flaws": ["..."],
      "position": "center"
    },
    {
      "name": "Conservative Traditional Perspective",
      "justification": "...", 
      "flaws": ["..."],
      "position": "right"
    }
  ]
}

Use specific, descriptive names that reflect actual policy positions.""",
            llm_config=llm_config
        )
        
        # JournalistAgent - Generates final report
        self.journalist = autogen.AssistantAgent(
            name="JournalistAgent",
            system_message="""You are a professional journalist that creates the final news report. For each headline, create:

1. FACTUAL HEADLINE (neutral, accurate)
2. SOURCE LINKS (all articles used)
3. NEUTRAL SUMMARY (objective facts only)
4. MULTI-PERSPECTIVE ANALYSIS (if political/world issue)

Return results in JSON format:
{
  "title": "Factual Headline",
  "sources": [{"source": "CNN", "title": "...", "url": "..."}],
  "neutral_summary": "...",
  "perspectives": [
    {
      "name": "Perspective Name",
      "justification": "...",
      "flaws": ["..."]
    }
  ]
}

Write in clear, professional journalistic style. Be objective and balanced.""",
            llm_config=llm_config
        )
        
        # User proxy for orchestrating the workflow
        self.user_proxy = autogen.UserProxyAgent(
            name="UserProxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=10,
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
            code_execution_config={"work_dir": "workspace"},
            llm_config=llm_config
        )

class NewsDataFetcher:
    """Handles actual data fetching from RSS feeds and news sources"""
    
    @staticmethod
    def fetch_google_news_rss(category="top"):
        """Fetch headlines from Google News RSS"""
        rss_urls = {
            "top": "https://news.google.com/rss",
            "world": "https://news.google.com/rss/sections/topic/WORLD",
            "politics": "https://news.google.com/rss/sections/topic/POLITICS"
        }
        
        url = rss_urls.get(category, rss_urls["top"])
        try:
            feed = feedparser.parse(url)
            headlines = []
            
            for entry in feed.entries[:10]:  # Get top 10
                headlines.append({
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.get("published", ""),
                    "source": entry.get("source", {}).get("title", "Unknown")
                })
            
            return headlines
        except Exception as e:
            print(f"Error fetching RSS: {e}")
            return []
    
    @staticmethod
    def fetch_articles_for_headline(headline, max_articles=6):
        """Fetch articles from different sources for a given headline"""
        # This is a simplified version - in production, you'd use NewsAPI or similar
        # For now, we'll simulate finding articles
        
        sources = [
            {"name": "CNN", "perspective": "left", "base_url": "https://www.cnn.com"},
            {"name": "Fox News", "perspective": "right", "base_url": "https://www.foxnews.com"},
            {"name": "Reuters", "perspective": "center", "base_url": "https://www.reuters.com"},
            {"name": "Associated Press", "perspective": "center", "base_url": "https://apnews.com"},
            {"name": "New York Times", "perspective": "left", "base_url": "https://www.nytimes.com"},
            {"name": "New York Post", "perspective": "right", "base_url": "https://nypost.com"}
        ]
        
        articles = []
        for source in sources[:max_articles]:
            # Simulate finding a relevant article
            articles.append({
                "source": source["name"],
                "title": f"Article about: {headline}",
                "url": f"{source['base_url']}/article-{len(articles)}",
                "perspective": source["perspective"],
                "content": f"This is a simulated article about {headline} from {source['name']} perspective."
            })
        
        return articles
    
    @staticmethod
    def extract_article_content(url):
        """Extract content from article URL (simplified)"""
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text[:2000]  # Limit content length
        except Exception as e:
            print(f"Error extracting content from {url}: {e}")
            return "Content extraction failed"

# Initialize the agents
news_agents = NewsAgents()
data_fetcher = NewsDataFetcher() 