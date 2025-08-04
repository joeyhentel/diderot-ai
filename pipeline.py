import json
import os
from datetime import datetime
from typing import List, Dict, Any
from agents import news_agents, data_fetcher
import time

class NewsAnalysisPipeline:
    """Orchestrates the multi-agent workflow for news analysis"""
    
    def __init__(self):
        self.agents = news_agents
        self.data_fetcher = data_fetcher
        self.workspace_dir = "workspace"
        os.makedirs(self.workspace_dir, exist_ok=True)
    
    def generate_daily_report(self) -> Dict[str, Any]:
        """Generate the complete daily news report"""
        print("🚀 Starting daily news report generation...")
        
        # Step 1: Find top headlines
        headlines = self._find_top_headlines()
        print(f"📰 Found {len(headlines)} headlines")
        
        # Step 2: Process each headline
        processed_headlines = []
        for i, headline in enumerate(headlines):
            print(f"🔍 Processing headline {i+1}/{len(headlines)}: {headline['title'][:50]}...")
            
            try:
                processed_headline = self._process_headline(headline)
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
    
    def _find_top_headlines(self) -> List[Dict[str, str]]:
        """Find top 10 headlines using the HeadlineFinderAgent"""
        try:
            # First, fetch actual headlines from RSS
            raw_headlines = self.data_fetcher.fetch_google_news_rss("top")
            
            if not raw_headlines:
                # Fallback to simulated headlines if RSS fails
                raw_headlines = self._get_fallback_headlines()
            
            # Use the agent to categorize and filter headlines
            headlines_text = "\n".join([f"- {h['title']}" for h in raw_headlines[:15]])
            
            # Create a chat with the headline finder agent
            chat_result = self.agents.user_proxy.initiate_chat(
                self.agents.headline_finder,
                message=f"""Please analyze these headlines and return the top 10 most significant ones, categorized as 'world', 'politics', or 'other':

{headlines_text}

Focus on world and political issues. Return only valid JSON in this format:
[{{"title": "Headline text", "category": "world|politics|other"}}]""",
                max_turns=3
            )
            
            # Extract JSON from the response
            response_text = chat_result.chat_history[-1]["content"]
            headlines = self._extract_json_from_response(response_text)
            
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
            print(f"Error in headline finding: {e}")
            return self._get_fallback_headlines()[:10]
    
    def _process_headline(self, headline: Dict[str, str]) -> Dict[str, Any]:
        """Process a single headline through the entire pipeline"""
        headline_title = headline['title']
        category = headline.get('category', 'other')
        
        # Step 1: Find articles for this headline
        articles = self._find_articles_for_headline(headline_title)
        
        # Step 2: Compile research from articles
        research_data = self._compile_research(articles)
        
        # Step 3: Determine perspectives and facts
        if category in ['world', 'politics']:
            perspectives_data = self._analyze_perspectives(research_data, articles)
        else:
            perspectives_data = {"perspectives": []}
        
        # Step 4: Generate final report
        final_report = self._generate_final_report(
            headline_title, 
            articles, 
            research_data, 
            perspectives_data,
            category
        )
        
        return final_report
    
    def _find_articles_for_headline(self, headline: str) -> List[Dict[str, str]]:
        """Find articles from different sources for a headline"""
        try:
            # Use the data fetcher to get articles
            articles = self.data_fetcher.fetch_articles_for_headline(headline)
            
            # Use the article finder agent to enhance the results
            articles_text = "\n".join([f"- {a['source']}: {a['title']}" for a in articles])
            
            chat_result = self.agents.user_proxy.initiate_chat(
                self.agents.article_finder,
                message=f"""For this headline: "{headline}"

I have found these articles:
{articles_text}

Please analyze and return a JSON list of the most relevant articles with their sources and perspectives:
[{{"source": "Source Name", "title": "Article Title", "url": "URL", "perspective": "left|center|right"}}]""",
                max_turns=2
            )
            
            response_text = chat_result.chat_history[-1]["content"]
            enhanced_articles = self._extract_json_from_response(response_text)
            
            # Merge with original articles
            if enhanced_articles:
                return enhanced_articles
            return articles
            
        except Exception as e:
            print(f"Error finding articles: {e}")
            return self.data_fetcher.fetch_articles_for_headline(headline)
    
    def _compile_research(self, articles: List[Dict[str, str]]) -> Dict[str, Any]:
        """Compile research from all articles"""
        try:
            # Prepare article data for the research compiler
            articles_data = []
            for article in articles:
                articles_data.append({
                    "source": article['source'],
                    "title": article['title'],
                    "content": article.get('content', ''),
                    "perspective": article.get('perspective', 'unknown')
                })
            
            articles_text = json.dumps(articles_data, indent=2)
            
            chat_result = self.agents.user_proxy.initiate_chat(
                self.agents.research_compiler,
                message=f"""Please analyze these articles and extract facts and opinions:

{articles_text}

Return the analysis in JSON format:
{{
  "Source Name": {{"facts": ["fact1", "fact2"], "opinions": ["opinion1", "opinion2"]}},
  ...
}}""",
                max_turns=3
            )
            
            response_text = chat_result.chat_history[-1]["content"]
            research_data = self._extract_json_from_response(response_text)
            
            return research_data
            
        except Exception as e:
            print(f"Error compiling research: {e}")
            return {}
    
    def _analyze_perspectives(self, research_data: Dict[str, Any], articles: List[Dict[str, str]]) -> Dict[str, Any]:
        """Analyze perspectives and identify flaws"""
        try:
            # Step 1: Determine solid facts and perspectives
            research_text = json.dumps(research_data, indent=2)
            
            chat_result = self.agents.user_proxy.initiate_chat(
                self.agents.determinator,
                message=f"""Based on this research data:

{research_text}

Please identify solid facts and map perspectives. Return in JSON format:
{{
  "solid_facts": ["fact1", "fact2"],
  "perspectives": {{
    "left": {{"sources": ["source1"], "justification": "..."}},
    "right": {{"sources": ["source2"], "justification": "..."}},
    "center": {{"sources": ["source3"], "justification": "..."}}
  }}
}}""",
                max_turns=3
            )
            
            response_text = chat_result.chat_history[-1]["content"]
            determination_data = self._extract_json_from_response(response_text)
            
            # Step 2: Identify flaws in each perspective
            determination_text = json.dumps(determination_data, indent=2)
            
            chat_result = self.agents.user_proxy.initiate_chat(
                self.agents.flaws_agent,
                message=f"""Based on this perspective analysis:

{determination_text}

Please identify potential flaws in each perspective. Return in JSON format:
{{
  "left_perspective": {{"flaws": ["flaw1", "flaw2"], "missing_context": "..."}},
  "right_perspective": {{"flaws": ["flaw1", "flaw2"], "missing_context": "..."}},
  "center_perspective": {{"flaws": ["flaw1", "flaw2"], "missing_context": "..."}}
}}""",
                max_turns=3
            )
            
            response_text = chat_result.chat_history[-1]["content"]
            flaws_data = self._extract_json_from_response(response_text)
            
            # Step 3: Consolidate all perspectives
            all_data = {
                "determination": determination_data,
                "flaws": flaws_data
            }
            
            all_data_text = json.dumps(all_data, indent=2)
            
            chat_result = self.agents.user_proxy.initiate_chat(
                self.agents.birds_eye,
                message=f"""Based on this complete analysis:

{all_data_text}

Please consolidate all perspectives into a comprehensive view. Return in JSON format:
{{
  "perspectives": [
    {{
      "name": "Specific Perspective Name",
      "justification": "...",
      "flaws": ["..."],
      "position": "left|center|right"
    }}
  ]
}}""",
                max_turns=3
            )
            
            response_text = chat_result.chat_history[-1]["content"]
            consolidated_data = self._extract_json_from_response(response_text)
            
            return consolidated_data
            
        except Exception as e:
            print(f"Error analyzing perspectives: {e}")
            return {"perspectives": []}
    
    def _generate_final_report(self, headline: str, articles: List[Dict[str, str]], 
                             research_data: Dict[str, Any], perspectives_data: Dict[str, Any],
                             category: str) -> Dict[str, Any]:
        """Generate the final report for a headline"""
        try:
            # Prepare all data for the journalist agent
            report_data = {
                "headline": headline,
                "category": category,
                "articles": articles,
                "research": research_data,
                "perspectives": perspectives_data.get("perspectives", [])
            }
            
            report_text = json.dumps(report_data, indent=2)
            
            chat_result = self.agents.user_proxy.initiate_chat(
                self.agents.journalist,
                message=f"""Please create the final news report based on this data:

{report_text}

Return the final report in JSON format:
{{
  "title": "Factual Headline",
  "category": "world|politics|other",
  "sources": [{{"source": "Source", "title": "Title", "url": "URL"}}],
  "neutral_summary": "...",
  "perspectives": [
    {{
      "name": "Perspective Name",
      "justification": "...",
      "flaws": ["..."]
    }}
  ]
}}""",
                max_turns=3
            )
            
            response_text = chat_result.chat_history[-1]["content"]
            final_report = self._extract_json_from_response(response_text)
            
            return final_report
            
        except Exception as e:
            print(f"Error generating final report: {e}")
            return {
                "title": headline,
                "category": category,
                "sources": [],
                "neutral_summary": f"Analysis unavailable for: {headline}",
                "perspectives": []
            }
    
    def _extract_json_from_response(self, response_text: str) -> Any:
        """Extract JSON from agent response"""
        try:
            # Look for JSON in the response
            json_start = response_text.find('[')
            if json_start == -1:
                json_start = response_text.find('{')
            
            if json_start != -1:
                json_end = response_text.rfind(']') + 1
                if json_end == 0:
                    json_end = response_text.rfind('}') + 1
                
                json_str = response_text[json_start:json_end]
                return json.loads(json_str)
            else:
                # Try to parse the entire response as JSON
                return json.loads(response_text)
                
        except Exception as e:
            print(f"Error extracting JSON: {e}")
            print(f"Response text: {response_text[:200]}...")
            return []
    
    def _get_fallback_headlines(self) -> List[Dict[str, str]]:
        """Get fallback headlines if RSS fails"""
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