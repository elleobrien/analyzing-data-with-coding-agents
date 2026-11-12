# Demo runbook

A live demo of about 22 minutes, run as the "Demo." slide in the deck. It uses the synthetic course-feedback survey in [github.com/elleobrien/course-survey-demo](https://github.com/elleobrien/course-survey-demo). The traps and the full answer key are in [demo-dataset.md](demo-dataset.md).

The goal is to show the room a confident analysis that runs without errors and gives the wrong answer, and then show them how to catch it without reading the code.

## What you need

- A clone of the demo repo in a neutral folder, such as your Desktop. Don't put it inside a folder that has its own `CLAUDE.md` or `AGENTS.md`, or the agent will read that too. Also keep this materials repo out of it, since the answers are here.
- Python with pandas and matplotlib, available as `python3` in that folder. Otherwise the agent may spend the demo trying to install packages.
- A coding agent. These notes assume Claude Code (the desktop app's Code tab), but the prompts work in any agent.
- **Model choice decides whether you get the miss.** A smaller model (Haiku) usually reports the naive answer. A larger one (Opus) usually catches the repeat submissions by itself. Either works with the "If…" notes below, but decide in advance which story you're telling, and test it once.
- Permission mode set so that every action asks first. That way the room sees what it's about to do.
- For a hybrid or recorded session, make the text big and share both the agent window and a file browser.
- Reset between practice runs by deleting anything the agent created (scripts, figures, `CLAUDE.md`), or by re-cloning.

## Demo

**1. Tour the folder (~3 min).** Show `README.md`, `data/survey.csv`, and the empty `scripts/` folder. Mention it's not real data and the XYZ courses are made up.

> Say: it can see this folder and the output of commands it runs. Not your browser, not your other folders, not anything you haven't put here. Everything it reads goes to a server you don't own.

**2. Look before analyzing (~5 min).**

> *Tell me about the data in data/survey.csv. Don't analyze it yet.*

Click open a step ("Read…" or "Ran python3…") to show that it actually opened the file. Ask the room: what did it look at?

**3. The question (~7 min).**

> *Calculate the average rating for each course and make a figure. Save the code as a script.*

Open the script and the figure.

Pause and ask: **"What did it decide that I didn't ask for?"** Expect it to have left out the N/A ratings. That's fine, since the README says N/A means skipped, but it's a choice. If it reports Applied Knot Theory as lowest at 3.39, that's the miss.

> *Explain in plain language what this script does. Did any student submit more than once?*

Models vary here. It may not have mentioned the repeats at all, it may say "no duplicate response IDs" (it checked IDs, not emails), or it may have noticed them and kept them anyway. All three make the point.

**4. Fix it and record it (~5 min).**

> *Keep only each student's latest submission and rerun.*

Expect Lighthouse Management to come out lowest (3.42), with Knot Theory up to 3.61. The answer flips.

> *Add that to CLAUDE.md so you do it next time.*

Open `CLAUDE.md` to show the note. That file is read at the start of every session in this folder.

**Optional, if there's time: another model.** Switch models, start a new session, and repeat step 3. A larger model usually catches the repeats on its own, though it may miscount them (for example, "6 of 7" when it's 5).

**Optional, if there's time: a notebook.**

> *Turn this script into a Jupyter notebook I can explore.*

Start `jupyter lab` in the folder, open the notebook, and use Restart and Run All.

> Say: the agent edits the file on disk. If the notebook is open in Jupyter while it works, reload before you run anything. Restart and Run All is your check that it really reruns from scratch.

## Expected numbers

| | Beekeeping (XYZ 110) | Pastry (XYZ 120) | Knot Theory (XYZ 230) | Lighthouses (XYZ 240) | Overall |
|---|---|---|---|---|---|
| Naive (repeats kept) | 3.95 | 3.92 | **3.39** | 3.41 | 3.71 (n=204) |
| One per student (latest) | 3.95 | 3.92 | 3.61 | **3.42** | 3.77 |
| N/A as 0 (wrong) | 3.72 | 3.64 | 3.19 | 3.09 | 3.45 |

There are 15 N/A ratings. 7 students submitted twice: 5 in Knot Theory, 1 in Beekeeping, and 1 in Lighthouses. Keeping each student's first submission gives Knot Theory 3.57, and the ranking stays the same.

## If…

- **It catches and removes the repeats by itself:** point out that it told you, and ask the room whether they would have read that far. Then ask which submission it kept, and whether keeping the first would change anything.
- **It asks to install a package:** deny it, and tell it to use `python3` in this folder, which already has pandas and matplotlib.
- **It stalls or loops:** press Esc, then restate the request in one sentence.
- **The live run goes sideways:** use the expected numbers above to tell the story.
