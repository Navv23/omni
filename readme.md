
# Omni: Organized Media News Intelligence

**Omni** is a CLI news reporting tool for fetching, classifying, and emailing news digests using Google News and Gemini NLP.

## Features
- Fetches news from multiple sources (specalized or financial)
- Summarizes and classifies news using Gemini (Google Generative AI)
- Sends structured news digests via email

## Quick Start

1. **Install dependencies** (in your virtual environment):
	```bash
	pip install -e .
	```

2. **Set required environment variables:**
	- `GEMINI_API_KEY`: Your Google Gemini API key (for NLP)
	- `EMAIL_USERNAME`: Sender email address (Gmail recommended)
	- `EMAIL_PASSWORD`: App password for the sender email

	Example (Linux/macOS):
	```bash
	export GEMINI_API_KEY=your-gemini-api-key
	export EMAIL_USERNAME=your-email@gmail.com
	export EMAIL_PASSWORD=your-app-password
	```

3. **Run from CLI:**
	```bash
	python -m omni.main --search "Apple earnings" --time 1d --recipient you@example.com
	```
	Or, if installed as a script:
	```bash
	omni --search "Apple earnings" --time 1d --recipient you@example.com
	```

## CLI Arguments
| Argument      | Description                                 | Required | Example                |
|-------------- |---------------------------------------------|----------|------------------------|
| --search      | Search keyword(s) for news                  | Yes      | "Apple earnings"       |
| --time        | Time period (e.g., 1d, 7d, 1y)              | No       | 1d                     |
| --financial   | Only classify as financial news             | No       | --financial            |
| --recipient   | Recipient email address                     | Yes      | you@example.com        |


## Example Usage
```bash
python -m omni.main --search "stock market" --time 7d --financial --recipient you@example.com
```
```Note: Once omni is installed in your env, run omni --help in your terminal to get help!```

## Testing
Run simple tests:
```bash
python -m unittest discover src/omni/tests
```

## Project Structure
- `src/omni/core/` – News crawling and classification logic
- `src/omni/io/` – Email sending
- `src/omni/main.py` – CLI entry point
- `src/omni/jobs/service.py` – Service orchestration
- `src/omni/tests/` – Unit tests

---
## Author
- Navaneethan.ghanti@gmail.com

For issues or contributions, please open a GitHub issue or PR.