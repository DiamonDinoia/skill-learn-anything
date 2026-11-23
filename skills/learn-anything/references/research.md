# Research behind the rules

The table lists the rules in `SKILL.md` that rest on a study of human
learning, what each study shows, and what it does not show. A study supports
the direction of a rule, not its exact numbers. Most studies used word lists,
prose, facts or math; the skill applies them to practical skills such as
cooking or music without a study of its own.

These rules are teaching defaults with no study behind them:

- the 0-5 level scale, the 1-4 grades and the 1-3 sureness scale;
- the numbers: 3-5 diagnostic questions, 2 passes per level, one hour as
  spacing, explanation after 2-3 failures, the 70% and 90% bounds;
- push-back on right answers and the grade 4 that it earns;
- the reading bridge;
- the evidence ladder L1-L5 and the cap at level 3 on self-report;
- the mapping of grades 1-4 to the FSRS ratings Again, Hard, Good, Easy.

| Rule in SKILL.md | Study | What it shows | Limit |
|---|---|---|---|
| Test instead of re-explain; recall counts, rereading does not (sections 4, 5) | Roediger & Karpicke 2006, Psychological Science, [10.1111/j.1467-9280.2006.01693.x](https://doi.org/10.1111/j.1467-9280.2006.01693.x) | Taking a recall test on prose gave better retention after days than studying it again | Prose passages; restudy was better on an immediate test |
| Repeated retrieval in the review log (section 6) | Karpicke & Roediger 2008, Science, [10.1126/science.1152408](https://doi.org/10.1126/science.1152408) | Repeated retrieval, not repeated study, drove retention of foreign vocabulary pairs | Word pairs |
| Rereading and highlighting are not evidence (section 4) | Dunlosky et al. 2013, Psychological Science in the Public Interest, [10.1177/1529100612453266](https://doi.org/10.1177/1529100612453266) | Practice testing and spaced practice rated high utility; rereading and highlighting low | Review of ten techniques, not one trial |
| Spaced review (section 6) | Cepeda et al. 2006, Psychological Bulletin, [10.1037/0033-2909.132.3.354](https://doi.org/10.1037/0033-2909.132.3.354) | Spaced study beats massed study for verbal recall across many experiments | Verbal recall tasks |
| Review gaps that grow (section 6) | Cepeda et al. 2008, Psychological Science, [10.1111/j.1467-9280.2008.02209.x](https://doi.org/10.1111/j.1467-9280.2008.02209.x) | The best gap between sessions grows with the time until the test | The best gap is not a fixed fraction of that time |
| Review mixed across subskills (section 6) | Rohrer & Taylor 2007, Instructional Science, [10.1007/s11251-007-9015-8](https://doi.org/10.1007/s11251-007-9015-8) | Shuffled math practice beat blocked practice on a delayed test | Math problems |
| Worked examples at level 0-1 (section 3) | Sweller & Cooper 1985, Cognition and Instruction, [10.1207/s1532690xci0201_3](https://doi.org/10.1207/s1532690xci0201_3) | Worked examples helped beginners learn algebra faster than problem solving | Well-structured problems |
| No worked examples from level 4 (section 3) | Kalyuga et al. 2003, Educational Psychologist, [10.1207/S15326985EP3801_4](https://doi.org/10.1207/S15326985EP3801_4) | Support that helps beginners can slow down learners with more knowledge | Review; the crossover level depends on the task |
| Guiding questions with feedback, not unaided discovery (section 4) | Alfieri et al. 2011, Journal of Educational Psychology, [10.1037/a0021017](https://doi.org/10.1037/a0021017) | Unassisted discovery did worse than explicit teaching; discovery with feedback, examples and prompts for explanation did better | Says nothing about when to switch to a direct explanation; effect sizes vary by domain and age |
| Feedback on the task and the reasoning (section 4) | Hattie & Timperley 2007, Review of Educational Research, [10.3102/003465430298487](https://doi.org/10.3102/003465430298487) | Feedback on the task and the process helps; praise of the person helps little | Review; "no praise" is the skill's choice, not a finding |
| Ask how sure; re-test confident errors (section 4) | Butterfield & Metcalfe 2001, JEP: Learning, Memory, and Cognition, [10.1037/0278-7393.27.6.1491](https://doi.org/10.1037/0278-7393.27.6.1491) | Errors made with high confidence were corrected more often after feedback | General-knowledge facts |
| Practice with prediction and feedback for practical skills (sections 4, 5) | Ericsson et al. 1993, Psychological Review, [10.1037/0033-295X.100.3.363](https://doi.org/10.1037/0033-295X.100.3.363) | Accumulated deliberate practice tracked the performance level of musicians | Correlational |
| Same rule, its limit | Macnamara et al. 2014, Psychological Science, [10.1177/0956797614535810](https://doi.org/10.1177/0956797614535810) | Meta-analysis: deliberate practice explains part of the differences in performance, less in education and professions than in games and music | Practice is not the only cause |
| About 80% success on new material (section 3) | Rosenshine 2012, "Principles of Instruction", American Educator 36(1), ERIC EJ971753 | The most effective teachers in classroom studies kept the success rate in guided practice at about 80% | Classroom and correlational; confirmed through secondary summaries, primary text not yet read |
| Review dates from a memory model (section 6) | Ye et al. 2022, KDD, [10.1145/3534678.3539081](https://doi.org/10.1145/3534678.3539081) | A memory model fitted to human review logs schedules reviews at lower cost than fixed rules | Flashcard-type items. The `fsrs` package runs a later model with default parameters, not fitted to this learner or to tutoring |
| Diagnostic questions before teaching (section 2.3) | Richland et al. 2009, JEP: Applied, [10.1037/a0016496](https://doi.org/10.1037/a0016496) | Questions answered wrongly before a reading improved later recall of that material | Prose passages and facts |
| The test, not the self-rating, sets the level (section 2.4) | Kruger & Dunning 1999, Journal of Personality and Social Psychology, [10.1037/0022-3514.77.6.1121](https://doi.org/10.1037/0022-3514.77.6.1121) | People with low scores rated their own skill well above their test results | Krueger & Mueller 2002, [10.1037/0022-3514.82.2.180](https://doi.org/10.1037/0022-3514.82.2.180): regression to the mean explains part of the effect |

The DOIs and titles above were resolved through the Crossref API on
2026-11-23. The Rosenshine row is the one source checked only through
secondary summaries.
