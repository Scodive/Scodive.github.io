---
layout: default
title: "What Is Actually Evolving in a Self-Evolving Agent?"
title_zh: "Agent 自进化，到底在进化什么？"
date: 2026-10-14
author_profile: true
excerpt: "What self-evolving agents actually repair, why completion alone can mislead selection, and when joint objectives, constraints and Pareto archives become useful."
excerpt_zh: "自进化 Agent 到底在修补什么，为什么单一完成率会误导选择，以及多目标优化、硬约束与 Pareto 档案在什么时候变得必要。"
topic: "Self-evolving agents"
topic_zh: "自进化 Agent"
reading_time: "18 min read"
reading_time_zh: "约 18 分钟"
figure_en: "/assets/agent-rsi/evolution-loop-en.svg"
figure_zh: "/assets/agent-rsi/evolution-loop-zh.svg"
figure_alt_en: "Diagram of what changes and what is inherited across agent self-evolution loops"
figure_alt_zh: "Agent 自进化循环中变化与继承关系的示意图"
---

<link rel="stylesheet" href="{{ '/assets/agent-rsi/article.css' | relative_url }}">
<div id="rsi-essay" class="blog-post-content">
<div class="bm-topbar">
<a class="bm-back-link" href="{{ '/blogs/' | relative_url }}" data-en="All essays" data-zh="全部文章">All essays</a>
<div class="bm-language" role="tablist" aria-label="Article language / 文章语言">
<button type="button" role="tab" data-bm-language="en" aria-selected="true" aria-pressed="true" aria-controls="bm-content-en" lang="en">English</button>
<button type="button" role="tab" data-bm-language="zh" aria-selected="false" aria-pressed="false" aria-controls="bm-content-zh" lang="zh-CN">中文</button>
</div>
</div>

<div id="bm-content-en" class="bm-language-content" lang="en" markdown="1">

# What Is Actually Evolving in a Self-Evolving Agent?

<p class="bm-meta">October 14, 2026 · Self-evolving agents · 18 min read<span id="vercount_container_page_pv" class="bm-meta__views" style="display:none;"> · <strong class="bm-meta__views-num" id="vercount_value_page_pv">--</strong> views</span></p>

<p class="bm-deck">What self-improvement methods actually fix, where their gains stop, and how the need for multi-objective optimization emerges.</p>

Imagine a coding agent that picks up a simple habit over training: whenever a test fails, keep retrying. On the dashboard, task completion climbs nicely. It looks like a clean win right up until you look at the traces and realize runs now drag on twice as long, tool calls have more than doubled, and every now and then the agent touches a file outside its permitted directory just to get a green test.

In one sense, the agent learned something genuinely useful: stubborn persistence solves harder bugs. At the same time, it learned an over-general heuristic with ugly side effects. Do you ship the update, roll it back, or search for a variant that retries only when retrying makes sense?

That tension is what I want to unpack across work on self-evolving agents and recursive self-improvement (RSI). Generating candidate edits to an agent has gotten surprisingly easy; deciding which edits count as real progress is where things still fall apart.

<div class="bm-thesis" markdown="1">

Multi-objective optimization enters naturally the moment one edit pulls several properties we care about in opposite directions, leaving single metrics silent on the collateral effects. Before choosing what can be traded off, what stays off-limits, or which variants to keep in an archive, those coupled outcomes have to show up in the same decision loop.

</div>

<nav class="bm-toc" aria-label="Contents" markdown="1">

