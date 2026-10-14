---
layout: default
title: "What Is Actually Evolving in a Self-Evolving Agent?"
date: 2026-10-14
author_profile: true
excerpt: "What self-evolving agents actually repair, why completion alone can mislead selection, and when joint objectives, constraints and Pareto archives become useful. English / 中文."
---

<link rel="stylesheet" href="{{ '/assets/agent-rsi/article.css' | relative_url }}">
<div id="rsi-essay" class="blog-post-content">
<div class="bm-language" role="group" aria-label="Article language / 文章语言">
<button type="button" data-bm-language="en" aria-pressed="true" aria-controls="bm-content-en" lang="en">English</button>
<button type="button" data-bm-language="zh" aria-pressed="false" aria-controls="bm-content-zh" lang="zh-CN">中文</button>
</div>

<div id="bm-content-en" class="bm-language-content" lang="en" markdown="1">

<p class="bm-kicker">Research essay · October 14, 2026</p>

# What Is Actually Evolving in a Self-Evolving Agent?

<p class="bm-deck">What self-improvement methods actually fix, where their gains stop, and how the need for multi-objective optimization emerges.</p>

Suppose a coding agent learns to retry whenever a test fails. Its completion rate rises. That looks like a successful update—until we notice that it now takes longer, makes many more tool calls, and occasionally edits files outside the permitted scope.

The agent has learned something useful: persistence helps solve difficult tasks. It has also learned an overly broad rule. Should we keep the update, reject it, or search for a version that retries more selectively?

This is the problem I want to understand through self-evolving agents and recursive self-improvement, or RSI. We are getting better at producing modifications to an agent. Deciding which modifications constitute progress is a separate challenge.

<div class="bm-thesis" markdown="1">

Multi-objective optimization enters the picture when the same change affects several things we care about, and improving one no longer tells us what happened to the others. The first task is to make those effects visible together. Only then can we decide which are negotiable, which are constraints, and which alternatives are worth preserving.

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

<h2 id="components-en">01 / What do self-evolving methods actually repair?</h2>

The useful progression in this literature is a sequence of bottlenecks. An agent may fail to retain experience, fail to change how it acts, lack the skill needed for the task, or waste its budget searching for improvements. Different methods intervene at different bottlenecks. 

### When experience disappears after execution

