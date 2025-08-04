# Diderot AI: Multi-Perspective Daily News

A sophisticated Streamlit web application that generates factual, non-biased daily news reports with multi-perspective analysis using AG2 (AutoGen 2) multi-agent workflows.

## 🎯 Features

- **Multi-Agent Workflow**: 7 specialized AI agents working together
- **Multi-Perspective Analysis**: Left, Center, and Right perspectives for political/world news
- **Factual Reporting**: Neutral summaries with source verification
- **Daily Caching**: Reports cached by date to avoid regeneration
- **Beautiful UI**: Modern Streamlit interface with responsive design
- **Real-time RSS Integration**: Live news feeds from major sources

## 🤖 Agent Architecture

### 1. **HeadlineFinderAgent**
- Fetches top 10 trending headlines from Google News RSS
- Categorizes headlines as 'world', 'politics', or 'other'
- Filters for significant political and world issues

### 2. **ArticleFinderAgent**
- Gathers articles from across the political spectrum:
  - **Left**: CNN, New York Times, MSNBC
  - **Center**: Reuters, Associated Press, BBC News
  - **Right**: Fox News, New York Post, Wall Street Journal

### 3. **ResearchCompilerAgent**
- Extracts verifiable facts and opinions from articles
- Cross-references information across sources
- Identifies potential bias and editorial content

### 4. **DeterminatorAgent**
- Identifies solid facts consistent across multiple sources
- Maps sources to political perspectives
- Analyzes justifications and rationales

### 5. **FlawsAgent**
- Identifies potential logical fallacies
- Notes missing context or counterarguments
- Points out potential bias or selective reporting

### 6. **BirdsEyeAgent**
- Consolidates all perspectives into comprehensive view
- Names perspectives based on actual ideological stances
- Orders from Left → Center → Right when political

### 7. **JournalistAgent**
- Generates final factual reports
- Creates neutral summaries and multi-perspective analysis
- Ensures professional journalistic standards

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key
- (Optional) News API key for enhanced article fetching

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd diderot-ai
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Required
   export OPENAI_API_KEY="your-openai-api-key"
   
   # Optional (for enhanced article fetching)
   export NEWS_API_KEY="your-news-api-key"
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

### Configuration

The application uses a `config.py` file for all settings. Key configurations:

- **OpenAI Model**: Defaults to `gpt-4o`, can be changed via `OPENAI_MODEL` env var
- **Max Headlines**: Set to 10 (configurable in `Config.MAX_HEADLINES`)
- **Cache Duration**: 24 hours (configurable in `Config.CACHE_DURATION_HOURS`)

## 📊 Output Format

For each headline, the system generates:

1. **Factual Headline** - Neutral, accurate title
2. **Source Articles** - Links to all referenced articles
3. **Neutral Summary** - Objective factual summary
4. **Multi-Perspective Analysis** (for world/political issues):
   - Named perspectives (e.g., "Progressive Reform", "Conservative Traditional")
   - Justifications for each perspective
   - Potential flaws and missing context

## 🗂️ File Structure

```
diderot-ai/
├── app.py                 # Main Streamlit application
├── agents.py              # AG2 agent definitions
├── pipeline.py            # Multi-agent workflow orchestration
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── daily_reports/        # Cached reports (YYYY-MM-DD.json)
└── workspace/           # Agent workspace directory
```

## 🔧 Customization

### Adding New News Sources

Edit `config.py` to add new sources:

```python
NEWS_SOURCES = {
    "left": [
        # Add new left-leaning sources here
    ],
    "center": [
        # Add new centrist sources here
    ],
    "right": [
        # Add new right-leaning sources here
    ]
}
```

### Modifying Agent Behavior

Each agent's behavior is defined in `agents.py`. You can modify:

- System messages for different analysis approaches
- Output formats for different report structures
- Agent interaction patterns

### Custom RSS Feeds

Add new RSS feeds in `config.py`:

```python
RSS_FEEDS = {
    "your_feed": "https://your-rss-feed-url.com",
    # ... existing feeds
}
```

## 🚀 Deployment

### Streamlit Cloud

1. Push your code to GitHub
2. Connect your repository to [Streamlit Cloud](https://streamlit.io/cloud)
3. Set environment variables in Streamlit Cloud dashboard
4. Deploy!

### Local Production

```bash
# Install production dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY="your-key"

# Run with production settings
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

## 🔍 Troubleshooting

### Common Issues

1. **OpenAI API Key Error**
   - Ensure `OPENAI_API_KEY` is set correctly
   - Check API key permissions and billing

2. **RSS Feed Errors**
   - Some RSS feeds may be temporarily unavailable
   - System falls back to simulated headlines

3. **Agent Communication Errors**
   - Check network connectivity
   - Verify OpenAI API rate limits

### Debug Mode

Enable debug logging by setting:

```bash
export DEBUG=1
```

## 📈 Performance

- **Report Generation**: ~5-10 minutes for 10 headlines
- **Caching**: Reports cached for 24 hours
- **API Usage**: ~50-100 OpenAI API calls per report
- **Memory Usage**: ~500MB RAM during processing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **AG2 (AutoGen 2)** for multi-agent orchestration
- **Streamlit** for the web interface
- **OpenAI** for the language models
- **News sources** for providing RSS feeds

## 📞 Support

For issues and questions:

1. Check the troubleshooting section
2. Review the configuration options
3. Open an issue on GitHub
4. Check the logs in the Streamlit interface

---

**Diderot AI** - Bringing multi-perspective analysis to daily news consumption.