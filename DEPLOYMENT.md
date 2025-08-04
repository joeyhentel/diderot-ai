# Deployment Guide: Diderot AI to Streamlit Cloud

This guide will help you deploy your Diderot AI application to Streamlit Cloud.

## 🚀 Prerequisites

1. **GitHub Account**: Your code must be in a GitHub repository
2. **Streamlit Cloud Account**: Sign up at [share.streamlit.io](https://share.streamlit.io)
3. **OpenAI API Key**: Get one from [OpenAI Platform](https://platform.openai.com/api-keys)

## 📋 Step-by-Step Deployment

### 1. Prepare Your Repository

Ensure your repository has the following structure:
```
diderot-ai/
├── app.py                 # Main Streamlit app
├── agents.py              # AG2 agents
├── pipeline.py            # Workflow orchestration
├── config.py              # Configuration
├── requirements.txt       # Dependencies
├── README.md             # Documentation
├── .gitignore            # Git ignore rules
└── daily_reports/        # Cache directory (will be created)
```

### 2. Push to GitHub

```bash
# Initialize git if not already done
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial Diderot AI deployment"

# Add your GitHub repository as remote
git remote add origin https://github.com/yourusername/diderot-ai.git

# Push to GitHub
git push -u origin main
```

### 3. Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud**: Visit [share.streamlit.io](https://share.streamlit.io)
2. **Sign in**: Use your GitHub account
3. **New App**: Click "New app"
4. **Repository**: Select your `diderot-ai` repository
5. **Main file path**: Enter `app.py`
6. **Python version**: Select Python 3.9 or higher
7. **Advanced settings**: Click "Advanced settings"

### 4. Configure Environment Variables

In the Advanced settings section, add these environment variables:

#### Required Variables:
```
OPENAI_API_KEY = your-actual-openai-api-key
```

#### Optional Variables:
```
OPENAI_MODEL = gpt-4o
NEWS_API_KEY = your-news-api-key
DEBUG = 0
```

### 5. Deploy

1. Click "Deploy!"
2. Wait for the build to complete (usually 2-5 minutes)
3. Your app will be available at `https://your-app-name.streamlit.app`

## 🔧 Configuration Options

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | ✅ Yes | - | Your OpenAI API key |
| `OPENAI_MODEL` | ❌ No | `gpt-4o` | Model to use for analysis |
| `NEWS_API_KEY` | ❌ No | - | News API key for enhanced fetching |
| `DEBUG` | ❌ No | `0` | Enable debug logging (1/0) |

### Streamlit Configuration

You can customize the Streamlit app by modifying `config.py`:

```python
STREAMLIT_CONFIG = {
    "page_title": "Your Custom Title",
    "page_icon": "📰",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Build Fails
- **Error**: "Module not found"
- **Solution**: Ensure all dependencies are in `requirements.txt`

#### 2. OpenAI API Errors
- **Error**: "OpenAI API key not configured"
- **Solution**: Check that `OPENAI_API_KEY` is set correctly in Streamlit Cloud

#### 3. Memory Issues
- **Error**: "Out of memory"
- **Solution**: The app uses ~500MB RAM. Consider upgrading your Streamlit Cloud plan.

#### 4. Timeout Errors
- **Error**: "Request timeout"
- **Solution**: Report generation takes 5-10 minutes. This is normal.

### Debug Mode

Enable debug mode to see detailed logs:

1. Set `DEBUG = 1` in environment variables
2. Redeploy the app
3. Check the logs in Streamlit Cloud dashboard

## 📊 Monitoring

### Streamlit Cloud Dashboard

Monitor your app in the Streamlit Cloud dashboard:

1. **App Status**: Check if the app is running
2. **Logs**: View real-time logs
3. **Usage**: Monitor API calls and performance
4. **Settings**: Modify environment variables

### Performance Metrics

- **Report Generation**: 5-10 minutes for 10 headlines
- **API Usage**: ~50-100 OpenAI calls per report
- **Memory Usage**: ~500MB during processing
- **Cache**: Reports cached for 24 hours

## 🔄 Updates

To update your deployed app:

1. **Make Changes**: Modify your code locally
2. **Commit & Push**: Push changes to GitHub
3. **Auto-Deploy**: Streamlit Cloud will automatically redeploy

```bash
git add .
git commit -m "Update description"
git push origin main
```

## 🛡️ Security

### API Key Security

- ✅ **Secure**: API keys are encrypted in Streamlit Cloud
- ✅ **Environment Variables**: Keys are not exposed in code
- ❌ **Don't**: Never commit API keys to GitHub

### Best Practices

1. **Use Environment Variables**: Never hardcode API keys
2. **Regular Updates**: Keep dependencies updated
3. **Monitor Usage**: Check OpenAI API usage regularly
4. **Backup**: Keep local copies of your code

## 📞 Support

### Streamlit Cloud Support

- **Documentation**: [docs.streamlit.io](https://docs.streamlit.io)
- **Community**: [discuss.streamlit.io](https://discuss.streamlit.io)
- **GitHub**: [github.com/streamlit/streamlit](https://github.com/streamlit/streamlit)

### Diderot AI Support

- **Issues**: Open an issue on your GitHub repository
- **Documentation**: Check the main README.md
- **Testing**: Run `python test_setup.py` locally

## 🎉 Success!

Once deployed, your Diderot AI app will:

- ✅ Generate daily news reports automatically
- ✅ Provide multi-perspective analysis
- ✅ Cache reports for 24 hours
- ✅ Work across all devices
- ✅ Scale automatically with usage

Your app URL will be: `https://your-app-name.streamlit.app`

---

**Happy Deploying! 🚀** 