# AI Job Assistant

A Streamlit app I built to manage my own apprenticeship search. I apply to around 10 roles a week across data, cyber security, networking and software, and I needed one place to log every application, see whether I'm hitting my weekly target, and track which ones get a response.

I use it every week. It's being extended into an AI assistant that scores my CV against a job advert, pulls out the skills the employer is asking for, and drafts a tailored cover letter.

<!-- Add a screenshot here once you've taken one: ![App screenshot](screenshot.png) -->

## What it does now

* **Log applications** with company, role, date and status
* **Weekly progress** against a target of 10 applications
* **Response rate** across everything I've applied for
* **Update statuses** as applications move along (applied, interview, offer, rejected)

## Coming next

* [ ] Store my CV once inside the app
* [ ] Keyword extraction: pull the key skills and terms out of a job advert
* [ ] CV match score: a score out of 100 plus the skills I'm missing
* [ ] Cover letter draft tailored to each job
* [ ] Save every analysed job straight into the tracker with its match score

## Tech stack

| Part | Tool |
| --- | --- |
| Interface | Streamlit |
| Language | Python |
| Storage | SQLite |
| Data handling | pandas |
| AI (planned) | Claude or OpenAI API |

## Running it locally

```bash
git clone https://github.com/YOUR_USERNAME/ai-job-assistant.git
cd ai-job-assistant

python -m venv .venv
# Windows
.venv\Scripts\activate
# Mac / Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

The app opens in your browser. The SQLite database is created on first run and stays on your machine.

## Privacy and security

* The database holds personal application data, so it's excluded from the repo by `.gitignore`.
* API keys will live in a local `.env` file, which is also excluded. Nothing secret is ever committed.

## Why I built it

Applying at volume gets messy fast. Spreadsheets didn't show me the numbers I cared about, so I built a tool that does, and I'm using it to learn how to build and ship a real Python app end to end.
