## Personal Research Assistant 
A simple Python tool that helps you quickly research any topic from the command line.
It searches the web, analyzes current results, and generates clear, concise summaries using state-of-the-art AI. 
Summaries are automatically saved with timestamps for easy organization and future reference.

This is a beginner-friendly command-line research assistant that:
- Accepts a topic
- Searches the web (Tavily API)
- Reads and analyzes results
- Summarizes  openAi
- Saves the summary to a timestamped text file

### 1) Prerequisites
- Python 3.9+
- an open ai key
- A Tavily Search API key

### 2) Get API Keys
- openai: create a key at `https://openai.com`
- Tavily: create a key at `https://tavily.com`

### 3) Setup
```bash
cd /Users/mac/AI/researchAssistant
cp .env.example .env
# edit .env and paste your keys

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4) Run
```bash
python src/main.py "quantum computing for beginners"
```

Optional flags:
- `--max-results 8` number of search results to analyze
- `--model gpt-4o-mini` openai model name

### 5) Project Structure
```
src/
  main.py          # CLI entrypoint and orchestration
  search.py        # Web search via Tavily
  summarize.py     # Summarization via openai 
  utils/
    io_utils.py    # Save summary to file
```

### 6) Notes
- Keys are loaded from `.env` via python-dotenv
- Summaries are written in `outputs/` as `<topic-slug>__YYYYmmdd-HHMMSS.txt`

