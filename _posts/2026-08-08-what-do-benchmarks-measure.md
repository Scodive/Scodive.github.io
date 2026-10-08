---
layout: default
title: "What Makes a Benchmark Worth Testing?"
date: 2026-08-08
author_profile: true
excerpt: "How case construction shapes scores, what a smaller test set preserves, and how to build evidence for the decisions we actually care about. English / 中文."
---

<link rel="stylesheet" href="{{ '/assets/benchmark-measurement/article.css' | relative_url }}">
<div id="benchmark-essay" class="blog-post-content">
<div class="bm-language" role="group" aria-label="Article language / 文章语言">
<button type="button" data-bm-language="en" aria-pressed="true" aria-controls="bm-content-en" lang="en">English</button>
<button type="button" data-bm-language="zh" aria-pressed="false" aria-controls="bm-content-zh" lang="zh-CN">中文</button>
</div>

<div id="bm-content-en" class="bm-language-content" lang="en" markdown="1">

<p class="bm-kicker">Research essay · Benchmark design</p>

# What Makes a Benchmark Worth Testing?

<p class="bm-deck">How case construction shapes scores, what a smaller test set preserves, and how to build evidence for the decisions we actually care about.</p>

A question has kept coming back in our work on agent evaluation: **if a small subset of cases tells us almost as much as the full benchmark, what were the other cases contributing?**

That question reaches beyond saving inference calls. A thousand cases can repeat the same failure condition. A difficult suite can give weaker models an uninformative wall of zeros. Two models can obtain the same score while differing sharply in tool use, state tracking, recovery, and efficiency. A smaller suite may preserve the average while erasing precisely those differences.

The ranking example makes the problem tangible: A solves six out of ten cases; B solves five, but all five are difficult. Calling A “better” silently assumes that the ten successes have equal value. Where did that assumption come from? Often, from how many cases happened to be collected or generated.

<div class="bm-thesis" markdown="1">

**Case construction is already part of the scoring rule.** The production process determines which demands enter a benchmark and how much weight they receive. Compression may faithfully preserve that score without validating its weights or preserving the evidence needed for other evaluation goals.

</div>

The practical question is therefore: how do we build a set of cases that provides enough distinct, trustworthy evidence for a stated decision?

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

<h2 id="compression-en">01 / What does a smaller test set preserve?</h2>

“Evaluate performance” can mean estimating a fixed benchmark’s mean, ordering nearby models, predicting utility on future work, or describing behavior across several goals. These are different statistical targets.

