#!/usr/bin/env python3
"""
Test script to verify Diderot AI setup
"""

import sys
import os
from datetime import datetime

def test_imports():
    """Test that all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import streamlit
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import autogen
        print("✅ AutoGen imported successfully")
    except ImportError as e:
        print(f"❌ AutoGen import failed: {e}")
        return False
    
    try:
        import feedparser
        print("✅ Feedparser imported successfully")
    except ImportError as e:
        print(f"❌ Feedparser import failed: {e}")
        return False
    
    try:
        import requests
        print("✅ Requests imported successfully")
    except ImportError as e:
        print(f"❌ Requests import failed: {e}")
        return False
    
    try:
        from bs4 import BeautifulSoup
        print("✅ BeautifulSoup imported successfully")
    except ImportError as e:
        print(f"❌ BeautifulSoup import failed: {e}")
        return False
    
    try:
        from config import Config
        print("✅ Config imported successfully")
    except ImportError as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    try:
        from simple_pipeline import SimpleNewsAnalysisPipeline
        print("✅ Simple Pipeline imported successfully")
    except ImportError as e:
        print(f"❌ Simple Pipeline import failed: {e}")
        return False
    
    return True

def test_configuration():
    """Test configuration setup"""
    print("\n🔧 Testing configuration...")
    
    try:
        from config import Config
        
        # Test configuration validation
        status = Config.validate_config()
        
        if status["openai_configured"]:
            print("✅ OpenAI API key configured")
        else:
            print("⚠️  OpenAI API key not configured")
            print("   Set OPENAI_API_KEY environment variable")
        
        if status["news_api_configured"]:
            print("✅ News API key configured")
        else:
            print("ℹ️  News API key not configured (optional)")
        
        for warning in status["warnings"]:
            print(f"⚠️  {warning}")
        
        for error in status["errors"]:
            print(f"❌ {error}")
        
        return len(status["errors"]) == 0
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_data_fetcher():
    """Test RSS feed fetching"""
    print("\n📰 Testing RSS feed fetching...")
    
    try:
        from agents import data_fetcher
        
        # Test Google News RSS
        headlines = data_fetcher.fetch_google_news_rss("top")
        
        if headlines:
            print(f"✅ Successfully fetched {len(headlines)} headlines from Google News")
            print(f"   Sample: {headlines[0]['title'][:50]}...")
        else:
            print("⚠️  No headlines fetched (RSS may be temporarily unavailable)")
        
        return True
        
    except Exception as e:
        print(f"❌ RSS feed test failed: {e}")
        return False

def test_pipeline_initialization():
    """Test pipeline initialization"""
    print("\n🔗 Testing pipeline initialization...")
    
    try:
        from simple_pipeline import SimpleNewsAnalysisPipeline
        
        pipeline = SimpleNewsAnalysisPipeline()
        print("✅ Simple Pipeline initialized successfully")
        
        # Test fallback headlines
        fallback_headlines = pipeline._get_fallback_headlines()
        if fallback_headlines:
            print(f"✅ Fallback headlines available ({len(fallback_headlines)} headlines)")
        
        return True
        
    except Exception as e:
        print(f"❌ Pipeline test failed: {e}")
        return False



def test_directories():
    """Test required directories"""
    print("\n📁 Testing directories...")
    
    required_dirs = ["daily_reports", "workspace"]
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ {dir_name}/ directory exists")
        else:
            try:
                os.makedirs(dir_name, exist_ok=True)
                print(f"✅ Created {dir_name}/ directory")
            except Exception as e:
                print(f"❌ Failed to create {dir_name}/ directory: {e}")
                return False
    
    return True

def main():
    """Run all tests"""
    print("🧪 Diderot AI Setup Test")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_configuration),
        ("Data Fetcher", test_data_fetcher),
        ("Pipeline Initialization", test_pipeline_initialization),
        ("Directories", test_directories)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your Diderot AI setup is ready.")
        print("\nTo run the application:")
        print("   streamlit run app.py")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the issues above.")
        print("\nCommon solutions:")
        print("   1. Install missing dependencies: pip install -r requirements.txt")
        print("   2. Set OpenAI API key: export OPENAI_API_KEY='your-key'")
        print("   3. Check internet connection for RSS feeds")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 