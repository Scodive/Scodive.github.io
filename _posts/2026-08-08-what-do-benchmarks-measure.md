---
layout: default
title: "What Makes a Benchmark Worth Testing?"
title_zh: "怎样设计一个真正有评测价值的 Benchmark？"
date: 2026-08-08
author_profile: true
excerpt: "How case construction shapes scores, what a smaller test set preserves, and how to build evidence for the decisions we actually care about."
excerpt_zh: "题目构造如何暗中决定评分规则，小规模测试集究竟保留了什么，以及如何为真正关心的决策构建可靠证据。"
topic: "Benchmark design"
topic_zh: "评测设计"
reading_time: "16 min read"
reading_time_zh: "约 16 分钟"
figure_en: "/assets/benchmark-measurement/scoring-en.svg"
figure_zh: "/assets/benchmark-measurement/scoring-zh.svg"
figure_alt_en: "Diagram illustrating how scoring rules and benchmark construction shape evaluation outcomes"
figure_alt_zh: "评分规则与题目构造如何影响评测结果的示意图"
---

<link rel="stylesheet" href="{{ '/assets/benchmark-measurement/article.css' | relative_url }}">
<div id="benchmark-essay" class="blog-post-content">
<div class="bm-topbar">
<a class="bm-back-link" href="{{ '/blogs/' | relative_url }}" data-en="All essays" data-zh="全部文章">All essays</a>
<div class="bm-language" role="tablist" aria-label="Article language / 文章语言">
<button type="button" role="tab" data-bm-language="en" aria-selected="true" aria-pressed="true" aria-controls="bm-content-en" lang="en">English</button>
<button type="button" role="tab" data-bm-language="zh" aria-selected="false" aria-pressed="false" aria-controls="bm-content-zh" lang="zh-CN">中文</button>
</div>
</div>

<div id="bm-content-en" class="bm-language-content" lang="en" markdown="1">

# What Makes a Benchmark Worth Testing?

<p class="bm-meta">August 8, 2026 · Benchmark design · 16 min read<span id="vercount_container_page_pv" class="bm-meta__views" style="display:none;"> · <strong class="bm-meta__views-num" id="vercount_value_page_pv">--</strong> views</span></p>

<p class="bm-deck">How case construction shapes scores, what a smaller test set preserves, and how to build evidence for the decisions we actually care about.</p>

A single question keeps coming back in our work on agent evaluation: **if a handful of cases gives us almost the same signal as the full benchmark, what was the rest of the suite actually doing?**

This is about more than trimming API bills. A thousand test cases can endlessly repeat the same failure mode, just as an overly brutal suite hands weaker models an uninformative wall of zeros. Two agents can walk away with the exact same headline score while differing dramatically in tool discipline, state tracking, recovery, and efficiency, yet a naive subsampled test set can match the average while erasing those exact distinctions.

Consider a simple ten-task ranking problem: model A solves six out of ten tasks; model B solves five, and every one of those five is hard. Calling A "better" silently presupposes that all ten successes carry equal weight. Where did that weighting come from? Usually not from a principled decision model, but from whichever variants happened to be scraped or generated in bulk.

<div class="bm-thesis" markdown="1">

**Case construction is already part of the scoring rule.** The way cases are sourced and balanced decides which demands enter a benchmark and how heavily each counts. Compressing a test set can faithfully track that aggregate number without ever validating its implicit weights or keeping the diagnostic evidence other decisions depend on.

</div>

The practical problem, then, is how to assemble a benchmark that gives distinct, trustworthy evidence for a stated evaluation decision instead of mistaking headcount for rigor.

<nav class="bm-toc" aria-label="Contents" markdown="1">

**In this essay**

