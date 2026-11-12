"""Generate the synthetic course-feedback survey for the AI Clinic Lab demo.

Not real data. Usage:  python3 make_survey.py [output.csv]
Writes survey.csv in the current folder unless you give a path. Seeded, so the
output is identical to data/survey.csv in github.com/elleobrien/course-survey-demo.

Planted traps (keep this script OUT of the demo folder so the agent can't read them):
  1. N/A: some ratings are "N/A" (students who skipped the question).
     pandas.read_csv turns the string "N/A" into NaN by default, so the agent
     may drop them without saying so. Counting them as 0 would be wrong.
  2. Duplicate submissions: a few students filled out the survey twice,
     forgetting they had already done it. Same email, different response_id
     and timestamp (hours to days apart), and answers that are close but not
     identical, so they are NOT exact duplicate rows.
     They're concentrated in one course, so they change that course's average.
"""
import csv, random, os, sys
from datetime import datetime, timedelta

random.seed(1110)  # Nov 10

COURSES = {
    # course: (n students, mean rating)
    "XYZ 110": (68, 4.1),
    "XYZ 120": (55, 3.9),
    "XYZ 230": (47, 3.85),
    "XYZ 240": (42, 3.6),
}
COURSE_NAMES = {  # deliberately unrelated to information science, so nothing maps to a real course
    "XYZ 110": "Intro to Beekeeping",
    "XYZ 120": "Pastry Science",
    "XYZ 230": "Applied Knot Theory",
    "XYZ 240": "Lighthouse Management",
}
COMMENTS_GOOD = ["Great examples in lecture.", "Labs were really helpful.", "Loved the final project.",
                 "Office hours saved me.", "Clear and well organized."]
COMMENTS_BAD = ["Too much work for the credit hours.", "Assignments were confusing.",
                "Wish there were more examples.", "Pacing was too fast.", "Grading felt inconsistent."]

def rating_for(mean):
    r = round(random.gauss(mean, 0.9))
    return max(1, min(5, r))

def comment_for(r):
    if random.random() < 0.55:
        return ""
    return random.choice(COMMENTS_GOOD if r >= 4 else COMMENTS_BAD)

start = datetime(2026, 4, 20, 8, 0)
rows, sid = [], 0
for course, (n, mean) in COURSES.items():
    for _ in range(n):
        sid += 1
        email = f"student{sid:03d}@example.edu"
        t = start + timedelta(minutes=random.randint(0, 60 * 24 * 10))
        r = rating_for(mean)
        rating = "N/A" if random.random() < 0.065 else r
        rows.append({"submitted_at": t, "email": email, "course": course,
                     "rating": rating, "would_recommend": "Yes" if r >= 4 or (r == 3 and random.random() < .5) else "No",
                     "comments": comment_for(r)})

# Trap 2: duplicate submissions. 7 students, 5 of them in XYZ 230 and unhappy.
dupe_specs = [("XYZ 230", 1), ("XYZ 230", 1), ("XYZ 230", 2), ("XYZ 230", 1), ("XYZ 230", 2),
              ("XYZ 110", 4), ("XYZ 240", 3)]
for course, low in dupe_specs:
    cands = [r for r in rows if r["course"] == course and r["rating"] != "N/A" and not r.get("_duped")]
    orig = random.choice(cands)
    orig["_duped"] = True
    orig["rating"] = low
    orig["would_recommend"] = "Yes" if low >= 4 else "No"
    orig["comments"] = random.choice(COMMENTS_GOOD if low >= 4 else COMMENTS_BAD)
    second = dict(orig)
    second["submitted_at"] = orig["submitted_at"] + timedelta(hours=random.randint(5, 96))
    second["rating"] = max(1, min(5, low + random.choice([0, 0, 1])))
    second["comments"] = random.choice(["", orig["comments"]])
    rows.append(second)

rows.sort(key=lambda r: r["submitted_at"])
for i, r in enumerate(rows, 1):
    r["response_id"] = f"R_{1000 + i}"
    r["course_name"] = COURSE_NAMES[r["course"]]
    r["submitted_at"] = r["submitted_at"].strftime("%Y-%m-%d %H:%M")

out = sys.argv[1] if len(sys.argv) > 1 else "survey.csv"
os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
cols = ["response_id", "submitted_at", "email", "course", "course_name", "rating", "would_recommend", "comments"]
with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
    w.writeheader(); w.writerows(rows)
print(f"wrote {len(rows)} rows to {os.path.normpath(out)}")
