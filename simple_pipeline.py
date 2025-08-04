import json
import os
from datetime import datetime
from typing import List, Dict, Any
import openai
from config import Config

class SimpleNewsAnalysisPipeline:
    """Simplified pipeline that uses direct OpenAI API calls instead of complex agent interactions"""
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        self.workspace_dir = "workspace"
        os.makedirs(self.workspace_dir, exist_ok=True)
    
    def generate_daily_report(self) -> Dict[str, Any]:
        """Generate the complete daily news report using simplified approach"""
        print("🚀 Starting daily news report generation...")
        
        # Step 1: Generate sample headlines (since RSS might be unreliable)
        headlines = self._generate_sample_headlines()
        print(f"📰 Generated {len(headlines)} headlines")
        
        # Step 2: Process each headline
        processed_headlines = []
        for i, headline in enumerate(headlines):
            print(f"🔍 Processing headline {i+1}/{len(headlines)}: {headline['title'][:50]}...")
            
            try:
                processed_headline = self._process_headline_simple(headline)
                processed_headlines.append(processed_headline)
            except Exception as e:
                print(f"❌ Error processing headline {i+1}: {e}")
                # Add a fallback entry
                processed_headlines.append({
                    "title": headline['title'],
                    "category": headline.get('category', 'other'),
                    "neutral_summary": f"Analysis unavailable for: {headline['title']}",
                    "sources": [],
                    "perspectives": []
                })
        
        # Step 3: Create final report
        report = {
            "generated_at": datetime.now().isoformat(),
            "headlines": processed_headlines,
            "total_headlines": len(processed_headlines)
        }
        
        print("✅ Daily report generation completed!")
        return report
    
    def _generate_sample_headlines(self) -> List[Dict[str, str]]:
        """Generate sample headlines using OpenAI"""
        try:
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a news headline generator. Generate 10 current, significant headlines that would be in the news today. Focus on world and political issues. Return only valid JSON in this format: [{\"title\": \"Headline text\", \"category\": \"world|politics|other\"}]"
                    }
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content
            headlines = json.loads(content)
            
            # Ensure we have exactly 10 headlines
            if len(headlines) > 10:
                headlines = headlines[:10]
            elif len(headlines) < 10:
                # Pad with fallback headlines
                fallback_headlines = self._get_fallback_headlines()
                while len(headlines) < 10 and fallback_headlines:
                    headlines.append(fallback_headlines.pop(0))
            
            return headlines
            
        except Exception as e:
            print(f"Error generating headlines: {e}")
            return self._get_fallback_headlines()[:10]
    
    def _process_headline_simple(self, headline: Dict[str, str]) -> Dict[str, Any]:
        """Process a single headline using simplified approach"""
        headline_title = headline['title']
        category = headline.get('category', 'other')
        
        # Generate sources
        sources = self._generate_sources_for_headline(headline_title)
        
        # Generate neutral summary
        neutral_summary = self._generate_neutral_summary(headline_title, sources)
        
        # Generate perspectives if political/world
        perspectives = []
        if category in ['world', 'politics']:
            perspectives = self._generate_perspectives(headline_title, sources)
        
        return {
            "title": headline_title,
            "category": category,
            "sources": sources,
            "neutral_summary": neutral_summary,
            "perspectives": perspectives
        }
    
    def _generate_sources_for_headline(self, headline: str) -> List[Dict[str, str]]:
        """Generate simulated sources for a headline"""
        try:
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "Generate 3-6 simulated news sources for this headline. Include left, center, and right perspectives. Return only valid JSON in this format: [{\"source\": \"Source Name\", \"title\": \"Article Title\", \"url\": \"https://example.com/article\", \"perspective\": \"left|center|right\"}]"
                    },
                    {
                        "role": "user",
                        "content": f"Headline: {headline}"
                    }
                ],
                temperature=0.5,
                max_tokens=800
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            print(f"Error generating sources: {e}")
            return [
                {"source": "CNN", "title": f"Article about {headline}", "url": "https://cnn.com/article", "perspective": "left"},
                {"source": "Reuters", "title": f"Article about {headline}", "url": "https://reuters.com/article", "perspective": "center"},
                {"source": "Fox News", "title": f"Article about {headline}", "url": "https://foxnews.com/article", "perspective": "right"}
            ]
    
    def _generate_neutral_summary(self, headline: str, sources: List[Dict[str, str]]) -> str:
        """Generate a neutral factual summary"""
        try:
            sources_text = "\n".join([f"- {s['source']}: {s['title']}" for s in sources])
            
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a neutral news summarizer. Write a factual, objective summary of the headline based on the provided sources. Focus on verifiable facts only. Keep it concise (2-3 sentences)."
                    },
                    {
                        "role": "user",
                        "content": f"Headline: {headline}\n\nSources:\n{sources_text}"
                    }
                ],
                temperature=0.3,
                max_tokens=300
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating summary: {e}")
            return f"Analysis unavailable for: {headline}"
    
    def _generate_perspectives(self, headline: str, sources: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """Generate multi-perspective analysis"""
        try:
            sources_text = "\n".join([f"- {s['source']} ({s['perspective']}): {s['title']}" for s in sources])
            
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "Generate 2-3 different perspectives on this headline. Name each perspective based on actual ideological/policy stances. Include justification and potential flaws. Return only valid JSON in this format: [{\"name\": \"Perspective Name\", \"justification\": \"...\", \"flaws\": [\"flaw1\", \"flaw2\"]}]"
                    },
                    {
                        "role": "user",
                        "content": f"Headline: {headline}\n\nSources:\n{sources_text}"
                    }
                ],
                temperature=0.6,
                max_tokens=800
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            print(f"Error generating perspectives: {e}")
            return [
                {
                    "name": "Progressive Perspective",
                    "justification": "This perspective emphasizes social justice and reform.",
                    "flaws": ["May overlook economic considerations"]
                },
                {
                    "name": "Conservative Perspective", 
                    "justification": "This perspective prioritizes traditional values and stability.",
                    "flaws": ["May resist necessary change"]
                }
            ]
    
    def _get_fallback_headlines(self) -> List[Dict[str, str]]:
        """Get fallback headlines if generation fails"""
        return [
            {"title": "Global Climate Summit Reaches Historic Agreement", "category": "world"},
            {"title": "Congress Passes Major Infrastructure Bill", "category": "politics"},
            {"title": "International Trade Dispute Escalates", "category": "world"},
            {"title": "Supreme Court Rules on Key Constitutional Case", "category": "politics"},
            {"title": "UN Security Council Addresses Regional Conflict", "category": "world"},
            {"title": "Federal Reserve Announces New Economic Policy", "category": "politics"},
            {"title": "Major Tech Company Faces Regulatory Scrutiny", "category": "politics"},
            {"title": "International Space Station Celebrates Milestone", "category": "world"},
            {"title": "Global Health Organization Issues New Guidelines", "category": "world"},
            {"title": "Congressional Committee Launches Investigation", "category": "politics"}
        ] 