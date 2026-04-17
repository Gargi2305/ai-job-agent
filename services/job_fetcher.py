import requests
from dotenv import load_dotenv
import os

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")


# ✅ JSEARCH
def fetch_jsearch_jobs(query="software engineer", location="India"):
    url = "https://jsearch.p.rapidapi.com/search"

    querystring = {
        "query": f"{query} {location}",
        "page": "1",
        "num_pages": "2",
        "date_posted": "month"
    }

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
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


# ✅ FILTER
def filter_jobs(jobs):
    filtered = []

    for job in jobs:
        title = (job.get("title") or "").lower()

        if "via" in title:
            continue

        if any(x in title for x in ["director", "vp", "chief"]):
            continue

        filtered.append(job)

    return filtered



# import requests
# from dotenv import load_dotenv
# import os

# load_dotenv() 
# RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")


# def fetch_jsearch_jobs(query="software engineer", location="India"):
#     url = "https://jsearch.p.rapidapi.com/search"

#     full_query = f"{query} {location}"

#     querystring = {
#         "query": full_query,
#         "page": "1",
#         "num_pages": "3",
#         "date_posted": "month"
#     }

#     headers = {
#         "X-RapidAPI-Key": RAPIDAPI_KEY,
#         "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
#     }

#     response = requests.get(url, headers=headers, params=querystring)
#     data = response.json()
#     print("API KEY:", RAPIDAPI_KEY)

#     return [
#         {
#             "title": job.get("job_title"),
#             "company": job.get("employer_name"),
#             "description": job.get("job_description"),
#             "location": job.get("job_city"),
#             "posted_at": job.get("job_posted_at_datetime_utc"),
#             "link": job.get("job_apply_link"), 
#             "source": "jsearch"
#         }
#         for job in data.get("data", [])
#     ]

# # 🔥 MULTI-QUERY (FIXED VERSION)
# def fetch_all_jobs():
#     queries = [
#         "software engineer",
#         "backend developer",
#         "full stack developer"
#     ]

#     all_jobs = []

#     for q in queries:
#         jobs = fetch_jsearch_jobs(query=q)

#         print(f"{q} → {len(jobs)} jobs")

#         # ✅ fallback if API returns nothing
#         if len(jobs) == 0:
#             print(f"⚠️ fallback for query: {q}")
#             jobs = fetch_jsearch_jobs(query="software engineer")

#         all_jobs.extend(jobs)

#     print("Total before dedup:", len(all_jobs))

#     # ✅ deduplicate
#     seen = set()
#     unique_jobs = []

#     for job in all_jobs:
#         key = (job.get("title"), job.get("company"))

#         if key not in seen:
#             seen.add(key)
#             unique_jobs.append(job)

#     print("Total after dedup:", len(unique_jobs))

#     return unique_jobs


# # ✅ LIGHT FILTER (no over-filtering)
# def filter_jobs(jobs):
#     filtered = []

#     for job in jobs:
#         title = (job.get("title") or "").lower()

#         # ❌ remove aggregator junk
#         if "via" in title:
#             continue

#         # ❌ remove only top leadership roles
#         if any(x in title for x in ["director", "vp", "chief"]):
#             continue

#         filtered.append(job)

#     return filtered