# AI Job Application Agent

An end-to-end system that automates job discovery, ranking, and application preparation using LLMs and Retrieval-Augmented Generation (RAG).

## 🚀 Features

- 🔍 Multi-source job aggregation (JSearch + Adzuna APIs)
- 🧠 Semantic job matching using skill extraction and contextual scoring
- 📄 Automated resume tailoring using RAG (FAISS-based retrieval)
- ✉️ LLM-powered cover letter generation
- ⚡ Intelligent filtering, deduplication, and caching to optimize performance
- 📊 Ranked job results based on candidate-job fit score

---

## 🏗️ Architecture

Pipeline:

1. Fetch jobs from APIs  
2. Deduplicate + filter irrelevant roles  
3. Extract skills from JD  
4. Retrieve relevant resume chunks (RAG)  
5. Compute match score  
6. Generate tailored resume + cover letter  
7. Rank and output top jobs  

---

## 🛠️ Tech Stack

- Backend: Python, FastAPI  
- LLM Integration  
- Vector Search: FAISS  
- APIs: JSearch, Adzuna  
- Processing: Modular pipeline (RAG, scoring, parsing)

---

## ⚙️ Setup

```
git clone https://github.com/Gargi2305/ai-job-agent.git  
cd ai-job-agent  
python3 -m venv venv  
source venv/bin/activate  
pip install -r requirements.txt
 ```

---

## 🔑 Environment Variables

Create a `.env` file in the root directory:

RAPIDAPI_KEY=your_key  
ADZUNA_APP_ID=your_id  
ADZUNA_APP_KEY=your_key  

---

## ▶️ Run

python test_pipeline.py  

---

## 📌 Example Output

Software Engineer - Adobe  
Score: 78  
Apply: https://...  

Backend Developer - Cisco  
Score: 72  
Apply: https://...  

---

## 📈 Key Highlights

- Processes 80+ job listings per run  
- Reduces manual job search effort significantly  
- Combines LLMs + RAG + backend systems design  

---

## 🔮 Future Improvements

- Parallel processing for faster scoring  
- Auto-apply functionality  
- UI dashboard for tracking applications  
- Resume PDF parsing  

---

## 👤 Author

Gargi Jain
