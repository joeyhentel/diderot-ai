import streamlit as st
import json
import os
from datetime import datetime, date
from simple_pipeline import SimpleNewsAnalysisPipeline
import time

# Page configuration
st.set_page_config(
    page_title="Diderot AI: Multi-Perspective Daily News",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .headline-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #1f77b4;
    }
    .perspective-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 3px solid #ff7f0e;
    }
    .left-perspective {
        border-left-color: #d62728;
    }
    .center-perspective {
        border-left-color: #2ca02c;
    }
    .right-perspective {
        border-left-color: #1f77b4;
    }
    .source-link {
        color: #1f77b4;
        text-decoration: none;
    }
    .source-link:hover {
        text-decoration: underline;
    }
    .loading-container {
        text-align: center;
        padding: 2rem;
    }
</style>
""", unsafe_allow_html=True)

def load_cached_report(date_str):
    """Load cached report for a specific date"""
    cache_file = f"daily_reports/{date_str}.json"
    if os.path.exists(cache_file):
        with open(cache_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def save_report(date_str, report_data):
    """Save report to cache"""
    os.makedirs("daily_reports", exist_ok=True)
    cache_file = f"daily_reports/{date_str}.json"
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)

def display_headline(headline_data, index):
    """Display a single headline with all its components"""
    with st.container():
        st.markdown(f"""
        <div class="headline-card">
            <h2>{index + 1}. {headline_data['title']}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Source Articles
        if headline_data.get('sources'):
            st.subheader("📰 Source Articles")
            for source in headline_data['sources']:
                st.markdown(f"- [{source['title']}]({source['url']}) ({source['source']})")
        
        # Neutral Summary
        if headline_data.get('neutral_summary'):
            st.subheader("📋 Neutral Factual Summary")
            st.write(headline_data['neutral_summary'])
        
        # Perspectives (only for world/political issues)
        if headline_data.get('perspectives') and headline_data['category'] in ['world', 'politics']:
            st.subheader("🔍 Multi-Perspective Analysis")
            
            for perspective in headline_data['perspectives']:
                # Determine perspective class for styling
                perspective_class = ""
                if 'left' in perspective['name'].lower():
                    perspective_class = "left-perspective"
                elif 'right' in perspective['name'].lower():
                    perspective_class = "right-perspective"
                elif 'center' in perspective['name'].lower():
                    perspective_class = "center-perspective"
                
                st.markdown(f"""
                <div class="perspective-card {perspective_class}">
                    <h4>🎯 {perspective['name']}</h4>
                    <p><strong>Justification:</strong> {perspective['justification']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if perspective.get('flaws'):
                    with st.expander(f"⚠️ Potential Flaws in {perspective['name']} Perspective"):
                        st.write(perspective['flaws'])
        
        st.divider()

def main():
    # Header
    st.markdown('<h1 class="main-header">Diderot AI: Multi-Perspective Daily News</h1>', unsafe_allow_html=True)
    
    # Sidebar for controls
    with st.sidebar:
        st.header("⚙️ Controls")
        
        # Date selection
        selected_date = st.date_input(
            "Select Date",
            value=date.today(),
            max_value=date.today()
        )
        
        # Force regenerate option
        force_regenerate = st.checkbox("Force Regenerate Report", value=False)
        
        # Generate button
        if st.button("🚀 Generate Today's Top 10 Headlines", type="primary"):
            st.session_state.generate_clicked = True
    
    # Main content area
    today_str = selected_date.strftime("%Y-%m-%d")
    
    # Check if we should generate or load from cache
    should_generate = (
        st.session_state.get('generate_clicked', False) or 
        force_regenerate or 
        not load_cached_report(today_str)
    )
    
    if should_generate:
        # Show loading state
        with st.spinner("🤖 AI agents are analyzing today's headlines..."):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Initialize pipeline
                pipeline = SimpleNewsAnalysisPipeline()
                
                # Generate report with progress updates
                status_text.text("🔍 Finding top headlines...")
                progress_bar.progress(10)
                
                status_text.text("📰 Gathering articles from multiple sources...")
                progress_bar.progress(30)
                
                status_text.text("🧠 Analyzing perspectives and compiling research...")
                progress_bar.progress(60)
                
                status_text.text("✍️ Generating final report...")
                progress_bar.progress(90)
                
                # Generate the report
                report_data = pipeline.generate_daily_report()
                
                # Save to cache
                save_report(today_str, report_data)
                
                progress_bar.progress(100)
                status_text.text("✅ Report generated successfully!")
                time.sleep(1)
                
                # Clear the generate flag
                st.session_state.generate_clicked = False
                
            except Exception as e:
                st.error(f"❌ Error generating report: {str(e)}")
                st.exception(e)
                return
    
    # Load and display the report
    report_data = load_cached_report(today_str)
    
    if report_data:
        # Display report metadata
        st.info(f"📅 Report for {selected_date.strftime('%B %d, %Y')} | Generated at {report_data.get('generated_at', 'Unknown time')}")
        
        # Display each headline
        for i, headline in enumerate(report_data.get('headlines', [])):
            display_headline(headline, i)
            
    else:
        st.warning("📭 No report found for the selected date. Click 'Generate Today's Top 10 Headlines' to create a new report.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.8rem;">
        <p>Diderot AI - Multi-Perspective News Analysis</p>
        <p>Powered by AG2 (AutoGen 2) Multi-Agent Workflows</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 