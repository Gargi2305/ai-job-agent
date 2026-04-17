from services.job_fetcher import fetch_jsearch_jobs, filter_jobs

# ✅ call function (it already has default query)
jobs = fetch_jsearch_jobs()
jobs = filter_jobs(jobs)

print("TOTAL:", len(jobs))

for job in jobs[:5]:
    print(job["title"], "-", job["company"])