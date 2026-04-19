import requests
from dotenv import load_dotenv
import os
import re

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")


# ✅ JSEARCH
# def fetch_jsearch_jobs(query="software engineer", location="India"):
#     url = "https://jsearch.p.rapidapi.com/search"

#     querystring = {
#         "query": query,
#         "page": "1",
#         "num_pages": "2",
#         "date_posted": "month"
#     }

#     headers = {
#         "X-RapidAPI-Key": RAPIDAPI_KEY,
#         "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
#     }

#     response = requests.get(url, headers=headers, params=querystring)
#     data = response.json()

#     if not data.get("data"):
#         print("⚠️ JSearch empty, fallback triggered")
#     querystring["query"] = query  # remove location
#     response = requests.get(url, headers=headers, params=querystring)
#     data = response.json()

#     return [
#         {
#             "title": job.get("job_title"),
#             "company": job.get("employer_name"),
#             "description": job.get("job_description"),
#             "location": job.get("job_city"),
#             "link": job.get("job_apply_link"),
#             "source": "jsearch"
#         }
#         for job in data.get("data", [])
#     ]

def fetch_jsearch_jobs(query="software engineer", location="India"):
    url = "https://jsearch.p.rapidapi.com/search"

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    # 🔹 First attempt
    querystring = {
        "query": f"{query} {location}",
        "page": "1",
        "num_pages": "2",
        "date_posted": "month"
    }

    response = requests.get(url, headers=headers, params=querystring)

    # ✅ DEBUG LINE (this is what I meant)
    print("JSearch status:", response.status_code)

    data = response.json()

    # 🔥 fallback only if empty
    if not data.get("data"):
        print("⚠️ JSearch empty, fallback triggered")

        querystring["query"] = query  # simpler query
        response = requests.get(url, headers=headers, params=querystring)

        # ✅ DEBUG AGAIN
        print("JSearch fallback status:", response.status_code)

        data = response.json()

    return [
        {
            "title": job.get("job_title"),
            "company": job.get("employer_name"),
            "description": job.get("job_description"),
            "location": job.get("job_city"),
            "link": job.get("job_apply_link"),
            "source": "jsearch"
        }
        for job in data.get("data", [])
    ]


# ✅ ADZUNA
def fetch_adzuna_jobs(query="software engineer", location="in"):
    url = f"https://api.adzuna.com/v1/api/jobs/{location}/search/1"

    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "results_per_page": 20,
        "what": query,
        "sort_by": "date"
    }

    response = requests.get(url, params=params)
    data = response.json()

    jobs = []

    for job in data.get("results", []):
        jobs.append({
            "title": job.get("title"),
            "company": job.get("company", {}).get("display_name"),
            "description": job.get("description"),
            "location": job.get("location", {}).get("display_name"),
            "link": job.get("redirect_url"),
            "source": "adzuna"
        })

    return jobs


# ✅ COMBINED FETCH
def fetch_all_jobs():
    queries = [
        "software engineer",
        "backend developer",
        "full stack developer"
    ]

    all_jobs = []

    for q in queries:
        j1 = fetch_jsearch_jobs(q)
        j2 = fetch_adzuna_jobs(q)

        print(f"{q} → JSearch:{len(j1)} | Adzuna:{len(j2)}")

        all_jobs.extend(j1)
        all_jobs.extend(j2)

    # ✅ DEDUP
    seen = set()
    unique_jobs = []

    for job in all_jobs:
        key = (job.get("title"), job.get("company"))

        if key not in seen:
            seen.add(key)
            unique_jobs.append(job)

    print("Total after dedup:", len(unique_jobs))

    return unique_jobs

# def filter_jobs(jobs):
#     filtered = []

#     for job in jobs:
#         title = (job.get("title") or "").lower()
#         desc = (job.get("description") or "").lower()
#         text = title + " " + desc

#         # ❌ remove junk
#         if "via" in title:
#             continue

#         # ❌ remove clearly senior roles
#         if any(x in title for x in [
#             "director", "vp", "chief",
#             "staff", "principal"
#         ]):
#             continue

#         # ⚠️ softer filter (allow borderline roles)
#         if any(x in title for x in ["senior", "lead", "manager"]):
#             continue
#             # only reject if experience ALSO high
#         if any(k in text for k in ["5 years", "6 years", "7 years", "8 years"]):
#             continue

#         # 🔥 SIMPLE experience filter (no complex regex)
#         if any(x in text for x in [
#             "5+ years", "6+ years", "7+ years",
#             "5 years", "6 years", "7 years",
#             "4-6 years", "5-7 years"
#         ]):
#             continue

#         filtered.append(job)

#     print(f"After experience filter: {len(filtered)} jobs")
#     return filtered


# # ✅ FILTER
def filter_jobs(jobs):
    filtered = []

    for job in jobs:
        title = (job.get("title") or "").lower()

        if "via" in title:
            continue

        if any(x in title for x in ["director", "vp", "chief","senior", "lead", "manager"]):
            continue

        filtered.append(job)

    return filtered


