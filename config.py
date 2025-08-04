import os
from typing import Dict, Any

class Config:
    """Configuration management for the Diderot AI news analysis system"""
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
    
    # News API Configuration (optional, for enhanced article fetching)
    NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
    
    # Application Settings
    MAX_HEADLINES = 10
    MAX_ARTICLES_PER_HEADLINE = 6
    CACHE_DURATION_HOURS = 24
    
    # RSS Feed URLs
    RSS_FEEDS = {
        "google_news_top": "https://news.google.com/rss",
        "google_news_world": "https://news.google.com/rss/sections/topic/WORLD",
        "google_news_politics": "https://news.google.com/rss/sections/topic/POLITICS",
        "reuters_world": "https://feeds.reuters.com/Reuters/worldNews",
        "ap_news": "https://feeds.ap.org/ap/english",
        "cnn_rss": "https://www.cnn.com/services/rss/",
        "fox_news": "https://feeds.foxnews.com/foxnews/latest"
    }
    
    # News Sources by Perspective
    NEWS_SOURCES = {
        "left": [
            {"name": "CNN", "base_url": "https://www.cnn.com", "rss": "https://www.cnn.com/services/rss/"},
            {"name": "New York Times", "base_url": "https://www.nytimes.com", "rss": "https://rss.nytimes.com/services/xml/rss/"},
            {"name": "MSNBC", "base_url": "https://www.msnbc.com", "rss": "https://www.msnbc.com/feed/"}
        ],
        "center": [
            {"name": "Reuters", "base_url": "https://www.reuters.com", "rss": "https://feeds.reuters.com/Reuters/worldNews"},
            {"name": "Associated Press", "base_url": "https://apnews.com", "rss": "https://feeds.ap.org/ap/english"},
            {"name": "BBC News", "base_url": "https://www.bbc.com/news", "rss": "https://feeds.bbci.co.uk/news/rss.xml"}
        ],
        "right": [
            {"name": "Fox News", "base_url": "https://www.foxnews.com", "rss": "https://feeds.foxnews.com/foxnews/latest"},
            {"name": "New York Post", "base_url": "https://nypost.com", "rss": "https://nypost.com/feed/"},
            {"name": "Wall Street Journal", "base_url": "https://www.wsj.com", "rss": "https://feeds.wsj.com/wsj/"}
        ]
    }
    
    # LLM Configuration
    LLM_CONFIG = {
        "config_list": [
            {
                "model": OPENAI_MODEL,
                "api_key": OPENAI_API_KEY,
            }
        ],
        "temperature": 0.1,
        "max_tokens": 4000,
        "timeout": 120
    }
    
    # Streamlit Configuration
    STREAMLIT_CONFIG = {
        "page_title": "Diderot AI: Multi-Perspective Daily News",
        "page_icon": "📰",
        "layout": "wide",
        "initial_sidebar_state": "expanded"
    }
    
    @classmethod
    def validate_config(cls) -> Dict[str, Any]:
        """Validate configuration and return status"""
        status = {
            "openai_configured": bool(cls.OPENAI_API_KEY),
            "news_api_configured": bool(cls.NEWS_API_KEY),
            "warnings": [],
            "errors": []
        }
        
        if not cls.OPENAI_API_KEY:
            status["errors"].append("OpenAI API key not configured")
        elif cls.OPENAI_API_KEY == "your-api-key-here":
            status["warnings"].append("Using placeholder OpenAI API key")
        
        if not cls.NEWS_API_KEY:
            status["warnings"].append("News API key not configured (will use RSS feeds only)")
        
        return status
    
    @classmethod
    def get_llm_config(cls) -> Dict[str, Any]:
        """Get LLM configuration with validation"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OpenAI API key not configured. Please set OPENAI_API_KEY environment variable.")
        
        return cls.LLM_CONFIG.copy() 