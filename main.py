from fastapi import FastAPI
from routes import analyze, match, tailor, cover, full_analysis

app = FastAPI()

app.include_router(analyze.router)
app.include_router(match.router)
app.include_router(tailor.router)
app.include_router(cover.router)
app.include_router(full_analysis.router)