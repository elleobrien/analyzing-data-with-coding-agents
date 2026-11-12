# Analyzing Data with Coding Agents

Materials from a one-hour lab for the UMSI AI Clinic, taught by Elle O'Brien (School of Information, University of Michigan) on November 10, 2026.

> Coding agents are much more powerful for data work than chatbots, but more power means more to check. This lab covers what agents can do with your data, how to direct one to build an analysis you can rerun and share, and how to make sure its results are actually right.

The audience was mostly first-year master's students, about half from data-focused pathways and half from UX, so the lab assumes some exposure to Python but doesn't require reading code. Feel free to reuse or adapt any of it.

## What's here

| | |
|---|---|
| [`slides/analyzing_data_with_coding_agents.pptx`](slides/analyzing_data_with_coding_agents.pptx) | The deck, with speaker notes ([PDF](slides/analyzing_data_with_coding_agents.pdf)) |
| [`docs/demo-runbook.md`](docs/demo-runbook.md) | Step-by-step plan for the ~22-minute live demo: prompts, what to point out, expected numbers, what to do if it goes sideways |
| [`docs/demo-dataset.md`](docs/demo-dataset.md) | The demo dataset, its two planted traps, and the answer key |
| [`dataset/make_survey.py`](dataset/make_survey.py) | Seeded script that generates the dataset |

**The demo data itself lives in a separate repo:** [github.com/elleobrien/course-survey-demo](https://github.com/elleobrien/course-survey-demo). That repo is the folder you open in the coding agent, so it holds only the data and a plain README. The answers are kept here, where the agent can't read them. Keep the two apart when you run the demo.

## The demo in one paragraph

A synthetic end-of-semester course survey (made-up courses, made-up students) with two traps: some ratings are `N/A`, and a few students submitted the survey twice. Ask an agent for the average rating per course and it usually returns a clean script, a nice figure, and the wrong worst course, because the repeat submissions pull one course down. The lab uses this to practice asking for a script instead of an answer, and asking "what did it decide that I didn't ask for?"

## License

The materials in this repo are released under [CC BY 4.0](LICENSE): reuse and adapt them for any purpose, with credit to Elle O'Brien. The demo data in [course-survey-demo](https://github.com/elleobrien/course-survey-demo) is CC0.