If a failure teaches the agent nothing that survives the next attempt, the system keeps paying to discover the same lesson. Reflexion retains verbal feedback, Voyager builds executable skills, and ACE organizes evolving context into a playbook.[1](#ref-1-en) [2](#ref-2-en) [10](#ref-10-en)

Their shared contribution is **turning execution into reusable experience**. The remaining question is when that experience should apply. “Retry after failure” is useful for a transient error and harmful when an action lacks authorization. Storing a lesson does not establish its scope. A memory system needs to distinguish a general rule from a rule that worked under particular conditions.

### When better instructions cannot fix the action structure

A reminder to “edit carefully” cannot make a coarse editing tool precise. Workflow and code search open a different space: ADAS and AFlow automate agent or workflow design; DGM modifies tools and execution logic, including more targeted editing.[5](#ref-5-en) [6](#ref-6-en) [8](#ref-8-en)

This addresses **limitations of the available operations and their organization**. It also explains why frozen-model improvements can be substantial. The model may already know enough to solve a problem, while the surrounding system makes the right action difficult to perform. Yet a better structure on one workload may remain fragile on another. We still need to identify what the change fixed and which situations it could disrupt.

### When the model needs to learn a capability

Sometimes a better wrapper is insufficient. SEAL rewards generated adaptation procedures according to performance after a weight update. Agent0 and AgentEvolver develop training signals through generated tasks and interaction.[11](#ref-11-en) [12](#ref-12-en) [13](#ref-13-en)

These methods address **the supply and use of learning experience**. Their next bottleneck is the quality of that experience. If a curriculum repeats familiar tasks or rewards a shared mistake, more training does not repair the missing signal. Task generation must be assessed through the distinctions it teaches the learner to make.

The learning and runtime routes can also feed each other. HELIX proposes a build–update–rebuild loop: evolve harnesses, use verified contrasting trajectories for model learning, then adapt the harness to the updated model. Its reported study covers one harness-evolution round and the resulting training records.[30](#ref-30-en)

### When the improvement process is itself inefficient

RSI moves the question up one level. Promptbreeder modifies mutation prompts; STOP applies a code improver to itself; HyperAgents opens the meta-agent to modification. AIDE² searches research-agent harnesses, while Dream-RSI searches exploration policies using recorded experience.[3](#ref-3-en) [4](#ref-4-en) [14](#ref-14-en) [16](#ref-16-en) [17](#ref-17-en)

The aim is **to improve how the next useful change is found**. A better final agent is one possible result. A procedure that produces better changes under the same budget is a stronger result and needs its own test. Recursion also inherits the evaluator's omissions: a more effective search procedure can become more effective at optimizing an incomplete definition of success.

<figure>
<picture>
<source media="(max-width: 640px)" srcset="{{ '/assets/agent-rsi/evolution-loop-en-mobile.svg' | relative_url }}">
<img src="{{ '/assets/agent-rsi/evolution-loop-en.svg' | relative_url }}" alt="An improver proposes changes to agent components. Execution produces evidence, selection retains changes, and the next run inherits them. A recursive path also changes the improver." loading="lazy">
</picture>
<figcaption><strong>Figure 1.</strong> An evolving system has an editable object and a selection loop. The solid path updates the agent; the dashed path also updates the improver.</figcaption>
</figure>

Across these routes, two decisions recur: what may change, and what evidence justifies keeping the change. The papers expand the first in different ways. The second leads directly to the need for joint evaluation.

<h2 id="objects-en">02 / A higher completion rate can leave the decision unresolved</h2>

Return to the coding agent. Imagine evaluating three policies on the same 100 tasks. The completion grader checks whether the requested result was produced; a separate audit checks whether the agent stayed within its permitted actions.

<div class="bm-table bm-table-wide bm-case" role="region" aria-label="Illustrative agent update comparison" tabindex="0" markdown="1">

| Policy | Completed tasks | Mean tool calls | 95th-percentile time | Runs with an unauthorized action |
|:--|:--|:--|:--|:--|
| P0 · Original | 80 / 100 | 6 | 40 seconds | 0 / 100 |
| P1 · Retry broadly | 89 / 100 | 14 | 110 seconds | 4 / 100 |
| P2 · Retry selectively and check scope | 88 / 100 | 8 | 55 seconds | 0 / 100 |

</div>

<p class="bm-note">Illustrative values for the thought experiment. Completion and authorization are counted separately, so a completed task can still involve an unauthorized action.</p>

A completion-only optimizer chooses P1. A strict time budget could favor P0. A deployment that prohibits unauthorized actions rules out P1 despite its higher completion rate. P2 becomes interesting because it preserves most of the additional completion while reducing the other costs.

Completion answers whether the requested result was produced. Deployment also asks how it was produced. Once execution affects resources and permissions, **reaching the endpoint and reaching it acceptably become distinct properties**.

Objectives and diagnostic signals serve different purposes. Repeated invalid tool calls may be a diagnostic explanation for latency rather than something we value separately. Evidence checks may help explain reliability without being a sufficient measure of it. We should choose objectives from the deployment requirement, then use diagnostics to explain how a candidate succeeds or fails. Otherwise, adding metrics can simply count the same benefit twice.

<h2 id="coupling-en">03 / Why not improve capability first, then repair the rest?</h2>

Because the objectives often share the same control decisions. More retries change completion, cost and time together. More verification can detect errors and increase latency. A stricter stopping rule can reduce exposure to unsafe actions and terminate legitimate work too early. A change aimed at one objective therefore needs to be re-evaluated on the others.

Imagine starting from P1 and applying a cost-saving patch: stop after fewer tool calls. The patch may remove wasted retries—or remove the attempt that solved the difficult cases. Then a capability patch reintroduces retries. Each local change can look good on its own target while the sequence makes little progress. 

The useful intervention may be conditional: retry a temporary service failure, fix malformed arguments, stop an unauthorized operation, and reserve verification for consequential edits. These failures can all appear as “task not completed,” yet call for different changes. A vector of scores reveals the effects; trajectory diagnostics can connect those effects to a better policy.

Meta-Harness makes this diagnosis concrete by letting its proposer inspect previous code, scores and full execution traces. The useful feedback is not just that a candidate failed, but where its mechanism stopped working.[29](#ref-29-en)

A final safety filter remains useful. It can reject P1 for deployment. But it cannot recover a useful policy that the search never generated or discarded earlier. If every generation retains only the highest-completion candidate, P2 may disappear before the deployment constraint is applied. Logging every candidate avoids literal deletion, but the choice of which parents receive more search budget still shapes what comes next. **Selection changes both the final choice and the material available for future search.**

Joint optimization therefore brings the relevant requirements into the improvement process: they guide which changes are proposed, retained and developed further. Measuring several properties is only the first step; those measurements must influence the search. A fixed utility, explicit constraints and a set of alternatives offer different ways to do that. 

There is a further possibility: the apparent trade-off may come from a poor design. Replacing an unreliable tool can increase completion and reduce retries simultaneously. The objective is to discover these joint gains where possible, and make the remaining trade-offs explicit where they persist. Choosing among existing compromises and discovering a policy that improves on them are different achievements.

<h2 id="objectives-en">04 / From several metrics to a joint decision</h2>

### First, identify what cannot be exchanged

If modifying a forbidden file is unacceptable, extra completed tasks cannot compensate for it. That requirement belongs in the feasible set, supported by action-level enforcement where possible. An observed violation disqualifies a candidate for that deployment. Passing a finite test suite still leaves uncertainty about future behavior.

This separates two questions that are easily mixed together: “is this candidate admissible?” and “which admissible candidate do we prefer?” Some risks admit an explicitly chosen tolerance; others are hard prohibitions. The optimizer should reflect the actual requirement.

### Next, make preferences explicit when they are known

A weighted utility is reasonable when the exchange rates are stable and defensible. SICA, for example, combines performance, cost and runtime in one utility.[7](#ref-7-en) That is already a way of accounting for several requirements.

The sensitivity is easy to see in our example. Temporarily compare completion and calls alone. Subtracting 0.1 percentage point per mean tool call gives P1 a score of 87.6 and P2 a score of 87.2. Raising that penalty to 0.5 gives 82 and 84, reversing the choice. The arithmetic is correct in both cases; the preference changed. Adding back the authorization constraint excludes P1 regardless of those weights.

A weighted score expresses a particular preference. Its ranking depends on those exchange rates and on metric normalization, even when the written weights remain unchanged.

### Preserve alternatives when one preference would be premature

If the same system will serve several workloads, a single early choice may be wasteful. Among candidates that satisfy the deployment requirements, one may be cheaper and another more effective. A Pareto archive keeps a candidate when no other evaluated, feasible candidate is at least as good on every chosen objective and strictly better on one.

<figure>
<picture>
<source media="(max-width: 640px)" srcset="{{ '/assets/agent-rsi/pareto-en-mobile.svg' | relative_url }}">
<img src="{{ '/assets/agent-rsi/pareto-en.svg' | relative_url }}" alt="Illustrative policies P0 and P2 trade completion against tool calls. P1 completes most tasks but fails the authorization requirement." loading="lazy">
</picture>
<figcaption><strong>Figure 2.</strong> The same hypothetical policies as the table. P0 and P2 remain useful under different resource budgets. P1 has the highest completion rate but fails the authorization requirement. The line connects the two illustrative choices.</figcaption>
</figure>

This gives P0 and P2 distinct roles: P0 fits a tighter resource budget; P2 offers higher completion at greater cost. The archive postpones the preference decision and provides different starting points for later mutations.

**Joint consideration is needed when relevant effects are coupled and not redundant. Preserving a frontier is useful when several trade-offs remain valuable.** If the deployment utility is fixed and known, searching directly for its optimum may be more efficient than maintaining a broad archive.

<h2 id="methods-en">05 / What do existing multi-objective methods contribute?</h2>

Existing multi-objective methods bring these requirements into different parts of the improvement process: workflow search, skill selection and policy learning.

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

MoFlow moves the trade-offs inside the search tree: a node stores multiple attainable outcomes rather than one score. Its convex-hull search supports selection under different linear preference weights from the discovered workflows.[33](#ref-33-en)

These formulations address different requirements. A platform requirement differs from an operational safety requirement. A reusable skill and a per-query policy have different opportunities to amortize their search cost. GEPA offers another distinction: its Pareto selection preserves strengths across problem instances, rather than automatically defining a quality–cost–safety frontier.[9](#ref-9-en)

Our work **MOAE** takes the per-query route: the model, tools and architecture remain fixed, while candidate policies change planning, tool use, verification and stopping. Objective-specific diagnostics guide changes; complete rollouts supply evaluation; an empirical archive precedes the final deployment choice.[23](#ref-23-en)

The broader design idea is to separate **what the search should preserve** from **what one deployment should return**. The value of those alternatives depends on candidate coverage and evaluation quality.

There is also a third purpose for keeping a candidate: learning from it. A failed harness can supply a useful negative example, while two successful ones can reveal an unnecessary step—a distinction made explicit in HELIX.[30](#ref-30-en) I would keep deployable options and diagnostic records separately: poor deployment performance need not erase useful evidence.

<h2 id="evidence-en">06 / Multi-objective search leaves several shared problems open</h2>


### A vector of proxies can still miss the real requirement

Adding objectives repairs an omission only if the new signals measure something meaningful. A judge can reward fluent explanations instead of grounded evidence. A tool-use metric can reward fewer calls while missing the checks those calls performed. Multiple weak proxies do not become reliable merely because they are optimized together.

Evolving the evaluator, as RQGM explores, makes the signal itself adaptable.[15](#ref-15-en) It also makes historical comparison harder. My preference would be to retain stable external checks alongside the evolving evaluation, so that changing behavior and changing standards can be distinguished.

### A useful skill may become harmful in a different combination

*When Self-Evolution Backfires* traces a failure chain: an admitted defective skill influences the skills distilled later, so deleting the original can leave its descendants in place. Its VaG method checks skills before admission and evaluates their joint contribution.[31](#ref-31-en) *Coalition-Aware Skill Reliability* examines how a skill's contribution changes with its partners and deployment domain, using coalition-aware selection and transfer-time masking.[32](#ref-32-en)

The question becomes “what does this update do inside the current system?” A local gain deserves checks on combinations and future reuse. This adds a time dimension to joint evaluation: a rule can help today's task and make tomorrow's updates less reliable.

### A noisy frontier can preserve lucky candidates

A candidate that looks excellent on one rollout may be fortunate rather than robust. With many objectives, more candidates can appear incomparable, increasing the burden of deciding which ones deserve another evaluation. A frontier can then grow faster than confidence in it.

This suggests a budget question beyond mutation: when should we generate a new policy, repeat a promising one, or test a suspected failure? A useful archive should retain uncertainty and failure evidence alongside point scores. “Nondominated in observed results” is a statement about the current evidence, not a permanent property of an agent.

### Progress on selected tasks does not establish transfer or recursion

The existing results are valuable, but they support different claims:

<div class="bm-table bm-table-wide" role="region" aria-label="Selected quantitative evidence and its scope" tabindex="0" markdown="1">

| Source | Reported observation | What it establishes—and what remains open |
|:--|:--|:--|
| [DGM][r8] | Coding success rose from **20% to 50%** on its **200-task** SWE-bench Verified evaluation after 80 iterations. | Evidence for better coding-agent implementations under that protocol; not a 50% result on the entire Verified set. |
| [AIDE²][r16] | **7 accepted improvements in 8 days**; external evaluation covered **4 benchmarks**. | Improved research agents. Their superiority as outer-loop improvers remained inconclusive because of noise and limited replication. |
| [Open-ended research case studies][r27] | **2 research problems**, roughly **6 days** and thousands of dollars of agent work. | The researchers reported no substantial research progress in those cases, despite engineering activity. This probes a different task from optimizing a supplied measurable objective. |

</div>

A better agent on unseen tasks is evidence for transfer beyond its selection set. A better **improver** requires a further comparison: let original and evolved improvers start from matched agents, with matched budgets and unseen task families, then compare the gains they produce. Private examples used repeatedly to select updates belong to the improvement process, even if their contents are hidden from the inner agent.

For persistent updates, another test is whether they survive a model or tool change. This connects evolution to the [agent deployment gap]({{ '/the-anchor-of-logic-and-the-sands-of-probability/' | relative_url }}). An inherited workflow may encode assumptions about the old model. A memory entry or tool patch may likewise carry a defect into future executions, a concern emphasized in recent safety synthesis.[28](#ref-28-en)

### Search itself consumes the resources being optimized

A cheap final policy may have been expensive to discover. A reusable workflow costing 100 USD to find and saving 0.10 USD per use needs 1,000 uses to break even before maintenance. Per-query search has a different accounting problem: it needs to justify its cost on that query. Reports should separate search, evaluation and deployed execution instead of combining them into an ambiguous “efficiency” claim.

<h2 id="research-en">07 / What would demonstrate a better improvement process?</h2>

I would return to the retry example and ask for an explanation that predicts behavior. Perhaps selective retries work because they distinguish temporary errors from missing permissions. Then the evaluation should vary those conditions while keeping the task goal similar. If the improvement disappears under that small change, the claimed lesson was too broad.

This is why [case construction]({{ '/what-do-benchmarks-measure/' | relative_url }}) is part of agent evolution. The suite decides which consequences of an update become visible. A suite full of retry-friendly tasks encourages one policy; paired cases that separate recoverable failures from forbidden actions can reveal a more useful distinction.

To test whether joint optimization actually helps, I would compare it with completion-only search plus a final filter, a fixed weighted utility, constrained search, and sequential tuning. All should receive the same candidate interface and comparable total evaluation budgets. The final comparison should use declared deployment preferences and independent tasks, not only the metric favored by the proposed optimizer.

Three observations would make the result informative: does joint evaluation recover usable candidates that the other procedures miss; do retained alternatives serve genuinely different requirements; and do targeted diagnostics generate joint gains rather than merely select different compromises? Archive size alone answers none of these questions. Hypervolume summarizes how much objective space a set of candidates covers relative to a reference point. Comparisons need fixed scales and a fixed reference, alongside actual deployment outcomes.

A reader can apply the same reasoning to the next RSI paper: identify the bottleneck repaired, inspect what is inherited, trace which signals select it, and ask what remains invisible to those signals. Then check whether the evidence supports a better answer, a better reusable agent, or a better process for producing improvements.

The motivation for multi-objective evolution follows from this chain. A single agent action can affect several requirements. A single completion score cannot identify all of those effects. Joint evaluation makes them visible; constraints express what is unacceptable; preferences choose among acceptable outcomes; and an archive can preserve choices that remain useful. **The research challenge is to make these decisions reliable enough that successive updates accumulate useful capability.**

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

<p class="bm-kicker">研究随笔 · 2026 年 10 月 14 日</p>

# Agent 自进化，到底在进化什么？

<p class="bm-deck">自我改进方法修复了什么，它们的收益止步于哪里，以及多目标优化为什么会自然成为下一个问题。</p>

假设一个编程 Agent 学会了“测试失败就继续重试”。任务完成率提高了，看起来是一次成功的更新。接着我们发现，它运行得更久，调用了更多工具，还偶尔修改了授权范围之外的文件。

这个 Agent 学到了有用的东西：坚持尝试有助于解决难题。但它也学到了一条适用范围过宽的规则。我们应该保留这次更新，直接放弃，还是继续寻找一种更有选择性的重试方式？

这是我想通过 self-evolving agents 和递归自我改进（RSI）理解的问题。我们越来越擅长让系统产生修改，但判断什么修改值得留下，仍然是另一项挑战。

<div class="bm-thesis" markdown="1">

当同一个改动会影响几个重要属性，而其中一个变好又无法说明其他属性发生了什么，多目标优化就有了具体的必要性。首先要让这些影响同时可见，然后才能决定：哪些可以取舍，哪些必须满足，哪些不同方案值得保留。

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

<h2 id="components-zh">01 / 自进化方法真正修复了什么？</h2>

理解这些工作，可以从一系列瓶颈出发：Agent 可能留不住经验，无法改变行动方式，缺少完成任务所需的能力，也可能把大量预算浪费在寻找改进上。不同方法处理的是不同瓶颈。

### 经验在执行结束后消失

如果一次失败没有留下任何能影响后续尝试的东西，系统就会反复付出代价，重新发现同一个教训。Reflexion 保留文字反思，Voyager 积累可执行技能，ACE 把持续更新的上下文组织成经验手册。[1](#ref-1-zh) [2](#ref-2-zh) [10](#ref-10-zh)

它们共同解决的是：**让执行产生可以复用的经验。** 接下来的问题，是这些经验应该在什么时候生效。“失败后重试”对暂时性错误可能有效，遇到缺少权限的操作时却可能有害。把经验存下来，并不能证明它的适用范围。记忆系统还需要区分一般规则，以及只在某些条件下成立的规则。

### 更好的指令也改变不了行动结构

一句“仔细编辑”无法把粗糙的编辑工具变得精确。工作流和代码搜索开放了另一种改进空间：ADAS 和 AFlow 自动设计 Agent 或工作流，DGM 则修改工具与执行逻辑，包括更精确的文件编辑方式。[5](#ref-5-zh) [6](#ref-6-zh) [8](#ref-8-zh)

这类方法处理的是：**可用操作及其组织方式造成的限制。** 这也解释了为什么固定底层模型仍然能带来明显收益。模型可能已经具备解决问题所需的知识，只是周围的系统让正确操作很难执行。不过，一种结构在某类任务上有效，换到另一类任务上仍然可能出问题。我们还需要知道，改动具体修复了什么，又可能破坏什么。

### 模型本身缺少某种能力

有时，改好外围系统仍然不够。SEAL 根据权重更新之后的表现，奖励生成的适应方案。Agent0 和 AgentEvolver 则通过生成任务与环境交互，构造训练所需的信号。[11](#ref-11-zh) [12](#ref-12-zh) [13](#ref-13-zh)

它们处理的是：**学习经验从哪里来，以及如何利用。** 下一道瓶颈就变成了经验质量。如果课程只是重复熟悉的任务，或者奖励了大家共同犯下的错误，更多训练也无法补上缺失的信号。评价任务生成，需要看它究竟教会学习者区分了什么。

学习与运行框架也可以相互推动。HELIX 提出“构建—更新—重建”的循环：先演化框架，再把验证过的对比轨迹用于模型学习，随后根据更新后的模型调整框架。论文报告的是一轮框架演化及其产生的训练记录。[30](#ref-30-zh)

### 寻找改进的过程本身效率不高

RSI 把问题再向上推进一层。Promptbreeder 修改生成变异的提示词，STOP 用代码改进程序修改它自身，HyperAgents 开放 meta-agent 的修改权限。AIDE² 搜索研究 Agent 的运行框架，Dream-RSI 则利用记录下来的经验搜索探索策略。[3](#ref-3-zh) [4](#ref-4-zh) [14](#ref-14-zh) [16](#ref-16-zh) [17](#ref-17-zh)

目标是：**让下一次有用的改动更容易被找到。** 最终得到一个更好的 Agent，是一种结果；在相同预算下更擅长产生后续改进，则是更强的结果，需要单独检验。递归也会继承评估器的遗漏：搜索能力提高，可能让系统更有效地优化一个并不完整的成功标准。

<figure>
<picture>
<source media="(max-width: 640px)" srcset="{{ '/assets/agent-rsi/evolution-loop-zh-mobile.svg' | relative_url }}">
<img src="{{ '/assets/agent-rsi/evolution-loop-zh.svg' | relative_url }}" alt="改进器修改 Agent 的不同组件；执行产生证据，筛选保留改动，下一次运行继承它们。递归路径进一步修改改进器本身。" loading="lazy">
</picture>
<figcaption><strong>图 1.</strong> 一个进化系统包含可修改的对象，以及决定改动能否留下的循环。实线路径更新 Agent，虚线路径进一步更新改进器。</figcaption>
</figure>

这几条路线都绕不开两个决定：允许修改什么，以及凭什么留下修改。不同论文以不同方式扩展了前者，后者则把我们带到了共同评估的问题上。

<h2 id="objects-zh">02 / 完成率提高了，选择仍然可能没有答案</h2>

回到编程 Agent。假设我们在相同的 100 个任务上比较三种策略。完成度评分器检查是否产出了要求的结果，另一个审计过程检查 Agent 是否始终在授权范围内行动。

<div class="bm-table bm-table-wide bm-case" role="region" aria-label="Agent 更新的假设比较" tabindex="0" markdown="1">

| 策略 | 完成任务 | 平均工具调用 | 第 95 百分位耗时 | 出现越权操作的运行 |
|:--|:--|:--|:--|:--|
| P0 · 原始策略 | 80 / 100 | 6 次 | 40 秒 | 0 / 100 |
| P1 · 广泛重试 | 89 / 100 | 14 次 | 110 秒 | 4 / 100 |
| P2 · 选择性重试，并检查操作范围 | 88 / 100 | 8 次 | 55 秒 | 0 / 100 |

</div>

<p class="bm-note">数字为假设示例。完成度与授权情况独立统计，因此完成任务的运行也可能包含越权操作。</p>

只看完成率，优化器会选 P1。严格限制耗时，可能会选 P0。如果部署要求禁止越权操作，P1 即使完成率最高也不能采用。P2 值得关注，是因为它保留了大部分新增的完成能力，同时降低了其他代价。

完成率回答有没有做到，部署还要问是怎么做到的。执行过程开始涉及资源与权限之后，**到达终点，以及以可接受的方式到达终点，就成为了不同属性。**

目标与诊断信号需要分开。反复调用无效工具，可能是解释延迟的诊断信号；证据检查次数可能有助于解释可靠性，但并不等于可靠性本身。我们应该从部署需求中确定目标，再用诊断信息解释候选为什么成功或失败。否则，多加几个指标，也可能只是把同一种收益重复计算。

<h2 id="coupling-zh">03 / 为什么不先提高能力，再修成本与安全？</h2>

因为这些目标经常受同一组决策影响。增加重试，会同时改变完成率、成本和时间。增加验证，可能发现更多错误，也会增加延迟。更严格的停止规则，可以减少危险操作的机会，也可能让正常任务过早结束。因此，一次针对某个目标的修改，仍然需要在其他相关目标上重新评估。

假设从 P1 出发，再加一个省钱的补丁：工具调用达到上限就停止。这个补丁可能删掉无效重试，也可能删掉恰好解决难题的那次尝试。随后，为了恢复完成率，又加回重试。每次局部修改都可能改善自己的目标，整个过程却没有取得多少进展。

有用的改动可能是一组条件规则：服务暂时出错时重试，参数格式错误时修正，操作越权时停止，对影响较大的编辑保留验证。这些情况都可能表现为“任务没完成”，却需要不同的修改。多个分数让后果可见，轨迹诊断则帮助我们把这些后果与更好的策略联系起来。

Meta-Harness 让提出修改的 Agent 检索此前的代码、分数和完整轨迹，使这种诊断可以落到具体行为上。反馈的价值，是帮助系统找到哪一步机制出了问题。[29](#ref-29-zh)

最后再加安全过滤，仍然有用：它可以阻止 P1 被部署。但它无法找回搜索从未生成、或者早已丢弃的策略。如果每一代只留下完成率最高的候选，P2 可能在部署约束介入之前就消失了。记录全部候选可以避免彻底丢失，但后续把搜索预算分给哪些父代，仍然会影响下一步能找到什么。**筛选不仅决定最后选谁，也决定后续搜索还能从什么出发。**

因此，共同优化要让相关要求参与整个改进过程：提出什么修改、保留哪些候选、继续探索哪些方向。测量多个属性只是第一步，测量结果还要影响搜索。固定效用、显式约束和保留一组方案，是实现这一点的不同方式。

还有一种容易被忽略的可能：看起来必须取舍，只是因为当前设计不好。换掉一个不可靠的工具，可能同时提高完成率、减少重试。我们应该尽量发现这样的共同改进，再把确实存在的取舍明确呈现出来。在现有的取舍中选择不同方案，与发现比它们更好的策略，是两种不同的进展。

<h2 id="objectives-zh">04 / 从多个指标，走到共同决策</h2>

### 先确定什么不能交换

如果修改禁止访问的文件不可接受，那么多完成几道题不能抵消这件事。这个要求应当决定候选是否可用，并在可能时通过操作层面的权限控制落实。已经观察到违规的候选，不适合这样的部署；通过有限测试，仍然不能消除未来行为的不确定性。

这样可以分开两个容易混在一起的问题：“这个候选是否符合要求”，以及“符合要求的候选里更喜欢哪一个”。某些风险可以设置明确的容忍范围，另一些行为则属于禁止事项。优化方式应当反映真实需求。

### 偏好明确时，就把它写清楚

当不同目标之间的交换关系稳定、且有依据时，加权效用是合理的。SICA 就把表现、成本和运行时间合成一个效用分数。[7](#ref-7-zh) 这已经是一种同时考虑多个要求的方式。

用前面的例子可以看清权重的影响。暂时只比较完成率和调用数：每次平均工具调用扣 0.1 个百分点，P1 得 87.6，P2 得 87.2；改成扣 0.5 个百分点，两者变成 82 和 84，排序反转。两次计算都没有错，改变的是偏好。如果再加上禁止越权的约束，无论这些权重如何设置，P1 都会被排除。

加权分数表达的是一种具体偏好。排序既取决于交换关系，也取决于指标如何归一化；即使写出来的权重没变，实际取舍也可能改变。

### 一次选择太早时，就保留不同方案

如果同一个系统要服务多种任务需求，过早确定唯一方案可能造成浪费。在满足部署要求的候选中，有的更便宜，有的完成率更高。Pareto 档案保留这样的候选：在已评估且符合要求的方案中，没有另一个方案在所有选定目标上都至少同样好，并且至少一个目标更好。

<figure>
<picture>
<source media="(max-width: 640px)" srcset="{{ '/assets/agent-rsi/pareto-zh-mobile.svg' | relative_url }}">
<img src="{{ '/assets/agent-rsi/pareto-zh.svg' | relative_url }}" alt="假设策略 P0 与 P2 在完成率和工具调用之间各有取舍。P1 完成率最高，但不符合授权要求。" loading="lazy">
</picture>
<figcaption><strong>图 2.</strong> 与表格对应的假设策略。P0 和 P2 适合不同资源预算，P1 虽然完成率最高，却不符合授权要求。连线用于连接这两个示例方案。</figcaption>
</figure>

于是，P0 和 P2 各有用途：P0 适合更紧的资源预算，P2 用更多成本换取更高完成率。档案推迟了偏好选择，也为后续变异保留了不同起点。

**当重要影响相互耦合、又不能彼此替代时，需要共同考虑；当多种取舍仍然有价值时，保留前沿才有意义。** 如果部署效用已经明确且长期不变，直接寻找它的最优解，可能比维护一个宽泛的档案更有效率。

<h2 id="methods-zh">05 / 现有多目标方法具体增加了什么？</h2>

现有多目标方法把这些要求带进了不同的改进环节：工作流搜索、技能选择，以及策略学习。

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

MoFlow 把取舍带进了搜索树内部：一个节点保留多种可达结果，再通过凸包搜索，从已发现的工作流中支持不同线性偏好权重下的选择。[33](#ref-33-zh)

这些方法回应了不同的需求。平台规范不等于操作安全，可复用技能与单次查询策略也有不同的成本摊销方式。GEPA 还提供了另一个区别：它的 Pareto 选择保留不同题目上的互补优势，并不自动构成质量、成本、安全这几个维度的前沿。[9](#ref-9-zh)

我们的工作 **MOAE** 采用单个查询的设置：模型、工具与架构固定，候选策略改变规划、工具使用、验证和停止方式。不同目标的诊断信息指导修改，完整执行提供评估证据，经验档案先于最终部署选择建立。[23](#ref-23-zh)

其中可以推广的设计思路，是分开**搜索中值得保留什么**，以及**某次部署最终返回什么**。这些方案的价值，取决于候选覆盖范围与评估质量。

保存候选还有第三种用途：从中学习。失败的框架可能提供有用的负例，两条成功轨迹的差别也可能暴露多余步骤，HELIX 明确讨论了这种经验价值。[30](#ref-30-zh) 我会把可部署方案与诊断记录分开保存，让暂时表现不好的候选也能留下有用的证据。

<h2 id="evidence-zh">06 / 多目标搜索之后，哪些共同问题仍然存在？</h2>


### 多个代理指标，仍然可能遗漏真实要求

增加一个目标，只有在新信号测到了有意义的东西时，才修复了原来的遗漏。评分器可能奖励解释流畅，而不是证据充分；工具效率指标可能奖励少调用，却没有识别被省掉的那些检查。几个薄弱的代理指标放在一起优化，并不会自动变得可靠。

RQGM 探索让评估器一起进化，使评价信号本身也能改变。[15](#ref-15-zh) 但历史结果也因此更难比较。我倾向于在可变评估之外保留稳定的外部检查，以便区分行为改变，以及评价标准改变。

### 有用的技能，换一种组合可能反而有害

*When Self-Evolution Backfires* 追踪了一条失败链：有缺陷的技能入库后，会影响后续技能的提炼；删除源头，仍然可能留下已经继承问题的后代。它提出的 VaG 在入库前检查技能，并评估组合贡献。[31](#ref-31-zh) *Coalition-Aware Skill Reliability* 进一步检查技能贡献如何随搭配和部署领域改变，通过组合感知选择与迁移时屏蔽来处理问题。[32](#ref-32-zh)

问题因此变成了“这次更新放进当前系统后，会产生什么影响”。局部收益还需要接受组合与后续复用的检验。共同评估也由此增加了时间维度：一条规则今天可能有用，却让明天的更新更不可靠。

### 带噪声的前沿，可能保留的是幸运候选

某个候选在一次运行中表现很好，可能只是运气好。目标变多以后，也会有更多候选看起来互有优劣，难以直接淘汰。档案可能增长得很快，对其中候选的信心却没有同步增加。

于是，预算问题不只在于如何产生变异，还包括什么时候应该生成新策略、重复评估有潜力的策略，或者专门检验一个疑似失败条件。有用的档案应当同时保留不确定性和失败证据。“在当前观测中不被支配”，描述的是现有证据，并不是 Agent 永久具有的属性。

### 在选定任务上进步，不等于迁移或递归能力已经成立

已有结果很有价值，但它们支持的是不同层次的主张：

<div class="bm-table bm-table-wide" role="region" aria-label="代表性定量证据及适用范围" tabindex="0" markdown="1">

| 来源 | 报告的结果 | 说明了什么，还有什么没解决？ |
|:--|:--|:--|
| [DGM][r8] | 80 轮迭代后，在选定的 **200 道** SWE-bench Verified 任务上，成功率从 **20% 升至 50%**。 | 支持该协议下编程 Agent 实现得到了改进；不是完整 Verified 数据集上的 50%。 |
| [AIDE²][r16] | **8 天接受 7 次改进**，另在 **4 个外部 benchmark** 上评估。 | 得到了更好的研究 Agent；由于噪声和重复实验有限，其作为外层改进器的优势仍不明确。 |
| [开放式研究案例][r27] | **2 个研究问题**，约 **6 天**、数千美元的 Agent 工作。 | 原研究者认为这些案例没有取得实质研究进展，尽管完成了工程活动。这与优化一个已给定、可测量的目标是不同任务。 |

</div>

在未见任务上表现更好，支持改进具有超出选择集的效果。要证明**改进器本身**更强，还需要下一步比较：让原始改进器与进化后的改进器，从匹配的 Agent 出发，使用相同预算，在未见任务族上比较各自带来的提升。用于反复筛选更新的私有样本，即使具体内容对内层 Agent 不可见，也已经参与了改进过程。

对于持久更新，还需要检查它能否经受模型或工具变化。这把进化问题与 [Agent Deployment Gap]({{ '/the-anchor-of-logic-and-the-sands-of-probability/' | relative_url }}) 联系起来：继承下来的工作流可能包含对旧模型的假设，记忆或工具补丁也可能把缺陷带入后续执行。近期安全综述同样关注这种持久状态带来的风险。[28](#ref-28-zh)

### 搜索本身，也在消耗我们试图优化的资源

最终策略便宜，不代表找到它的过程便宜。假设寻找可复用工作流花了 100 美元，每次使用节省 0.10 美元，那么不计维护成本，需要使用 1,000 次才回本。单查询搜索面对的是另一种账：它必须在当前查询上解释这笔开销。报告应当分开搜索、评估和部署执行，而不是都放进一个含义不清的“效率提升”。

<h2 id="research-zh">07 / 怎样证明改进过程真的更好了？</h2>

我会回到重试的例子，要求一种能够预测行为的解释。假如选择性重试有效，是因为它区分了临时错误和缺少权限，那么评估就应当在任务目标相近的情况下，改变这两个条件。如果稍微换一下条件，收益就消失了，说明原来总结出的经验过于宽泛。

这就是为什么 [case 如何构建]({{ '/what-do-benchmarks-measure/' | relative_url }}) 属于 Agent 进化问题。测试集决定一次更新的哪些后果能够被看见。大量适合重试的题会鼓励一种策略；把可恢复故障与禁止操作区分开的成对案例，则可能揭示更有用的规则。

要验证共同优化是否有用，我会比较：只优化完成率、最后再过滤；固定加权效用；约束搜索；逐项目标调优，以及保留多个目标方案的搜索。它们应当使用相同的候选修改接口，以及可比的总评估预算。最终比较依据事先声明的部署偏好和独立任务，而不是只报告新优化器偏爱的那个指标。

三个观察会让结果更有解释力：共同评估是否找到了其他流程遗漏的可用候选；保留下来的不同方案是否确实服务于不同需求；定向诊断是否产生了共同改进，而不只是选中了另一种妥协。档案更大，本身无法回答这些问题。超体积概括一组方案相对参考点覆盖了多大的目标范围。比较时要固定目标尺度和参考点，并结合实际部署表现。

读下一篇 RSI 论文时，也可以沿着这条线追问：它修复了什么瓶颈，下一次执行继承了什么，哪些信号决定保留，哪些影响仍然不可见。然后判断证据究竟支持一个更好的答案、一个更好的可复用 Agent，还是一个更好的改进过程。

多目标进化的动机就从这里逐步形成：Agent 的同一个行动会影响几个要求，单一完成率无法识别全部影响；共同评估让这些影响可见，约束表达不可接受的行为，偏好决定如何选择可接受的结果，档案则可以保留仍然有价值的不同方案。**真正的研究挑战，是让这些决定足够可靠，使连续更新能够积累有用的能力。**

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
