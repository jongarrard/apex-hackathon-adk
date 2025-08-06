# Apex Hackathon - Google ADK AI Agents

This repository contains AI agents built with Google's Agent Development Kit (ADK) for our hackathon project.

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Git
- Google Cloud account (for ADK)

### Setup Instructions

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone <your-repo-url>
   cd apex-hackathon-adk
   ```

2. **Run the automated setup**:
   ```bash
   python3 setup.py
   ```
   This will:
   - Create a virtual environment
   - Install all dependencies
   - Set up the project for development

3. **Activate your virtual environment**:
   ```bash
   source .venv/bin/activate
   ```
   Or use the provided script:
   ```bash
   source ./activate_venv.sh
   ```

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

5. **Run the agent** (choose one):
   
   **🚀 FastAPI Server** (for API endpoints):
   ```bash
   adk api_server
   ```
   
   **🌐 Web UI** (interactive chat interface):
   ```bash
   adk web
   ```
   
   **💬 Terminal Chat** (command line):
   ```bash
   adk run multi_tool_agent
   ```

## 📁 Project Structure

```
apex-hackathon-adk/
├── multi_tool_agent/          # Main agent package
│   ├── __init__.py           # Makes it a Python package
│   ├── __main__.py           # Entry point (allows python -m multi_tool_agent)
│   ├── agent.py              # Agent configuration
│   └── tools.py              # Agent tools
├── .env.example              # Environment variables template
├── .gitignore               # Git ignore rules
├── requirements.txt         # Python dependencies
├── pyproject.toml          # Project configuration
├── setup.py                # Automated setup script
├── dev.py                  # Development helper script
└── README.md               # This file
```

## 🛠️ Development

### Adding New Tools

1. Add your tool function to `multi_tool_agent/tools.py`
2. Import and add it to the agent in `multi_tool_agent/agent.py`
3. Run the agent to test your changes!

### Code Formatting

```bash
# Format code
black .

# Check code style
flake8

# Type checking
mypy multi_tool_agent/
```

## 📚 Resources

- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [ADK Quickstart Guide](https://google.github.io/adk-docs/get-started/quickstart/)
- [Python Best Practices](https://docs.python-guide.org/)

## 🤝 Team Collaboration

### Git Workflow

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Run tests: `pytest`
4. Commit: `git commit -m "Add your feature"`
5. Push: `git push origin feature/your-feature-name`
6. Create a pull request

### Environment Setup for New Team Members

1. Make sure you have Python 3.9+ installed
2. Run `python3 setup.py` - it handles everything!
3. Copy `.env.example` to `.env` and fill in your API keys
4. You're ready to code! 🎉

## 🔧 Troubleshooting

### Common Issues

**"Module not found" errors:**
- Make sure your virtual environment is activated
- Run `pip install -e .` to install the project in development mode

**Virtual environment issues:**
- Delete `.venv` folder and run `python3 setup.py` again
- Make sure you're using Python 3.9 or higher

## 📝 Notes

- The project uses modern Python features (3.9+)
- Code is formatted with Black and linted with Flake8
- Type hints are encouraged for better code quality
- All dependencies are pinned for reproducible builds