1. [What existing methods actually repair](#components-en)
2. [When a higher score stops answering the question](#objects-en)
3. [Why fixing one objective at a time can fail](#coupling-en)
4. [From several metrics to a joint decision](#objectives-en)
5. [What multi-objective methods add](#methods-en)
6. [The problems that remain](#evidence-en)
7. [What would demonstrate a better improvement process?](#research-en)
8. [Paper-by-paper guide](#paper-map-en)

</nav>

<h2 id="components-en">What do self-evolving methods actually repair?</h2>

One clean way to organize this literature is by bottleneck. An agent might forget every lesson as soon as a run ends, stay boxed in by clumsy tools, lack an underlying skill, or waste most of its search budget generating weak patches. Each family of self-evolution papers pokes at a different layer.

### When experience disappears after execution

Without cross-run memory, every failure forces the agent to pay the full tuition all over again. *Reflexion* carries verbal critiques across trials, *Voyager* compiles working code snippets into a reusable skill library, and *ACE* turns execution feedback into an evolving context playbook.[1](#ref-1-en) [2](#ref-2-en) [10](#ref-10-en)

All three tackle the same gap: **turning finished runs into experience the next run can actually use.** Storing a rule, however, does not specify its boundaries. "Retry after a failure" rescues transient network hiccups and turns reckless when the failure was a permission refusal, so memory systems still need a way to track *when* a lesson stops applying.

### When better instructions cannot fix the action structure

Telling an agent to "edit carefully" does not fix an imprecise file-patching tool. Changing code and workflow topology opens a much bigger lever: *ADAS* and *AFlow* search over workflows automatically, while *DGM* rewrites its own tools and execution control flow, including sharper edit primitives.[5](#ref-5-en) [6](#ref-6-en) [8](#ref-8-en)

What moves here is **the set of actions available and how they compose**, which explains why optimizing around frozen weights can jump scores so sharply. Plenty of times the base model already knows enough to fix the bug, while awkward harness plumbing gets in its way. Even then, a workflow tuned for one bug class can stay surprisingly brittle on the next unless we inspect what changed and where it breaks.

### When the model needs to learn a capability

Scaffolding only goes so far when the base model misses core reasoning steps. *SEAL* rewards generated self-edit directives by downstream performance *after* gradient updates, while *Agent0* and *AgentEvolver* manufacture training tasks and trajectories from environment interaction.[11](#ref-11-en) [12](#ref-12-en) [13](#ref-13-en)

The target here is **the quality and supply of training signal**. As soon as weights start updating, data quality becomes the choke point: repetitive curricula or noisy reward proxies simply bake bad habits into parameters faster. Curriculum builders therefore have to be judged on which real distinctions they teach the policy.

Runtime scaffolding and parameter updates can also interlock. *HELIX* sketches a build–update–rebuild loop that evolves harnesses, feeds contrasting verified traces into model updates, and re-adapts the harness around the new checkpoint (though its published experiment covers one harness round and its training trace export).[30](#ref-30-en)

### When the improvement process is itself inefficient

RSI steps back one level from improving the agent to improving the *improver*. *Promptbreeder* mutates the prompts that mutate task prompts; *STOP* runs an optimizer on its own optimizer script; *HyperAgents* exposes both task code and meta-agent logic to edits; *AIDE²* iterates on research harnesses; and *Dream-RSI* updates exploration policies using replayed trajectories.[3](#ref-3-en) [4](#ref-4-en) [14](#ref-14-en) [16](#ref-16-en) [17](#ref-17-en)

The goal shifts to **finding better edits under the same search budget**. Ending up with a stronger task agent is nice; ending up with an update loop that consistently proposes stronger edits is a much stiffer claim and requires its own baseline test. Worse, recursion inherits any blind spot in the evaluator: a smarter search procedure only becomes faster at gaming an incomplete objective.

<figure>
<picture>
<source media="(max-width: 640px)" srcset="{{ '/assets/agent-rsi/evolution-loop-en-mobile.svg' | relative_url }}">
<img src="{{ '/assets/agent-rsi/evolution-loop-en.svg' | relative_url }}" alt="An improver proposes changes to agent components. Execution produces evidence, selection retains changes, and the next run inherits them. A recursive path also changes the improver." loading="lazy">
</picture>
<figcaption><strong>Figure 1.</strong> An evolving system has an editable object and a selection loop. The solid path updates the agent; the dashed path also updates the improver.</figcaption>
</figure>

Across all four layers, everything boils down to two engineering levers: what is allowed to mutate, and what evidence earns an update the right to survive. Most papers push hard on the first lever; taking the second seriously pushes straight toward multi-objective evaluation.

<h2 id="objects-en">A higher completion rate can leave the decision unresolved</h2>

Go back to our coding agent on a 100-task suite, pairing a completion test with an audit checking whether every tool call respected file and command permissions:

<div class="bm-table bm-table-wide bm-case" role="region" aria-label="Illustrative agent update comparison" tabindex="0" markdown="1">

| Policy | Completed tasks | Mean tool calls | 95th-percentile time | Runs with an unauthorized action |
|:--|:--|:--|:--|:--|
| P0 · Original | 80 / 100 | 6 | 40 seconds | 0 / 100 |
| P1 · Retry broadly | 89 / 100 | 14 | 110 seconds | 4 / 100 |
| P2 · Retry selectively and check scope | 88 / 100 | 8 | 55 seconds | 0 / 100 |

</div>

<p class="bm-note">Illustrative values for the thought experiment. Completion and authorization are counted separately, so a completed task can still involve an unauthorized action.</p>

If the selector optimizes raw pass rate alone, P1 wins effortlessly. Under a hard 45-second tail-latency SLA, P0 looks safer. If touching forbidden paths is a strict blocker, P1 is dead on arrival regardless of its 89% solve rate, leaving P2 as the clear practical winner because it preserves almost all the upside while keeping cost and safety intact.

Once agents run real tools under latency budgets and security rules, passing the unit test tells you *whether* the agent crossed the finish line, not *how* it got there. **Reaching the endpoint and reaching it within policy are separate properties.**

Separating *objectives* from *diagnostics* helps keep scorecards clean too. Counting repeated invalid tool syntax as both a latency hit and its own weighted objective double-counts the same bug. Derive the core objectives directly from deployment constraints, and use finer trajectory stats to diagnose why a policy landed where it did.

<h2 id="coupling-en">Why not improve capability first, then repair the rest?</h2>

The standard instinct is sequential: push completion up first, then prune token cost and safety regressions afterward. The snag is that capability, latency, and safety usually run through the exact same control knobs. Raising retry limits moves solve rate, API spend, and tail runtime all at once; adding verification catches bugs while adding seconds to every turn; tightening stopping rules cuts unsafe exploration while occasionally cutting legitimate debugging short.

Play out sequential hill-climbing on P1. First someone bolts on a cost patch capping tool calls at 10; maybe it cuts dead loops, or maybe it chops off the last two retries that actually solved the hard tickets. Next cycle, a capability proposer sees those dropped tickets and bumps the retry budget right back up. Every isolated hill-climb looks defensible on its own dashboard while the overall agent treads water.

Real fixes are usually conditional rules: retry transient I/O errors, repair malformed parameters in place, abort on permission denial, and reserve expensive tests for risky edits. All four failures look identical in a binary pass/fail column, yet each demands a surgical edit. Scalar vectors expose the side effects together; trace inspection shows *where* in the mechanism the policy misfired.

*Meta-Harness* puts this diagnostic loop directly inside the optimizer by giving its proposer code diffs, evaluation numbers, and raw execution trajectories instead of an opaque average score.[29](#ref-29-en)

Why not simply maximize completion during search and slap a safety filter on at deployment time? A deployment gate will happily block P1 from production, yet it cannot magically invent P2 if greedy survival already pruned P2 three generations ago. Even when teams archive every rollout log, deciding which parent checkpoints deserve the next round of mutation spend still steers what the search discovers next. **Selection shapes tomorrow's search pool, not just today's winner.**

Joint optimization pulls deployment constraints upstream into candidate generation, survival, and branching. Scalar scores, explicit constraints, and multi-variant archives are simply different mechanisms for letting those constraints steer the loop early.

Sometimes a perceived trade-off is just sloppy plumbing anyway. Swapping a flaky file-patcher for a reliable diff tool can simultaneously boost solve rate and slash retry calls. Joint diagnostics help spot genuine Pareto improvements alongside true, unavoidable trade-offs.

<h2 id="objectives-en">From several metrics to a joint decision</h2>

### First, identify what cannot be exchanged

If deleting forbidden files is unacceptable, completing five extra tickets never compensates for doing it once. Hard boundaries belong inside feasibility checks backed by runtime sandboxing wherever possible: observed violations disqualify a candidate outright (keeping in mind that zero violations on 100 eval tasks still only bounds empirical risk, never proves formal immunity).

Explicit constraints untangle two decisions people routinely blur together: "Is this policy safe and compliant to run?" versus "Among compliant candidates, which cost-quality balance fits best?"

### Next, make preferences explicit when they are known

When the trade-off between quality, spend, and runtime is well understood and stable, folding them into a scalar utility is clean and direct. *SICA* does exactly this, blending task success, dollar cost, and wall-clock time into one objective.[7](#ref-7-en)

Our table illustrates how sensitive scalar weights are, even over clean numbers. Ignore authorization for a second and trade completion against tool calls: docking `0.1` percentage points per call scores P1 at `87.6` over P2's `87.2`; bump that penalty to `0.5` points per call and the gap flips (`82` vs. `84`). Both calculations are accurate, yet tiny normalization or weight tweaks flip the champion, and re-enabling the hard authorization check disqualifies P1 either way.

### Preserve alternatives when one preference would be premature

When a single codebase serves latency-sensitive interactive users alongside offline batch jobs, locking onto one weighted sum prematurely throws away useful variants. Among candidates that pass every hard constraint, keeping the non-dominated Pareto set preserves every policy where no admissible rival equals or beats it on all metrics with a strict win on at least one:

<figure>
<picture>
<source media="(max-width: 640px)" srcset="{{ '/assets/agent-rsi/pareto-en-mobile.svg' | relative_url }}">
<img src="{{ '/assets/agent-rsi/pareto-en.svg' | relative_url }}" alt="Illustrative policies P0 and P2 trade completion against tool calls. P1 completes most tasks but fails the authorization requirement." loading="lazy">
</picture>
<figcaption><strong>Figure 2.</strong> The same hypothetical policies as the table. P0 and P2 remain useful under different resource budgets. P1 has the highest completion rate but fails the authorization requirement. The line connects the two illustrative choices.</figcaption>
</figure>

P0 fits tight latency caps; P2 pays slightly more tool budget for higher resolution, and holding both in an archive delays choosing weights until deployment while giving future mutations diverse stepping stones. When deployment utility is genuinely fixed and stable, single-objective optimization skips unnecessary archive overhead; when trade-offs interact and shift across workloads, maintaining the frontier pulls its weight.

<h2 id="methods-en">What do existing multi-objective methods contribute?</h2>

Recent multi-objective agent work threads these trade-offs directly into workflow search, skill curation, and weight updates:

<div class="bm-table bm-table-wide" role="region" aria-label="Problems addressed by multi-objective methods" tabindex="0" markdown="1">

| Work | The decision it broadens | What it searches or trains |
|:--|:--|:--|
| [EvoFlow][r18] | Which workflows offer useful quality–cost trade-offs? | Workflow populations, prompts and model choices. |
| [AgentBreeder][r19] | Can capability and measured safety both influence scaffold selection? | Multi-agent scaffolds; its Blue setting targets both. |
| [SkillMOO][r20] | Which skills improve pass rate without ignoring execution cost? | Skill bundles for a fixed solver, using NSGA-II. |
| [MOCHA][r21] | Can a skill be correct while meeting platform requirements? | Skill text and metadata, using Chebyshev scalarization and hypervolume-based exploration. |
| [ParetoPO][r22] | Can policy learning account for accuracy and tool-use efficiency together? | Model weights through multi-objective reinforcement learning. |
| [MoFlow][r33] | How can one search serve different preferences across accuracy, cost, latency, robustness and consistency? | Stepwise workflows, with sets of reachable trade-offs stored in tree-search nodes. |
| [MOAE][r23] | Which execution policies offer useful task, trajectory and safety trade-offs for this query? | Compact policies evaluated through complete rollouts, with a Pareto archive. |

</div>

*MoFlow* is a neat twist because it embeds sets of reachable trade-offs inside each search-tree node and uses convex-hull selection to let users pivot across linear preference weights afterward.[33](#ref-33-en) Across these methods, the scope varies just as much as the algorithm: satisfying static platform rules differs from guarding runtime permissions, optimizing reusable skills amortizes search differently than optimizing per-query execution, and *GEPA* uses Pareto survival across *problem instances* to keep complementary puzzle-solvers alive rather than explicitly mapping a cost-safety frontier.[9](#ref-9-en)

Our own work on **MOAE** focuses on per-query policy evolution with the base model, tools, and outer architecture held fixed: diagnostic feedback guides compact edits to planning, tool verification, and stopping rules, scored over full rollouts and filtered into an empirical Pareto archive before picking a candidate to emit.[23](#ref-23-en)

The recurring design idea across this table is decoupling **what search keeps alive** from **what one production caller receives**. And beyond deployable policies sits a third asset: keeping informative failures and paired contrast traces as training/diagnostic fuel (as *HELIX* emphasizes), cleanly separated from the set of deployable finalists.[30](#ref-30-en)

<h2 id="evidence-en">Multi-objective search leaves several shared problems open</h2>

Putting multiple metrics on a Pareto chart solves selection blindness, yet five harder headaches carry straight over across every self-evolving loop:

### A vector of proxies can still miss the real requirement

Multi-objective optimizers are only as honest as the signals fed into them. An LLM judge can still reward eloquent excuses over verified facts, and a tool-call penalty can still encourage skipping sanity checks. Combining weak proxy metrics does not automatically manufacture grounded truth.

Co-evolving evaluators alongside agents, as *RQGM* explores, keeps rubrics from saturating.[15](#ref-15-en) The price is losing a fixed yardstick over time, so practical systems still need frozen external checks anchored outside the co-evolution loop to distinguish genuine gains from metric drift.

### A useful skill may become harmful in a different combination

Shared memory adds temporal coupling. *When Self-Evolution Backfires* traces a nasty failure mode where one buggy skill poisons subsequent distilled skills, so deleting the original bad entry leaves its corrupted descendants running wild; its *VaG* gate audits candidates jointly before admission.[31](#ref-31-en) *Coalition-Aware Skill Reliability* similarly tracks how skill utility shifts across skill pairings and domains via coalition-aware gating and transfer masking.[32](#ref-32-en)

Once edits persist, evaluating an update in isolation is incomplete: you also have to test how it composes with existing skills and whether it corrupts the *next* generation of updates.

### A noisy frontier can preserve lucky candidates

With stochastic rollouts, one lucky draw on a difficult task looks indistinguishable from genuine skill. Add four or five evaluation axes and almost any outlier avoids domination by scoring high on one noisy corner, causing empirical Pareto frontiers to balloon far faster than statistical confidence in any single point.

Search budgets therefore need to balance mutation against replication: when to generate a fresh edit, when to re-roll a promising frontier point to tighten error bars, and when to probe suspected failure slices. Storing variance estimates and negative traces directly inside the archive makes it harder to mistake "non-dominated on one rollout" for a durable capability gain.

### Progress on selected tasks does not establish transfer or recursion

Headline numbers across self-evolution papers often establish narrower claims than quick summaries suggest:

<div class="bm-table bm-table-wide" role="region" aria-label="Selected quantitative evidence and its scope" tabindex="0" markdown="1">

| Source | Reported observation | What it establishes, and what remains open |
|:--|:--|:--|
| [DGM][r8] | Coding success rose from **20% to 50%** on its **200-task** SWE-bench Verified evaluation after 80 iterations. | Evidence for better coding-agent implementations under that protocol; not a 50% result on the entire Verified set. |
| [AIDE²][r16] | **7 accepted improvements in 8 days**; external evaluation covered **4 benchmarks**. | Improved research agents. Their superiority as outer-loop improvers remained inconclusive because of noise and limited replication. |
| [Open-ended research case studies][r27] | **2 research problems**, roughly **6 days** and thousands of dollars of agent work. | The researchers reported no substantial research progress in those cases, despite engineering activity. This probes a different task from optimizing a supplied measurable objective. |

</div>

Scoring higher on unseen test tasks supports generalization past the training slice. Proving an *evolved improver* is genuinely stronger demands a cleaner experiment: freeze the baseline and evolved improvers, start both from identical base agents under matched search budgets on unseen task families, and compare the delta they produce. Any hidden dev set reused across 80 rounds of hill-climbing belongs to the search budget, even if the inner task prompt never sees it directly.

And for anything persisted to disk (skills, memory notes, code patches), durability across underlying upgrades ties straight back to the [agent deployment gap]({{ '/the-anchor-of-logic-and-the-sands-of-probability/' | relative_url }}): inherited artifacts often overfit old model quirks or carry latent defects across runs, a risk surveyed in recent safety reviews.[28](#ref-28-en)

### Search itself consumes the resources being optimized

A sleek runtime policy can hide an enormous discovery bill. Paying `$100` in search calls to shave `$0.10` per task requires 1,000 production calls just to break even before factoring maintenance; per-query evolution faces the tighter hurdle of paying off its search cost *within that single query*. Keeping search spend, evaluation spend, and steady-state deployment cost on separate ledger lines stops vague "efficiency" claims from muddying the economics.

<h2 id="research-en">What would demonstrate a better improvement process?</h2>

Come back once more to our retrying coding agent. If "selective retries" actually works because it distinguishes transient server hiccups from missing permissions, design an ablation suite that toggles those two failure causes independently while holding the core problem fixed. If the gain evaporates when error semantics flip, the evolved rule never learned the real boundary.

This is where [benchmark case design]({{ '/what-do-benchmarks-measure/' | relative_url }}) stops being passive measurement and turns into part of optimization itself. A suite skewed toward transient timeouts teaches one lesson; paired counterfactual cases separating recoverable errors from prohibited edits force the update loop to learn the right distinction.

To test whether joint multi-objective evolution truly beats simpler heuristics, benchmark it head-to-head against four grounded baselines under identical mutation APIs and equal evaluation budgets: greedy completion plus a deployment gate, a fixed scalarized utility, constrained search, and sequential one-metric-at-a-time tuning. Judge the winners on *independent* tasks using pre-committed deployment preferences rather than the internal proxy optimized during search.

Three empirical signals decide whether the extra machinery pays off:
1. Does joint optimization discover admissible candidates that sequential or post-hoc filtering misses?
2. Do items along the archived frontier serve genuinely distinct production regimes rather than clustering around sampling noise?
3. Do trace-informed diagnostics uncover genuine Pareto improvements rather than merely shuffling points along the same old trade-off curve?

(Raw archive size proves nothing, and hypervolume comparisons only hold water with fixed bounds, a fixed reference point, and downstream deployment validation.)

That same checklist makes reading new self-evolution papers surprisingly sharp: trace what bottleneck actually mutates, what persists across runs, which metrics filter survivors, and what blind spots stay hidden from those metrics. Multi-objective framing is not extra decoration; it is simply what happens when a single edit alters capability, cost, and safety together, and we refuse to stay blind to two-thirds of the consequences.

<h2 id="paper-map-en">Paper-by-paper guide</h2>

The tables below retain the component-level comparison for reference. The survey offers a broader taxonomy.[26](#ref-26-en)

<details markdown="1">
<summary>Prompts, memory and skills</summary>

<div class="bm-table bm-table-wide" role="region" aria-label="Prompt, memory and skill methods" tabindex="0" markdown="1">

| Method | What changes and persists? | Feedback and optimization target |
|:--|:--|:--|
| [Pre-commit gating / VaG][r31] · 2026 | Skill admission and the retained pool | Validity, harmlessness, consistency and joint skill contribution. |
| [Coalition-aware reliability][r32] · 2026 | Which skills are accepted or masked | Contribution with different skill partners and after domain transfer. |
| [Reflexion][r1] · 2023 | Verbal reflections retained across trials | Task feedback becomes lessons intended to improve later success. |
| [Voyager][r2] · 2023 | Executable skills and a growing skill library | Environment feedback, execution errors and verification support exploration and skill acquisition. |
| [Promptbreeder][r3] · 2023 | Task prompts **and mutation prompts** | Task accuracy selects prompts; mutation prompts influence how future candidates are produced. |
| [GEPA][r9] · 2025 | Prompts inside language-model programs | Execution traces guide edits; selection preserves complementary strengths across problem instances. |
| [ACE][r10] · 2025 | Structured context playbooks | Generation, reflection and curation turn execution feedback into reusable guidance for future tasks. |

</div>

</details>

<details markdown="1">
<summary>Workflows and agent code</summary>

<div class="bm-table bm-table-wide" role="region" aria-label="Workflow and agent code methods" tabindex="0" markdown="1">

| Method | What changes and persists? | Feedback and optimization target |
|:--|:--|:--|
| [ADAS][r5] · 2024 | Agent implementations generated by a fixed meta-agent; an archive of designs | Validation performance guides further designs. |
| [Meta-Harness][r29] · 2026 | Executable harness code; raw history stays queryable | Task performance and resource use, informed by code and trajectory diagnosis. |
| [AFlow][r6] · 2024 | Code-based workflows, including operators and connections | Execution feedback and tree search optimize task performance. |
| [SICA][r7] · 2025 | Agent source, tools and surrounding logic; a selected agent becomes the next modifier | A utility combines task performance, monetary cost and elapsed time. |
| [DGM][r8] · 2025 | Coding-agent tools and workflows, retained in a branching archive | Coding success selects promising agents while the archive permits further exploration. |

</div>

</details>

<details markdown="1">
<summary>Recursive improvement</summary>

<div class="bm-table bm-table-wide" role="region" aria-label="Recursive and meta-level improvement methods" tabindex="0" markdown="1">

| Method | Editable part of the improvement loop | What selects a change? |
|:--|:--|:--|
| [STOP][r4] · 2023 | A code-improvement program applied to its own code | Utility of the programs produced by the improver. |
| [HyperAgents][r14] · 2026 | Both the task agent and its meta-agent | Downstream performance; improvement behavior is evaluated separately. |
| [AIDE²][r16] · 2026 | The research harness: search, context, verification and inner-loop selection | Aggregate private task grades under a fixed per-task dollar budget. |
| [Dream-RSI][r17] · 2026 | Exploration-policy code: branching, parallelism and stopping | Replay-estimated quality–cost frontier coverage, with a parallelism penalty. |
| [RQGM][r15] · 2026 | Agents and evaluators, updated across evaluation epochs | Utility under the current epoch's evaluator. |

</div>

</details>

<details markdown="1">
<summary>Weight updates and curricula</summary>

<div class="bm-table bm-table-wide" role="region" aria-label="Weight adaptation and curriculum methods" tabindex="0" markdown="1">

| Method | What changes? | Feedback and optimization target |
|:--|:--|:--|
| [HELIX][r30] · 2026 | Harness variants and verified sibling trajectories for subsequent model updates | Current execution quality and useful learning records; studied over one harness-evolution round. |
| [SEAL][r11] · 2025 | Generated self-edits specify adaptation data or directives; an inner update changes weights | Outer-loop reinforcement learning rewards performance **after adaptation**. |
| [Agent0][r12] · 2025 | Curriculum and executor policies through alternating training | Curriculum rewards use uncertainty and tool interaction; executor training uses correctness proxies derived from generated answers. |
| [AgentEvolver][r13] · 2025 | Generated tasks, reused experience, step-level credit and trained policy weights | Environment return and more efficient learning from interaction. |

</div>

</details>

Two adjacent cases make the target boundary clear: [AlphaEvolve][r25] evolves target algorithm code; [EvoDrive][r24] evolves scenario-generator programs, with the driving policy fixed during that search. In each case, distinguish an agent doing the optimization from the artifact being optimized.

<h2 id="references-en">References</h2>

<p class="bm-note">Years identify the initial manuscript or article; links lead to primary sources.</p>

<ol class="bm-references">
<li id="ref-1-en"><a href="https://arxiv.org/abs/2303.11366">Reflexion: Language Agents with Verbal Reinforcement Learning</a>. 2023.</li>
<li id="ref-2-en"><a href="https://arxiv.org/abs/2305.16291">Voyager: An Open-Ended Embodied Agent with Large Language Models</a>. 2023.</li>
<li id="ref-3-en"><a href="https://arxiv.org/abs/2309.16797">Promptbreeder: Self-Referential Self-Improvement Via Prompt Evolution</a>. 2023.</li>
<li id="ref-4-en"><a href="https://arxiv.org/abs/2310.02304">STOP: Self-Taught Optimizer: Recursively Self-Improving Code Generation</a>. 2023.</li>
<li id="ref-5-en"><a href="https://arxiv.org/abs/2408.08435">Automated Design of Agentic Systems (ADAS)</a>. 2024.</li>
<li id="ref-6-en"><a href="https://arxiv.org/abs/2410.10762">AFlow: Automating Agentic Workflow Generation</a>. 2024.</li>
<li id="ref-7-en"><a href="https://arxiv.org/abs/2504.15228">A Self-Improving Coding Agent (SICA)</a>. 2025.</li>
<li id="ref-8-en"><a href="https://arxiv.org/abs/2505.22954">Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents</a>. 2025.</li>
<li id="ref-9-en"><a href="https://arxiv.org/abs/2507.19457">GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning</a>. 2025.</li>
<li id="ref-10-en"><a href="https://arxiv.org/abs/2510.04618">Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models</a>. 2025.</li>
<li id="ref-11-en"><a href="https://arxiv.org/abs/2506.10943">Self-Adapting Language Models</a>. 2025.</li>
<li id="ref-12-en"><a href="https://arxiv.org/abs/2511.16043">Agent0: Unleashing Self-Evolving Agents from Zero Data via Tool-Integrated Reasoning</a>. 2025.</li>
<li id="ref-13-en"><a href="https://arxiv.org/abs/2511.10395">AgentEvolver: Towards Efficient Self-Evolving Agent System</a>. 2025.</li>
<li id="ref-14-en"><a href="https://arxiv.org/abs/2603.19461">HyperAgents</a>. 2026.</li>
<li id="ref-15-en"><a href="https://arxiv.org/abs/2606.26294">The Red Queen Gödel Machine: Co-Evolving Agents and Their Evaluators</a>. 2026.</li>
<li id="ref-16-en"><a href="https://arxiv.org/abs/2609.26457">Recursive self-improvement of AI research agents (AIDE²)</a>. 2026.</li>
<li id="ref-17-en"><a href="https://arxiv.org/abs/2609.14858">Dream-RSI: Recursive Self-Improvement through Evolving Worlds</a>. 2026.</li>
<li id="ref-18-en"><a href="https://arxiv.org/abs/2502.07373">EvoFlow: Evolving Diverse Agentic Workflows On The Fly</a>. 2025.</li>
<li id="ref-19-en"><a href="https://arxiv.org/abs/2502.00757">AgentBreeder: Mitigating the AI Safety Risks of Multi-Agent Scaffolds via Self-Improvement</a>. 2025.</li>
<li id="ref-20-en"><a href="https://arxiv.org/abs/2604.09297">SkillMOO: Multi-objective Optimization of Agent Skills for Software Engineering</a>. 2026.</li>
<li id="ref-21-en"><a href="https://arxiv.org/abs/2605.19330">MOCHA: Multi-Objective Chebyshev Annealing for Agent Skill Optimization</a>. 2026.</li>
<li id="ref-22-en"><a href="https://arxiv.org/abs/2606.16111">ParetoPO: Towards Pareto-Optimal Tool-Integrated Agents with Pareto Ranking Policy Optimization</a>. 2026.</li>
<li id="ref-23-en"><a href="https://arxiv.org/abs/2609.05992">MOAE: Multi-Objective Agent Evolution with Pareto-Preserving Search</a>. 2026.</li>
<li id="ref-24-en"><a href="https://arxiv.org/abs/2606.03678">EvoDrive: Pareto Evolution for Safety-Critical Autonomous Driving via Self-Improving LLM Agents</a>. 2026.</li>
<li id="ref-25-en"><a href="https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/">AlphaEvolve</a>. 2025.</li>
<li id="ref-26-en"><a href="https://arxiv.org/abs/2507.21046">A Survey of Self-Evolving Agents: What, When, How, and Where to Evolve on the Path to Artificial Super Intelligence</a>. 2025.</li>
<li id="ref-27-en"><a href="https://arxiv.org/abs/2607.27191">Can AI agents conduct open-ended AI research? Early evidence from two case studies</a>. 2026.</li>
<li id="ref-28-en"><a href="https://arxiv.org/abs/2610.00093">Safety in Self-Evolving Agents: A Survey</a>. 2026.</li>
<li id="ref-29-en"><a href="https://arxiv.org/abs/2603.28052">Meta-Harness: End-to-End Optimization of Model Harnesses</a>. 2026.</li>
<li id="ref-30-en"><a href="https://arxiv.org/abs/2608.13951">HELIX: Model-Harness Co-evolution for Recursive Self-Improvement</a>. 2026.</li>
<li id="ref-31-en"><a href="https://arxiv.org/abs/2608.05810">When Self-Evolution Backfires: Pre-Commit Gating against Skill Contamination in LLM Agents</a>. 2026.</li>
<li id="ref-32-en"><a href="https://arxiv.org/abs/2608.22610">Coalition-Aware Skill Reliability for Self-Evolving Agents</a>. 2026.</li>
<li id="ref-33-en"><a href="https://arxiv.org/abs/2609.38294">MoFlow: Multi-Objective Agentic Workflow Generation</a>. 2026.</li>

</ol>

</div>

<div id="bm-content-zh" class="bm-language-content" lang="zh-CN" hidden markdown="1">

# Agent 自进化，到底在进化什么？

<p class="bm-meta">2026 年 10 月 14 日 · 自进化 Agent · 约 18 分钟<span id="busuanzi_container_page_pv" class="bm-meta__views" style="display:none;"> · <strong class="bm-meta__views-num" id="busuanzi_value_page_pv">--</strong> 次阅读</span></p>

<p class="bm-deck">自我改进方法到底修好了什么，收益又在哪里撞墙，以及多目标优化是怎么自然变成刚需的。</p>

设想一个编程 Agent 在进化过程中摸索出一条很直观的经验：“只要测试挂了，就再试一次。”看榜单上的任务完成率，确实一路往上走。但点开执行轨迹就会发现另一面：单次耗时拉长了一倍多，工具调用翻倍，偶尔为了把报错压下去，它甚至会改动授权范围之外的文件。

从某个角度看，它确实学会了一件好事——遇到硬骨头不轻易放弃；但同时它也把一条适用面过宽的启发式塞进了策略里。面对这种更新，是咬牙上线、直接退回，还是接着找一个更懂分寸的“选择性重试”版本？

这正是研究 self-evolving agents 和递归自我改进（RSI）时最容易被忽略的关口：今天我们已经很擅长让系统自动提出改法，难的从来是**判断哪一次修改才算得上真正的进步**。

<div class="bm-thesis" markdown="1">

只要一次改动会同时牵动几件彼此制衡的事，光靠某一项指标变好就看不清全貌，多目标优化自然就会走进决策中心。第一步先把这些相互牵连的后果摆到同一张桌面上，接下来才谈得上哪些维度可以交换、哪些红线绝不让步、又有哪些不同取舍的方案值得留作备选。

</div>

<nav class="bm-toc" aria-label="文章目录" markdown="1">

1. [现有方法真正修复了什么？](#components-zh)
2. [什么时候，更高的分数不再足以回答问题？](#objects-zh)
3. [为什么不能一个目标一个目标地修？](#coupling-zh)
4. [从多个指标，走到共同决策](#objectives-zh)
5. [多目标方法具体增加了什么？](#methods-zh)
6. [哪些共同问题仍然没有解决？](#evidence-zh)
7. [怎样证明改进过程真的更好了？](#research-zh)
8. [逐篇论文对照](#paper-map-zh)

</nav>

<h2 id="components-zh">自进化方法真正修复了什么？</h2>

把这批文献放在一起看，最清晰的脉络其实是“堵点转移”：有时候 Agent 是跑完一轮就把教训忘光，有时候是被笨拙的工具和流程卡死，有时候是模型底层压根缺那块能力，还有些工作是在替“怎么找改法”本身提效。不同路线修补的其实是不同层的瓶颈。

### 经验在执行结束后消失

如果上一轮踩过的坑留不到下一轮，系统就得一次次交同样的学费。*Reflexion* 把文字反思写进跨轮次记忆，*Voyager* 把跑通的代码沉淀成可调用的技能库，*ACE* 则把不断演化的上下文整理成一套经验手册。[1](#ref-1-zh) [2](#ref-2-zh) [10](#ref-10-zh)

这几类方法瞄准的是同一件事：**别让执行过的经验白白流掉。** 可惜记下一条规则，不等于标清它的适用边界。“失败后重试”遇到临时网络抖动很有用，碰上权限被拒时却纯属乱撞。光会存经验还不够，记忆系统还得分辨清哪些是通用规律，哪些只在特定条件下成立。

### 更好的指令也改变不了行动结构

如果编辑器本身一次只能整文件重写，提示词里喊再多遍“务必小心修改”也于事无补。改动工作流和工具代码打开了另一扇门：*ADAS* 与 *AFlow* 自动搜索 Agent 拓扑与代码工作流，*DGM* 则干脆放开手去改工具定义和执行控制逻辑，换上更精准的文件编辑原语。[5](#ref-5-zh) [6](#ref-6-zh) [8](#ref-8-zh)

这类工作松动的是**可用动作空间与组织方式**。很多时候基座模型本来就懂怎么解题，纯粹是被顺手度极差的外围管线绊住了脚，所以不动权重也能刷出大涨幅。但换个角度看，围绕某类工作流磨出来的强结构换个场景照样可能水土不服，依然得查明它到底修掉了哪类问题、又踩中了哪类新约束。

### 模型本身缺少某种能力

光换外围脚手架有时确实不够。*SEAL* 让模型自己生成微调数据或适应指令，再按**权重更新之后**的表现回传奖励；*Agent0* 与 *AgentEvolver* 则通过自动命题和环境交互来生产训练信号。[11](#ref-11-zh) [12](#ref-12-zh) [13](#ref-13-zh)

它们补的是**学习信号的供给与利用效率**。一旦动了模型权重，瓶颈马上变成样本质量：要是课程一直在翻炒熟悉题型，或者奖励代理不小心放过了投机答案，多训几轮只会把毛病焊得更牢。评判任务生成器好不好，最终要看它究竟教会策略分清了哪些关键区别。

外围架构和权重更新也能互相喂养。*HELIX* 提出了“构建—更新—重建”闭环：先演化外围框架，再挑出经验证的对比轨迹拿去训练模型，随后再回头调整框架适配新权重（不过原论文的完整闭环验证只做到了一轮框架演化及其训练轨迹产出）。[30](#ref-30-zh)

### 寻找改进的过程本身效率不高

RSI 把镜头又往后拉了一格，不再只改任务 Agent，而是顺手去改那个“负责提改进的人”。*Promptbreeder* 连用来改写提示词的“变异提示”也一起进化；*STOP* 让代码优化器反过来重写自身代码；*HyperAgents* 打开了 meta-agent 的修改权限；*AIDE²* 专门打磨科研 Agent 的框架；*Dream-RSI* 则借回放历史经验去搜寻更聪明的探索策略。[3](#ref-3-zh) [4](#ref-4-zh) [14](#ref-14-zh) [16](#ref-16-zh) [17](#ref-17-zh)

走到这一层，目标已经成了**在同等预算下更快找对下一个好改法**。最终产出一个更好的任务 Agent 算一重收获；证明改进器自身越改越会找方法则是另一重强得多、也必须单设对照的主张。同时递归有个天然风险：它也会一并放大评估器的盲区——搜索器越聪明，就越擅长朝你不完整的评分标准里钻空子。

<figure>
<picture>
<source media="(max-width: 640px)" srcset="{{ '/assets/agent-rsi/evolution-loop-zh-mobile.svg' | relative_url }}">
<img src="{{ '/assets/agent-rsi/evolution-loop-zh.svg' | relative_url }}" alt="改进器修改 Agent 的不同组件；执行产生证据，筛选保留改动，下一次运行继承它们。递归路径进一步修改改进器本身。" loading="lazy">
</picture>
<figcaption><strong>图 1.</strong> 一个进化系统包含可修改的对象，以及决定改动能否留下的循环。实线路径更新 Agent，虚线路径进一步更新改进器。</figcaption>
</figure>

把这四条路线合到一起看，核心无非两道关：准许修改系统的哪一部分，以及凭什么证据批准修改留下。大多数论文在前一关上花样翻新，真到了后一关就绕不开多目标评估。

<h2 id="objects-zh">完成率提高了，选择仍然可能没有答案</h2>

回到开头的编程 Agent。在 100 道测试题上同时运行“完成度判定器”与“权限范围审计”，看看下面三套策略的对比结果：

<div class="bm-table bm-table-wide bm-case" role="region" aria-label="Agent 更新的假设比较" tabindex="0" markdown="1">

| 策略 | 完成任务 | 平均工具调用 | 第 95 百分位耗时 | 出现越权操作的运行 |
|:--|:--|:--|:--|:--|
| P0 · 原始策略 | 80 / 100 | 6 次 | 40 秒 | 0 / 100 |
| P1 · 广泛重试 | 89 / 100 | 14 次 | 110 秒 | 4 / 100 |
| P2 · 选择性重试，并检查操作范围 | 88 / 100 | 8 次 | 55 秒 | 0 / 100 |

</div>

<p class="bm-note">数字为假设示例。完成度与授权情况独立统计，因此完成任务的运行也可能包含越权操作。</p>

只盯着通过率看，优化器会毫不犹豫选中 P1；如果卡死 45 秒的尾延迟上限，只有 P0 勉强过线；一旦线上一票否决越权修改文件，完成率最高的 P1 同样直接出局——反倒是 P2 成了最站得住的选择，几乎吃下了全部通过率涨幅，同时守住了延迟和权限边界。

一旦 Agent 要花真金白银调工具、又要在权限红线内干活，“做没做成”和“怎么做成”就彻底分家了。**能走到终点，与规规矩矩地走到终点，本来就是两项不同的能力指标。**

顺便也要把**优化目标**与**诊断信号**拆开算。比如反复调用错参数固然能解释耗时为什么涨了，但它本质上是延迟上升的原因记录；如果把每次参数出错和端到端耗时同时放进加权目标里，等于对同一个毛病罚了两遍分。目标应该严格从真实上线约束里定，轨迹诊断指标留着帮你排查“候选为什么成、为什么败”。

<h2 id="coupling-zh">为什么不能一个目标一个目标地修？</h2>

工程上最容易想到的省事路径是“先把完成率刷上去，回头再慢慢砍成本、补安全护栏”。问题在于，这几个维度偏偏拧在同一套控制开关上：多给两次重试机会，完成率、API 费用和尾延迟会一起往上蹿；加上一步自检可能捞回几个 bug，但每次调用都要多等好几秒；收紧提前终止规则能压住乱逛的风险，有时却恰好把还在认真排错的正常任务给掐断了。

不妨想象从 P1 接着往下做逐项修补：第一轮工程师打了个省钱补丁，强行把工具上限卡在 10 次——它可能刚好砍掉了瞎转圈，也完全可能恰好切掉了最后那两次救命的重试；下一轮负责提能力的开发者看到难题又失败了，转头又把重试上限放回去。每一轮局部分数都好像挺合理，整套系统却只在原地打转。

真正顶用的修改往往长成一组条件分支：临时接口报错就退避重试，参数格式写错就当场修正，撞上权限拒绝立刻收手，只有高风险编辑才补跑全量测试。在“完成/失败”那一栏里，四种问题看上去全都一模一样；只有在多维指标和执行轨迹同时摊开后，修改器才知道该往哪根神经下刀。

*Meta-Harness* 就把这种“看病下药”直接塞进了提出改法的环节里，让 proposer 直接查阅过往代码版本、各维分数以及完整执行轨迹，而不只是对着一个光秃秃的平均分瞎猜。[29](#ref-29-zh)

那干脆搜索时全力冲完成率、部署前再套一层安全拦截门行不行？拦截门当然能把 P1 挡在生产门外，但它变不出一个搜索早期就被淘汰掉的 P2。哪怕团队把所有历史轨迹全记进了日志，下一轮把有限的变异算力分给哪几个父代，照样决定着搜不搜得到好方案。**筛选决定的不只是最后留下谁，还决定了下一轮搜索还能从哪些候选出发。**

共同优化说白了就是把线上的真约束提前请进搜索环里，让它直接参与“提什么改法、留哪个版本、往哪支继续搜”。多目标效用、硬性门槛与 Pareto 档案，本质上只是让这些约束尽早插手的三种工具。

当然还有一种最划算的情况：有些所谓的“两难取舍”，纯粹只是因为当前实现太糙。把一个动不动格式出错的补丁工具换成稳妥的 diff 接口，往往能同时拉高通过率、顺便砍掉一半无谓重试。多维诊断恰好能帮你把这类实打实的联合改进从真正的硬取舍里挑出来。

<h2 id="objectives-zh">从多个指标，走到共同决策</h2>

### 先确定什么不能交换

如果误改受保护配置文件属于绝不容忍的红线，那多做出几道题也填不平一次越权事故。这类底线必须放进可行域筛选条件里，能靠运行沙箱硬隔离的尽量用硬隔离兜底——一旦在评测里踩了红线直接一票淘汰（同时清醒记住，有限测试零违规只意味着经验风险受控，不代表形式化安全证明）。

把硬门槛单拎出来，能立刻厘清两个老被搅浑的问题：“这个策略合不合规、能不能上线？”和“在都合规的候选中，我们更偏爱哪一组性价比？”

### 偏好明确时，就把它写清楚

如果项目对质量、费用和延迟之间的交换比例已经非常明确且长期稳定，把它们揉成一个加权效用函数简单又直接。*SICA* 就是这样把任务成功度、花销和运行耗时合到一个总效用分里的。[7](#ref-7-zh)

拿前面那张小表试算一下就知道单靠权重有多敏感。暂时不看权限红线、只换算完成率和调用次数：每次平均调用扣 `0.1` 个百分点时，P1 是 `87.6`、P2 是 `87.2`，P1 险胜；只要把罚分调到每次 `0.5` 个百分点，分数瞬间倒挂成 `82` 比 `84`。两遍算术都没错，仅仅是尺子和偏好稍微挪了一格；而一旦加上那条不可越权的硬约束，不管权重怎么调，P1 都只能直接退场。

### 一次选择太早时，就保留不同方案

要是同一个 Agent 框架既要伺候对延迟极敏感的实时对话用户，又要跑追求高成功率的夜间批处理作业，过早拍板唯一权重反而会浪费掉大批可用候选。在所有跨过安全与权限门槛的合规策略中，维持一套非支配 Pareto 档案——只留下那些“没有另一个合规对手在所有关注指标上都不输它、且至少有一项严格压过它”的候选：

<figure>
<picture>
<source media="(max-width: 640px)" srcset="{{ '/assets/agent-rsi/pareto-zh-mobile.svg' | relative_url }}">
<img src="{{ '/assets/agent-rsi/pareto-zh.svg' | relative_url }}" alt="假设策略 P0 与 P2 在完成率和工具调用之间各有取舍。P1 完成率最高，但不符合授权要求。" loading="lazy">
</picture>
<figcaption><strong>图 2.</strong> 与表格对应的假设策略。P0 和 P2 适合不同资源预算，P1 虽然完成率最高，却不符合授权要求。连线用于连接这两个示例方案。</figcaption>
</figure>

这样 P0 和 P2 就各有归宿：P0 扛住低成本预算档，P2 多花一点工具调用换更高完成率，还顺带给下一代变异留出了两条不同的起跑线。反之，如果线上场景和成本换算早就钉死了几年不变，单目标直冲最优通常更省事；档案真正值钱的地方，在于取舍彼此耦合又会随场景摆动的时候。

<h2 id="methods-zh">现有多目标方法具体增加了什么？</h2>

眼下这批多目标自进化工作，大致顺着三个切入口把多种约束带进了搜索和训练环节：工作流拓扑搜索、技能包筛选与底层策略学习。

<div class="bm-table bm-table-wide" role="region" aria-label="多目标方法所解决的选择问题" tabindex="0" markdown="1">

| 工作 | 它扩展了什么选择问题？ | 搜索或训练什么？ |
|:--|:--|:--|
| [EvoFlow][r18] | 哪些工作流提供了有用的质量与成本取舍？ | 工作流种群、提示词和模型选择。 |
| [AgentBreeder][r19] | 能力与测得的安全性，能否共同影响系统结构的筛选？ | 多 Agent 系统结构；Blue 设置同时考虑两者。 |
| [SkillMOO][r20] | 哪些技能能提高通过率，同时不忽略执行成本？ | 固定执行模型使用的技能组合，采用 NSGA-II。 |
| [MOCHA][r21] | 技能能否同时给出正确结果，并符合平台要求？ | 技能文本与元数据，结合 Chebyshev 标量化和超体积探索。 |
| [ParetoPO][r22] | 策略学习能否同时考虑准确率与工具使用效率？ | 通过多目标强化学习更新模型权重。 |
| [MoFlow][r33] | 一次搜索如何服务准确率、成本、延迟、鲁棒性与一致性之间的不同偏好？ | 逐步构建工作流，在搜索树节点中保留可达的取舍集合。 |
| [MOAE][r23] | 对当前查询，哪些执行策略提供了有用的任务、轨迹与安全取舍？ | 用完整执行评估紧凑策略，并维护 Pareto 档案。 |

</div>

*MoFlow* 挺有意思的一点，是把多种可达取舍直接存进搜索树节点里，之后再用凸包选择按用户不同的线性偏好实时挑出对应工作流。[33](#ref-33-zh) 而放眼整张表，各家瞄准的问题性质其实很不一样：满足平台形式规范不同于防住运行期越权，能反复摊销搜索成本的通用技能也不同于单次查询实时适应；像 *GEPA* 同样用了 Pareto 筛选，但它保的是跨不同题目的互补优势，并非刻意画一条“质量—成本—安全”前沿。[9](#ref-9-zh)

我们自己的工作 **MOAE** 走的是单查询适应路线：保持底层模型、工具集和大框架不动，专门在执行前用分目标诊断去改动规划、工具核验和停止策略，用完整 rollout 实测后收进 Pareto 档案，把最终选哪一档推迟到输出门槛之前。[23](#ref-23-zh)

穿透这些不同实现，真正通用的设计思想是把**搜索过程中该保住的多样性**和**单次交付时必须选出的最终答案**拆开看。至于那些跑砸了但很说明问题的失败路径或成功对比，也该作为诊断语料单独存下（就像 *HELIX* 所强调的那样），既不污染可部署候选池，也不浪费反面经验。[30](#ref-30-zh)

<h2 id="evidence-zh">多目标搜索之后，哪些共同问题仍然存在？</h2>

把指标画成多目标前沿只能解决“别看漏其他维度”，下面这五个老问题几乎在所有自进化环里照样存在：

### 多个代理指标，仍然可能遗漏真实要求

加一个评价维度，前提是那道新信号真的咬住了业务关心的问题。裁判模型一样可能偏袒写得天花乱坠的空话而放过没依据的结论；工具效率惩罚一样可能逼着 Agent 省掉最关键的二次核验。几个有漏洞的代理指标堆在一起多目标优化，并不会负负得正变可靠。

像 *RQGM* 让评估器和 Agent 一块协同进化，能防止裁判很快过时失效。[15](#ref-15-zh) 代价是失去了固定的纵向标尺，所以实际系统里总还得在闭环外钉住几把不随演化改动的外部测试，才能分清到底是 Agent 真强了，还是裁判自己放松了尺子。

### 有用的技能，换一种组合可能反而有害

一旦改动持久写入共享记忆或技能库，时间耦合就跟着来了。*When Self-Evolution Backfires* 揭露过一条很具体的传染链：一条带缺陷的技能混进库里之后，会污染后续提炼出来的衍生技能，哪怕回头删掉罪魁祸首，它的污染后代依然留在系统里作祟；文中提出的 *VaG* 会在准入前联合检验技能与已有库的相互作用。[31](#ref-31-zh) *Coalition-Aware Skill Reliability* 则用组合感知的准入机制与迁移屏蔽，专门追踪同一个技能换了搭档或领域后贡献度怎么剧烈变化。[32](#ref-32-zh)

这意味着评估一次更新时，只测“它单干行不行”是不够的，还得验“它放进现有技能池里搭伙行不行、会不会带坏下一批学出来的规则”。

### 带噪声的前沿，可能保留的是幸运候选

在带随机性的多轮执行里，某个候选碰巧蒙对一道难题，看起来就像天降神兵。目标维度一多，几乎任何撞大运的异常样本都能凭某一维擦边亮眼而躲过支配淘汰，导致经验 Pareto 档案迅速膨胀，可信度却完全没跟上。

因此搜索预算不止要管“怎么产生新变异”，还要管资源该怎么分配：什么时候生成新改法、什么时候给前沿上有希望的候选多复跑几轮压低方差、什么时候专测高危边界。把重复方差和已知反例一并记录进档案，才不至于把“单次侥幸不被支配”误认成稳定实力。

### 在选定任务上进步，不等于迁移或递归能力已经成立

看几份有代表性的定量结果就知道，报告的涨幅和外推范围之间往往隔着一层窗口纸：

<div class="bm-table bm-table-wide" role="region" aria-label="代表性定量证据及适用范围" tabindex="0" markdown="1">

| 来源 | 报告的结果 | 说明了什么，还有什么没解决？ |
|:--|:--|:--|
| [DGM][r8] | 80 轮迭代后，在选定的 **200 道** SWE-bench Verified 任务上，成功率从 **20% 升至 50%**。 | 支持该协议下编程 Agent 实现得到了改进；不是完整 Verified 数据集上的 50%。 |
| [AIDE²][r16] | **8 天接受 7 次改进**，另在 **4 个外部 benchmark** 上评估。 | 得到了更好的研究 Agent；由于噪声和重复实验有限，其作为外层改进器的优势仍不明确。 |
| [开放式研究案例][r27] | **2 个研究问题**，约 **6 天**、数千美元的 Agent 工作。 | 原研究者认为这些案例没有取得实质研究进展，尽管完成了工程活动。这与优化一个已给定、可测量的目标是不同任务。 |

</div>

在未见过的测试题上拿到更高分，证明改动确实泛化出了最初的挑选题集；可真想宣称“改进器自己进化得更会找改法了”，必须做另一场对照：让初始改进器和进化后的改进器站在完全相同的起点 Agent 上，拿着一样的预算去攻全新的任务家族，比谁拉出的净涨幅更大。别忘了，哪怕内层提示从没直接见过那 200 道挑选用的测试题，只要外层循环拿它们反复筛了 80 轮候选，这批样本就已经实打实耗进优化成本里了。

至于那些会被持久化保存下来的产物——技能、经验笔记、工具补丁——它们能不能抗住底层模型升级换代，又会直接连回到上一篇谈的 [模型迁移与部署落差]({{ '/the-anchor-of-logic-and-the-sands-of-probability/' | relative_url }})。许多留下来的经验暗含着对旧模型习性的依赖，甚至会把隐蔽缺陷一路捎给未来的执行，近期关于自进化安全的综述也把这类持久状态污染列作了核心风险。[28](#ref-28-zh)

### 搜索本身，也在消耗我们试图优化的资源

最终上线策略跑起来再便宜，也掩盖不了搜出它花了多少钱。花 100 美元算力搜出一个可复用工作流、每次执行省下 0.10 美元，不计后续维护成本就已经得跑满 1,000 次才能打平本钱；单查询现场演化面临的算术更苛刻，必须在当下这一条请求里把搜索花销赚回来。把“搜索成本”“评测成本”和“稳态执行成本”分开记账，才不会被一句含糊的“效率提升”带偏。

<h2 id="research-zh">怎样证明改进过程真的更好了？</h2>

再回到那只爱重试的编程 Agent。假如研究者认为“选择性重试”奏效是因为区分开了临时超时与权限不足，验证办法很简单：保持任务目标大致相同，专门构造一批只切换错误成因（网络超时 vs. 权限拒绝）的对照题。条件微调一下收益就烟消云散的话，那刚才总结出的经验不过是一句过拟合规则。

这也恰恰说明为什么 [测试题如何构造]({{ '/what-do-benchmarks-measure/' | relative_url }}) 本身就是 Agent 进化不可或缺的一环。测试集长什么样，决定了一套优化循环能看到哪些后果：题库里全是重启一下就好的软报错，系统必然学会无脑重试；只有把可恢复故障与严禁越界操作成对放进同一张考卷，进化环才有机会学到真正讲究分寸的行为规则。

真想实证多目标联合优化值不值那份复杂度，最好的办法是在同一套代码编辑接口与等额总评估预算下，跟四个实在基线正面交锋：只拼完成率再后置拦截、固定标量加权、硬约束搜索，以及单目标逐轮修补。最终裁判必须依据事前锁定的真实部署偏好和独立测试集来打分，绝不能偏袒新优化器自己最顺眼的那项代理指标。

实验里看三条硬证据就够决定胜负：
1. 联合评估有没有找回那些只靠后置过滤或逐项调优早就漏掉的好策略？
2. 档案前沿保下来的几个方案，是不是确实各自服务于不同的线上预算与需求，而非随机采样的噪点？
3. 基于执行轨迹的诊断改法，是不是真的挖出了“同时变好”的联合帕累托改进，而不是只在旧的苦差事之间挪位置？

（档案留了几十个点说明不了问题，用超体积比大小也只有在锁定边界、固定参考点并挂钩真实交付效果时才算数。）

顺着这套检查表去读下一篇 RSI 论文，思路也会格外清楚：先看它到底在改系统的哪一层堵点、什么东西会遗传到下一轮、靠哪几个信号决定谁能活下来，再反问一句“还有哪些真实代价躲在这些信号的盲区外”。多目标视角从来不是为了给算法加戏，仅仅是因为当一次修改会同时改写能力、开销与安全时，我们没法假装看不见另外那三分之二的后果。

<h2 id="paper-map-zh">逐篇论文对照</h2>

下面的表格保留具体组件层面的对照，供查阅。领域综述提供了更广的分类背景。[26](#ref-26-zh)

<details markdown="1">
<summary>提示词、记忆与技能</summary>

<div class="bm-table bm-table-wide" role="region" aria-label="提示词、记忆和技能方法比较" tabindex="0" markdown="1">

| 方法 | 修改并保留什么？ | 反馈与优化目标 |
|:--|:--|:--|
| [Pre-commit gating / VaG][r31] · 2026 | 技能准入与保留的技能池 | 有效性、无害性、一致性，以及技能组合贡献。 |
| [Coalition-aware reliability][r32] · 2026 | 接受或屏蔽哪些技能 | 不同技能搭配和领域迁移后的贡献。 |
| [Reflexion][r1] · 2023 | 跨轮次保留的文字反思 | 把任务反馈转化为经验，改善后续尝试的成功率。 |
| [Voyager][r2] · 2023 | 可执行技能，以及持续扩充的技能库 | 利用环境反馈、执行错误和验证结果，促进探索与技能积累。 |
| [Promptbreeder][r3] · 2023 | 任务提示词，以及**生成变异的提示词** | 任务准确率筛选提示词；变异提示词影响下一批候选如何产生。 |
| [GEPA][r9] · 2025 | 语言模型程序中的提示词 | 执行轨迹指导修改；筛选时保留在不同题目上各有优势的候选。 |
| [ACE][r10] · 2025 | 结构化的上下文经验手册 | 通过生成、反思和整理，把执行反馈转成后续任务可用的指导。 |

</div>

</details>

<details markdown="1">
<summary>工作流与 Agent 代码</summary>

<div class="bm-table bm-table-wide" role="region" aria-label="工作流与 Agent 代码方法比较" tabindex="0" markdown="1">

| 方法 | 修改并保留什么？ | 反馈与优化目标 |
|:--|:--|:--|
| [ADAS][r5] · 2024 | 固定 meta-agent 生成的 Agent 实现，以及设计档案 | 验证任务上的表现指导后续设计。 |
| [Meta-Harness][r29] · 2026 | 可执行框架代码；历史代码与轨迹可检索 | 利用代码和轨迹诊断，改进任务表现与资源使用。 |
| [AFlow][r6] · 2024 | 代码形式的工作流，包括操作与连接关系 | 用执行反馈和树搜索提高任务表现。 |
| [SICA][r7] · 2025 | Agent 源码、工具与运行逻辑；被选中的 Agent 继续承担修改任务 | 把任务表现、费用和耗时合成效用分数。 |
| [DGM][r8] · 2025 | 编程 Agent 的工具与工作流，保存在可分支探索的档案中 | 用编程任务成功率寻找有潜力的候选，同时保留继续探索的路径。 |

</div>

</details>

<details markdown="1">
<summary>递归改进</summary>

<div class="bm-table bm-table-wide" role="region" aria-label="递归与元层次改进方法比较" tabindex="0" markdown="1">

| 方法 | 改进循环中可修改的部分 | 什么决定保留改动？ |
|:--|:--|:--|
| [STOP][r4] · 2023 | 把代码改进程序用于修改它自己的代码 | 由该改进器产生的程序能取得多高的效用。 |
| [HyperAgents][r14] · 2026 | 任务 Agent 和 meta-agent 都可修改 | 下游任务表现；另外评估其产生改进的能力。 |
| [AIDE²][r16] · 2026 | 研究 Agent 的运行框架，包括搜索、上下文、验证和内层选择 | 在固定单任务费用预算下，汇总私有任务评分。 |
| [Dream-RSI][r17] · 2026 | 决定分支、并行和停止的探索策略代码 | 回放估计的质量—成本前沿覆盖程度，并加入并行结构相关的惩罚。 |
| [RQGM][r15] · 2026 | 在不同评估阶段更新 Agent 与评估器 | 当前阶段评估器定义的效用。 |

</div>

</details>

<details markdown="1">
<summary>权重更新与课程生成</summary>

<div class="bm-table bm-table-wide" role="region" aria-label="权重适应与课程生成方法比较" tabindex="0" markdown="1">

| 方法 | 修改什么？ | 反馈与优化目标 |
|:--|:--|:--|
| [HELIX][r30] · 2026 | 框架变体，以及供后续模型更新使用的验证轨迹 | 当前执行质量与学习材料价值；实验覆盖一轮框架演化。 |
| [SEAL][r11] · 2025 | 生成 self-edits，指定适应所需的数据或指令；内层更新权重 | 外层强化学习奖励的是**适应之后**的下游表现。 |
| [Agent0][r12] · 2025 | 交替训练课程生成策略与执行策略 | 课程奖励涉及不确定性和工具交互；执行器利用生成答案构造正确性代理信号。 |
| [AgentEvolver][r13] · 2025 | 生成的任务、复用的经验、步骤级归因，以及训练后的策略权重 | 提高环境回报，更有效地利用交互进行训练。 |

</div>

</details>

还有两个相邻例子有助于确定修改对象：[AlphaEvolve][r25] 进化目标算法代码；[EvoDrive][r24] 进化场景生成程序，搜索期间驾驶策略固定。理解它们时，需要分开负责优化的 Agent，以及被优化的产物。

<h2 id="references-zh">参考文献</h2>

<p class="bm-note">年份对应初始稿件或文章，链接指向一手来源。</p>

<ol class="bm-references">
<li id="ref-1-zh"><a href="https://arxiv.org/abs/2303.11366">Reflexion: Language Agents with Verbal Reinforcement Learning</a>. 2023.</li>
<li id="ref-2-zh"><a href="https://arxiv.org/abs/2305.16291">Voyager: An Open-Ended Embodied Agent with Large Language Models</a>. 2023.</li>
<li id="ref-3-zh"><a href="https://arxiv.org/abs/2309.16797">Promptbreeder: Self-Referential Self-Improvement Via Prompt Evolution</a>. 2023.</li>
<li id="ref-4-zh"><a href="https://arxiv.org/abs/2310.02304">STOP: Self-Taught Optimizer: Recursively Self-Improving Code Generation</a>. 2023.</li>
<li id="ref-5-zh"><a href="https://arxiv.org/abs/2408.08435">Automated Design of Agentic Systems (ADAS)</a>. 2024.</li>
<li id="ref-6-zh"><a href="https://arxiv.org/abs/2410.10762">AFlow: Automating Agentic Workflow Generation</a>. 2024.</li>
<li id="ref-7-zh"><a href="https://arxiv.org/abs/2504.15228">A Self-Improving Coding Agent (SICA)</a>. 2025.</li>
<li id="ref-8-zh"><a href="https://arxiv.org/abs/2505.22954">Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents</a>. 2025.</li>
<li id="ref-9-zh"><a href="https://arxiv.org/abs/2507.19457">GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning</a>. 2025.</li>
<li id="ref-10-zh"><a href="https://arxiv.org/abs/2510.04618">Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models</a>. 2025.</li>
<li id="ref-11-zh"><a href="https://arxiv.org/abs/2506.10943">Self-Adapting Language Models</a>. 2025.</li>
<li id="ref-12-zh"><a href="https://arxiv.org/abs/2511.16043">Agent0: Unleashing Self-Evolving Agents from Zero Data via Tool-Integrated Reasoning</a>. 2025.</li>
<li id="ref-13-zh"><a href="https://arxiv.org/abs/2511.10395">AgentEvolver: Towards Efficient Self-Evolving Agent System</a>. 2025.</li>
<li id="ref-14-zh"><a href="https://arxiv.org/abs/2603.19461">HyperAgents</a>. 2026.</li>
<li id="ref-15-zh"><a href="https://arxiv.org/abs/2606.26294">The Red Queen Gödel Machine: Co-Evolving Agents and Their Evaluators</a>. 2026.</li>
<li id="ref-16-zh"><a href="https://arxiv.org/abs/2609.26457">Recursive self-improvement of AI research agents (AIDE²)</a>. 2026.</li>
<li id="ref-17-zh"><a href="https://arxiv.org/abs/2609.14858">Dream-RSI: Recursive Self-Improvement through Evolving Worlds</a>. 2026.</li>
<li id="ref-18-zh"><a href="https://arxiv.org/abs/2502.07373">EvoFlow: Evolving Diverse Agentic Workflows On The Fly</a>. 2025.</li>
<li id="ref-19-zh"><a href="https://arxiv.org/abs/2502.00757">AgentBreeder: Mitigating the AI Safety Risks of Multi-Agent Scaffolds via Self-Improvement</a>. 2025.</li>
<li id="ref-20-zh"><a href="https://arxiv.org/abs/2604.09297">SkillMOO: Multi-objective Optimization of Agent Skills for Software Engineering</a>. 2026.</li>
<li id="ref-21-zh"><a href="https://arxiv.org/abs/2605.19330">MOCHA: Multi-Objective Chebyshev Annealing for Agent Skill Optimization</a>. 2026.</li>
<li id="ref-22-zh"><a href="https://arxiv.org/abs/2606.16111">ParetoPO: Towards Pareto-Optimal Tool-Integrated Agents with Pareto Ranking Policy Optimization</a>. 2026.</li>
<li id="ref-23-zh"><a href="https://arxiv.org/abs/2609.05992">MOAE: Multi-Objective Agent Evolution with Pareto-Preserving Search</a>. 2026.</li>
<li id="ref-24-zh"><a href="https://arxiv.org/abs/2606.03678">EvoDrive: Pareto Evolution for Safety-Critical Autonomous Driving via Self-Improving LLM Agents</a>. 2026.</li>
<li id="ref-25-zh"><a href="https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/">AlphaEvolve</a>. 2025.</li>
<li id="ref-26-zh"><a href="https://arxiv.org/abs/2507.21046">A Survey of Self-Evolving Agents: What, When, How, and Where to Evolve on the Path to Artificial Super Intelligence</a>. 2025.</li>
<li id="ref-27-zh"><a href="https://arxiv.org/abs/2607.27191">Can AI agents conduct open-ended AI research? Early evidence from two case studies</a>. 2026.</li>
<li id="ref-28-zh"><a href="https://arxiv.org/abs/2610.00093">Safety in Self-Evolving Agents: A Survey</a>. 2026.</li>
<li id="ref-29-zh"><a href="https://arxiv.org/abs/2603.28052">Meta-Harness: End-to-End Optimization of Model Harnesses</a>. 2026.</li>
<li id="ref-30-zh"><a href="https://arxiv.org/abs/2608.13951">HELIX: Model-Harness Co-evolution for Recursive Self-Improvement</a>. 2026.</li>
<li id="ref-31-zh"><a href="https://arxiv.org/abs/2608.05810">When Self-Evolution Backfires: Pre-Commit Gating against Skill Contamination in LLM Agents</a>. 2026.</li>
<li id="ref-32-zh"><a href="https://arxiv.org/abs/2608.22610">Coalition-Aware Skill Reliability for Self-Evolving Agents</a>. 2026.</li>
<li id="ref-33-zh"><a href="https://arxiv.org/abs/2609.38294">MoFlow: Multi-Objective Agentic Workflow Generation</a>. 2026.</li>

</ol>

</div>

</div>
<script src="{{ '/assets/agent-rsi/article.js' | relative_url }}" defer></script>

[r1]: https://arxiv.org/abs/2303.11366
[r2]: https://arxiv.org/abs/2305.16291
[r3]: https://arxiv.org/abs/2309.16797
[r4]: https://arxiv.org/abs/2310.02304
[r5]: https://arxiv.org/abs/2408.08435
[r6]: https://arxiv.org/abs/2410.10762
[r7]: https://arxiv.org/abs/2504.15228
[r8]: https://arxiv.org/abs/2505.22954
[r9]: https://arxiv.org/abs/2507.19457
[r10]: https://arxiv.org/abs/2510.04618
[r11]: https://arxiv.org/abs/2506.10943
[r12]: https://arxiv.org/abs/2511.16043
[r13]: https://arxiv.org/abs/2511.10395
[r14]: https://arxiv.org/abs/2603.19461
[r15]: https://arxiv.org/abs/2606.26294
[r16]: https://arxiv.org/abs/2609.26457
[r17]: https://arxiv.org/abs/2609.14858
[r18]: https://arxiv.org/abs/2502.07373
[r19]: https://arxiv.org/abs/2502.00757
[r20]: https://arxiv.org/abs/2604.09297
[r21]: https://arxiv.org/abs/2605.19330
[r22]: https://arxiv.org/abs/2606.16111
[r23]: https://arxiv.org/abs/2609.05992
[r24]: https://arxiv.org/abs/2606.03678
[r25]: https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/
[r26]: https://arxiv.org/abs/2507.21046
[r27]: https://arxiv.org/abs/2607.27191
[r28]: https://arxiv.org/abs/2610.00093
[r29]: https://arxiv.org/abs/2603.28052
[r30]: https://arxiv.org/abs/2608.13951
[r31]: https://arxiv.org/abs/2608.05810
[r32]: https://arxiv.org/abs/2608.22610
[r33]: https://arxiv.org/abs/2609.38294
