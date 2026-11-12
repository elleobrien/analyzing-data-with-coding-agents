# The demo dataset: a synthetic course-feedback survey

> **Spoiler warning.** This page is the answer key. Don't put it, or `dataset/make_survey.py`, in the folder you point the agent at. A coding agent reads everything in its folder, and an agent that can read the answers won't make the mistake you want to show.

**Not real data.** The department code (XYZ), the courses, the students, and their emails are all made up. The courses are deliberately unrelated to any real program (beekeeping, pastry, knots, lighthouses), so no real course can be read into the ratings. Course ratings can be a sensitive topic, so if you adapt this, don't swap in real course numbers.

- **The data, as students see it:** [github.com/elleobrien/course-survey-demo](https://github.com/elleobrien/course-survey-demo) (`data/survey.csv` plus a README describing the columns). Clone this repo to run the demo.
- **The generator:** [`dataset/make_survey.py`](../dataset/make_survey.py). It's seeded, so `python3 make_survey.py` writes a file identical to the one in the demo repo. Edit it to change the traps or make a new version.

## The data

219 rows, one per submission to an end-of-semester course feedback survey, from 212 students in 4 courses.

| column | meaning |
|---|---|
| `response_id` | R_1001 … one per submission |
| `submitted_at` | date and time submitted (Apr 20–30, 2026) |
| `email` | student###@example.edu (fake; example.edu is a reserved domain) |
| `course` | XYZ 110, XYZ 120, XYZ 230, XYZ 240 |
| `course_name` | Intro to Beekeeping, Pastry Science, Applied Knot Theory, Lighthouse Management |
| `rating` | 1–5, or `N/A` if they skipped it |
| `would_recommend` | Yes / No |
| `comments` | optional free text, often blank |

## The two traps

1. **N/A ratings (15 rows).** pandas reads the string `N/A` as missing by default, so an agent can drop these rows **without saying so**. Dropping them is correct here (the README says N/A means skipped), but it's a silent choice worth surfacing. Counting them as 0 would be wrong.
2. **Repeat submissions (7 students, 14 rows).** These students filled out the survey twice, forgetting they'd already done it. Same `email`, different `response_id` and `submitted_at` (5–96 hours apart), and close but not identical answers. They are **not exact duplicate rows**, so `drop_duplicates()` on the whole row won't catch them, and neither will checking `response_id`. Five of the seven are unhappy XYZ 230 students; one is in XYZ 110 and one in XYZ 240.

## What each choice gives you (average rating)

| | Overall | XYZ 110 Beekeeping | XYZ 120 Pastry | XYZ 230 Knot Theory | XYZ 240 Lighthouses |
|---|---|---|---|---|---|
| Naive: N/A dropped, repeats kept | 3.71 (n=204) | 3.95 | 3.92 | **3.39** ← lowest | 3.41 |
| N/A counted as 0 (wrong) | 3.45 | 3.72 | 3.64 | 3.19 | 3.09 |
| N/A dropped, one submission per student (latest) | 3.77 (n=197) | 3.95 | 3.92 | 3.61 | **3.42** ← lowest |

**The demo moment:** "Which course got the worst feedback?" The naive answer is Applied Knot Theory. Once repeat submissions are removed, it's Lighthouse Management. The answer flips because a few people submitted twice.

Keeping each student's first submission instead of the latest gives Knot Theory 3.57 and the same ranking. Either is defensible. What matters is saying which one you chose.

## What agents actually did with it

Trial runs with Claude Code (November 2026), each in a fresh copy of the demo folder, with the prompt *"Calculate the average rating for each course in data/survey.csv and make a figure. Save the code as a script."*

| Model | Mentioned N/A | Mentioned repeats | Removed repeats | Headline answer |
|---|---|---|---|---|
| Opus 5.5 | 4/4 | 4/4 | 3/4 | correct 3/4 |
| Haiku 5.5 | 4/4 | 2/4 | 0/4 | naive 4/4 |

- N/A was always excluded and never counted as 0. Every run read the README, which defines N/A.
- The larger model usually caught the repeats but often miscounted them ("6 of the 7" were in Knot Theory, when it's 5).
- One Haiku run gave a false all-clear, "no duplicate responses," because it checked `response_id` instead of `email`.
- Another Haiku run noticed the repeats and asked which to keep, but said the averages "would shift a little." In fact the lowest course changes.

Results vary from run to run and will change as models change. If you want the demo to show a miss, a smaller, faster model makes one more likely. Check before you present.
