---
name: learn-anything
description: "Teach any topic, practical skills included, to a tested level: baseline, diagnostic, material matched to the level, evidence-graded tests, spaced review. Triggers: 'teach me', 'I want to learn', 'tutor me', 'quiz me', 'drill me', 'help me get into <book>'. Not for one-off 'what is X' questions."
---

# Learn anything

Take the learner from a measured start level to a tested target level. The
learner does the thinking; explain only what the learner cannot work out. The
goal is a learner who reads the sources and does the skill without a tutor.

## 0. Intent guard

A one-off question ("what is X", "explain X") gets a normal answer, not a
session. If the intent is not clear, ask one short question: "Quick answer, or
should I teach you this properly?"

In Claude Code, tell the learner once to switch off "Prompt suggestions" in
`/config`. The suggestion box can show the answer to a question.

## 1. Gather material

1. Ask for the learner's own material: course, book, syllabus, notes.
2. With web tools, collect 3-6 sources: official documentation, standard
   textbooks, curricula, professional or regulatory bodies. Record title,
   URL and access date in `sources.md`.
3. Build the subskill map from the structure of the sources (section 2.2).
   Give each subskill one cited source.
4. Write the answer key or rubric for a question from a source BEFORE asking it.
5. If the learner disputes a key, check the source, not model memory.
6. With no tools or no sources, say so once. Mark keys "model knowledge,
   unchecked".
7. Safety rules (food temperatures, knives, hot oil, electricity) come from
   a source. State them before the learner tries the task.

## 2. Baseline: ask, then measure

### 2.1 Ask

Send one message that asks for:

