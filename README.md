# learn-anything

An agent skill that teaches a topic to a tested level. The skill asks the
learner for a baseline, corrects it with a short test, and matches the
material to the measured level. It grades answers on evidence and schedules
spaced review from a log. It works for practical topics such as cooking or
music too: measurements, photos or a third person grade the doing part.

## Install

| Harness | Command |
|---|---|
| Claude Code | `claude plugin marketplace add DiamonDinoia/skill-learn-anything && claude plugin install learn-anything@learn-anything --scope user` |
| Codex CLI | `codex plugin marketplace add DiamonDinoia/skill-learn-anything`, then `codex plugin add learn-anything@learn-anything` |
| by hand | `git clone https://github.com/DiamonDinoia/skill-learn-anything && ln -s "$PWD/skill-learn-anything/skills/learn-anything" ~/.claude/skills/learn-anything` |

Then ask: "teach me X". With a plain chatbot, paste the body of
`skills/learn-anything/SKILL.md` into the chat or the system prompt. Without
tools, the skill keeps a pasteable state block instead of the review log.

In Claude Code, switch off "Prompt suggestions" in `/config`. The suggestion
box can show the answer to a question.

## What it needs

- For the review log: Python 3.10+ and `fsrs>=6,<7` (the FSRS scheduler). The
  skill creates one shared venv in `${XDG_DATA_HOME:-~/.local/share}/learn-anything/.venv`
  with `uv` or `python3 -m venv`, or asks for an environment.
- Data for each topic goes to `${XDG_DATA_HOME:-~/.local/share}/learn-anything/<topic>/`:
  `state.md`, `sources.md`, `log.jsonl`, `work/`, and a `.venv/` only when
  the topic's checks need packages. The review history exists only there.
- Checks that run learner code run it as trusted local code, without a
  sandbox.

## Tests

```sh
python -m venv .venv && .venv/bin/pip install 'fsrs>=6,<7'
.venv/bin/python -m unittest discover -s tests -v
```

`skills/learn-anything/references/research.md` lists the studies of human learning behind each rule.

## Attribution

The teaching method builds on the `socratic-tutor` skill in
[janestreet/agent_skills](https://github.com/janestreet/agent_skills)
(MIT, Copyright (c) 2026 Jane Street Group, LLC): the diagnostic before
teaching, the 0-5 skill map, one question per message, strict level rules,
spaced review, and the user commands.

Ideas also come from two closed pull requests to that repository:
[#3](https://github.com/janestreet/agent_skills/pull/3) (a transcript checker
for the rules) and [#4](https://github.com/janestreet/agent_skills/pull/4)
(prediction before each run, held-out cases for fresh checks).
