# AI Job Application Agent

An end-to-end job search automation system that fetches, filters, ranks, and tracks relevant job opportunities using resume-aware matching.

## Overview

This project automates the job discovery workflow by aggregating postings from external APIs, evaluating their relevance against a candidate's resume, and presenting ranked results in real time. High-quality matches are stored in Google Sheets for tracking and follow-up.

The goal is to reduce manual job search effort and surface the most relevant opportunities quickly.

---

## Demo


<img width="442.5" height="350.5" alt="image" src="https://github.com/user-attachments/assets/569aee2d-b926-42f9-ab69-a36050cd9621" />

*Real-time job scoring and ranking based on resume relevance*

---

## Features

- Multi-source job aggregation (Adzuna, optional JSearch)
- Intelligent filtering (removes senior / irrelevant roles)
- Resume-aware scoring based on skill matching
- Real-time streaming of results via FastAPI
- Persistent storage using Google Sheets
- Deduplication to avoid repeated jobs
- Simple frontend interface to trigger and view results

---

## Tech Stack

- **Backend:** FastAPI, Python  
- **APIs:** Adzuna Jobs API, JSearch (RapidAPI)  
- **Processing:** Rule-based filtering + heuristic scoring  
- **Storage:** Google Sheets API  
- **Frontend:** HTML, CSS, JavaScript  

---

## System Architecture

1. Fetch jobs from external APIs  
2. Deduplicate and filter results  
3. Extract relevant skills from job descriptions  
4. Compare with resume content  
5. Compute relevance score  
6. Stream results to frontend  
7. Store high-quality matches in Google Sheets  

---

## Scoring Logic

- Matches job-required skills with resume content  
- Applies normalization and basic synonym handling  
- Uses weighted scoring for core technical skills  
- Produces a capped score (0–95) to avoid overconfidence  

---

## Setup

### 1. Clone repository
```
git clone https://github.com/Gargi2305/ai-job-agent

cd ai-job-agent
```
### 2. Create virtual environment

```
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Add environment variables

Create a `.env` file:

```
RAPIDAPI_KEY=your_key
ADZUNA_APP_ID=your_id
ADZUNA_APP_KEY=your_key
```

---

### 5. Google Sheets Setup

- Create a Google Sheet (e.g., `JobPilot`)
- Enable **Google Sheets API** and **Google Drive API**
- Add `credentials.json` to project root (not committed)
- Share the sheet with the service account email

---

### 6. Run backend

```
uvicorn main:app --reload
```

---

### 7. Run frontend

Open `frontend/index.html` in a browser and click:


Run Job Search


---

## Output

- Jobs are streamed in real time on the UI  
- Each job includes a relevance score  
- High-scoring jobs are stored in Google Sheets  
- Duplicate jobs are automatically skipped  

---

## Example Workflow

- Run the system once or twice daily  
- Review top-ranked jobs instantly  
- Track shortlisted jobs in Google Sheets  
- Apply externally using provided links  

---

## Design Decisions

- Adzuna used as primary source for reliability  
- JSearch included as secondary source (rate-limited)  
- Google Sheets chosen for lightweight persistent tracking  
- Rule-based filtering to reduce noise before scoring  

---

## Future Improvements

- Embedding-based semantic similarity (LLMs / vector search)  
- Automated job alerts / scheduling  
- Auto-apply integrations  

---



## Author

Gargi Jain