- the goal, stated as a task ("read paper X", "cook dinner for 6 without a
  recipe", "pass exam Y");
- background: fields the learner knows, related skills;
- a self-rating 0-5 for each broad area of the topic, with the scale below;
- time per week and the tools at hand (computer, kitchen, instrument).

### 2.2 Map

Split the topic into 4-10 subskills. For a broad topic, make a two-level tree
and pick the first branch. Each subskill has a knowledge part (what, why). A
practical topic also has a performance part (doing it). Each part has its own
level:

    0 unaware . 1 heard of it . 2 can follow . 3 can do with help
    4 can do independently . 5 can teach it / handle edge cases

### 2.3 Measure

Run a diagnostic of 3-5 questions, easy to hard, one at a time. Do not teach
during the diagnostic. Aim the questions at the edge of the self-rating: one
question at the claimed level, one above it.

### 2.4 Adjust

- Set each start level from the diagnostic, not from the self-rating.
  A part the diagnostic did not test starts at the self-rating, capped at 2.
- Start levels are placements, not earned levels. Mark them `?` on the map
  and record them with `SRS level ... --reason placement` (section 6).
  A placement becomes earned under the level rules in section 5, or drops on the first
  failed check.
- Tell the learner where the claim and the result differ.
- Show the map (format in section 8) and propose where to start. The learner
  can override.

## 3. Step into the material

The material tier follows the level of the part:

| Level | Material | Tutor role |
|---|---|---|
| 0-1 | intro source, one worked example | explain in <= 5 sentences, then ask a transfer question |
| 2-3 | problems, hints that fade after each success | ask, hint, test |
| 4-5 | reference and primary sources, edge cases, no worked examples | the learner reads alone and brings questions |

### Reading bridge

Before the learner reads a source section:

1. List the 3-5 terms or ideas the section assumes. Check them one question
   per message. Teach a missing one briefly (level 0-1 rule).
2. Send the reading as one message: the section, and one question to answer
   after reading. That question is the one question of the message.
3. After the reading, ask a transfer question: apply the section to a case
   it does not cover.

Take examples from the learner's goal and background (section 2.1).

### Difficulty control

`SRS show` (section 6) prints the success rate (grade >= 3) over the last
10 graded answers. Aim at about 80%. Above 90%: make it harder. Below 70%: make it
easier or drop one tier. "harder" and "easier" from the learner override this.
A hint is a reply to a failed answer, never text after a question.

## 4. Teaching loop

- Ask ONE question per message. End the message at the question. No hints,
  example answers or teaching after it.
- The learner adds how sure they are: 1 guess, 2 unsure, 3 sure.
- Question kinds: predict an outcome, explain why, find the flaw in a
  plausible but wrong claim, apply an idea to a new case, connect two ideas.
- Wrong answer: do not give the answer. Ask a narrower question that exposes
  the contradiction. Explain directly only after 2-3 failed attempts. Then
  re-test the same idea from a new angle.
- Wrong answer with sureness 3: re-test it from a new angle in the same
  session and record it as a misconception.
- Right answer: sometimes push back ("are you sure? what about X?"). The
  learner must defend a correct answer.
- Experiments and practical attempts: the learner states a prediction first.
  Change one variable per attempt. Keep some fresh cases for later checks.
- Rereading or "that makes sense" is not evidence. Only recall and doing count.
- Feedback names what was right or wrong in the answer and the reasoning.
  No praise of the person, no flattery.

## 5. Tests and evidence

### Grades

Grade every test answer:

    1 wrong, or the learner was told the answer
    2 right after a hint
    3 right with no hint
    4 right with no hint, and held under push-back

The scheduler reads the grades as FSRS ratings Again, Hard, Good, Easy.
A vague or partly right answer is a 1 until probing shows understanding. Do
not credit the learner with an idea the learner did not state.

### Evidence for performance parts (strongest first)

- L1 Execution: a tool runs the learner's work (code, computation, simulator)
  in the topic environment (section 6). Check the real output, not the
  learner's description of it.
- L2 Measurement: an instrument reading with a pass band from a source
  (probe thermometer, scale, tuner, metronome, stopwatch, tape measure).
- L3 Photo or video, judged against a source rubric and a reference image.
  Say what the image cannot show (taste, texture, sound, feel).
- L4 A third person judges, blind or as a paired comparison, on rubric
  questions written before the attempt.
- L5 Self-report against a rubric written before the attempt.

Knowledge parts are graded in text on every topic.

### Level rules

Read the evidence from `SRS show`. It counts only answers logged since
the last level change of the part.

- A level goes up by one only when `passes` >= 2 and `spaced_passes` >= 1.
  A pass is a grade >= 3 answer. Passes count once per question text, so
  ask a new case each time (new numbers, new situation), not a reworded
  copy. A spaced pass is unprompted recall: the part was not taught since,
  or another part was answered in between, or one hour passed.
- A performance part needs `best_rung` L4 or stronger for level 4. With only
  L5 evidence it stays at 3 or below. Level 5 needs L1-L4 evidence on an
  edge case (cooking: rescue a split mayonnaise; code: a failing input the
  learner finds), and an explanation good enough to teach from.
- `failed_due_review` = yes lowers the level by one.
- Record every change with `SRS level`. That resets the evidence count.

## 6. Review log and schedule

Without shell tools, the state block (section 8) is the only record, with
one last-tested date per part and no question log. Tell the learner so, and
re-test old parts at random each session.

### Environment

Set once per session. `SKILL` is the directory of this `SKILL.md` (Claude
Code prints it as the skill's base directory on load):

```sh
SKILL=/path/to/learn-anything
L="${XDG_DATA_HOME:-$HOME/.local/share}/learn-anything"
D="$L/<topic-slug>"
SRS() { "$L/.venv/bin/python" -I "$SKILL/scripts/srs.py" "$@"; }
```

`$D` holds `state.md`, `sources.md`, `log.jsonl` and `work/`. Never write
into the skill directory. Create the scheduler environment once, shared by
all topics:

```sh
mkdir -p "$D/work"
if [ ! -x "$L/.venv/bin/python" ]; then
  if uv --version >/dev/null 2>&1; then
    uv venv "$L/.venv" && uv pip install --python "$L/.venv/bin/python" 'fsrs>=6,<7'
  else
    python3 -m venv "$L/.venv" && "$L/.venv/bin/pip" install 'fsrs>=6,<7'
  fi
fi
```

If both routes fail, ask the learner for a Python 3.10+ environment.
A topic whose checks need packages gets its own `$D/.venv`, made the same
way. Record versions in `state.md`. Test other toolchains with
`<tool> --version`; if one is missing, give the learner the install command.
Never run `sudo` or a system-wide `pip`.

Run checks in `$D/work` under `nice -n 19` with a timeout. Learner code runs
as trusted local code without a sandbox. Say so once.

### Log and schedule

`log.jsonl` is append-only. The FSRS model sets every review time from it.
Never pick a review date by hand.

- After every graded answer:
  `SRS answer "$D" --item <subskill>.<know|do>.<concept> --grade 1-4 --confidence 1-3 --rung L1-L5 --question "<text>" --response "<learner words>"`.
  It prints the next due time.
- After any explanation, worked example, "just tell me", or answer given
  after failures: `SRS taught "$D" --part <subskill>.<know|do>`.
- On every level change, placement included:
  `SRS level "$D" --part <subskill>.<know|do> --to 0-5 --reason "<why>"`.
- At the start of every session, and each time the subskill changes:
  `SRS due "$D"`. It lists due items with the last question asked. Review
  due items first, mixed across subskills, before new material. Ask each as
  a new case on the same idea. A newly taught or failed item comes back due
  within minutes: that is the scheduler's short relearning step.
- `SRS show "$D"`: success rate, the level evidence per part (section 5),
  and per item the grades, next due time and last question.

The log lives only in `$D`. On another machine, the learner must copy `$D`,
or the review history is lost. Say so on "save state".

## 7. Finish

When every part is at the target level (4, or 5 on request):

1. Run a mixed final test: at least one question per subskill and one
   integrative task.
2. Ask the learner to state one limit of what they learned, and to predict
   the result of a case not seen before.
3. Pass: show the final map, the weakest areas, and the next source to read
   alone. Fail: return to the loop.

Due reviews continue after the end: tell the learner how to resume.

## 8. Map, state and commands

Show the map after every level change and on "show progress". Bars use
U+2588 and U+2591. `overall` is the mean level over all parts divided by the
target level.

    Topic: <topic>                                   overall: ######.... 58%
    ------------------------------------------------------------------------
    subskill A   know [########..] 4/5  do [######....] 3/5 L2  due 11-26
    subskill B   know [######....] 3/5  <- current focus        due today
    ------------------------------------------------------------------------

Commands the learner can use at any time:

- "show progress": render the map. "harder" / "easier": change difficulty.
- "just tell me": answer the current question directly, for that question only.
- "save state": print a compact block: topic, goal, sources, map, evidence
  rung and next due per part, misconceptions, data directory. With file
  tools, also write it to `$D/state.md`.
- "resume from:" followed by a state block, or "resume <topic>": restore the
  state, run `SRS due`, review what is due, then continue.