1. [What compression actually preserves](#compression-en)
2. [How case counts become weights](#weights-en)
3. [What frontier labs choose to measure](#frontier-en)
4. [What careful construction looks like](#construction-en)
5. [Turning responses into evidence](#response-en)
6. [The scorer is a measurement instrument](#scoring-en)
7. [Coverage under a limited budget](#budget-en)
8. [Designing a case, then a suite](#protocol-en)
9. [Three claims worth testing](#validation-en)

</nav>

<h2 id="compression-en">What does a smaller test set preserve?</h2>

When people say "evaluate performance," they routinely conflate four distinct statistical goals: estimating a static benchmark mean, ranking two closely matched models, predicting utility on unseen production traffic, or profiling behavior across several operational criteria. A test subset built for one of these rarely solves the others automatically.

Take micro-benchmarking. In its studied settings, *tinyBenchmarks* showed that just 100 curated questions could estimate overall scores across roughly 14,000 MMLU items, and *Anchor Points* similarly leaned on cross-model item correlations to shrink evaluation cost.[16](#ref-16-en) [17](#ref-17-en) Yet *How Reliable is Language Model Micro-Benchmarking?* found that low aggregate estimation error does not guarantee reliable head-to-head ordering between close models; separating nearby contenders in its experiments required around 250 items, at which point plain random sampling looked competitive.[18](#ref-18-en)

A benchmark can compress neatly for at least three very different reasons: the items keep repeating the same bottleneck, the calibration models share strongly correlated skill profiles so even diverse items move together, or the target is simply a single scalar mean (which is much easier to reconstruct than a multi-dimensional behavior profile).

A quick thought experiment makes the hidden assumption obvious. Two models can behave identically on a curated subset and diverge everywhere else, leaving no signal inside the subset to tell them apart. Compression works only insofar as cross-item correlations, model populations, or task structures stay consistent, and every new model architecture puts those assumptions back on trial.

<div class="bm-table bm-table-wide" role="region" aria-label="Comparison table" tabindex="0" markdown="1">

| Intended use | Evidence the suite must retain | What a low score-estimation error leaves open |
|---|---|---|
| Estimate a fixed suite's mean | Calibration on held-out models | Whether the original suite represents useful work |
| Compare nearby models | Paired differences and uncertainty | Whether a small gap has the correct sign |
| Diagnose several behaviors | Evidence for each goal and interpretable omissions | Whether a rare behavior disappeared during selection |
| Screen costly failures | Detection within relevant risk strata | Whether a high mean hides an important tail |
| Choose a deployment model | Utility on an independent workload | Whether the benchmark's weights match actual needs |

</div>

Our own subset experiments sharpened a related divide: packing more failing tasks into a sample did not automatically broaden coverage across task families, nor did gains on an individual coverage metric guarantee a better overall trade-off. Coverage and score fidelity move independently, which is why claiming score preservation always demands a separate held-out estimation check.

At bottom, compression tells us about a prediction problem over scores; it only says something about benchmark *quality* once we spell out what decision-relevant information the full suite was meant to capture.

<h2 id="weights-en">The hidden step: case counts become weights</h2>

Suppose we partition a benchmark into disjoint task families. If family `g` holds `n_g` items and model `m` scores an average `s_mg` on that family, the ordinary benchmark average is simply:

<div class="bm-equation">S<sub>D</sub>(m) = Σ<sub>g</sub> (n<sub>g</sub> / N) s<sub>mg</sub></div>

That ratio `n_g / N` acts as a silent priority weight. Whenever one workflow happens to be easy to synthesize or verify programmatically, generating extra variants gives it outsized control over the final leaderboard. Production convenience quietly turns into an evaluation preference.

Equal item weighting makes total sense when tasks come from genuine production sampling and every success brings roughly similar value, or when extra samples narrow confidence intervals within a family. It breaks down the moment synthetic quotas or scraping convenience stand in for real traffic frequencies, error costs, or stated research goals.

Go back to our ten-task example. Model A passes all five routine tasks and one of five hard ones; model B fails every routine task and passes all five hard ones. Now duplicate each of the five hard records once without changing a single model trajectory or answer:

<div class="bm-table bm-table-wide" role="region" aria-label="Comparison table" tabindex="0" markdown="1">

| Suite composition | A | B | Leader by the ordinary mean |
|---|---|---|---|
| 5 routine + 5 hard | 6/10 = 60.0% | 5/10 = 50.0% | A |
| 5 routine + the same 5 hard records twice | 7/15 = 46.7% | 10/15 = 66.7% | B |
| Independent task demands added | 0 | 0 | Ranking still reverses |

</div>

Obviously copying static records is a constructed counterexample that adds zero new evidence while lifting the hard family's weight from 1/2 to 2/3 (unlike repeated stochastic rollouts, which actually reduce execution variance). Even so, it illustrates how fragile raw averages are.

Call `p` the weight assigned to the hard family in the real downstream setting. Holding both within-family means constant gives:

<div class="bm-equation">U<sub>A</sub>(p) = 1 − 0.8p &nbsp;&nbsp; U<sub>B</sub>(p) = p &nbsp;&nbsp; U<sub>A</sub> = U<sub>B</sub> ⇔ p = 5/9 ≈ 55.6%</div>

<figure><img loading="lazy" src="{{ '/assets/benchmark-measurement/weights-en.svg' | relative_url }}" alt="Figure 1 · A ranking is conditional on task weights. Analytic toy example: the curves cross at p = 5/9. The vertical guides show the original mix and the duplicated hard-case mix."><figcaption><strong>Figure 1 · A ranking is conditional on task weights.</strong> Analytic toy example: the curves cross at p = 5/9. The vertical guides show the original mix and the duplicated hard-case mix.</figcaption></figure>

Below `55.6%`, A leads; above it, B takes over. Put in terms of value ratio, if every hard-task success is worth `r` routine wins, B comes out ahead whenever `r > 1.25`. **Difficulty by itself settles neither `p` nor `r`.** An obscure puzzle can be irrelevant to users, while an everyday bread-and-butter task can dominate business impact.

*The Benchmark Lottery* captured this cleanly in real NLP benchmarks: picking four out of SuperGLUE's eight tasks creates 70 valid subsets and produces six different top-ranked models.[21](#ref-21-en) The real design burden lies in explaining why the chosen mix deserves to carry the verdict.

The cleaner engineering split is explicit weighting: derive family weights from the intended workload or decision value, and spend case count inside each family purely to tighten estimation precision. More synthetic permutations should never buy extra vote share, and whenever tasks serve overlapping goals, aggregation needs an explicit rule rather than pretending families sit in neat silos.

<details markdown="1"><summary>Would item response theory automatically put B ahead?</summary>

In the simplest Rasch model, it would not. With the same complete item set, fixed item difficulties, common discrimination, a single ability dimension, and local independence, the total number correct is sufficient for the ability parameter. The likelihood derivative is Σy<sub>i</sub> − Σσ(θ − b<sub>i</sub>), so the fitted ability increases with the total correct. A score of 5/10 does not overtake 6/10 just because the correct items look harder. More elaborate models change the assumptions; they still do not determine what a user should value.

</details>

<h2 id="frontier-en">What frontier labs choose to measure</h2>

Frontier model cards offer a live snapshot of what labs currently care to prove: software patches, professional deliverables, SaaS automation, GUI computer use, and science workflows. The table below reflects release reports checked on October 8, 2026:

<div class="bm-table bm-table-wide" role="region" aria-label="Comparison table" tabindex="0" markdown="1">

| Release report | Selected benchmarks | Settings that define the comparison |
|---|---|---|
| OpenAI · GPT-6.1 Sol | DeepSWE 1.1; GDP.pdf; AutomationBench 1.0.6; OSWorld 2.0; Terminal-Bench Science 0.1 | OSWorld uses partial reward on a specified offline version; reasoning settings and per-task cost are reported.[1](#ref-1-en) |
| Anthropic · Sonnet 5.5 | Terminal-Bench 4.0; FrontierCode 1.1; CursorBench 4.0; GDPval-AA v2.1; OSWorld 2.1 | OSWorld is partial credit; the highest reasoning setting does not win every task. FrontierCode: 46.2% at Max versus 52.1% at Xhigh.[2](#ref-2-en) |
| Google DeepMind · Gemini 4 Argon | Engineering, knowledge work, science, long context, and computer use | The OSWorld offline evaluation specifies its version and 500-step budget, taking the best of three runs; self-evaluated and externally reported results are distinguished.[3](#ref-3-en) |

</div>

Seen together, these suites converge around three practical criteria: real overlap with high-value work, verifiable end states, and enough headroom to separate top models before budgets explode. Public release blogs summarize outcomes well enough, though they leave internal suite selection criteria largely unstated.

Even across the same headline suite, bare benchmark names rarely support direct apples-to-apples comparisons. Offline vs. hybrid online/offline runs, strict binary pass vs. partial credit, pass@1 vs. best-of-3, tool sandboxes, and scaffolding changes all alter the measurement instrument itself. A model claim only means something relative to its **task version, family mix, scaffold, compute budget, and grader**.

Seeing a benchmark in a frontier launch tells you it has industry influence. Checking whether it merits real trust means opening up how the items were built.

<h2 id="construction-en">What careful construction actually does</h2>

Labels like "human-written," "expert-crafted," or "algorithmically generated" only describe the assembly line; what makes a benchmark credible are the verification gates wired into that pipeline.

<div class="bm-table bm-table-wide" role="region" aria-label="Comparison table" tabindex="0" markdown="1">

| Benchmark | Construction evidence | The next question |
|---|---|---|
| GPQA, original | 448 expert-written science questions; expert accuracy 65%, non-expert accuracy 34% despite internet access.[4](#ref-4-en) | How far does scientific question answering transfer to open-ended research? |
| DeepSWE | 113 tasks across 91 repositories and five languages; prompts, behavioral verifiers, reference solutions, and quality review.[5](#ref-5-en) [22](#ref-22-en) | Which engineering workload does the repository and task mix represent? |
| AutomationBench 1.0.6 | Six business functions, 47 tools, isolated company states, and positive and negative end-state assertions.[6](#ref-6-en) | Do workflow quotas and interaction rules match the intended deployment? |
| AppWorld, original | Nine apps, 457 APIs, 750 tasks; programmatic state checks, including unwanted changes.[7](#ref-7-en) | What does success reveal beyond completing the specified task? |
| ToolSandbox | Stateful tools, implicit dependencies, a simulated user, and intermediate/final milestones.[8](#ref-8-en) | Do milestones accommodate valid alternative paths? |
| OSWorld 2.0 | 108 long-horizon tasks; end-state grading and trajectory-level challenge exposure.[9](#ref-9-en) | Does challenge attribution remain reliable across frameworks and budgets? |
| HealthBench, original | 5,000 conversations; 262 doctors; 48,562 contextual rubric criteria.[10](#ref-10-en) | How do rubric judgments relate to outcomes in the intended setting? |

</div>

DeepSWE shows what disciplined task acceptance looks like in practice: every item ships with a prompt, behavioral tests, and a working reference patch, checks alternate valid solutions, and runs repeated trials to weed out flakiness.[22](#ref-22-en) That gives real confidence at the *single-task* level. Still, representativeness is a separate check, since filtering active open-source repos above a popularity bar captures one particular slice of software engineering, and holding a single harness constant controls noise without guaranteeing equal model fit (notably, the native-framework spot check covered ten tasks).

AutomationBench approaches realism from the state side by intentionally planting ambiguous record names, stale fields, and policy constraints buried inside messages, paired with assertions covering both required actions and forbidden side effects.[6](#ref-6-en) Passing five of six checks earns partial credit in its reference example, while full success requires all six, cleanly distinguishing "edited a record" from "edited the right record without touching anything else." Even then, the relative share of each business function still has to be justified if scores are meant to reflect real office workloads.

Automated generators can enforce crisp criteria too: *AutoBencher*, for instance, optimizes generated suites directly for difficulty, topic relevance, and performance divergence.[11](#ref-11-en) The missing step in many generated suites is verifying whether those synthetic targets actually translate into sound downstream model judgments.

Looking across the field more broadly, that validation gap shows up almost everywhere. In *Measuring what Matters*, 29 domain experts audited 445 benchmark papers:[12](#ref-12-en)

<figure><img loading="lazy" src="{{ '/assets/benchmark-measurement/validity-en.svg' | relative_url }}" alt="Figure 2 · Defining a target and validating its measurement are separate steps. Bean et al., 445 papers: 78.2% defined the phenomenon, 53.4% provided construct-validity evidence, and 16.0% used uncertainty estimates or statistical tests. Categories overlap; these are rates of reported practices."><figcaption><strong>Figure 2 · Defining a target and validating its measurement are separate steps.</strong> Bean et al., 445 papers: 78.2% defined the phenomenon, 53.4% provided construct-validity evidence, and 16.0% used uncertainty estimates or statistical tests. Categories overlap; these are rates of reported practices.</figcaption></figure>

<h2 id="response-en">A response is a clue; execution makes it interpretable</h2>

Take an agent task tagged as a "state-tracking" eval. On a hard run, the agent might crash on a broken file path before ever reaching the state mutation step; on an easy run, it might pass through a completely legitimate shortcut that skips consulting old feedback at all. Either outcome is fair game as an end-to-end datapoint, yet neither justifies stamping that score as proof of state-tracking ability.

OSWorld 2.0 already moves in this direction by distinguishing challenges an agent actually ran into, got blocked from reaching, or bypassed completely.[9](#ref-9-en) Extending that habit turns execution traces into an audit of construct validity: checking whether what the benchmark *claims* to stress is what the trajectory actually encountered.

<div class="bm-table bm-table-wide" role="region" aria-label="Comparison table" tabindex="0" markdown="1">

| Observed response | Competing explanation | A useful check |
|---|---|---|
| Removing old feedback changes nothing | The task did not need it; another source supplied it; the model was robust; the intervention failed | Inspect information access, verify the intervention, and distinguish valid alternative routes |
| Removing feedback sharply reduces success | The information mattered; or length, formatting, feasibility, or tool behavior also changed | Use a matched non-target edit and an information-restoration control |
| Many failures occur before a target challenge | An upstream bottleneck obscures the target | Report overall task outcomes alongside challenge-reach counts |
| Many cases respond in the same way | Repeated evidence; or correlated source models | Group by task family and test new model families |
| Partial score changes but completion does not | Local progress changed; the completion threshold did not | Read intermediate state and final delivery together |

</div>

A reliable behavioral audit checks five links in sequence: what the task says it tests, which facts and states the rollout actually touched, whether ablations keep the task solvable, whether matched placebo and restoration controls isolate the active factor, and whether the same pattern holds across distinct model families.

Crucially, valid alternative paths deserve protection rather than penalty. If a user requirement can be solved cleanly via one batched query or three sequential queries, both routes should pass. If a purported memory benchmark turns out to be solvable straight from the final prompt, that undermines its diagnostic label as a memory probe without erasing its utility as an end-to-end workflow test.

Denominators matter just as much. Conditioning metrics exclusively on trajectories that survived long enough to hit the target obstacle flatters models that fail cheaply at step two. Always keep both denominators visible (all attempted tasks alongside target-reached trajectories) and separate execution crashes or missing grader logs cleanly.

Tracing these mismatches between intended capability labels and executed evidence, then showing that fixing them changes downstream model selection for the better, is one of the highest-leverage openings in evaluation research.

<h2 id="scoring-en">The scorer is part of the experiment</h2>

A sloppy verifier can fail a perfectly valid patch just because it hardcoded an unmentioned helper name, or wave through a broken hack because it only asserted one superficial printout. Checking that a reference solution passes establishes exactly one positive datapoint; serious verifier acceptance requires testing plausible alternative solutions alongside adversarial bad ones.

OpenAI's audit of 138 hard tasks sampled from SWE-bench Verified made this gap tangible: 59.4% of those audited tasks carried substantive test or specification defects.[13](#ref-13-en) Once hidden test expectations diverge from the problem prompt, benchmark scores quietly measure unstated test assumptions rather than task competence.

<figure><img loading="lazy" src="{{ '/assets/benchmark-measurement/scoring-en.svg' | relative_url }}" alt="Figure 3 · Correct grading and metric meaning are two different questions. Left: the selected 138-task SWE audit, not the full 500-task suite; 40.6% is the remainder outside the listed issue categories. Right: OSWorld 2.0, Opus 4.8, maximum thinking, batched calls, 500 steps. Binary completion is 20.6%; mean partial reward is 54.8%. Sources: [13] and [9]."><figcaption><strong>Figure 3 · Correct grading and metric meaning are two different questions.</strong> Left: the selected 138-task SWE audit, not the full 500-task suite; 40.6% is the remainder outside the listed issue categories. Right: OSWorld 2.0, Opus 4.8, maximum thinking, batched calls, 500 steps. Binary completion is 20.6%; mean partial reward is 54.8%. Sources: [13] and [9].</figcaption></figure>

Even when the grading script has zero bugs, aggregate metrics are still easy to misinterpret, as the right-hand panel highlights. Mean partial credit tracks incremental progress toward goal state, whereas binary completion measures full delivery: scoring 54.8% partial reward on OSWorld 2.0 alongside 20.6% binary completion does not mean the agent finished half its tasks.

Protocol audits have also uncovered trivial gaming paths hiding in plain sight. In a causal-discovery evaluation, exploiting generator variable ordering jumped a baseline from 0.018 to 0.639.[14](#ref-14-en) On the R-Judge safety benchmark, a trivial baseline labeling every single example "unsafe" scored F1 = 0.690, beating five out of 21 models making nuanced predictions.[15](#ref-15-en) Stress-testing graders against degenerate strategies checks whether the metric rewards competence or artifacts.

Every new benchmark item therefore needs negative test cases just as badly as a golden solution: known wrong patches, lazy shortcuts, and forbidden side effects should all trigger predictable failure.

<h2 id="budget-en">Under a fixed budget, optimize the evidence you need</h2>

Adding harder items breaks ties when top models cluster near the ceiling, yet once every candidate model fails almost everywhere, piling on impossible questions stops adding discriminative signal. Under a basic one-dimensional Rasch model with unit discrimination, Fisher item information follows `p(1 - p)`, peaking at `p = 0.5`:

<figure><img loading="lazy" src="{{ '/assets/benchmark-measurement/information-en.svg' | relative_url }}" alt="Figure 4 · Difficulty is relative to the population being measured. Analytic Rasch curve, I(θ) = p(1 − p), with p = σ(θ − b). It describes information for local ability estimation; business importance and failure cost are separate quantities."><figcaption><strong>Figure 4 · Difficulty is relative to the population being measured.</strong> Analytic Rasch curve, I(θ) = p(1 − p), with p = σ(θ − b). It describes information for local ability estimation; business importance and failure cost are separate quantities.</figcaption></figure>

Catching rare catastrophic failures obeys a completely different sample-size law. If independent runs fail silently 1% of the time, the chance of seeing zero failures across `n` runs is `0.99^n`:

<figure><img loading="lazy" src="{{ '/assets/benchmark-measurement/rare-en.svg' | relative_url }}" alt="Figure 5 · Estimating a mean and detecting a rare failure require different designs. In this independent 1% failure model, zero failures remain likely after 20 tests (81.8%) or 100 tests (36.6%). At least 299 tests give roughly a 95% chance of observing one or more failures."><figcaption><strong>Figure 5 · Estimating a mean and detecting a rare failure require different designs.</strong> In this independent 1% failure model, zero failures remain likely after 20 tests (81.8%) or 100 tests (36.6%). At least 299 tests give roughly a 95% chance of observing one or more failures.</figcaption></figure>

That tension is why useful multi-goal evaluations output a vector rather than pretending one scalar summarizes everything: tool accuracy, memory retention, state updates, error recovery, and latency-bounded efficiency answer orthogonal questions. Strong results on four axes do not fill a missing fifth.

To talk concretely about coverage, pick an explicit unit. Let `U_g` denote the audited behavioral conditions under goal `g`, and `E_g(S)` the distinct conditions actually exercised and verified in subset `S`:

<div class="bm-equation">C<sub>g</sub>(S) = |E<sub>g</sub>(S) ∩ U<sub>g</sub>| / |U<sub>g</sub>|</div>

Counting deduplicated conditions forces honesty: generating a hundred paraphrases of the same constraint raises sample count, not distinct coverage `C_g(S)`, so repetition and breadth should be reported separately. (And leaving `U_g` undefined means coverage is unknown, never 100%.)

CheckList demonstrated this matrix discipline cleanly for static NLP by crossing capabilities against test types.[20](#ref-20-en) Stateful agent benchmarks carry an extra burden: the test case only counts if the trajectory *actually hits* the condition at runtime, meaning label coverage, tool-call coverage, and behaviorally verified coverage measure very different things.

When no compact subset maximizes coverage, low redundancy, estimation accuracy, and inference cost simultaneously, keeping a Pareto frontier preserves legitimate engineering trade-offs. Even then, a frontier only reflects the objectives fed into it, so those objectives still need validation against the real deployment choice.

<h2 id="protocol-en">Design a case, then design the suite</h2>

Take a concrete workflow case: **update the right customer order using the latest valid approval prior to the cutoff timestamp, notify its owner, and leave every other order untouched.** Inside the sandbox sit two similarly named orders, an earlier approval email, and a superseding amendment.

Tagging this item "memory and planning" is only a loose summary. Turning it into a reliable measurement unit takes seven explicit checks:

<div class="bm-table bm-table-wide" role="region" aria-label="Comparison table" tabindex="0" markdown="1">

| Design layer | Concrete requirement | Acceptance check |
|---|---|---|
| Task contract | Entity identity, cutoff time, approval precedence, recipient, prohibited changes | All required information is available through allowed access |
| Initial state | Resolve the relationship between old approval and later message | Reset is reproducible; the conflict is real and resolvable |
| Valid solutions | Batch queries and sequential queries are both permitted | Alternative correct implementations pass |
| Wrong solutions | Wrong order, stale approval, missing notification, extra notification | Each targeted mistake is rejected |
| Challenge exposure | Which versions were read, and when? | Separate failure to reach the message from misuse after reading it |
| Response controls | Change only the intended information availability | Preserve feasibility; add matched edits and restoration |
| Place in the suite | Routine workload, rare risk, or deliberate challenge? | State its family, aggregation weight, and coverage unit |

</div>

Working down that checklist ties failure analysis directly to observables: saying "the agent fetched the amended approval yet still wrote back the stale value" gives engineers something actionable to debug, whereas saying "the agent lacks memory" does not. Meanwhile, tasks that only offer reliable end-to-end grading can remain valuable workload samples without pretending to isolate fine-grained cognitive traits.

At the suite level, build order prevents silent bias. Define the decision and goals first; carve out independent task families and behavioral conditions; assign explicit weights anchored in the use case; verify individual tasks; probe early model rollouts for blind spots and clones; and finally freeze the benchmark for independent testing. When both diagnostic stress tests and representative production slices matter, score and interpret them as separate groups rather than mashing them into one opaque average.

Periodic additions modeled after *Dynabench* help track emerging failure modes over time, while pairing those versioned updates with a frozen anchor split lets teams tell genuine model progress apart from drift in the test set itself.[19](#ref-19-en)

<h2 id="validation-en">Three claims worth testing</h2>

A framework only earns its keep if we spell out what empirical outcomes could prove it wrong. Three testable claims stand out right away on realistic agent benchmarks:

<div class="bm-table bm-table-wide" role="region" aria-label="Comparison table" tabindex="0" markdown="1">

| Hypothesis | Experiment | Result that would weaken it |
|---|---|---|
| Production quotas materially affect comparisons | Hold model outcomes and independent task content fixed; vary family multiplicities; compare ordinary means with declared family weights | Rankings are stable, or the original frequencies already match the intended use |
| Score fidelity and goal fidelity can separate | Compare score-preserving subsets on independently audited goals, near-model comparisons, and new model families | Cheap score estimators retain all required evidence equally well |
| Response-assisted construction improves independent judgments | Compare accepted, response-informed suites with random, stratified, structural, difficulty, and score-estimation baselines under matched information and total cost | Simple baselines match it, gains stay within source models, or construction cost erases the benefit |

</div>

To keep any of these comparisons honest, lock in evaluation goals, selection criteria, acceptance bars, and tolerances before scoring held-out models. Final validation has to run on genuinely independent evidence: separate deployment workloads for model selection, verified behavioral failures for diagnostics, and held-out task families for transfer. Evaluating a selector on the exact development responses used to pick the cases merely proves the selector converged on its own objective.

Cost accounting needs to look at the full lifecycle too, bundling item authoring, model probing, and ongoing inference runs together, then comparing selectors at both equal task count and equal total spend. Paying heavily up front to curate a compact suite can pay off handily over dozens of evaluations, provided the break-even volume is measured openly.

All of this circles back to a principled stopping rule for suite size: enough for *which* judgment, with *what* error bars, over *which* model population? Extra cases stop earning their keep once their marginal contribution to independent goal evidence or ranking accuracy drops below a declared threshold, rather than whenever a development loss curve happens to look flat.

## The question every additional case should answer

A benchmark does far more than store a folder of prompts. It allocates attention across user needs, turns capabilities into observable traces, codifies what counts as success, and condenses those verdicts into a decision.

Because those four steps lock together, suite compression, task authoring, grader validation, and leaderboard aggregation cannot be engineered in isolation. If generation convenience sets family counts, a distilled subset only reproduces an arbitrary priority faster. If execution never touches the labeled skill, nominal coverage hides blind spots. If the scorer leaks credit to shortcuts, running more tasks just gives sharper precision around the wrong metric.

The alternative is straightforward if unglamorous: make every step auditable. Justify family weights, test alternative and broken paths, verify challenge exposure, stress-test the scorer, and validate against independent choices. For every extra test case added to a suite, we should be able to point to the exact decision it sharpens and the new evidence it brings that existing cases could not supply.

<h2 id="references-en">Sources and figure data</h2>

<p class="bm-note">Web sources checked October 8, 2026. Figures 1, 4, and 5 are analytic examples; Figures 2 and 3 redraw public data. <a href="{{ '/assets/benchmark-measurement/figure-data.json' | relative_url }}">Data and sources</a>.</p>

<ol class="bm-references"><li id="ref-1-en">OpenAI. <a href="https://openai.com/index/introducing-gpt-6-1-sol/">Introducing GPT-6.1 Sol</a>. Model release report, 2026.</li><li id="ref-2-en">Anthropic. <a href="https://www.anthropic.com/claude-sonnet-5-5">Introducing Claude Sonnet 5.5</a>. Model release report, 2026.</li><li id="ref-3-en">Google DeepMind. <a href="https://deepmind.google/models/evals-methodology/gemini-4-argon">Gemini 4 Argon: Model evaluation</a>. Official evaluation methodology, 2026.</li><li id="ref-4-en">Rein et al. <a href="https://arxiv.org/abs/2311.12022">GPQA: A Graduate-Level Google-Proof Q&amp;A Benchmark</a>. 2023 preprint; COLM 2024.</li><li id="ref-5-en">Datacurve. <a href="https://deepswe.datacurve.ai/">DeepSWE v1.1</a>. Official project, v1.1.</li><li id="ref-6-en">Zapier. <a href="https://zapier.com/benchmarks">AutomationBench</a>. Official project, leaderboard v1.0.6.</li><li id="ref-7-en">Trivedi et al. <a href="https://arxiv.org/abs/2407.18901">AppWorld: A Controllable World of Apps and People for Benchmarking Interactive Coding Agents</a>. ACL 2024; original 750-task release.</li><li id="ref-8-en">Lu et al. <a href="https://aclanthology.org/2025.naacl-findings.65/">ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use Capabilities</a>. Findings of NAACL 2025.</li><li id="ref-9-en">Yuan et al. <a href="https://osworld-v2.xlang.ai/">OSWorld 2.0: Benchmarking Computer Use Agents on Long-Horizon Real-World Tasks</a>. 2026 preprint and project; configuration specified in Figure 3.</li><li id="ref-10-en">Arora et al. <a href="https://arxiv.org/abs/2505.08775">HealthBench: Evaluating Large Language Models Towards Improved Human Health</a>. 2025 preprint; original release.</li><li id="ref-11-en">Li et al. <a href="https://arxiv.org/abs/2407.08351">AutoBencher: Towards Declarative Benchmark Construction</a>. ICLR 2025.</li><li id="ref-12-en">Bean et al. <a href="https://arxiv.org/html/2511.04703v1">Measuring what Matters: Construct Validity in Large Language Model Benchmarks</a>. NeurIPS 2025 Datasets and Benchmarks; Section 2.</li><li id="ref-13-en">OpenAI. <a href="https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/">Why we no longer evaluate SWE-bench Verified</a>. February 23, 2026; selected audit of 138 difficult tasks.</li><li id="ref-14-en">Shao et al. <a href="https://arxiv.org/html/2607.22368v1">Do Agent Benchmarks Measure Capability? Protocol Validity in the Age of Agentic AI</a>. 2026 preprint; causal-discovery example in Case 6.</li><li id="ref-15-en">Wang et al. <a href="https://arxiv.org/html/2607.28685v1">Safety, or Just Capability? A Validity Audit of Agent-Safety Benchmarks</a>. 2026 preprint.</li><li id="ref-16-en">Maia Polo et al. <a href="https://proceedings.mlr.press/v235/maia-polo24a.html">tinyBenchmarks: evaluating LLMs with fewer examples</a>. ICML 2024.</li><li id="ref-17-en">Vivek et al. <a href="https://aclanthology.org/2024.eacl-long.95/">Anchor Points: Benchmarking Models with Much Fewer Examples</a>. EACL 2024.</li><li id="ref-18-en">Yauney, Warraich, and Swayamdipta. <a href="https://proceedings.iclr.cc/paper_files/paper/2026/hash/2e2960f2fe9e981f33f51c78656e3ca2-Abstract-Conference.html">How Reliable is Language Model Micro-Benchmarking?</a>. ICLR 2026.</li><li id="ref-19-en">Kiela et al. <a href="https://aclanthology.org/2021.naacl-main.324/">Dynabench: Rethinking Benchmarking in NLP</a>. NAACL 2021.</li><li id="ref-20-en">Ribeiro et al. <a href="https://aclanthology.org/2020.acl-main.442/">Beyond Accuracy: Behavioral Testing of NLP Models with CheckList</a>. ACL 2020.</li><li id="ref-21-en">Dehghani et al. <a href="https://arxiv.org/html/2107.07002v1">The Benchmark Lottery</a>. 2021 preprint.</li><li id="ref-22-en">Datacurve. <a href="https://deepswe.datacurve.ai/blog/deepswe">DeepSWE: Measuring frontier coding agents</a>. Construction and quality-assurance methodology, May 26, 2026.</li></ol>

</div>

<div id="bm-content-zh" class="bm-language-content" lang="zh-CN" hidden markdown="1">

# 怎样设计一个真正有评测价值的 Benchmark？

<p class="bm-meta">2026 年 8 月 8 日 · 评测设计 · 约 16 分钟<span id="busuanzi_container_page_pv" class="bm-meta__views" style="display:none;"> · <strong class="bm-meta__views-num" id="busuanzi_value_page_pv">--</strong> 次阅读</span></p>

<p class="bm-deck">题目构建如何暗中定下评分规则，小题集到底保住了什么，以及怎样为真正关心的决策搭建证据。</p>

做 Agent 评测做得越久，一个问题就越绕不开：**如果只挑出一小撮 case，就能还原出接近整套 benchmark 的结果，那剩下的几百上千道题到底在干什么？**

这绝不只是一笔算力账。一千道题里，可能翻来覆去测的都是同一道门槛；一整份难到离谱的考卷，也可能只给弱模型留下一排毫无区分度的零分。更微妙的是，两个模型哪怕最后拿了完全一样的平均分，在工具使用、状态追踪、出错恢复和执行效率上也可能差得极远——而一个只盯着保住均分的精简子集，往往会在对齐平均分的同时，把这些真正关键的差异抹得干干净净。

拿一个极简的十道题排序例子就能看穿问题所在：模型 A 做对了 10 题里的 6 题，模型 B 做对了 5 题，但全是最难的那 5 题。凭 6 比 5 宣布 A “更强”，暗含了一句没人挑明的前提——这十道题每道题的价值一模一样。可这份“等价值”的假设是从哪来的？现实中大多并非出自谨慎的价值权重设计，仅仅取决于当初哪种题更好爬、更好造，恰好攒下了多少道。

<div class="bm-thesis" markdown="1">

**题目构造本身就是评分规则的一部分。** 怎么出题、怎么配额，早就决定了哪些能力需求能走进考卷，以及各自说话有多大分量。把题集压缩做小，可以精准还原出这个原始总分，但既无法替它证明权重本身合不合理，也保不住其他评测决策真正需要的行为证据。

</div>

真正值得花心思回答的是：怎样组一套测试题，才能为我们关心的具体判断提供充分、可信且不虚胖的证据，而不是拿题海数量凑出“科学”的错觉？

<nav class="bm-toc" aria-label="文章目录" markdown="1">

**阅读路线**

1. [压缩究竟保住了什么](#compression-zh)
2. [题目数量怎样变成权重](#weights-zh)
3. [头部公司选择测什么](#frontier-zh)
4. [认真构题具体做了什么](#construction-zh)
5. [把响应变成可解释的证据](#response-zh)
6. [评分器也是测量工具](#scoring-zh)
7. [有限预算下的有效覆盖](#budget-zh)
8. [先设计一道题，再设计一组题](#protocol-zh)
9. [三个值得检验的主张](#validation-zh)

</nav>

<h2 id="compression-zh">小题集到底保住了什么？</h2>

平时随口说的“评估性能”，其实常常混着四件统计上完全不同的事：估算固定题库的平均分、给实力接近的两个模型排前后、预测上线真实业务后的实际效用，或是刻画模型在多个维度上的行为短板。面向其中一件事凑出的小题集，很少能顺带把另外三件事也一起做好。

看看微型评测（micro-benchmarking）的文献就很清楚。在 *tinyBenchmarks* 的实验设定里，只挑 100 道题就能比较准地估算约 14,000 道 MMLU 题目的总成绩；*Anchor Points* 也同样利用不同题目在各个模型之间的得分相关性来砍掉评测开销。[16](#ref-16-zh) [17](#ref-17-zh) 但随后的 *How Reliable is Language Model Micro-Benchmarking?* 紧接着指出了边界所在：总分估计误差小，并不保证能稳稳排清两个水平接近的模型——在它的设定下，真想把相近对手拉开区分度，题量往往得回到 250 题左右，而到这个规模时，单纯随机抽样也已经差不多一样有效了。[18](#ref-18-zh)

一套 benchmark 能被大幅压缩，至少可能出自三种截然不同的原因：题库本身大量重复考察同一类难点；拿来校准的那批模型能力高度同质化，面对不同题目几乎同涨同落；或者我们预测的本来就只是一个标量平均分——还原出“一个数”，天生就比还原一整张多维能力画像容易得多。

不妨做个小思想实验：完全可以有两个模型，在精挑出来的子集上答得一模一样，到了子集之外的题目上却表现迥异。单靠这个子集里的任何观测，根本分不出它们谁是谁。抽样预测之所以能成立，靠的是题间关联、模型分布和任务结构保持稳定；一旦换上训练范式截然不同的新模型，这些隐含前提都得重新接受检验。

<div class="bm-table bm-table-wide" role="region" aria-label="对照表" tabindex="0" markdown="1">

| 评测用途 | 题集必须保留的证据 | 总分估计误差小仍未回答的问题 |
|---|---|---|
| 估计固定题集平均分 | 留出模型上的校准 | 原题集是否代表有用的工作 |
| 区分相近模型 | 配对差异与不确定性 | 微小差距的方向是否正确 |
| 诊断多种行为 | 各目标证据与可解释的遗漏 | 罕见行为是否在选题中消失 |
| 筛查高代价失败 | 相关风险分层内的检出能力 | 高平均分是否掩盖重要尾部 |
| 选择部署模型 | 独立工作负载上的效用 | benchmark 权重是否符合实际需求 |

</div>

我们在开发对比里也一次次撞见同一个落差：多塞进几道失败案例，未必就能多覆盖几个任务家族；单看某一项覆盖率指标往上走，也绝不保证综合权衡就一定更好。覆盖广度与成本控制是一回事，能不能守住总分预测精度又是另一回事——后者永远需要独立的留出模型估分实验来作证。

说到底，压缩表现得好，证明的是“总分可预测”；至于被保留下来的信息值不值得信，还得先问清楚这套 benchmark 最初到底想衡量什么。

<h2 id="weights-zh">隐藏的一步：题目数量变成了权重</h2>

假设我们把题库划成互不重叠的任务家族。如果家族 `g` 塞进了 `n_g` 道题，模型 `m` 在这一族里的均分是 `s_mg`，那平时习以为常的总均分其实是：

<div class="bm-equation">S<sub>D</sub>(m) = Σ<sub>g</sub> (n<sub>g</sub> / N) s<sub>mg</sub></div>

公式里每个 `n_g / N` 都相当于一票权重。只要某类任务恰好更容易合成或者更好写自动化断言，随手多造几十道变体，就能显著抬高它在排行榜上的话语权。造题时的省事，不知不觉就成了评测里的偏心。

如果题目本就按真实业务流量抽样，或者同家族里加题纯粹为了压低估计方差，等权当然说得通。麻烦出在“为了方便爬数或凑够整数配额”的题目占比，悄悄替我们拍板了真实场景的业务频率、出错代价和研究优先级。

回到刚才那十道题的例子：五道常规题，A 全对、B 全错；五道难题，A 对一道、B 全对。现在不做任何实质改动，只把那五条难题记录原封不动复制一遍：

<div class="bm-table bm-table-wide" role="region" aria-label="对照表" tabindex="0" markdown="1">

| 题集组成 | A | B | 等权平均下的领先者 |
|---|---|---|---|
| 5 道常规题 + 5 道难题 | 6/10 = 60.0% | 5/10 = 50.0% | A |
| 5 道常规题 + 原来 5 条难题记录各出现两次 | 7/15 = 46.7% | 10/15 = 66.7% | B |
| 新增独立任务需求 | 0 | 0 | 排名仍然翻转 |

</div>

把确定性记录原样复制两份当然是个刻意构造的极简反例——它不像对非确定性 Agent 多跑几轮 rollout 那样能降低运行噪声，实质上零新增任何独立证据，却硬生生把难题家族的权重从 `1/2` 抬到了 `2/3`。

如果真实业务中难题家族占的比重是 `p`，固定两组各自的准确率，两者的期望效用分别是：

<div class="bm-equation">U<sub>A</sub>(p) = 1 − 0.8p &nbsp;&nbsp; U<sub>B</sub>(p) = p &nbsp;&nbsp; U<sub>A</sub> = U<sub>B</sub> ⇔ p = 5/9 ≈ 55.6%</div>

<figure><img loading="lazy" src="{{ '/assets/benchmark-measurement/weights-zh.svg' | relative_url }}" alt="图 1 · 排名依赖任务权重。解析构造例子：两条曲线在 p = 5/9 相交。竖虚线对应原题集和难题记录复制后的题集。"><figcaption><strong>图 1 · 排名依赖任务权重。</strong>解析构造例子：两条曲线在 p = 5/9 相交。竖虚线对应原题集和难题记录复制后的题集。</figcaption></figure>

`p` 不到 `55.6%` 时 A 赢，跨过去就是 B 反超；换算成单题价值倍率 `r`，只要一道难题顶得上 `1.25` 道常规题以上，B 就应该排在前面。关键在于：**题目本身有多难，并不能替你决定 `p` 或 `r` 该取多少。** 一道偏门极难题在实际生产里可能压根没人碰，而一道简单的高频常规操作一旦出错却可能代价惨重。

*The Benchmark Lottery* 早在传统 NLP 基准里就拿出过现成证据：仅仅从 SuperGLUE 的 8 个子任务里挑出 4 个来算总榜，70 种合法组合竟能选出 6 个不同的第一名。[21](#ref-21-zh) 设计考卷时真正逃不掉的问题是：你凭什么选用这一套组合与比例？

工程上更清醒的做法是把两件事解耦：由真实业务或科学目标来拍板**各任务家族占多少权重**，而**每个家族内部放多少道题**则只服务于压低测算误差。多生成几套等价变体，不该白白多赚几张投票；遇到任务目标彼此交叠时，也得把合并规则挑明，别装作各家族全都能井水不犯河水。

<details markdown="1"><summary>题目反应理论会自动把 B 排到前面吗？</summary>

最简单的 Rasch 模型不会。在共同完整题集、固定题目难度、共同区分度、单维能力和局部独立的条件下，总正确数是能力参数的充分统计量。似然导数为 Σy<sub>i</sub> − Σσ(θ − b<sub>i</sub>)，所以拟合能力随总正确数增加。5/10 不会因为答对的题看起来更难就超过 6/10。更复杂的模型会改变假设，但仍不能替使用者决定什么更重要。

</details>

<h2 id="frontier-zh">头部公司选择测什么？</h2>

从各家大模型的发布报告里，大致能看清当前行业最急于证明的能力版图：工程代码改动、专业知识交付、SaaS 业务自动化、桌面操作与科学研究流程。下面是截至 2026 年 10 月 8 日核对的三份代表性发布配置：

<div class="bm-table bm-table-wide" role="region" aria-label="对照表" tabindex="0" markdown="1">

| 发布报告 | 使用的部分 benchmark | 决定比较含义的设置 |
|---|---|---|
| OpenAI · GPT-6.1 Sol | DeepSWE 1.1、GDP.pdf、AutomationBench 1.0.6、OSWorld 2.0、Terminal-Bench Science 0.1 | OSWorld 使用指定离线版本的部分得分；同时报告推理设置与每任务成本。[1](#ref-1-zh) |
| Anthropic · Sonnet 5.5 | Terminal-Bench 4.0、FrontierCode 1.1、CursorBench 4.0、GDPval-AA v2.1、OSWorld 2.1 | OSWorld 为部分得分；最高推理档位并非每项都最佳。FrontierCode 的 Max 为 46.2%，Xhigh 为 52.1%。[2](#ref-2-zh) |
| Google DeepMind · Gemini 4 Argon | 工程、知识工作、科学、长上下文与电脑操作 | OSWorld 离线评测明确版本和 500 步预算，三次运行取最高；区分自测与外部报告结果。[3](#ref-3-zh) |

</div>

在我看来，这一轮选型其实围着三项共同需求转：够贴近真实产品工作流、终点状态可以被稳定验收、在花得起的算力下还能拉出强模型之间的身位。不过公开报告终究偏重结果展示，各家内部究竟怎么筛选和裁剪题池，外人大多看不到全貌。

更常见的一个误区是：光看榜单上写着同一个 benchmark 名字，就直接拿分数拉通比较。离线的还是在线离线混跑、严格全对才算分还是按步骤给部分分、跑一轮还是三次取最好、外围配了什么工具权限和脚手架——只要其中一项变了，量出来的就已经不是同一把尺子。一条靠得住的模型分数结论，永远绑定在**题集版本、家族权重、外围框架、预算上限与评分脚本**这五件事上。

头部实验室用不用某个 benchmark，只能说明它有影响力；值不值得我们把决策押上去，还得拆开看它是怎么把题做出来的。

<h2 id="construction-zh">认真构题，具体做了什么？</h2>

“纯人工手写”“领域专家设计”“算法自动生成”听上去像三种流派，其实说的都只是生产工艺；真正让一套题集立得住的，是工艺流程里卡住了多少道质量关。

<div class="bm-table bm-table-wide" role="region" aria-label="对照表" tabindex="0" markdown="1">

| Benchmark | 构建依据 | 下一层问题 |
|---|---|---|
| GPQA 原版 | 448 道专家科学题；专家准确率 65%，非专家可联网时为 34%。[4](#ref-4-zh) | 科学问答能向开放式研究迁移多远？ |
| DeepSWE | 113 个任务、91 个仓库、五种语言；题面、行为判定器、参考解与质量审查。[5](#ref-5-zh) [22](#ref-22-zh) | 仓库与任务组合代表哪一种工程工作负载？ |
| AutomationBench 1.0.6 | 六类业务职能、47 个工具、隔离公司状态，以及正负终态断言。[6](#ref-6-zh) | 工作流配额和交互规则是否对应目标部署？ |
| AppWorld 原版 | 九个应用、457 个 API、750 个任务；程序化状态检查，包含不应发生的改动。[7](#ref-7-zh) | 成功除了说明完成指定任务，还能说明什么？ |
| ToolSandbox | 有状态工具、隐含依赖、模拟用户、中间与最终里程碑。[8](#ref-8-zh) | 里程碑是否容纳合法替代路径？ |
| OSWorld 2.0 | 108 个长流程任务；终态评分与轨迹层面的挑战触达分析。[9](#ref-9-zh) | 换框架或预算后，挑战归因是否仍然可靠？ |
| HealthBench 原版 | 5,000 段对话、262 位医生、48,562 条情境评分标准。[10](#ref-10-zh) | rubric 判断怎样联系目标场景中的实际结果？ |

</div>

DeepSWE 的工程验收流程很值得细看：每道题必须配齐题面、行为判定器和可跑通的参考解，测试专门对着可观察行为下断言，兼容不同的合法实现写法，还要靠重复运行排掉不稳定用例。[22](#ref-22-zh) 这套做法把**单题质量**兜得很扎实。但单题靠谱不自动等于全局有代表性——按热度门槛筛出的活跃开源仓库代表的是特定工程切面，而且用同一套固定框架控变量，也不等于这框架天然对各家模型一视同仁（顺带一提，原构建报告里测试原生框架差异时也只用了十道题）。

AutomationBench 则从业务状态复杂度入手：特意往测试环境里塞重名记录、过期字段和藏在聊天消息里的业务约束，验收时既查该做的改了没有，也查不该碰的记录有没有受损。[6](#ref-6-zh) 官方示例里，6 条断言过 5 条只能拿部分分，6 条全过才算真正完成——这就把“随便改了一条记录”与“改对目标且零误伤”明确分开了。当然，真要拿它的总分代表某个岗位的工作负载，六大业务线的配额比例依然需要额外论证。

即便是算法自动生成的考卷，同样可以把设计目的摆上桌面，比如 *AutoBencher* 会顺着难度、主题重要性和行为分叉度直接去优化生成出的测试集。[11](#ref-11-zh) 真正关键的后一步在于验证：这些被优化出来的建构指标，到底有没有换来更靠谱的下游评判。

把视野放大到整个领域，这恰恰是最普遍的短板。在 *Measuring what Matters* 这项综述里，29 位专家一起审计了 445 篇 benchmark 论文：[12](#ref-12-zh)

<figure><img loading="lazy" src="{{ '/assets/benchmark-measurement/validity-zh.svg' | relative_url }}" alt="图 2 · 定义目标与验证测量是不同环节。Bean 等人审查 445 篇论文：78.2% 定义所测对象，53.4% 提供构念效度论据，16.0% 使用不确定性估计或统计检验。类别可重叠，统计的是论文报告中的做法。"><figcaption><strong>图 2 · 定义目标与验证测量是不同环节。</strong>Bean 等人审查 445 篇论文：78.2% 定义所测对象，53.4% 提供构念效度论据，16.0% 使用不确定性估计或统计检验。类别可重叠，统计的是论文报告中的做法。</figcaption></figure>

<h2 id="response-zh">响应提供线索，执行使它可以解释</h2>

很多贴着“状态跟踪”标签的 Agent 测试题，在实跑时经常出现两种假象：模型可能刚起步就卡在文件路径报错上，压根没走到考验状态更新的那一步；反过来，它也可能走了一条完全合规的近路，压根没用到历史反馈就把题做完了。无论哪种情况，任务本身算过还是算不过都很合理，但硬把结果归因到“状态跟踪能力有多强”，证据就虚了。

OSWorld 2.0 已经开始在报告里统计每个内置难点究竟是“真被触发了”、“中途被前置故障挡住了”还是“全程被绕过去了”。[9](#ref-9-zh) 沿着这条路再推一步，执行轨迹本身就能变成构念效度（construct validity）的检验尺：看一道题号称要考的难点，在真实跑起来时到底考没考到。

<div class="bm-table bm-table-wide" role="region" aria-label="对照表" tabindex="0" markdown="1">

| 观察到的响应 | 竞争性解释 | 有用的检查 |
|---|---|---|
| 删除旧反馈后没有变化 | 任务不依赖它；别处仍有信息；模型稳健；干预未生效 | 检查信息读取，确认干预生效，识别合法替代路径 |
| 删除反馈后成功率明显下降 | 信息确实重要；也可能同时改变了长度、格式、可解性或工具行为 | 使用匹配的非目标改动，以及恢复信息的对照 |
| 大量失败发生在目标挑战之前 | 前置瓶颈遮住了目标 | 同时报告总体任务结果与挑战触达数 |
| 很多题出现相同响应 | 证据重复；也可能是源模型高度相关 | 按任务家族分组，并检验新模型家族 |
| 部分得分变化，完成率不变 | 局部进展变化，完整交付门槛未跨过 | 联合阅读中间状态与最终交付 |

</div>

一套靠得住的行为审计，通常要串起五个问题：题面承诺测什么？执行轨迹里实际读取并触发了哪些信息与状态？把关键因素删掉做消融时，题目本身是否还保持合法可解？做完配对的安慰剂修改和信息恢复对照后，变化是不是真的锁定在了目标机制上？这套解释换到另一家模型家族上还能不能成立？

在这个过程里，一定要保护好合法的替代解法。只要能正确交付，一次性批量查询和分几轮小查询都应该算通过；要是某道号称测长程记忆的题，后来发现单看最后一句输入就能直接解出来，那它丢掉的是“测记忆”的标签依据，并不妨碍它继续作为端到端工程样本留在库里。

分母的口径同样马虎不得。如果只挑那些“成功走到了关键难点”的轨迹来算得分，反而会把早早就挂在第二步的模型衬托得格外亮眼。务必把全量任务分母和难点触达分母同时摆出来，再把运行崩溃、评分异常导致的样本缺失单列一栏。

在研究上，最划算的切入口之一就是系统排查“标签宣称测什么”与“轨迹实际露出了什么”之间的错配，再用实证证明：修补这些错配真的能改写独立的模型选型结论。

<h2 id="scoring-zh">评分器也是实验的一部分</h2>

再精细的题目，配上一个粗糙的评分脚本也会全盘走样。判定器完全可能因为暗自写死了题面根本没提到的函数名，把一份完全正确的代码拒之门外；也可能因为图省事只盯了一个浅层输出，把糊弄过去的错解当成满分放行。标准参考解能跑通，顶多证明了一个正例可用；真正严谨的验收套件，既要能放行合法的替代解法，也得稳稳拦住刻意构造的错误实现。

OpenAI 对 SWE-bench Verified 中挑出的 138 道高难题做的专项审计，把这件事摆在了明面上：在这批被审计题目里，高达 59.4% 存在实质性的单元测试或题意规范缺陷。[13](#ref-13-zh) 只要判定脚本预设的要求没在题面写明，最终榜单量出来的就不再纯粹是模型水平，而是模型猜对隐藏测试偏好的运气。

<figure><img loading="lazy" src="{{ '/assets/benchmark-measurement/scoring-zh.svg' | relative_url }}" alt="图 3 · 判分正确与指标含义是两个问题。左：SWE 审计选择的 138 题，而非完整 500 题；40.6% 是所列问题之外的剩余比例。右：OSWorld 2.0，Opus 4.8、maximum thinking、批量调用、500 步；完整完成率 20.6%，平均部分得分 54.8%。来源：[13]、[9]。"><figcaption><strong>图 3 · 判分正确与指标含义是两个问题。</strong>左：SWE 审计选择的 138 题，而非完整 500 题；40.6% 是所列问题之外的剩余比例。右：OSWorld 2.0，Opus 4.8、maximum thinking、批量调用、500 步；完整完成率 20.6%，平均部分得分 54.8%。来源：[13]、[9]。</figcaption></figure>

哪怕代码层面零 bug，指标本身照样会被念歪——图 3 右侧就是现成例子。部分得分反映的是朝着终点推进了多远，二值完成率衡量的才是整套交付是否全部过关；把 54.8% 的平均部分分听成“模型完成了一半以上的任务”，和实际 20.6% 的完整通过率之间差着一大截。

近来的评测协议审计还抖出了不少靠走捷径拿高分的漏洞：某个因果发现测试被发现能利用题面变量的排列规律，硬把得分从 0.018 刷到 0.639；[14](#ref-14-zh) 在 Agent 安全基准 R-Judge 上，只要无脑把所有样本一律判成“不安全”，F1 竟然就能拿到 0.690，直接超过 21 个认真做区分判断模型里的 5 个。[15](#ref-15-zh) 拿退化策略和投机取巧去撞评分器，正是检验“规则奖励的到底是不是能力”最直接的办法。

所以做题集的验收测试时，负例和正例同样不可或缺：错解、偷懒近路和禁止出现的副作用，都必须稳定触及红线才行。

<h2 id="budget-zh">固定预算下，优化真正需要的证据</h2>

当顶尖模型纷纷刷到接近满分时，加难题能帮你重新拉开分差；可一旦题难到几乎所有模型全军覆没，继续往上堆更难的题，几乎提供不了任何关于强弱差异的新信息。在区分度取 1 的单维 Rasch 模型里，每道题提供的 Fisher 信息量等于 `p(1 - p)`，刚好在通过率 `p = 0.5` 时达到峰值：

<figure><img loading="lazy" src="{{ '/assets/benchmark-measurement/information-zh.svg' | relative_url }}" alt="图 4 · 难度要相对于被测群体来谈。Rasch 解析曲线，I(θ) = p(1 − p)，p = σ(θ − b)。它描述局部能力估计的信息量；业务重要性和失败代价是另外的量。"><figcaption><strong>图 4 · 难度要相对于被测群体来谈。</strong>Rasch 解析曲线，I(θ) = p(1 − p)，p = σ(θ − b)。它描述局部能力估计的信息量；业务重要性和失败代价是另外的量。</figcaption></figure>

但如果你关心的是揪出罕见的高危事故，样本量账本就得彻底换一套算法。在各次测试相互独立、真实事故率只有 `1%` 的前提下，连测 `n` 次一次都没撞见的概率依然有 `0.99^n`：

<figure><img loading="lazy" src="{{ '/assets/benchmark-measurement/rare-zh.svg' | relative_url }}" alt="图 5 · 估计均值与检出罕见失败需要不同设计。在这个独立、失败率为 1% 的模型中，测 20 题仍有 81.8% 的概率看不到失败，测 100 题为 36.6%。至少 299 题才有约 95% 的机会观察到一次或更多失败。"><figcaption><strong>图 5 · 估计均值与检出罕见失败需要不同设计。</strong>在这个独立、失败率为 1% 的模型中，测 20 题仍有 81.8% 的概率看不到失败，测 100 题为 36.6%。至少 299 题才有约 95% 的机会观察到一次或更多失败。</figcaption></figure>

正因如此，成熟的多目标 Agent 评测给出的往往是一张维度向量，而不是硬压成一个总分：工具调用合规度、长程反馈记忆、状态写回准确性、异常恢复和质量受约束下的效率，各管各的问题。前四项拿满，补不上第五项的缺口。

真要谈“覆盖全不全”，得先说清楚按什么单位数。令 `U_g` 表示目标 `g` 下所有经过梳理审计的行为条件集合，`E_g(S)` 表示被选中的测试集 `S` 在实际合格执行中真正证实测到的条件，那么去重后的独立条件覆盖率就是：

<div class="bm-equation">C<sub>g</sub>(S) = |E<sub>g</sub>(S) ∩ U<sub>g</sub>| / |U<sub>g</sub>|</div>

最费功夫的一步恰恰在于把 `U_g` 定义清楚并逐条审计。换一百种说法来问同一个约束条件，增加的是重复观测数，而不是独立覆盖率 `C_g(S)`——重复度和广度必须分开记账。（至于 `U_g` 压根还没定义或审计的情况，覆盖率叫“未知”，绝对不是 100%。）

当年 CheckList 按“语言能力维度 × 测试类型”搭起行为测试矩阵，给静态 NLP 树了很好的样板。[20](#ref-20-zh) 到有状态的 Agent 这里又多出一层要求：行为条件不仅要写在题面里，还必须在真实执行中确实发生过。因此，标签覆盖率、工具调用覆盖率和经执行证实的行为覆盖率，根本在回答三个不同层面的问题。

在覆盖度、低冗余、分数还原和评测预算无法同时拉满时，用 Pareto 前沿把几组合理取舍并排留下来很有用；但也别忘了，前沿本身高度依赖你输进去了哪些优化目标，那些目标反过来依然要接受真实部署场景的检验。

<h2 id="protocol-zh">先设计一道题，再设计一组题</h2>

不妨落到一道具体例题来看：**在指定截止时刻前依据最新有效的审批记录，更新正确的订单、通知对应负责人，并确保其余订单丝毫不受影响。** 沙箱环境里特意放进了两笔名字相近的订单、一封更早的批准邮件，以及一条随后推翻旧结论的变更消息。

给这道题打上“记忆与规划”的标签只是开头。真要把它做进可信赖的基准里，至少得过一遍下面七层设计检查：

<div class="bm-table bm-table-wide" role="region" aria-label="对照表" tabindex="0" markdown="1">

| 设计层 | 具体要求 | 验收检查 |
|---|---|---|
| 任务契约 | 实体身份、截止时刻、审批优先级、收件人、禁止改动 | 必要信息可通过允许的访问方式获得 |
| 初始状态 | 明确旧审批与后续消息的关系 | 可复现重置；冲突真实存在且可解决 |
| 合法解 | 允许批量查询，也允许逐步查询 | 不同正确实现都能通过 |
| 错误解 | 错订单、过期审批、漏通知、多通知 | 逐项拒绝这些特定错误 |
| 挑战触达 | 读取了哪个版本，何时读取？ | 区分未触达消息与读后误用 |
| 响应对照 | 只改变目标信息的可用性 | 保持可解，加入匹配改动与恢复对照 |
| 题集地位 | 常规工作、稀有风险，还是刻意挑战？ | 明确家族、聚合权重和覆盖单位 |

</div>

走完这七层检查，问题定位会直接落在可观察证据上：“Agent 其实读到了最新的变更批文，写回时却沿用了缓存里的旧状态”，远比一句泛泛的“Agent 记忆力不好”好修得多。当然，那些只能稳定验收最终结果、不好拆细归因的任务，也依然可以保留作端到端测试样本，大可不必勉强贴上细粒度诊断标签。

把视角拉高到整套题集的搭建顺序，先后次序同样大有讲究：先锁定这份评测要服务什么决策、看重哪些目标；再划定相互独立的任务家族和行为条件清单，按实际用途拍板家族权重；接着逐题验收正反例与消融对照；再用少量前期模型试跑把题集里的盲区和雷同用例扫出来；最后冻结题库，专供后续独立评估。如果既想要压力诊断题、又想要贴近真实分布的代表性样本，最稳妥的是分两组单独计分解释，而不是揉进一个糊涂均分里。

长期运行还可以参考 *Dynabench* 的动态补题思路，不断把新露头的高危失败收进版本化挑战集，同时保留一组始终冻结的锚定子集，用来区分到底是模型真进步了，还是考卷本身悄悄改了难度。[19](#ref-19-zh)

<h2 id="validation-zh">三个值得检验的主张</h2>

一套评测方法论只有亮出“什么样的实验结果能把我推翻”，才算真正立住了研究计划。在真实的 Agent 任务上，下面这三条假设最值得优先拿数据验证：

<div class="bm-table bm-table-wide" role="region" aria-label="对照表" tabindex="0" markdown="1">

| 假设 | 实验 | 会削弱该假设的结果 |
|---|---|---|
| 生产配额实质影响模型比较 | 固定模型结果与独立任务内容，改变家族重复倍率；比较普通均值与明确家族权重 | 排名本来就稳定，或原频率已符合用途 |
| 总分保真与目标保真可以分离 | 在独立审计的目标、相近模型比较和新模型家族上检查保分子集 | 低成本成绩估计法同样保住全部必要证据 |
| 响应辅助构建改善独立判断 | 在匹配信息与总成本下，与随机、分层、结构、难度、成绩估计基线比较 | 简单基线持平、收益仅限源模型，或构建成本抵消收益 |

</div>

每一组对照实验开始前，评测目标、选题算法、验收门限和误差容忍范围都得提前冻结好。最终裁判必须落在真正独立的证据上：模型选型要拿到另一套业务负载里验，行为归因要对照人工确认过的缺陷，泛化迁移要上新任务家族。如果拿当初用来挑题的同一批响应分数回头自夸“效果很好”，那不过是证明选择器确实迎合了自己的目标函数。

核算成本也不能只盯最终推理那几毛钱：构题、用参考模型探测响应、再到后续反复评测的总开销全都要算进来，同时报告“同题量”和“同总预算”两条对比线。前期重金细挑出来的精简题集，在高频复用的回归流水线里照样能快速回本，而这个收支平衡点本身就是重要实验结果。

到这里，一开始那个“到底多少道题才够”的问题才有了严肃的停止规则：不是看开发曲线什么时候走平，而是看再多加一批题，对独立目标证据或最终决策质量的边际改善是不是已经跌破事先定好的容忍阈值——针对**特定决策、特定误差要求与特定模型群体**，够了才算真的够了。

## 每增加一道题，都应该回答的问题

说到底，benchmark 从来不只是把一批提示词和测试用例打包在一起。它暗中决定着我们把注意力分给哪些需求、把能力拆解成哪些可观察事件、拿什么尺子判别成败，又如何把成百上千条结果汇总成一个拍板结论。

这四道工序环环相扣，根本没法拆开单看：如果生成便利决定了各族题量配额，再怎么精简压缩也只是更快地复刻了某种缺乏依据的偏心；如果轨迹根本没踩中标称的难点，再高的名义覆盖率背后也是证据空白；如果评分脚本还在给投机取巧送分，加题越多只会让有偏的榜单个个看起来更加精确。

实打实的解法其实很朴素，就是把每个环节摊开在阳光下：交代清家族配比的理由，拿合法替代解和刻意错误解双向压测评分器，盯着轨迹核实挑战真被触达，再把整套选择交回独立决策里校验。**往考卷里多加任何一道新题之前，都值得先追问一句：它到底让哪一个具体判断更准了？又带来了什么既有题目提供不了的新证据？**

<h2 id="references-zh">资料与图表数据</h2>

<p class="bm-note">网页资料查阅于 2026 年 10 月 8 日。图 1、4、5 为解析例子，图 2、3 为公开数据重绘。<a href="{{ '/assets/benchmark-measurement/figure-data.json' | relative_url }}">数据与来源</a>。</p>

<ol class="bm-references"><li id="ref-1-zh">OpenAI. <a href="https://openai.com/index/introducing-gpt-6-1-sol/">Introducing GPT-6.1 Sol</a>. 模型发布报告，2026；查阅于2026-10-08。</li><li id="ref-2-zh">Anthropic. <a href="https://www.anthropic.com/claude-sonnet-5-5">Introducing Claude Sonnet 5.5</a>. 模型发布报告，2026；查阅于2026-10-08。</li><li id="ref-3-zh">Google DeepMind. <a href="https://deepmind.google/models/evals-methodology/gemini-4-argon">Gemini 4 Argon: Model evaluation</a>. 官方方法说明，2026。</li><li id="ref-4-zh">Rein et al. <a href="https://arxiv.org/abs/2311.12022">GPQA: A Graduate-Level Google-Proof Q&amp;A Benchmark</a>. 2023预印本，COLM 2024。</li><li id="ref-5-zh">Datacurve. <a href="https://deepswe.datacurve.ai/">DeepSWE v1.1</a>. 官方项目与构建说明；查阅于2026-10-08。</li><li id="ref-6-zh">Zapier. <a href="https://zapier.com/benchmarks">AutomationBench</a>. 官方项目，榜单版本1.0.6；查阅于2026-10-08。</li><li id="ref-7-zh">Trivedi et al. <a href="https://arxiv.org/abs/2407.18901">AppWorld: A Controllable World of Apps and People for Benchmarking Interactive Coding Agents</a>. ACL 2024。本文使用原论文750题口径。</li><li id="ref-8-zh">Lu et al. <a href="https://aclanthology.org/2025.naacl-findings.65/">ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use Capabilities</a>. Findings of NAACL 2025。</li><li id="ref-9-zh">Yuan et al. <a href="https://osworld-v2.xlang.ai/">OSWorld 2.0: Benchmarking Computer Use Agents on Long-Horizon Real-World Tasks</a>. 2026预印本与项目页；图3为项目页所列配置，查阅于2026-10-08。</li><li id="ref-10-zh">Arora et al. <a href="https://arxiv.org/abs/2505.08775">HealthBench: Evaluating Large Language Models Towards Improved Human Health</a>. 2025预印本，原版数据。</li><li id="ref-11-zh">Li et al. <a href="https://arxiv.org/abs/2407.08351">AutoBencher: Towards Declarative Benchmark Construction</a>. ICLR 2025。</li><li id="ref-12-zh">Bean et al. <a href="https://arxiv.org/html/2511.04703v1">Measuring what Matters: Construct Validity in Large Language Model Benchmarks</a>. NeurIPS 2025 Datasets and Benchmarks。图2使用第2节结果。</li><li id="ref-13-zh">OpenAI. <a href="https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/">Why we no longer evaluate SWE-bench Verified</a>. 2026-02-23；138道困难题的选择性审计。</li><li id="ref-14-zh">Shao et al. <a href="https://arxiv.org/html/2607.22368v1">Do Agent Benchmarks Measure Capability? Protocol Validity in the Age of Agentic AI</a>. 2026预印本。因果发现实例见Case 6。</li><li id="ref-15-zh">Wang et al. <a href="https://arxiv.org/html/2607.28685v1">Safety, or Just Capability? A Validity Audit of Agent-Safety Benchmarks</a>. 2026预印本。</li><li id="ref-16-zh">Maia Polo et al. <a href="https://proceedings.mlr.press/v235/maia-polo24a.html">tinyBenchmarks: evaluating LLMs with fewer examples</a>. ICML 2024。</li><li id="ref-17-zh">Vivek et al. <a href="https://aclanthology.org/2024.eacl-long.95/">Anchor Points: Benchmarking Models with Much Fewer Examples</a>. EACL 2024。</li><li id="ref-18-zh">Yauney, Warraich, and Swayamdipta. <a href="https://proceedings.iclr.cc/paper_files/paper/2026/hash/2e2960f2fe9e981f33f51c78656e3ca2-Abstract-Conference.html">How Reliable is Language Model Micro-Benchmarking?</a>. ICLR 2026。</li><li id="ref-19-zh">Kiela et al. <a href="https://aclanthology.org/2021.naacl-main.324/">Dynabench: Rethinking Benchmarking in NLP</a>. NAACL 2021。</li><li id="ref-20-zh">Ribeiro et al. <a href="https://aclanthology.org/2020.acl-main.442/">Beyond Accuracy: Behavioral Testing of NLP Models with CheckList</a>. ACL 2020。</li><li id="ref-21-zh">Dehghani et al. <a href="https://arxiv.org/html/2107.07002v1">The Benchmark Lottery</a>. 2021预印本。</li><li id="ref-22-zh">Datacurve. <a href="https://deepswe.datacurve.ai/blog/deepswe">DeepSWE: Measuring frontier coding agents</a>. 构建与质量验收方法，2026-05-26。</li></ol>

</div>

</div>
<script src="{{ '/assets/benchmark-measurement/article.js' | relative_url }}" defer></script>
