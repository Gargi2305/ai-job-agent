from services.job_fetcher import fetch_all_jobs, filter_jobs
from routes.full_analysis import full_logic
from models.schemas import CoverLetterRequest
import os
import json
from services.sheets import load_seen_jobs, save_job

SEEN_FILE = "seen_jobs.json"


def load_seen_jobs():
    if not os.path.exists(SEEN_FILE):
        return set()

    with open(SEEN_FILE, "r") as f:
        return set(json.load(f))


def save_seen_jobs(seen_jobs):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen_jobs), f)


def run_job_pipeline(resume):
    jobs = fetch_all_jobs()
    jobs = filter_jobs(jobs)

    print(f"\nTotal jobs fetched: {len(jobs)}\n")

    seen_jobs = load_seen_jobs()

    results = []

    for i, job in enumerate(jobs, 1):
        try:
            title = (job.get("title") or "")
            company = (job.get("company") or "")
            desc_lower = (job.get("description") or "").lower()
            title_lower = title.lower()

            job_id = f"{title}_{company}"

            # ✅ skip seen
            if job_id in seen_jobs:
                continue

            # 🚫 skip very senior
            if any(k in title_lower for k in ["principal", "staff", "architect"]):
                continue

            # 🔥 QUICK FILTER (ADD HERE)
            text = title_lower + " " + desc_lower
            quick_keywords = ["software", "backend", "developer", "engineer"]

            if not any(k in text for k in quick_keywords):
                continue

            print(f"[{i}/{len(jobs)}] {title} - {company}")

            jd_text = (job.get("description") or "") + " " + title

            if not jd_text.strip():
                continue

            req = CoverLetterRequest(
                jd=jd_text,
                resume=resume
            )

            response = full_logic(req)

            score = response["match"]["match_score"]

            # ⚠️ penalize senior
            if any(k in title_lower or k in desc_lower for k in ["senior", "lead", "manager", "director"]):
                score = max(0, score - 30)

            print(f"   → Score: {score}")
            print(f"   → Apply: {job.get('link')}")

            results.append({
                "title": title,
                "company": company,
                "score": score,
                "link": job.get("link")
            })

            # ✅ save seen immediately
            seen_jobs.add(job_id)
            # save_seen_jobs(seen_jobs)
            save_job({
                        "title": title,
                        "company": company,
                        "score": score,
                        "link": job.get("link"),
                        "description": jd_text
                    })

        except Exception as e:
            print(f"   ❌ Skipped: {e}")
            continue

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    print("\n✅ Done\n")
    print(f"Final results: {len(results)}\n")

    return results

# # from services.job_fetcher import fetch_all_jobs, filter_jobs
# # from routes.full_analysis import full_logic
# # from models.schemas import CoverLetterRequest


# # def run_job_pipeline(resume):
# #     jobs = fetch_all_jobs()
# #     jobs = filter_jobs(jobs)

# #     print("Fetched jobs:", len(jobs))

# #     results = []

# #     for job in jobs[:10]:   # limit for now
# #         try:
# #             print("\n--- NEW JOB ---")
# #             print("Step 1: preparing JD")

# #             jd_text = (job.get("description") or "") + " " + (job.get("title") or "")

# #             if not jd_text.strip():
# #                 print("Skipped empty JD")
# #                 continue

# #             print("Step 2: creating request")

# #             req = CoverLetterRequest(
# #                 jd=jd_text,
# #                 resume=resume
# #             )

# #             print("Step 3: calling full_logic")

# #             response = full_logic(req)

# #             print("Step 4: got response")

# #             score = response["match"]["match_score"]

# #             print("Step 5: score =", score)

# #             results.append({
# #                 "title": job.get("title"),
# #                 "company": job.get("company"),
# #                 "score": score
# #             })

# #         except Exception as e:
# #             print("❌ Error:", e)

# #     results = sorted(results, key=lambda x: x["score"], reverse=True)

# #     print("Final results count:", len(results))

# #     return results

# from services.job_fetcher import fetch_all_jobs, filter_jobs
# from routes.full_analysis import full_logic
# from models.schemas import CoverLetterRequest


# def run_job_pipeline(resume):
#     jobs = fetch_all_jobs()
#     jobs = filter_jobs(jobs)

#     print("Fetched jobs:", len(jobs))

#     results = []

#     for job in jobs[:10]:   # limit for now
#         try:
#             print("\n--- NEW JOB ---")
#             print("Step 1: preparing JD")

#             jd_text = (job.get("description") or "") + " " + (job.get("title") or "")

#             if not jd_text.strip():
#                 print("Skipped empty JD")
#                 continue

#             print("Step 2: creating request")

#             req = CoverLetterRequest(
#                 jd=jd_text,
#                 resume=resume
#             )

#             print("Step 3: calling full_logic")

#             response = full_logic(req)

#             print("Step 4: got response")

#             score = response["match"]["match_score"]

#             print("Step 5: score =", score)

#             results.append({
#                 "title": job.get("title"),
#                 "company": job.get("company"),
#                 "score": score
#             })

#         except Exception as e:
#             print("❌ Error:", e)

#     results = sorted(results, key=lambda x: x["score"], reverse=True)

#     print("Final results count:", len(results))

#     return results