tinyBenchmarks showed that 100 selected examples could estimate scores on roughly 14,000 MMLU questions in its studied settings. Anchor Points similarly exploited relationships between item outcomes across models to reduce evaluation cost.[16](#ref-16-en) [17](#ref-17-en) But *How Reliable is Language Model Micro-Benchmarking?* found that strong aggregate prediction need not yield reliable comparisons between close models; in its settings, distinguishing such models could require up to about 250 examples, where random sampling became competitive.[18](#ref-18-en)

There are at least three reasons a benchmark can be compressible. Its cases may repeat the same challenge. The calibration models may have highly correlated abilities, so they respond similarly even to substantively different cases. Or the prediction target may simply be a mean: recovering one number is easier than recovering an entire behavior profile.

A useful thought experiment exposes the assumption. Two models can behave identically on a selected subset and differently everywhere else. Observations on the subset alone cannot tell them apart. Prediction becomes possible through assumptions about cross-item relationships, model populations, or task structure—and those assumptions need validation on new models.

<div class="bm-table bm-table-wide" role="region" aria-label="Comparison table" tabindex="0" markdown="1">

| Intended use | Evidence the suite must retain | What a low score-estimation error leaves open |
|---|---|---|
| Estimate a fixed suite’s mean | Calibration on held-out models | Whether the original suite represents useful work |
| Compare nearby models | Paired differences and uncertainty | Whether a small gap has the correct sign |
| Diagnose several behaviors | Evidence for each goal and interpretable omissions | Whether a rare behavior disappeared during selection |
| Screen costly failures | Detection within relevant risk strata | Whether a high mean hides an important tail |
| Choose a deployment model | Utility on an independent workload | Whether the benchmark’s weights match actual needs |

</div>

Our development comparisons sharpened a related distinction: more failed cases did not always mean broader coverage of task families, and improvements on individual coverage measures did not imply a better overall trade-off. Those observations concern coverage and cost. Establishing score preservation requires a separate held-out score-estimation experiment.

**Compression is evidence about a prediction problem. It becomes evidence about benchmark quality only after we specify what information the benchmark was meant to preserve.**

<h2 id="weights-en">02 / The hidden step: case counts become weights</h2>

Partition a benchmark into non-overlapping task families. Family g contains n<sub>g</sub> cases, with model m achieving a family mean s<sub>mg</sub>. The ordinary mean is:

<div class="bm-equation">S<sub>D</sub>(m) = Σ<sub>g</sub> (n<sub>g</sub> / N) s<sub>mg</sub></div>

The factor n<sub>g</sub>/N is a weight. If a workflow is easy to generate or verify, producing more variants increases its influence on the score. A production convenience has become an evaluation preference.

Equal weighting is well motivated when cases are sampled from the target workload and successes have comparable value. Multiple cases can also improve precision within a family. The problem arises when convenience sampling or generation quotas quietly stand in for workload frequency, error cost, or a declared scientific priority.

Consider the ten-case example. A solves all five routine cases and one of five hard cases. B solves none of the routine cases and all five hard cases. Now copy each hard-case record once, leaving every model response unchanged.

<div class="bm-table bm-table-wide" role="region" aria-label="Comparison table" tabindex="0" markdown="1">

| Suite composition | A | B | Leader by the ordinary mean |
|---|---|---|---|
| 5 routine + 5 hard | 6/10 = 60.0% | 5/10 = 50.0% | A |
| 5 routine + the same 5 hard records twice | 7/15 = 46.7% | 10/15 = 66.7% | B |
| Independent task demands added | 0 | 0 | Ranking still reverses |

</div>

This is a constructed counterexample: copying deterministic records adds no independent task evidence, but moves the hard-family weight from 1/2 to 2/3. Repeated stochastic executions are a different operation: they can reduce execution noise.

Let p be the hard-family weight in the intended use. Keeping the two family means fixed gives:

<div class="bm-equation">U<sub>A</sub>(p) = 1 − 0.8p &nbsp;&nbsp; U<sub>B</sub>(p) = p &nbsp;&nbsp; U<sub>A</sub> = U<sub>B</sub> ⇔ p = 5/9 ≈ 55.6%</div>

<figure><img loading="lazy" src="{{ '/assets/benchmark-measurement/weights-en.svg' | relative_url }}" alt="Figure 1 · A ranking is conditional on task weights. Analytic toy example: the curves cross at p = 5/9. The vertical guides show the original mix and the duplicated hard-case mix."><figcaption><strong>Figure 1 · A ranking is conditional on task weights.</strong> Analytic toy example: the curves cross at p = 5/9. The vertical guides show the original mix and the duplicated hard-case mix.</figcaption></figure>

A has the higher observed utility below that threshold; B has the higher utility above it. Equivalently, if each hard-case success is worth r times a routine success, B wins when r > 1.25. **Difficulty itself does not choose p or r.** An obscure hard task can be unimportant, while a simple everyday task can matter enormously.

*The Benchmark Lottery* provides an empirical counterpart: choosing four of SuperGLUE’s eight tasks yields 70 combinations and six different first-place models.[21](#ref-21-en) The important design question is what justifies the combination.

This suggests a concrete separation: set family weights from the intended use, and allocate cases within families to improve precision. More variants should not automatically create more importance. For overlapping goals, aggregation needs an explicit overlap rule rather than the partition formula above.

<details markdown="1"><summary>Would item response theory automatically put B ahead?</summary>

In the simplest Rasch model, it would not. With the same complete item set, fixed item difficulties, common discrimination, a single ability dimension, and local independence, the total number correct is sufficient for the ability parameter. The likelihood derivative is Σy<sub>i</sub> − Σσ(θ − b<sub>i</sub>), so the fitted ability increases with the total correct. A score of 5/10 does not overtake 6/10 just because the correct items look harder. More elaborate models change the assumptions; they still do not determine what a user should value.

</details>

<h2 id="frontier-en">03 / What frontier labs choose to measure</h2>

Model releases reveal which kinds of work their authors emphasize: engineering changes, professional deliverables, business automation, computer use, and scientific workflows. The following snapshot was checked on October 8, 2026.

<div class="bm-table bm-table-wide" role="region" aria-label="Comparison table" tabindex="0" markdown="1">

| Release report | Selected benchmarks | Settings that define the comparison |
|---|---|---|
| OpenAI · GPT-6.1 Sol | DeepSWE 1.1; GDP.pdf; AutomationBench 1.0.6; OSWorld 2.0; Terminal-Bench Science 0.1 | OSWorld uses partial reward on a specified offline version; reasoning settings and per-task cost are reported.[1](#ref-1-en) |
| Anthropic · Sonnet 5.5 | Terminal-Bench 4.0; FrontierCode 1.1; CursorBench 4.0; GDPval-AA v2.1; OSWorld 2.1 | OSWorld is partial credit; the highest reasoning setting does not win every task. FrontierCode: 46.2% at Max versus 52.1% at Xhigh.[2](#ref-2-en) |
| Google DeepMind · Gemini 4 Argon | Engineering, knowledge work, science, long context, and computer use | The OSWorld offline evaluation specifies its version and 500-step budget, taking the best of three runs; self-evaluated and externally reported results are distinguished.[3](#ref-3-en) |

</div>

My reading is that these selections serve three needs: relevance to product workflows, checkable outputs, and room to distinguish strong models at meaningful cost. That explains their usefulness as evaluation choices; the public reports do not disclose the complete internal selection process.

The benchmark name alone is insufficient to compare scores. Offline versus combined online/offline tasks, binary completion versus partial reward, one run versus best-of-three, and different tool permissions or agent frameworks define different measurements. A useful model claim is conditional on **the task set, weights, framework, budget, and scorer version**.

Adoption by a frontier lab establishes influence. To understand why a benchmark deserves confidence, we need to inspect its construction.

<h2 id="construction-en">04 / What careful construction actually does</h2>

“Human-written,” “expert-designed,” and “algorithmically generated” describe production methods. Their value comes from the checks those methods enable.

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

DeepSWE makes the acceptance process concrete. Each task includes a prompt, verifier, and reference solution; checks focus on observable behavior, exercise alternative valid implementations, and include repeated runs for flakiness. That supports confidence in individual tasks. Representativeness is a separate question: active open-source repositories above a popularity threshold define a particular slice of engineering. A fixed framework controls conditions but does not establish equal suitability for every model; the native-framework comparison in the construction report used ten tasks.[22](#ref-22-en)

AutomationBench deliberately creates ambiguous records, stale information, and business rules embedded in messages. Its checks include required actions and prohibited side effects. In the official example, satisfying five of six assertions gives partial credit; full success requires all six. These choices make “update a record” materially different from “update the correct record and avoid damaging another.” The family quotas still need a rationale if the score is to estimate an actual workload.[6](#ref-6-en)

Algorithmic generation can make goals explicit too. AutoBencher optimizes dimensions including difficulty, topic importance, and novel performance patterns.[11](#ref-11-en) The next step is to validate the connection between those construction goals and the judgment the resulting suite supports.

The wider evidence shows why this connection matters. In *Measuring what Matters*, 29 experts reviewed 445 benchmark papers.[12](#ref-12-en)

<figure><img loading="lazy" src="{{ '/assets/benchmark-measurement/validity-en.svg' | relative_url }}" alt="Figure 2 · Defining a target and validating its measurement are separate steps. Bean et al., 445 papers: 78.2% defined the phenomenon, 53.4% provided construct-validity evidence, and 16.0% used uncertainty estimates or statistical tests. Categories overlap; these are rates of reported practices."><figcaption><strong>Figure 2 · Defining a target and validating its measurement are separate steps.</strong> Bean et al., 445 papers: 78.2% defined the phenomenon, 53.4% provided construct-validity evidence, and 16.0% used uncertainty estimates or statistical tests. Categories overlap; these are rates of reported practices.</figcaption></figure>

<h2 id="response-en">05 / A response is a clue; execution makes it interpretable</h2>

An agent task labeled “state tracking” can fail before the agent reaches the relevant state change. It can also succeed through a valid path that never requires remembering old feedback. In both cases, the task result is meaningful, but the label overstates the evidence for that specific capability.

OSWorld 2.0 already analyzes whether challenges were encountered, blocked, or left untested.[9](#ref-9-en) This suggests a stronger way to use response examples: inspect the gap between the demand a case claims to test and the demand its execution actually exercises.

<div class="bm-table bm-table-wide" role="region" aria-label="Comparison table" tabindex="0" markdown="1">

| Observed response | Competing explanation | A useful check |
|---|---|---|
| Removing old feedback changes nothing | The task did not need it; another source supplied it; the model was robust; the intervention failed | Inspect information access, verify the intervention, and distinguish valid alternative routes |
| Removing feedback sharply reduces success | The information mattered; or length, formatting, feasibility, or tool behavior also changed | Use a matched non-target edit and an information-restoration control |
| Many failures occur before a target challenge | An upstream bottleneck obscures the target | Report overall task outcomes alongside challenge-reach counts |
| Many cases respond in the same way | Repeated evidence; or correlated source models | Group by task family and test new model families |
| Partial score changes but completion does not | Local progress changed; the completion threshold did not | Read intermediate state and final delivery together |

</div>

A useful audit follows five links: what the task promises to measure; which information and states execution actually reaches; whether the intervention preserves a valid task; whether matched and restoration controls isolate the intended change; and whether the interpretation transfers to another model family.

Legal alternative paths matter. If a task permits either a batch query or several smaller queries, both should pass when they produce the right result. If a purported memory task can be solved entirely from the current request, that is evidence against its memory interpretation, not necessarily against its value as an end-to-end task.

The denominators matter too. Reporting only trajectories that reached the challenge can make a model that fails early look strong on the few surviving runs. Retain both the overall task denominator and the challenge-reach denominator, with missing execution or scoring evidence shown separately.

**The research opportunity is to identify systematic mismatches between claimed demands and observed evidence, then show that repairing them improves an independent evaluation decision.**

<h2 id="scoring-en">06 / The scorer is part of the experiment</h2>

A verifier can reject a correct implementation because it expects an unstated function name, or accept a wrong implementation because it checks only a convenient output. Passing a reference solution establishes one positive example. A stronger acceptance test also exercises valid alternatives and deliberately wrong solutions.

OpenAI’s audit of 138 selected difficult SWE-bench Verified tasks reported material test or specification issues in 59.4% of that audited set.[13](#ref-13-en) This directly identifies a mechanism by which model scores can reflect verifier requirements that the task did not state.

<figure><img loading="lazy" src="{{ '/assets/benchmark-measurement/scoring-en.svg' | relative_url }}" alt="Figure 3 · Correct grading and metric meaning are two different questions. Left: the selected 138-task SWE audit, not the full 500-task suite; 40.6% is the remainder outside the listed issue categories. Right: OSWorld 2.0, Opus 4.8, maximum thinking, batched calls, 500 steps. Binary completion is 20.6%; mean partial reward is 54.8%. Sources: [13] and [9]."><figcaption><strong>Figure 3 · Correct grading and metric meaning are two different questions.</strong> Left: the selected 138-task SWE audit, not the full 500-task suite; 40.6% is the remainder outside the listed issue categories. Right: OSWorld 2.0, Opus 4.8, maximum thinking, batched calls, 500 steps. Binary completion is 20.6%; mean partial reward is 54.8%. Sources: [13] and [9].</figcaption></figure>

The right panel illustrates a different issue: a perfectly implemented metric can still be misread. Partial credit measures progress toward delivery; binary completion measures whether the entire requirement was met. A partial score of 54.8% does not mean 54.8% of tasks were completed.

Recent protocol audits also test whether unintended strategies can earn high scores. One causal-discovery example raised a score from 0.018 to 0.639 by exploiting a variable-ordering pattern in the generator.[14](#ref-14-en) An agent-safety audit found that labeling every example “unsafe” achieved F1 = 0.690 on R-Judge, exceeding five of 21 models that made differentiated judgments.[15](#ref-15-en) These are concrete tests of the relationship between the scoring rule and the behavior it is meant to reward.

A benchmark acceptance suite should therefore contain both sides: behaviors that deserve credit and behaviors that should be rejected, including unintended side effects.

<h2 id="budget-en">07 / Under a fixed budget, optimize the evidence you need</h2>

Harder cases help when current models are saturated. When almost every model fails, adding more difficult cases can produce little additional information about their differences. In a one-dimensional Rasch model with unit discrimination, item information is p(1 − p), maximized at p = 0.5.

<figure><img loading="lazy" src="{{ '/assets/benchmark-measurement/information-en.svg' | relative_url }}" alt="Figure 4 · Difficulty is relative to the population being measured. Analytic Rasch curve, I(θ) = p(1 − p), with p = σ(θ − b). It describes information for local ability estimation; business importance and failure cost are separate quantities."><figcaption><strong>Figure 4 · Difficulty is relative to the population being measured.</strong> Analytic Rasch curve, I(θ) = p(1 − p), with p = σ(θ − b). It describes information for local ability estimation; business importance and failure cost are separate quantities.</figcaption></figure>

Rare-failure screening has another sample-size logic. With independent cases and a true failure probability of 1%, the probability of observing no failures in n trials is 0.99<sup>n</sup>.

<figure><img loading="lazy" src="{{ '/assets/benchmark-measurement/rare-en.svg' | relative_url }}" alt="Figure 5 · Estimating a mean and detecting a rare failure require different designs. In this independent 1% failure model, zero failures remain likely after 20 tests (81.8%) or 100 tests (36.6%). At least 299 tests give roughly a 95% chance of observing one or more failures."><figcaption><strong>Figure 5 · Estimating a mean and detecting a rare failure require different designs.</strong> In this independent 1% failure model, zero failures remain likely after 20 tests (81.8%) or 100 tests (36.6%). At least 299 tests give roughly a 95% chance of observing one or more failures.</figcaption></figure>

For multi-goal agent evaluation, the useful output is often a vector: evidence for tool use, feedback retention, state updates, recovery, and quality-preserving efficiency. A high value on one axis does not fill a missing axis.

Coverage should have a defined unit. Let U<sub>g</sub> be the set of audited behavioral conditions for goal g, and E<sub>g</sub>(S) the conditions supported by acceptable execution evidence from selected cases S. A simple distinct-condition coverage is:

<div class="bm-equation">C<sub>g</sub>(S) = |E<sub>g</sub>(S) ∩ U<sub>g</sub>| / |U<sub>g</sub>|</div>

Here the difficult work is defining and auditing the conditions. If a hundred variants all support the same condition, they increase repeated observations, not the number of distinct conditions. Report those counts separately. An empty or unassessed U<sub>g</sub> is unknown coverage, not 100%.

CheckList’s capability-by-test-type organization offers a useful precedent.[20](#ref-20-en) Stateful agents add the requirement that the condition must actually occur during execution. Label coverage, tool-call coverage, and interpretable behavioral coverage consequently answer different questions.

A Pareto frontier can preserve trade-offs between coverage, redundancy, quality, and cost when no suite wins on all of them. Its meaning is conditional on the objectives and candidate pool. The objectives themselves need validation against the evaluation decision.

<h2 id="protocol-en">08 / Design a case, then design the suite</h2>

Consider an illustrative task: **update the correct order using the approval valid at a specified time, notify its owner, and leave other orders unchanged.** The environment contains two similarly named orders, an earlier approval, and a later change message.

Calling this a “memory and planning” task is only the beginning. Its construction should specify the following.

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

This brings the interpretation closer to observable behavior: “the agent read the new approval but used the old state” is more actionable than “the agent lacks memory.” A task that supports only end-to-end completion can remain valuable without receiving a finer diagnostic label.

At suite level, the construction order matters. Start with the decision and its goals; identify independent task families and behavioral conditions; assign weights from the intended use; construct and accept instances; use model responses to detect gaps and redundancy; then freeze the suite for independent evaluation. If diagnostic challenges and representative workload samples are both useful, retain both groups with their own interpretation.

Dynamic collection, as in Dynabench, can discover new failures.[19](#ref-19-en) Retaining an anchor set alongside versioned challenge sets helps distinguish model progress from changes to the measuring instrument.

<h2 id="validation-en">09 / Three claims worth testing</h2>

The argument becomes a research program when it specifies results that could prove it wrong. These are the three hypotheses I would prioritize; they remain to be tested on the target agent tasks.

<div class="bm-table bm-table-wide" role="region" aria-label="Comparison table" tabindex="0" markdown="1">

| Hypothesis | Experiment | Result that would weaken it |
|---|---|---|
| Production quotas materially affect comparisons | Hold model outcomes and independent task content fixed; vary family multiplicities; compare ordinary means with declared family weights | Rankings are stable, or the original frequencies already match the intended use |
| Score fidelity and goal fidelity can separate | Compare score-preserving subsets on independently audited goals, near-model comparisons, and new model families | Cheap score estimators retain all required evidence equally well |
| Response-assisted construction improves independent judgments | Compare accepted, response-informed suites with random, stratified, structural, difficulty, and score-estimation baselines under matched information and total cost | Simple baselines match it, gains stay within source models, or construction cost erases the benefit |

</div>

For each comparison, freeze the evaluation goals, selectors, acceptance rules, and tolerances before the target run. Use independent evidence for the final judgment: a separate workload for model selection, confirmed behavioral defects for diagnosis, or new task families for transfer. Reusing the selection response as the sole success metric would only show that the optimizer optimized its objective.

Cost accounting should include task construction, model probing, and recurring evaluation. Report both equal-case-count and equal-total-cost comparisons. A costly selection stage can be worthwhile when reused many times; the break-even point is part of the result.

A stopping rule should answer the original question about “how many cases are enough”: enough for which goals, with what uncertainty, on which population? Additional cases become unnecessary for a declared use when their marginal improvement in independent goal satisfaction or decision quality falls below a prespecified tolerance. A flat development score alone cannot establish that condition.

## The question every additional case should answer

A benchmark does more than collect tasks. It distributes attention among demands, turns those demands into observable events, decides which events count as success, and aggregates the results into a judgment.

That is why compression, construction, scoring, and ranking belong in the same discussion. If production quotas determine the weights, a compact suite may reproduce an arbitrary preference very efficiently. If task labels are unsupported by execution, broad nominal coverage may hide missing evidence. If the scorer rewards the wrong behavior, adding cases can make a biased judgment look more precise.

The constructive alternative is to make each link inspectable: justify the mix, verify the case, observe the challenge, test the scorer, and validate the resulting decision. **For every additional case, ask which judgment it improves—and what new evidence makes that improvement possible.**

<h2 id="references-en">Sources and figure data</h2>

<p class="bm-note">Web sources checked October 8, 2026. Figures 1, 4, and 5 are analytic examples; Figures 2 and 3 redraw public data. <a href="{{ '/assets/benchmark-measurement/figure-data.json' | relative_url }}">Data and sources</a>.</p>

<ol class="bm-references"><li id="ref-1-en">OpenAI. <a href="https://openai.com/index/introducing-gpt-6-1-sol/">Introducing GPT-6.1 Sol</a>. Model release report, 2026.</li><li id="ref-2-en">Anthropic. <a href="https://www.anthropic.com/claude-sonnet-5-5">Introducing Claude Sonnet 5.5</a>. Model release report, 2026.</li><li id="ref-3-en">Google DeepMind. <a href="https://deepmind.google/models/evals-methodology/gemini-4-argon">Gemini 4 Argon: Model evaluation</a>. Official evaluation methodology, 2026.</li><li id="ref-4-en">Rein et al. <a href="https://arxiv.org/abs/2311.12022">GPQA: A Graduate-Level Google-Proof Q&amp;A Benchmark</a>. 2023 preprint; COLM 2024.</li><li id="ref-5-en">Datacurve. <a href="https://deepswe.datacurve.ai/">DeepSWE v1.1</a>. Official project, v1.1.</li><li id="ref-6-en">Zapier. <a href="https://zapier.com/benchmarks">AutomationBench</a>. Official project, leaderboard v1.0.6.</li><li id="ref-7-en">Trivedi et al. <a href="https://arxiv.org/abs/2407.18901">AppWorld: A Controllable World of Apps and People for Benchmarking Interactive Coding Agents</a>. ACL 2024; original 750-task release.</li><li id="ref-8-en">Lu et al. <a href="https://aclanthology.org/2025.naacl-findings.65/">ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use Capabilities</a>. Findings of NAACL 2025.</li><li id="ref-9-en">Yuan et al. <a href="https://osworld-v2.xlang.ai/">OSWorld 2.0: Benchmarking Computer Use Agents on Long-Horizon Real-World Tasks</a>. 2026 preprint and project; configuration specified in Figure 3.</li><li id="ref-10-en">Arora et al. <a href="https://arxiv.org/abs/2505.08775">HealthBench: Evaluating Large Language Models Towards Improved Human Health</a>. 2025 preprint; original release.</li><li id="ref-11-en">Li et al. <a href="https://arxiv.org/abs/2407.08351">AutoBencher: Towards Declarative Benchmark Construction</a>. ICLR 2025.</li><li id="ref-12-en">Bean et al. <a href="https://arxiv.org/html/2511.04703v1">Measuring what Matters: Construct Validity in Large Language Model Benchmarks</a>. NeurIPS 2025 Datasets and Benchmarks; Section 2.</li><li id="ref-13-en">OpenAI. <a href="https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/">Why we no longer evaluate SWE-bench Verified</a>. February 23, 2026; selected audit of 138 difficult tasks.</li><li id="ref-14-en">Shao et al. <a href="https://arxiv.org/html/2607.22368v1">Do Agent Benchmarks Measure Capability? Protocol Validity in the Age of Agentic AI</a>. 2026 preprint; causal-discovery example in Case 6.</li><li id="ref-15-en">Wang et al. <a href="https://arxiv.org/html/2607.28685v1">Safety, or Just Capability? A Validity Audit of Agent-Safety Benchmarks</a>. 2026 preprint.</li><li id="ref-16-en">Maia Polo et al. <a href="https://proceedings.mlr.press/v235/maia-polo24a.html">tinyBenchmarks: evaluating LLMs with fewer examples</a>. ICML 2024.</li><li id="ref-17-en">Vivek et al. <a href="https://aclanthology.org/2024.eacl-long.95/">Anchor Points: Benchmarking Models with Much Fewer Examples</a>. EACL 2024.</li><li id="ref-18-en">Yauney, Warraich, and Swayamdipta. <a href="https://proceedings.iclr.cc/paper_files/paper/2026/hash/2e2960f2fe9e981f33f51c78656e3ca2-Abstract-Conference.html">How Reliable is Language Model Micro-Benchmarking?</a>. ICLR 2026.</li><li id="ref-19-en">Kiela et al. <a href="https://aclanthology.org/2021.naacl-main.324/">Dynabench: Rethinking Benchmarking in NLP</a>. NAACL 2021.</li><li id="ref-20-en">Ribeiro et al. <a href="https://aclanthology.org/2020.acl-main.442/">Beyond Accuracy: Behavioral Testing of NLP Models with CheckList</a>. ACL 2020.</li><li id="ref-21-en">Dehghani et al. <a href="https://arxiv.org/html/2107.07002v1">The Benchmark Lottery</a>. 2021 preprint.</li><li id="ref-22-en">Datacurve. <a href="https://deepswe.datacurve.ai/blog/deepswe">DeepSWE: Measuring frontier coding agents</a>. Construction and quality-assurance methodology, May 26, 2026.</li></ol>

</div>

<div id="bm-content-zh" class="bm-language-content" lang="zh-CN" markdown="1" hidden>

<p class="bm-kicker">Research essay · Benchmark design</p>

# 怎样设计一个真正有评测价值的 Benchmark？

<p class="bm-deck">题目构建如何进入分数，小题集究竟保住了什么，以及怎样为真正关心的判断设计证据。</p>

在做 Agent 评测时，一个问题反复出现：**如果只用一小部分 case，就能获得接近完整 benchmark 的信息，其余题目究竟贡献了什么？**

这不只是节省模型调用的问题。一千道题可能反复检验同一种失败条件；很难的题集可能只让弱模型得到一排无法解释的零。两个模型总分相同，工具使用、状态跟踪、错误恢复和效率却可能截然不同。小题集可以保住平均分，同时丢掉恰好最值得了解的差别。

排名的例子让问题变得具体：A 答对十题中的六题；B 答对五题，但五题都是难题。称 A“更好”，暗含了十次成功价值相同的假设。这个假设从哪里来？很多时候，它来自各类题目恰好被收集或生成了多少道。

<div class="bm-thesis" markdown="1">

**题目构建本身就是评分规则的一部分。** 生产过程决定哪些需求进入 benchmark，以及它们占多大权重。压缩可以忠实保留这个分数，却没有验证权重是否合理，也没有保证其他评测目标所需的证据仍然存在。

</div>

因此，真正需要回答的是：怎样构建一组题，为事先明确的判断提供足够、可靠且不过度重复的证据？

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

<h2 id="compression-zh">01 / 小题集到底保住了什么？</h2>

“评估性能”可能指估计固定题集的平均分、区分相近模型、预测未来工作的效用，也可能指描述多个目标上的行为。这些是不同的统计对象。

tinyBenchmarks 在其研究设置中，用 100 道精选题估计约 14,000 道 MMLU 的成绩。Anchor Points 同样利用题目结果在模型之间的关联降低评测成本。[16](#ref-16-zh) [17](#ref-17-zh) 但 *How Reliable is Language Model Micro-Benchmarking?* 发现，总体预测准确未必保证相近模型之间的可靠比较；在其设置中，区分这类模型可能需要多达约 250 道题，此时随机抽样也开始有竞争力。[18](#ref-18-zh)

一个 benchmark 可压缩，至少有三种解释。题目可能反复测同一种挑战；校准模型的能力可能高度相关，因而对实质不同的题也表现相似；预测目标也可能只是平均数——恢复一个数，本来就比恢复整个行为画像容易。

一个思想实验可以揭示其中的假设。两个模型可以在选定子集上完全一致，在其余题上完全不同。只观察子集，无法区分它们。预测之所以可行，依赖的是跨题关系、模型群体或任务结构的假设，而这些假设需要在新模型上验证。

<div class="bm-table bm-table-wide" role="region" aria-label="对照表" tabindex="0" markdown="1">

| 评测用途 | 题集必须保留的证据 | 总分估计误差小仍未回答的问题 |
|---|---|---|
| 估计固定题集平均分 | 留出模型上的校准 | 原题集是否代表有用的工作 |
| 区分相近模型 | 配对差异与不确定性 | 微小差距的方向是否正确 |
| 诊断多种行为 | 各目标证据与可解释的遗漏 | 罕见行为是否在选题中消失 |
| 筛查高代价失败 | 相关风险分层内的检出能力 | 高平均分是否掩盖重要尾部 |
| 选择部署模型 | 独立工作负载上的效用 | benchmark 权重是否符合实际需求 |

</div>

我们的开发比较也让一个相关区别变得清楚：更多失败 case 未必覆盖更多任务家族，单项覆盖指标提高也未必形成更好的综合取舍。这些观察涉及覆盖与成本；要证明总分保真，需要另做留出模型上的成绩估计实验。

**压缩提供的是关于预测问题的证据。只有明确 benchmark 原本要保留什么信息，才能进一步讨论它对题集质量意味着什么。**

<h2 id="weights-zh">02 / 隐藏的一步：题目数量变成了权重</h2>

把题集划分为不重叠的任务家族。家族 g 有 n<sub>g</sub> 道题，模型 m 在其中的平均成绩为 s<sub>mg</sub>。通常的平均分就是：

<div class="bm-equation">S<sub>D</sub>(m) = Σ<sub>g</sub> (n<sub>g</sub> / N) s<sub>mg</sub></div>

其中 n<sub>g</sub>/N 就是权重。如果某种工作流容易生成或验证，多做一些变体就会提高它对总分的影响。生产上的便利，变成了评测中的偏好。

当题目来自目标工作负载的合理抽样，且各次成功价值相近时，等权有充分理由。同一家族的多道题也能提高组内估计精度。问题出在便利采样或生成配额悄悄替代了真实频率、错误代价或明确的研究重点。

回到十道题的例子。五道常规题，A 全对、B 全错；五道难题，A 对一道、B 全对。现在把每条难题记录复制一次，所有模型响应都保持不变。

<div class="bm-table bm-table-wide" role="region" aria-label="对照表" tabindex="0" markdown="1">

| 题集组成 | A | B | 等权平均下的领先者 |
|---|---|---|---|
| 5 道常规题 + 5 道难题 | 6/10 = 60.0% | 5/10 = 50.0% | A |
| 5 道常规题 + 原来 5 条难题记录各出现两次 | 7/15 = 46.7% | 10/15 = 66.7% | B |
| 新增独立任务需求 | 0 | 0 | 排名仍然翻转 |

</div>

这是一个构造反例：复制确定性的记录没有增加独立任务证据，却把难题家族的权重从 1/2 提高到了 2/3。重复随机执行是另一回事，它可以减少执行噪声。

令目标用途中的难题家族权重为 p，保持两类题的组内均值不变，则：

<div class="bm-equation">U<sub>A</sub>(p) = 1 − 0.8p &nbsp;&nbsp; U<sub>B</sub>(p) = p &nbsp;&nbsp; U<sub>A</sub> = U<sub>B</sub> ⇔ p = 5/9 ≈ 55.6%</div>

<figure><img loading="lazy" src="{{ '/assets/benchmark-measurement/weights-zh.svg' | relative_url }}" alt="图 1 · 排名依赖任务权重。解析构造例子：两条曲线在 p = 5/9 相交。竖虚线对应原题集和难题记录复制后的题集。"><figcaption><strong>图 1 · 排名依赖任务权重。</strong>解析构造例子：两条曲线在 p = 5/9 相交。竖虚线对应原题集和难题记录复制后的题集。</figcaption></figure>

低于这一阈值，A 的观测效用更高；高于这一阈值，B 更高。等价地，如果每次难题成功的价值是常规题的 r 倍，r > 1.25 时 B 领先。**难度本身不能决定 p 或 r。** 冷门难题可能不重要，高频简单任务却可能极其重要。

*The Benchmark Lottery* 给出了实际研究中的对应现象：从 SuperGLUE 的八项任务中选四项，70 种组合产生了六个不同的第一名。[21](#ref-21-zh) 设计上真正需要回答的是：为什么选择这种组合？

由此可以明确区分两件事：根据用途确定家族权重，根据估计精度分配家族内部的题量。更多变体不应自动制造更高的重要性。对于相互重叠的目标，聚合时还需要明确处理重叠，不能直接套用上面的分区公式。

<details markdown="1"><summary>题目反应理论会自动把 B 排到前面吗？</summary>

最简单的 Rasch 模型不会。在共同完整题集、固定题目难度、共同区分度、单维能力和局部独立的条件下，总正确数是能力参数的充分统计量。似然导数为 Σy<sub>i</sub> − Σσ(θ − b<sub>i</sub>)，所以拟合能力随总正确数增加。5/10 不会因为答对的题看起来更难就超过 6/10。更复杂的模型会改变假设，但仍不能替使用者决定什么更重要。

</details>

<h2 id="frontier-zh">03 / 头部公司选择测什么？</h2>

模型发布报告展示了作者重点关注哪些工作：工程修改、专业交付物、业务自动化、电脑操作和科学工作流。下面是截至 2026 年 10 月 8 日核对的代表性报告。

<div class="bm-table bm-table-wide" role="region" aria-label="对照表" tabindex="0" markdown="1">

| 发布报告 | 使用的部分 benchmark | 决定比较含义的设置 |
|---|---|---|
| OpenAI · GPT-6.1 Sol | DeepSWE 1.1、GDP.pdf、AutomationBench 1.0.6、OSWorld 2.0、Terminal-Bench Science 0.1 | OSWorld 使用指定离线版本的部分得分；同时报告推理设置与每任务成本。[1](#ref-1-zh) |
| Anthropic · Sonnet 5.5 | Terminal-Bench 4.0、FrontierCode 1.1、CursorBench 4.0、GDPval-AA v2.1、OSWorld 2.1 | OSWorld 为部分得分；最高推理档位并非每项都最佳。FrontierCode 的 Max 为 46.2%，Xhigh 为 52.1%。[2](#ref-2-zh) |
| Google DeepMind · Gemini 4 Argon | 工程、知识工作、科学、长上下文与电脑操作 | OSWorld 离线评测明确版本和 500 步预算，三次运行取最高；区分自测与外部报告结果。[3](#ref-3-zh) |

</div>

我的理解是，这些选择服务于三种需要：贴近产品工作流、交付物可以检查、在有意义的成本下区分强模型。这解释了它们作为评测选择的用途；公开报告没有披露完整的内部筛选过程。

只有 benchmark 名称，不足以比较分数。离线任务与在线离线合并任务、完整完成率与部分得分、单次运行与三次取优、不同工具权限或 Agent 框架，定义的是不同测量。一个有用的模型结论，依赖于**题集、权重、框架、预算和评分版本**。

被头部公司采用说明实际影响力。要理解一个 benchmark 为什么值得信任，还需要进入它的构建过程。

<h2 id="construction-zh">04 / 认真构题，具体做了什么？</h2>

“人工编写”“专家设计”“算法生成”描述的是生产方式。它们的价值来自这种方式具体支持了哪些检查。

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

DeepSWE 把验收过程写得很具体。每题包含题面、判定器和参考解；检查聚焦可观察行为，检验合法替代实现，并通过重复运行检查不稳定性。这些工作支持逐题质量。代表性则是另一层问题：超过关注度门槛的活跃开源仓库，对应特定工程工作范围。固定框架控制了条件，但没有自动证明它对每个模型同样适配；构建报告中的原生框架对照使用了十道题。[22](#ref-22-zh)

AutomationBench 有意放入同名记录、过期信息，以及藏在消息中的业务规则。检查同时覆盖必须发生的操作和禁止出现的副作用。官方例子中，六项断言通过五项只获得部分分，全部通过才算完整成功。这让“更新了记录”与“更新了正确记录且没有破坏其他记录”成为实质不同的结果。如果要用总分估计真实工作负载，任务家族配额仍需要依据。[6](#ref-6-zh)

算法生成也可以把目标显式化。AutoBencher 优化难度、主题重要性、新性能模式等维度。[11](#ref-11-zh) 接下来需要验证的是：这些构建目标，与最终题集能够支持的判断之间有什么联系。

更大范围的证据说明了这种联系为何重要。*Measuring what Matters* 中，29 位专家审查了 445 篇 benchmark 论文。[12](#ref-12-zh)

<figure><img loading="lazy" src="{{ '/assets/benchmark-measurement/validity-zh.svg' | relative_url }}" alt="图 2 · 定义目标与验证测量是不同环节。Bean 等人审查 445 篇论文：78.2% 定义所测对象，53.4% 提供构念效度论据，16.0% 使用不确定性估计或统计检验。类别可重叠，统计的是论文报告中的做法。"><figcaption><strong>图 2 · 定义目标与验证测量是不同环节。</strong>Bean 等人审查 445 篇论文：78.2% 定义所测对象，53.4% 提供构念效度论据，16.0% 使用不确定性估计或统计检验。类别可重叠，统计的是论文报告中的做法。</figcaption></figure>

<h2 id="response-zh">05 / 响应提供线索，执行使它可以解释</h2>

一个标为“状态跟踪”的 Agent 任务，可能在模型遇到相关状态变化之前就失败；也可能通过不需要保留旧反馈的合法路径成功。两种情况下任务结果都有意义，但标签可能夸大了它对指定能力提供的证据。

OSWorld 2.0 已经分析挑战被触达、被阻断或未测试的情况。[9](#ref-9-zh) 这提示了一种更有力的响应分析：检查题目声称要测的需求，与执行中真正发生的需求之间的差距。

<div class="bm-table bm-table-wide" role="region" aria-label="对照表" tabindex="0" markdown="1">

| 观察到的响应 | 竞争性解释 | 有用的检查 |
|---|---|---|
| 删除旧反馈后没有变化 | 任务不依赖它；别处仍有信息；模型稳健；干预未生效 | 检查信息读取，确认干预生效，识别合法替代路径 |
| 删除反馈后成功率明显下降 | 信息确实重要；也可能同时改变了长度、格式、可解性或工具行为 | 使用匹配的非目标改动，以及恢复信息的对照 |
| 大量失败发生在目标挑战之前 | 前置瓶颈遮住了目标 | 同时报告总体任务结果与挑战触达数 |
| 很多题出现相同响应 | 证据重复；也可能是源模型高度相关 | 按任务家族分组，并检验新模型家族 |
| 部分得分变化，完成率不变 | 局部进展变化，完整交付门槛未跨过 | 联合阅读中间状态与最终交付 |

</div>

有用的审计可以沿五个环节展开：任务承诺测什么；执行真正触达了哪些信息和状态；干预后任务是否仍然有效；匹配对照与恢复对照能否隔离目标变化；这套解释能否迁移到另一个模型家族。

合法替代路径很重要。任务允许批量查询或多次小查询时，只要达到正确结果，两者都应通过。如果一道声称测记忆的题仅靠当前请求就能解决，这削弱的是它的记忆解释，而不一定是它作为端到端任务的价值。

分母也很重要。只报告触达挑战的轨迹，可能让经常前序失败的模型在少数幸存执行上显得很强。应同时保留总体任务分母与挑战触达分母，并单列执行或评分证据缺失。

**值得研究的，是找出“声称测到的需求”与“实际获得的证据”之间的系统性错配，再证明修复能够改善独立的评测判断。**

<h2 id="scoring-zh">06 / 评分器也是实验的一部分</h2>

判定器可能因为预设了题面没有要求的函数名而拒绝正确实现，也可能因为只检查一个方便的输出而接受错误实现。参考解能通过，只建立了一个正例。更完整的验收还需要合法替代解，以及刻意构造的错误解。

OpenAI 对 SWE-bench Verified 中选出的 138 道困难题进行审计，在该审计集合的 59.4% 中发现实质性的测试或说明问题。[13](#ref-13-zh) 这直接指出了一种机制：模型成绩可能反映的是题面没有声明的判定器要求。

<figure><img loading="lazy" src="{{ '/assets/benchmark-measurement/scoring-zh.svg' | relative_url }}" alt="图 3 · 判分正确与指标含义是两个问题。左：SWE 审计选择的 138 题，而非完整 500 题；40.6% 是所列问题之外的剩余比例。右：OSWorld 2.0，Opus 4.8、maximum thinking、批量调用、500 步；完整完成率 20.6%，平均部分得分 54.8%。来源：[13]、[9]。"><figcaption><strong>图 3 · 判分正确与指标含义是两个问题。</strong>左：SWE 审计选择的 138 题，而非完整 500 题；40.6% 是所列问题之外的剩余比例。右：OSWorld 2.0，Opus 4.8、maximum thinking、批量调用、500 步；完整完成率 20.6%，平均部分得分 54.8%。来源：[13]、[9]。</figcaption></figure>

右图说明另一类问题：即使指标实现完全正确，也可能被错误解读。部分得分衡量朝交付目标推进了多少；完整完成率衡量全部要求是否满足。54.8% 的部分得分，不等于 54.8% 的任务已经完成。

近期协议审计也检验了非预期策略能否拿到高分。一个因果发现案例利用生成器中的变量排列规律，将得分从 0.018 提高到 0.639。[14](#ref-14-zh) 一项 Agent 安全审计发现，把 R-Judge 中所有例子都判为“不安全”，F1 可达 0.690，超过 21 个作出区分判断的模型中的五个。[15](#ref-15-zh) 这些是在具体检验评分规则与预期奖励行为之间的关系。

因此，benchmark 的验收应同时包含值得给分的行为，以及应当拒绝的行为，包括不应发生的副作用。

<h2 id="budget-zh">07 / 固定预算下，优化真正需要的证据</h2>

当前模型接近满分时，提高难度有助于扩大区分空间；几乎所有模型都失败时，继续加难题可能很少增加关于模型差别的信息。在区分度为 1 的单维 Rasch 模型中，单题信息量为 p(1 − p)，在 p = 0.5 时最大。

<figure><img loading="lazy" src="{{ '/assets/benchmark-measurement/information-zh.svg' | relative_url }}" alt="图 4 · 难度要相对于被测群体来谈。Rasch 解析曲线，I(θ) = p(1 − p)，p = σ(θ − b)。它描述局部能力估计的信息量；业务重要性和失败代价是另外的量。"><figcaption><strong>图 4 · 难度要相对于被测群体来谈。</strong>Rasch 解析曲线，I(θ) = p(1 − p)，p = σ(θ − b)。它描述局部能力估计的信息量；业务重要性和失败代价是另外的量。</figcaption></figure>

稀有失败筛查有另一套样本量逻辑。假设各题独立，真实失败概率为 1%，n 次测试中一次失败都看不到的概率是 0.99<sup>n</sup>。

<figure><img loading="lazy" src="{{ '/assets/benchmark-measurement/rare-zh.svg' | relative_url }}" alt="图 5 · 估计均值与检出罕见失败需要不同设计。在这个独立、失败率为 1% 的模型中，测 20 题仍有 81.8% 的概率看不到失败，测 100 题为 36.6%。至少 299 题才有约 95% 的机会观察到一次或更多失败。"><figcaption><strong>图 5 · 估计均值与检出罕见失败需要不同设计。</strong>在这个独立、失败率为 1% 的模型中，测 20 题仍有 81.8% 的概率看不到失败，测 100 题为 36.6%。至少 299 题才有约 95% 的机会观察到一次或更多失败。</figcaption></figure>

对于多目标 Agent 评测，有用的输出往往是一个向量：工具使用、反馈保留、状态更新、错误恢复，以及保证质量前提下的效率。一维的高分不会补上另一维的证据缺失。

覆盖需要明确单位。令 U<sub>g</sub> 为目标 g 下经过审计的行为条件集合，E<sub>g</sub>(S) 为所选题集 S 通过合格执行证据支持的条件。一个简单的去重条件覆盖率是：

<div class="bm-equation">C<sub>g</sub>(S) = |E<sub>g</sub>(S) ∩ U<sub>g</sub>| / |U<sub>g</sub>|</div>

这里最难的工作是定义并审计行为条件。如果一百个变体都支持同一条件，它们增加的是重复观测，而非独立条件的数量。这两类计数应分别报告。U<sub>g</sub> 为空或尚未审计时，覆盖是未知，而非 100%。

CheckList 按“能力维度 × 测试类型”组织行为测试，是一个有用的先例。[20](#ref-20-zh) 有状态 Agent 又增加了一项要求：相关条件必须在执行中实际发生。因此，标签覆盖、工具调用覆盖、可解释的行为覆盖，回答的是不同问题。

当没有一套题在所有目标上都最佳时，Pareto 前沿可以保留覆盖、冗余、质量与成本之间的取舍。它的含义依赖目标定义和候选池；目标本身仍需要根据评测决策验证。

<h2 id="protocol-zh">08 / 先设计一道题，再设计一组题</h2>

考虑一道示例任务：**根据指定时刻有效的审批，更新正确订单，通知负责人，不改动其他订单。** 环境中存在两个同名订单、一份较早审批，以及一条后来的变更消息。

把它称为“记忆与规划”任务只是开始。构建时还应明确以下内容。

<div class="bm-table bm-table-wide" role="region" aria-label="对照表" tabindex="0" markdown="1">

| 设计层 | 具体要求 | 验收检查 |
|---|---|---|
| 任务合同 | 实体身份、截止时刻、审批优先级、收件人、禁止改动 | 必要信息可通过允许的访问方式获得 |
| 初始状态 | 明确旧审批与后续消息的关系 | 可复现重置；冲突真实存在且可解决 |
| 合法解 | 允许批量查询，也允许逐步查询 | 不同正确实现都能通过 |
| 错误解 | 错订单、过期审批、漏通知、多通知 | 逐项拒绝这些特定错误 |
| 挑战触达 | 读取了哪个版本，何时读取？ | 区分未触达消息与读后误用 |
| 响应对照 | 只改变目标信息的可用性 | 保持可解，加入匹配改动与恢复对照 |
| 题集地位 | 常规工作、稀有风险，还是刻意挑战？ | 明确家族、聚合权重和覆盖单位 |

</div>

这样，解释会更接近可观察行为：“Agent 读到了新审批，却使用了旧状态”，比“Agent 缺乏记忆”更便于检查和修复。只支持端到端完成判断的任务，也可以保留价值，无需贴上更细的诊断标签。

到了题集层面，构建顺序很重要。先明确决策与目标；识别独立任务家族和行为条件；根据用途设定权重；构造并验收实例；用模型响应检查缺口与冗余；最后冻结题集，进入独立评估。如果诊断挑战和代表性工作样本都有用途，就保留两组及各自的解释。

Dynabench 这样的动态收集可以发现新失败。[19](#ref-19-zh) 同时保留锚定集与分版本挑战集，有助于区分模型进步和测量工具本身的变化。

<h2 id="validation-zh">09 / 三个值得检验的主张</h2>

当论证明确哪些结果会推翻它时，才能形成研究计划。下面是我会优先检验的三个假设；它们还需要在目标 Agent 任务上验证。

<div class="bm-table bm-table-wide" role="region" aria-label="对照表" tabindex="0" markdown="1">

| 假设 | 实验 | 会削弱该假设的结果 |
| 生产配额实质影响模型比较 | 固定模型结果与独立任务内容，改变家族重复倍率；比较普通均值与明确家族权重 | 排名本来就稳定，或原频率已符合用途 |
| 总分保真与目标保真可以分离 | 在独立审计的目标、相近模型比较和新模型家族上检查保分子集 | 低成本成绩估计法同样保住全部必要证据 |
| 响应辅助构建改善独立判断 | 在匹配信息与总成本下，与随机、分层、结构、难度、成绩估计基线比较 | 简单基线持平、收益仅限源模型，或构建成本抵消收益 |

</div>

每次比较，都应在目标运行前冻结评测目标、选题规则、验收规则和容忍度。最终判断使用独立证据：模型选择用另一份工作负载，诊断用已确认的行为缺陷，迁移用新的任务家族。如果只用选题时的响应作为成功指标，就只是证明优化器优化了自己的目标。

成本核算应包含构题、模型探测与后续评测，同时报告相同题数和相同总成本的比较。昂贵的选题阶段在多次复用后可能值得，收支平衡点也是结果的一部分。

停止增题的规则，应回答最初的“多少题才够”：对什么目标、允许多大不确定性、面向哪个群体才够？当新增题对独立需求满足或决策质量的边际改善低于预先设定的容忍度时，才能说它对声明用途已不再必要。开发曲线变平，本身不足以建立这个结论。

## 每增加一道题，都应该回答的问题

一个 benchmark 所做的，不只是收集任务。它在不同需求之间分配注意力，把需求转成可观察事件，决定哪些事件算成功，再把结果聚合为判断。

因此，压缩、构建、评分与排名需要放在同一个讨论中。如果生产配额决定权重，小题集可能只是高效复现了一种缺乏依据的偏好；如果任务标签缺少执行支持，广泛的名义覆盖可能掩盖证据缺口；如果评分器奖励了错误行为，增加题量可能让有偏的判断看起来更加精确。

可执行的改进，是让每个环节都能检查：解释题集组合，验收任务，观察挑战，检验评分器，验证最终决策。**每增加一道题，都应追问：它改善了哪一个判断，又提供了什么新的证据，使这种改善成为可能？**

<h2 id="references-zh">资料与图表数据</h2>

<p class="bm-note">网页资料查阅于 2026 年 10 月 8 日。图 1、4、5 为解析例子，图 2、3 为公开数据重绘。<a href="{{ '/assets/benchmark-measurement/figure-data.json' | relative_url }}">数据与来源</a>。</p>

<ol class="bm-references"><li id="ref-1-zh">OpenAI. <a href="https://openai.com/index/introducing-gpt-6-1-sol/">Introducing GPT-6.1 Sol</a>. 模型发布报告，2026；查阅于2026-10-08。</li><li id="ref-2-zh">Anthropic. <a href="https://www.anthropic.com/claude-sonnet-5-5">Introducing Claude Sonnet 5.5</a>. 模型发布报告，2026；查阅于2026-10-08。</li><li id="ref-3-zh">Google DeepMind. <a href="https://deepmind.google/models/evals-methodology/gemini-4-argon">Gemini 4 Argon: Model evaluation</a>. 官方方法说明，2026。</li><li id="ref-4-zh">Rein et al. <a href="https://arxiv.org/abs/2311.12022">GPQA: A Graduate-Level Google-Proof Q&amp;A Benchmark</a>. 2023预印本，COLM 2024。</li><li id="ref-5-zh">Datacurve. <a href="https://deepswe.datacurve.ai/">DeepSWE v1.1</a>. 官方项目与构建说明；查阅于2026-10-08。</li><li id="ref-6-zh">Zapier. <a href="https://zapier.com/benchmarks">AutomationBench</a>. 官方项目，榜单版本1.0.6；查阅于2026-10-08。</li><li id="ref-7-zh">Trivedi et al. <a href="https://arxiv.org/abs/2407.18901">AppWorld: A Controllable World of Apps and People for Benchmarking Interactive Coding Agents</a>. ACL 2024。本文使用原论文750题口径。</li><li id="ref-8-zh">Lu et al. <a href="https://aclanthology.org/2025.naacl-findings.65/">ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use Capabilities</a>. Findings of NAACL 2025。</li><li id="ref-9-zh">Yuan et al. <a href="https://osworld-v2.xlang.ai/">OSWorld 2.0: Benchmarking Computer Use Agents on Long-Horizon Real-World Tasks</a>. 2026预印本与项目页；图3为项目页所列配置，查阅于2026-10-08。</li><li id="ref-10-zh">Arora et al. <a href="https://arxiv.org/abs/2505.08775">HealthBench: Evaluating Large Language Models Towards Improved Human Health</a>. 2025预印本，原版数据。</li><li id="ref-11-zh">Li et al. <a href="https://arxiv.org/abs/2407.08351">AutoBencher: Towards Declarative Benchmark Construction</a>. ICLR 2025。</li><li id="ref-12-zh">Bean et al. <a href="https://arxiv.org/html/2511.04703v1">Measuring what Matters: Construct Validity in Large Language Model Benchmarks</a>. NeurIPS 2025 Datasets and Benchmarks。图2使用第2节结果。</li><li id="ref-13-zh">OpenAI. <a href="https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/">Why we no longer evaluate SWE-bench Verified</a>. 2026-02-23；138道困难题的选择性审计。</li><li id="ref-14-zh">Shao et al. <a href="https://arxiv.org/html/2607.22368v1">Do Agent Benchmarks Measure Capability? Protocol Validity in the Age of Agentic AI</a>. 2026预印本。因果发现实例见Case 6。</li><li id="ref-15-zh">Wang et al. <a href="https://arxiv.org/html/2607.28685v1">Safety, or Just Capability? A Validity Audit of Agent-Safety Benchmarks</a>. 2026预印本。</li><li id="ref-16-zh">Maia Polo et al. <a href="https://proceedings.mlr.press/v235/maia-polo24a.html">tinyBenchmarks: evaluating LLMs with fewer examples</a>. ICML 2024。</li><li id="ref-17-zh">Vivek et al. <a href="https://aclanthology.org/2024.eacl-long.95/">Anchor Points: Benchmarking Models with Much Fewer Examples</a>. EACL 2024。</li><li id="ref-18-zh">Yauney, Warraich, and Swayamdipta. <a href="https://proceedings.iclr.cc/paper_files/paper/2026/hash/2e2960f2fe9e981f33f51c78656e3ca2-Abstract-Conference.html">How Reliable is Language Model Micro-Benchmarking?</a>. ICLR 2026。</li><li id="ref-19-zh">Kiela et al. <a href="https://aclanthology.org/2021.naacl-main.324/">Dynabench: Rethinking Benchmarking in NLP</a>. NAACL 2021。</li><li id="ref-20-zh">Ribeiro et al. <a href="https://aclanthology.org/2020.acl-main.442/">Beyond Accuracy: Behavioral Testing of NLP Models with CheckList</a>. ACL 2020。</li><li id="ref-21-zh">Dehghani et al. <a href="https://arxiv.org/html/2107.07002v1">The Benchmark Lottery</a>. 2021预印本。</li><li id="ref-22-zh">Datacurve. <a href="https://deepswe.datacurve.ai/blog/deepswe">DeepSWE: Measuring frontier coding agents</a>. 构建与质量验收方法，2026-05-26。</li></ol>

</div>

</div>
<script src="{{ '/assets/benchmark-measurement/article.js' | relative_url }}" defer></script>
