## Description
This script processes a large JSON file to calibrate an industrial robot.  
It downloads the file (secured by an API key), separates math-based questions from open-ended questions, fixes any incorrect arithmetic results, and uses a Large Language Model (LLM) to answer the open-ended questions.

## Requirements
- Python 3.7+ (recommended 3.9+)
- Installed libraries listed in `requirements.txt` (e.g., `requests`, `beautifulsoup4`, `python-dotenv`, `openai`)
- Valid API key to download the file
- OpenAI API Key for LLM usage
