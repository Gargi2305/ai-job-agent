from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from services.sheets import save_job 
from routes import analyze, match, tailor, cover, full_analysis

from PyPDF2 import PdfReader
import io
import json

app = FastAPI()

# ✅ CORS (required for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ existing routes
app.include_router(analyze.router)
app.include_router(match.router)
app.include_router(tailor.router)
app.include_router(cover.router)
app.include_router(full_analysis.router)

# ---------------------------------------------------
# 🔥 1. OLD (HARDCODED RESUME) — keep for testing
# ---------------------------------------------------
@app.get("/run-agent-stream")
def run_agent_stream():
    from prepare_input import load_resume
    from services.job_fetcher import fetch_all_jobs, filter_jobs
    from routes.full_analysis import full_logic
    from models.schemas import CoverLetterRequest

    resume = load_resume()
    jobs = filter_jobs(fetch_all_jobs())

    def generate():
        for i, job in enumerate(jobs, 1):
            try:
                jd_text = (job.get("description") or "") + " " + (job.get("title") or "")
                if not jd_text.strip():
                    continue

                req = CoverLetterRequest(jd=jd_text, resume=resume)
                response = full_logic(req)

                score = response["match"]["match_score"]

                yield json.dumps({
                    "index": i,
                    "title": job.get("title"),
                    "company": job.get("company"),
                    "score": score,
                    "link": job.get("link")
                }) + "\n"

            except:
                continue

    return StreamingResponse(generate(), media_type="text/plain")


# ---------------------------------------------------
# 🚀 2. NEW (PDF UPLOAD — MAIN FEATURE)
# ---------------------------------------------------

@app.post("/run-agent-upload")
async def run_agent_upload(file: UploadFile = File(...)):
    from services.job_fetcher import fetch_all_jobs, filter_jobs
    from routes.full_analysis import full_logic
    from models.schemas import CoverLetterRequest

    # ✅ Read PDF
    content = await file.read()
    reader = PdfReader(io.BytesIO(content))

    resume = ""
    for page in reader.pages:
        resume += page.extract_text() or ""

    jobs = filter_jobs(fetch_all_jobs())

    def generate():
      for i, job in enumerate(jobs, 1):
          try:
              title = job.get("title")
              company = job.get("company")

              jd_text = (job.get("description") or "") + " " + title
              if not jd_text.strip():
                  continue

              req = CoverLetterRequest(jd=jd_text, resume=resume)
              response = full_logic(req)

              score = response["match"]["match_score"]

              # ✅ ADD THIS BLOCK
              job_data = {
                  "title": title,
                  "company": company,
                  "score": score,
                  "link": job.get("link"),
                  "description": job.get("description") or ""
              }

              save_job(job_data)  # 🔥 THIS WAS MISSING

              data = {
                  "index": i,
                  "title": title,
                  "company": company,
                  "score": score,
                  "link": job.get("link")
              }

              yield json.dumps(data) + "\n"

          except Exception as e:
              print("Sheet save error:", e)  # 🔥 add this for debugging
              continue


# @app.post("/run-agent-upload")
# async def run_agent_upload(file: UploadFile = File(...)):
#     from services.job_fetcher import fetch_all_jobs, filter_jobs
#     from routes.full_analysis import full_logic
#     from models.schemas import CoverLetterRequest

#     # ✅ Read PDF
#     content = await file.read()
#     reader = PdfReader(io.BytesIO(content))

#     resume = ""
#     for page in reader.pages:
#         resume += page.extract_text() or ""

#     jobs = filter_jobs(fetch_all_jobs())

#     def generate():
#         for i, job in enumerate(jobs, 1):
#             try:
#                 jd_text = (job.get("description") or "") + " " + (job.get("title") or "")
#                 if not jd_text.strip():
#                     continue

#                 req = CoverLetterRequest(jd=jd_text, resume=resume)
#                 response = full_logic(req)

#                 score = response["match"]["match_score"]

#                 yield json.dumps({
#                     "index": i,
#                     "title": job.get("title"),
#                     "company": job.get("company"),
#                     "score": score,
#                     "link": job.get("link")
#                 }) + "\n"

#             except:
#                 continue

    return StreamingResponse(generate(), media_type="text/plain")