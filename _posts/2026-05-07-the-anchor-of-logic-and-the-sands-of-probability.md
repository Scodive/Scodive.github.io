---
layout: default
title: "When the Model Changes, What Happens to the Agent?"
title_zh: "模型换了，Agent 为什么变了？"
date: 2026-05-07
last_modified_at: 2026-10-08
author_profile: true
excerpt: "Why an agent tuned for one model can change behavior on another, and how to measure, adapt, and validate a model migration."
excerpt_zh: "为什么在一个模型上调顺的 Agent 换到另一个模型后行为会走样，以及如何测量、适配并验证一次模型迁移。"
topic: "Agent architecture"
topic_zh: "Agent 架构"
reading_time: "15 min read"
reading_time_zh: "约 15 分钟"
figure_en: "/assets/model-migration/architecture-en.svg"
figure_zh: "/assets/model-migration/architecture-zh.svg"
figure_alt_en: "Architecture diagram separating stable task contracts from replaceable model-specific adapters"
figure_alt_zh: "将稳定任务契约与可替换模型适配层解耦的架构图"
---

<link rel="stylesheet" href="{{ '/assets/model-migration/article.css' | relative_url }}">
<div id="migration-essay" class="blog-post-content">
<div class="bm-topbar">
<a class="bm-back-link" href="{{ '/blogs/' | relative_url }}" data-en="All essays" data-zh="全部文章">All essays</a>
<div class="bm-language" role="tablist" aria-label="Article language / 文章语言">
<button type="button" role="tab" data-bm-language="en" aria-selected="true" aria-pressed="true" aria-controls="bm-content-en" lang="en">English</button>
<button type="button" role="tab" data-bm-language="zh" aria-selected="false" aria-pressed="false" aria-controls="bm-content-zh" lang="zh-CN">中文</button>
</div>
</div>

<div id="bm-content-en" class="bm-language-content" lang="en" markdown="1">

# When the Model Changes, What Happens to the Agent?

<p class="bm-meta">May 7, 2026 · Agent architecture · 15 min read<span id="vercount_container_page_pv" class="bm-meta__views" style="display:none;"> · <strong class="bm-meta__views-num" id="vercount_value_page_pv">--</strong> views</span></p>

<p class="bm-deck">Model swaps, version upgrades, and the gap between the model we optimize for and the one we deploy.</p>

Anyone who has tuned an agent for a few weeks knows the feeling: the prompts settle down, the tools behave, and the eval curve stops wobbling. Then production switches models. Maybe finance wants a cheaper provider, maybe the vendor retires an older snapshot, or maybe latency forces a drop to a smaller tier. The API still accepts every request without complaint, yet the system running behind it suddenly acts like a stranger.

A search step that used to return a crisp answer wanders into a multi-turn exploration loop. A model that once waited politely for tool output starts batching several calls in parallel. A summarizer drops an edge-case constraint, or a retry loop that rescued the old model causes the new one to fire a side effect twice. Nothing about this requires the replacement model to be obviously "dumber."

What I keep coming back to is a simpler question: **when we say an agent system works, what did we actually optimize?** Did we build a reusable system property, write a set of workarounds around one model's quirks, or tune a fragile interaction that breaks the moment either half changes?

<div class="bm-thesis" markdown="1">

An agent's behavior belongs to the joint system of model, harness, environment, and budget. Portability does not mean freezing the system in place; it means keeping the task contract fixed while measuring and bounding the work needed to adapt the rest.

</div>

<nav class="bm-toc" aria-label="Contents" markdown="1">

**In this essay**

1. [Define what changed](#object-en)
2. [Find the hidden dependencies](#coupling-en)
3. [Read the evidence in both directions](#evidence-en)
4. [Separate replacement from adaptation](#diagnosis-en)
5. [Decouple around enforceable contracts](#architecture-en)
6. [Optimize for the production model](#adaptation-en)
7. [Count the full cost](#economics-en)
8. [Migrate a release, not a model name](#migration-en)
9. [Make portability a research object](#research-en)

</nav>

<h2 id="object-en">The model is only one part of the deployed policy</h2>

I use *harness* to mean everything wrapped around the model: prompts, context assembly, memory policies, tool interfaces, routing, validators, retries, and stopping rules. Task outcomes depend on all of those pieces alongside the workload and resource limits.

<div class="bm-equation">J(M, H, D, B, E) = E[task utility | model M, harness H, workload D, budget B, environment E]</div>

Even with code `H` completely untouched, swapping `M` shifts the distribution of actions the agent takes. Different actions change the environment, which in turn changes the observations coming back on the next step. Swapping the model therefore alters both the decision maker and the sequence of states it ends up seeing.

Four kinds of model changes come up in practice, and they carry different risks:

<div class="bm-table bm-table-wide" role="region" aria-label="Comparison" tabindex="0" markdown="1">

| Change | Typical reason | What needs to be re-established |
|---|---|---|
| Same family, new version | Upgrade or provider retirement | Behavioral compatibility, including previously reliable edge cases |
| Different model or provider | Cost, latency, availability, capability | Interface semantics, task quality, operating budget |
| Tuned on A, deployed on B | Strong model used during development; cheaper executor in production | Whether the gains survive on B, and the adaptation cost |
| Model switch during a session | Routing, escalation, outage fallback | Whether B receives sufficient state and understands pending actions |

</div>

Having model A *design* a workflow for model B is also not the same as evaluating and tuning a workflow on A and copying it blindly onto B. A stronger architect can certainly draft clean code or few-shot examples for a smaller executor, as long as final selection relies on B's own execution scores. Who wrote the prompt matters far less than which model the selection signal came from.

Classic longitudinal checks, such as Chen et al.'s comparison of March and June 2023 ChatGPT snapshots, documented clear behavioral drift across tasks and instruction-following.[1](#ref-1-en) That sort of study justifies behavioral regression testing, even though an outside observer can rarely tell whether a shift came from training mix, RLHF, or serving changes. With a black-box endpoint, the only reliable anchor is the observable contract and where it breaks.

<h2 id="coupling-en">The dependencies hidden inside a “working” system</h2>

Surface-level dependencies are easy enough to spot: a JSON parser expects an exact key, or two providers format tool errors differently. The harder ones are behavioral assumptions baked into the harness without anyone writing them down. The workflow quietly assumes the model will search before answering, carry unresolved constraints into summaries, recover cleanly from a bad edit, or stop as soon as the job is done.

Worse, bug fixes during development routinely turn one model's quirks into structural dependencies. Suppose the original model tends to ignore a constraint, so an engineer repeats it three times across the system prompt and tool hints. Swap in a model that takes every instruction literally, and it now checks that same constraint three separate times until it hits the turn limit. What started as a local patch has turned into cross-component coupling.

<div class="bm-table bm-table-wide" role="region" aria-label="Comparison" tabindex="0" markdown="1">

| Dependency | What can change after a swap | Repair at the right layer |
|---|---|---|
| Output and tool protocol | Missing fields, different stop events, parallel calls | Normalize messages and validate schemas; preserve error semantics |
| Planning and stopping | More exploration, premature completion, excessive checking | Explicit completion evidence and bounded execution policies |
| Context and memory | Different use of summaries, tool outputs, or examples | Store facts and unresolved obligations with provenance; test reconstruction |
| Recovery | Repeating a failed action or treating a business rejection as an outage | Classify errors; define which actions can be retried safely |
| Budget | More reasoning, longer tool loops, higher tail latency | Measure quality against time and cost; tune operating points |
| Evaluation | A new answer style pleases the judge but violates the task | Independent end-state checks and audited judging examples |

</div>

Because agents run in closed loops, small early divergences snowball quickly. One slightly different search query changes the retrieved context; that altered context shifts the plan, tool arguments, conversation history, and ultimately when the agent decides to stop. Evaluating only single-turn responses hides most of the real failure modes.

<figure><img loading="lazy" src="{{ '/assets/model-migration/loop-en.svg' | relative_url }}" alt="Figure 1 · A model swap changes the trajectory distribution. Conceptual diagram. The same initial request can lead to different future states; a recorded transcript covers only one path."><figcaption><strong>Figure 1 · A model swap changes the trajectory distribution.</strong> Conceptual diagram. The same initial request can lead to different future states; a recorded transcript covers only one path.</figcaption></figure>

That is also why transcript replay and live closed-loop runs answer different questions. Feeding two models the exact same recorded history is a great way to pinpoint where tool arguments or single-step decisions diverge, yet it tells you nothing about the downstream states model B will steer itself into once it runs free. Controlled replay is for diagnosis; closed-loop evaluation is for measuring performance.

<h2 id="evidence-en">Portability is real, just selective</h2>

Empirical results point in both directions, depending on which piece of the harness gets moved. On the pessimistic side, Sclar et al. showed that even meaning-preserving prompt formatting tweaks cause wide swings in accuracy, with rankings correlating weakly across models.[2](#ref-2-en) Holding a single prompt template fixed is therefore rarely a neutral way to compare two models.

Yet structural improvements do travel remarkably well. SWE-agent built its agent-computer interface around GPT-4 Turbo and found that the same interface transferred effectively to Claude 3 Opus, lifting resolution rate on SWE-bench Lite by 10.7 percentage points over a plain shell baseline.[3](#ref-3-en) Good ergonomics around files, editing, and terminal feedback help across model families, even if optimal phrasing and token budgets still shift.

<figure><img loading="lazy" src="{{ '/assets/model-migration/transfer-en.svg' | relative_url }}" alt="Figure 2 · A frozen harness can help other models. AHE v3, Terminal-Bench 2, 89 tasks: seed versus evolved harness, with no target-model re-evolution. The harness was evolved using GPT-5.4 high. Source: [4], Section 4.3."><figcaption><strong>Figure 2 · A frozen harness can help other models.</strong> AHE v3, Terminal-Bench 2, 89 tasks: seed versus evolved harness, with no target-model re-evolution. The harness was evolved using GPT-5.4 high. Source: [4], Section 4.3.</figcaption></figure>

In AHE v3, freezing a harness evolved on GPT-5.4 high still improved other model families by 5.1 to 10.1 percentage points.[4](#ref-4-en) At the same time, its ablations found that transplanting the system prompt alone can actually hurt performance, and configurations tuned at one reasoning effort do not automatically fit another timeout budget.

Looking at target-specific synthesis rather than direct harness copying, *AI4AI at Test-Time* had stronger builder models construct scaffolds for designated target models. Even with positive aggregate averages, stronger targets regressed in 9 out of 20 matched builder-by-benchmark theory-of-mind comparisons.[5](#ref-5-en) Adding extra structure can get in the way when the target model already handles a step smoothly on its own.

The practical line to draw is between **durable task knowledge** and **model-specific compensation**. "Never refund the same order twice" is part of the domain regardless of which LLM is on call; "ask the model to double-check its plan three times before calling a tool" is a behavioral patch whose payoff expires whenever the underlying model changes.

<h2 id="diagnosis-en">Separate the replacement effect from the adaptation opportunity</h2>

Suppose harness H<sub>A</sub> was tuned on model A, and H<sub>B</sub> was tuned on model B. Testing both harnesses against both models on the same held-out workload gives a simple 2x2 table where the off-diagonal cells carry most of the signal.

<figure><img loading="lazy" src="{{ '/assets/model-migration/matrix-en.svg' | relative_url }}" alt="Figure 3 · A crossed evaluation separates two decisions. Hypothetical success rates, not experimental results. Replacing A with B under H_A loses 20 points; adapting B to H_B gains 25 points. A positive interaction contrasts relative fit, not an intrinsic model ability."><figcaption><strong>Figure 3 · A crossed evaluation separates two decisions.</strong> Hypothetical success rates, not experimental results. Replacing A with B under H_A loses 20 points; adapting B to H_B gains 25 points. A positive interaction contrasts relative fit, not an intrinsic model ability.</figcaption></figure>

<div class="bm-equation">Replacement = J(B,H<sub>A</sub>) − J(A,H<sub>A</sub>)<br>Adaptation = J(B,H<sub>B</sub>) − J(B,H<sub>A</sub>)<br>Interaction = [J(B,H<sub>B</sub>) − J(B,H<sub>A</sub>)] − [J(A,H<sub>B</sub>) − J(A,H<sub>A</sub>)]</div>

In the example matrix above, the +35-point interaction says that switching from H<sub>A</sub> to H<sub>B</sub> helps B far more than A under those test conditions. It does not claim to isolate some context-free "true intelligence" of either model, nor does it guarantee H<sub>B</sub> is the best possible harness for B rather than just the best configuration found within a finite search budget.

Both columns of that table matter for engineering decisions, because they answer different questions. Evaluating under fixed H<sub>A</sub> tells you what breaks if you swap the endpoint tomorrow afternoon; evaluating after tuning H<sub>B</sub> tells you where the replacement settles once it gets fair engineering investment. Reporting only one of the two makes it far too easy to dismiss a promising cheaper model or overestimate how plug-and-play a migration will be.

Within each comparison, task instances, permissions, scorers, environment resets, and resource limits all have to match. Equal-dollar and equal-latency budgets should also stay separate from equal-token or equal-turn caps, since tokenizers count differently and one turn of batched tool calls does far more work than a single-step turn.

Resource accounting is not nitpicking. Anthropic documented a six-point swing on Terminal-Bench 2.0 between strict and uncapped execution resources while holding the Claude model, harness, and tasks completely fixed.[6](#ref-6-en) Infrastructure limits routinely disguise themselves as model quality regressions.

<h2 id="architecture-en">Decouple around contracts you can actually enforce</h2>

A thin provider wrapper solves transport compatibility: matching JSON shapes, streaming chunks, and error codes. Behavioral portability needs a stronger boundary between what the task requires and how a particular model gets there.

A clean way to split the stack is into three layers: durable application state and invariants at the core, an execution layer that mediates side effects and writes audit logs, and a versioned model adapter that handles message formatting, tool descriptions, context packing, and sampling settings.

<figure><img loading="lazy" src="{{ '/assets/model-migration/architecture-en.svg' | relative_url }}" alt="Figure 4 · Separate stable task requirements from replaceable execution choices. Proposed architecture. The adapter may change how a request is expressed; it may not silently weaken permissions, success criteria, or required checks."><figcaption><strong>Figure 4 · Separate stable task requirements from replaceable execution choices.</strong> Proposed architecture. The adapter may change how a request is expressed; it may not silently weaken permissions, success criteria, or required checks.</figcaption></figure>

Take a customer-support agent tasked with issuing a refund once for an eligible order, logging the transaction, and notifying the user only after confirmation. Let the model propose the refund, while the tool layer enforces eligibility against the source database, attaches an idempotency key, and persists the transaction ID. If an API call times out, the controller checks ledger state before allowing a retry, and task completion depends on committed database state rather than the model announcing "Done."

Deterministic guardrails cleanly eliminate whole classes of operational bugs when wired right, though they still cannot tell you whether the model misread an ambiguous ticket, cited weak evidence, or wrote an unhelpful reply. Code locks down the formal boundary; semantic competence still has to be measured empirically.

<div class="bm-table bm-table-wide" role="region" aria-label="Comparison" tabindex="0" markdown="1">

| Keep stable | Allow model-specific adaptation | Check at the boundary |
|---|---|---|
| Business predicates and permissions | Wording, examples, tool descriptions | Equivalent permitted actions and success conditions |
| Authoritative facts and event history | Context windows, summaries, retrieval order | Provenance, unresolved obligations, reconstruction accuracy |
| Side-effect semantics | Serial or parallel scheduling where dependencies permit | Idempotency, ordering, committed-state confirmation |
| Required delivery quality | Reasoning effort, retry and escalation thresholds | Held-out quality, tail latency, total cost |
| Evaluation contract | Model invocation and protocol conversion | No leakage of answers; stable grading criteria |

</div>

Passing schema validation is only half the check: a parser catches a missing `order_id`, yet it cannot catch a valid-looking ID that belongs to the wrong customer, and a summary can pass JSON typing while dropping a key exception. Validation has to connect back to domain facts and execution evidence rather than stopping at syntax.

Anthropic's Managed Agents architecture moves in this direction by decoupling the model-and-harness "brain" from execution tools and an external session event log.[7](#ref-7-en) Lifecycle decoupling lets a harness crash or restart from durable state, though by itself it does not guarantee two different models will behave identically given that state.

Mid-session model handoffs follow the exact same rule. Pass along the active goal, verified facts, completed and pending tool calls, unresolved obligations, and evidence pointers, treating natural-language summaries purely as convenience views. Letting model B reconstruct a structured state machine is much safer than asking it to interpret model A's free-form diary.

<h2 id="adaptation-en">Optimize for the executor you will actually deploy</h2>

Frameworks like DSPy separate a declarative task pipeline from the prompts and few-shot demonstrations compiled to maximize an evaluation metric.[8](#ref-8-en) Multi-stage optimizers such as MIPRO jointly tune instructions and examples across stages.[9](#ref-9-en) The underlying discipline translates nicely to migrations: keep the logical pipeline stable, then recompile the adapter around the model actually serving traffic.

Whenever migrating from A to B, evaluate three variants side by side: a plain neutral baseline, the frozen A-tuned harness, and a B-adapted version with an explicit tuning budget. Recording the tuning budget keeps comparisons honest, because otherwise a fancy migration pipeline only looks great next to an untuned competitor.

Strong frontier models can still help as proposers that draft candidate prompts, examples, or tool docstrings, provided candidate selection runs on B's own validation outcomes and gets verified on held-out task families (with proposer cost included in the tally). Selecting winners on A and running only the finalist on B evaluates zero-shot transfer, not adaptation.

Every architecture also hits a capability floor eventually. No amount of prompt compilation or schema renaming will supply missing vision tokens, missing tool permissions, or reliable recall across an overstuffed context window. Sometimes B needs task decomposition, stricter retrieval, or escalation to a larger tier; if those fail the quality-cost bar, the honest decision is not to deploy B on that slice.

Going the other direction, upgrading to a stronger model is a chance to delete scaffolding rather than pile more on. Test stripping away repeated reminders, forced chain-of-thought stages, and defensive retries. Baselines like Agentless's straightforward localization–repair–validation pipeline are a helpful reminder to check how much autonomous orchestration a task genuinely needs.[10](#ref-10-en)

<h2 id="economics-en">The cheapest model is not necessarily the cheapest system</h2>

Sticker price per token rarely matches total system cost. A smaller, cheaper model often emits extra tool loops, requires heavier validation checks, triggers more escalations, and leaves more cleanup for humans. Unit economics should track cost per *valid* completion together with total spend and failure rate, because cheap successes on easy queries can hide expensive failures on hard ones.

To put numbers on that trade-off, imagine a strong model costs 8 normalized units per request, a cheap route costs 1, verification adds 0.2, and a fraction `f` of failed checks falls back to the strong route (costing another 8). These are toy normalized units rather than live API tariffs:

<div class="bm-equation">C<sub>hybrid</sub> = 1 + 0.2 + 8f &nbsp;&nbsp; C<sub>hybrid</sub> &lt; 8 ⇔ f &lt; 0.85</div>

<div class="bm-table bm-table-wide" role="region" aria-label="Comparison" tabindex="0" markdown="1">

| Fallback fraction f | Expected hybrid cost | Share of the direct strong-route cost |
|---|---|---|
| 10% | 2.0 | 25% |
| 50% | 5.2 | 65% |
| 85% | 8.0 | 100% |
| 100% | 9.2 | 115% |

</div>

Break-even math only holds if the verifier actually catches bad answers. A sloppy checker pushes fallback `f` down on paper by shipping silent errors to users. Any hybrid router needs measurements of false accepts, needless escalations, tail latency added by sequential fallback, and whether the fallback model receives clean state instead of half-corrupted assumptions from the first attempt.

One-time migration effort matters too. With engineering cost `K` and verified unit savings `Δc > 0`, `K / Δc` requests is only a rough payback horizon while traffic stays steady. If the target model is deprecated before traffic reaches that break-even volume, the migration ends up losing money despite lower per-token pricing.

<h2 id="migration-en">Migrate a versioned system, not just a model name</h2>

Instead of changing a single `model=` config string, treat migration as promoting a versioned release bundle: pinned model snapshot ID (where vendors expose revisions), prompt and adapter versions, tool schemas, memory format, budget caps, routing rules, and evaluator versions. Pinning cannot freeze upstream SaaS behavior indefinitely, yet it gives debugging teams a reproducible baseline when something shifts.

Validating that release works best as a funnel, catching cheap protocol bugs before paying for full closed-loop runs:

<div class="bm-table bm-table-wide" role="region" aria-label="Comparison" tabindex="0" markdown="1">

| Stage | Main question | Evidence to retain |
|---|---|---|
| Interface checks | Can the system exchange valid requests, calls, results, and errors? | Parsing failures, unsupported semantics, lost fields |
| Controlled replay | Where do local decisions first diverge? | Identical contexts, action validity, matched perturbations |
| Closed-loop paired runs | Does the replacement complete the same work? | Reset tasks, repeated trials, outcome transitions, side effects |
| Held-out adaptation test | Did tuning repair the regression beyond development examples? | Task-family separation, frozen configurations, tuning cost |
| Shadow and limited rollout | Do offline results survive real traffic? | Representative slices, latency tails, escalation, external-state checks |
| Rollback rehearsal | Can the previous system resume safely? | Compatible state, versioned memories, reconciliation of committed actions |

</div>

Aggregate accuracy alone misses what moved underneath. If the old release solved 80 of 100 tasks and the new one solves 80 as well, that identical headline score can mask 10 old failures repaired alongside 10 previously working capabilities broken. Tracking paired pass/fail flips across multiple trials matters far more than comparing group averages from a single run.

Benchmarks like τ-bench highlight this variance directly through `pass^k`, measuring whether an agent succeeds consistently across `k` independent trials rather than getting lucky once.[11](#ref-11-en) Migration checks benefit from reporting both task-level regressions and multi-trial consistency, while separating genuine model mistakes from flaky tool infrastructure.

Two operational traps also show up around shadow traffic and rollbacks. Shadow execution has to isolate writes completely, since letting two refund agents mutate the same production order creates chaos rather than an A/B test. Similarly, reverting an API config string does not un-send an email or reverse a bank transfer; rollback plans need state reconciliation and compensating actions built in.

Whatever acceptance bar teams choose (max regression per critical slice, zero tolerance on forbidden writes, ceiling on p95 cost and latency), lock it down *before* inspecting target test scores so edge-case failures do not get explained away inside a small average gain.

<h2 id="research-en">What would make this a substantive research contribution?</h2>

Once basic API translation is solved, the interesting technical territory is everything left over: which parts of a tuned harness genuinely generalize, which components stay brittle across model families, how few target-model runs it takes to recover quality, and whether cheap probes can warn us before a full migration fails.

<div class="bm-table bm-table-wide" role="region" aria-label="Comparison" tabindex="0" markdown="1">

| Research question | Experiment | A result that would weaken the claim |
|---|---|---|
| Which dependencies are portable? | Cross model families with component swaps: prompts, tools, memory, recovery | Gains depend mainly on one source family or disappear under matched budgets |
| Can compatibility probes predict closed-loop regressions? | Freeze probes, then test unseen model versions and task families | Probe success does not improve prediction beyond a small random end-to-end sample |
| Does explicit state reduce mid-session migration failures? | Switch at matched checkpoints; compare transcript, summary, and structured-state handoffs with matched information | Benefits vanish when information content or handoff cost is controlled |
| Can adaptation be made cheaper? | Compare quality-versus-target-evaluation-cost curves against simple retuning | Similar quality requires comparable or greater total cost |
| Does a universal harness beat a small adapter family? | Compare a shared harness, lightweight adapters, and separately tuned systems | Separate tuning retains a large quality advantage with manageable maintenance |

</div>

Framed this way, architectural debates turn into testable hypotheses. The endgame probably is not a single universal prompt or harness that dominates every model family. A far more realistic outcome is a durable domain-contract layer paired with lightweight, testable adapters that adapt more cheaply and regress less dramatically than either blind swaps or full rewrites.

More broadly, model compatibility belongs alongside unit tests and schema migrations as an empirical property we actively maintain. Code and databases already carry version guarantees; production agents need the same kind of evidence showing that a specific tuple of model, memory policy, tool contract, and budget still honors what users rely on.

When an architecture makes swaps easy to diagnose, inexpensive to retune, and safe to roll back, those properties deserve direct measurement right alongside task accuracy.

<h2 id="sources-en">Sources and figure data</h2>

<p class="bm-note">Revised October 8, 2026. Figure 2 redraws reported data; Figures 1 and 4 are conceptual, and Figure 3 and the cost table are illustrative calculations. <a href="{{ '/assets/model-migration/figure-data.json' | relative_url }}">Data and sources</a>.</p>

<ol class="bm-references"><li id="ref-1-en">Chen, Zaharia, and Zou. <a href="https://arxiv.org/abs/2307.09009">How is ChatGPT’s behavior changing over time?</a>. 2023 preprint; historical version comparison.</li><li id="ref-2-en">Sclar et al. <a href="https://arxiv.org/abs/2310.11324">Quantifying Language Models’ Sensitivity to Spurious Features in Prompt Design</a>. ICLR 2024.</li><li id="ref-3-en">Yang et al. <a href="https://arxiv.org/html/2405.15793v3">SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering</a>. NeurIPS 2024; v3, interface analysis.</li><li id="ref-4-en">Lin et al. <a href="https://arxiv.org/html/2604.25850v3">Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses</a>. 2026 preprint, v3; Section 4.3 and Figure 3.</li><li id="ref-5-en">Qian et al. <a href="https://arxiv.org/html/2608.12307v1">AI4AI at Test-Time: Strong-to-Weak Capability Transfer via Harnesses</a>. 2026 preprint, v1; Section 5.6.</li><li id="ref-6-en">Anthropic. <a href="https://www.anthropic.com/engineering/infrastructure-noise">Quantifying infrastructure noise in agentic coding evals</a>. Engineering report, February 2026.</li><li id="ref-7-en">Anthropic. <a href="https://www.anthropic.com/engineering/managed-agents">Scaling Managed Agents: Decoupling the brain from the hands</a>. Engineering report, April 2026.</li><li id="ref-8-en">Khattab et al. <a href="https://arxiv.org/abs/2310.03714">DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines</a>. ICLR 2024.</li><li id="ref-9-en">Opsahl-Ong et al. <a href="https://arxiv.org/abs/2406.11695">Optimizing Instructions and Demonstrations for Multi-Stage Language Model Programs</a>. EMNLP 2024; MIPRO.</li><li id="ref-10-en">Xia et al. <a href="https://arxiv.org/abs/2407.01489">Agentless: Demystifying LLM-based Software Engineering Agents</a>. 2024 manuscript, v2; three-stage baseline.</li><li id="ref-11-en">Yao et al. <a href="https://arxiv.org/abs/2406.12045">τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains</a>. 2024 benchmark paper; repeated-run reliability.</li></ol>

</div>

<div id="bm-content-zh" class="bm-language-content" lang="zh-CN" hidden markdown="1">

# 模型换了，Agent 为什么变了？

<p class="bm-meta">2026 年 5 月 7 日 · Agent 架构 · 约 15 分钟<span id="busuanzi_container_page_pv" class="bm-meta__views" style="display:none;"> · <strong class="bm-meta__views-num" id="busuanzi_value_page_pv">--</strong> 次阅读</span></p>

<p class="bm-deck">模型替换、版本升级，以及“用强模型调优、换小模型上线”背后的系统耦合问题。</p>

做过几周 Agent 调优的人多半遇过类似一幕：提示词磨平了，工具接入跑顺了，离线评测也稳步过了线。紧接着线上切换底层模型——可能是为了压缩成本换家供应商，可能是旧版本按期退役，也可能是为了压低延迟换到更小的档位。接口依然一路返回 200，系统表现却陡然变了样。

原本一轮就能结束的检索，突然在循环里反复打转；之前会乖乖等工具返回再继续的模型，开始一次并发抛出好几个调用；摘要器顺手漏掉了还没满足的约束条件；更麻烦的是，过去专门用来救场的重试逻辑，到了新模型手里反而把带有副作用的操作重复执行了一遍。出现这些问题，并不需要新模型的“智力”明显退步。

这背后真正值得追问的是：**当我们说一套 Agent 系统已经“调好了”，到底调好了什么？** 收益是沉淀在了系统本身可复用的结构里，还是只是在替某一个特定模型的脾气打补丁，一旦换掉其中一端就原形毕露？

<div class="bm-thesis" markdown="1">

Agent 在线上呈现出的行为，从来不是模型单独决定的，而是模型、外围系统（harness）、环境与预算共同作用的结果。所谓可迁移性，核心在于把真正不可妥协的任务契约固定下来，同时度量并控制重新适配这套组合所需的工程代价。

</div>

<nav class="bm-toc" aria-label="目录" markdown="1">

**阅读路线**

1. [先定义究竟换了什么](#object-zh)
2. [找出系统里的隐含依赖](#coupling-zh)
3. [同时看迁移成功与失败的证据](#evidence-zh)
4. [分开比较直接替换与重新适配](#diagnosis-zh)
5. [围绕可执行的要求解耦](#architecture-zh)
6. [面向生产模型优化](#adaptation-zh)
7. [计算完整成本](#economics-zh)
8. [迁移一个系统版本](#migration-zh)
9. [把可迁移性变成研究对象](#research-zh)

</nav>

<h2 id="object-zh">生产中的行为策略，不只由模型决定</h2>

下文用 *harness* 统称包裹在模型外围的整套执行系统，包括提示词、上下文拼装、记忆读写、工具接口、路由、校验器、重试与停止规则。最终的任务成效，正是由这一整套框架连同负载和资源上限共同决定。

<div class="bm-equation">J(M, H, D, B, E) = E[task utility | model M, harness H, workload D, budget B, environment E]</div>

哪怕外围代码 `H` 一行不改，只要换掉模型 `M`，第一步选出的动作分布就变了。动作一变，环境状态随之改变，下一轮喂回模型的观察也不再相同。换句话说，换模型不只是换掉了做决定的人，连它后面会碰上的局面也一并改写了。

工程上常见的模型替换至少有四种情形，需要分开排查：

<div class="bm-table bm-table-wide" role="region" aria-label="对照表" tabindex="0" markdown="1">

| 变化 | 常见原因 | 需要重新建立的依据 |
|---|---|---|
| 同系列换新版本 | 升级或旧版本退役 | 行为兼容，包括原本稳定的边界情况 |
| 更换模型或服务商 | 成本、延迟、可用性、能力 | 接口语义、任务质量与运行预算 |
| 在 A 上调优，在 B 上生产 | 开发用强模型，执行用便宜模型 | 收益能否在 B 上保留，以及适配成本 |
| 会话中途换模型 | 路由、升级处理、故障回退 | B 是否拿到足够状态，是否理解未完成动作 |

</div>

还要分清两种常被混为一谈的做法：“让强模型 A 替弱模型 B 设计工作流”，和“直接在 A 上跑通调优后原封不动拷给 B”。强模型确实能帮忙写出更好的代码或示例，但最终拍板留哪版方案，信号必须来自 B 自己的执行成绩。设计者是谁，决定不了优化目标是谁。

像 Chen 等人对 2023 年 3 月与 6 月两版 ChatGPT 的经典追踪对比，清楚记录了同一模型家族跨版本在指令遵循与任务表现上的漂移。[1](#ref-1-zh) 这类证据能支撑我们做行为回归测试，但从外部观察黑箱接口，很难判断某次退化究竟源自训练数据配比调整还是奖励信号变化。面对无法拆开的模型权重，唯一抓得住的依据是可观察的行为契约，以及它在哪些场景下失守。

<h2 id="coupling-zh">一个“能用”的系统，藏着哪些依赖？</h2>

显性的依赖一眼就能看出来，比如解析器写死了某个 JSON 字段，或者两家服务商报错格式不兼容。真正棘手的是那些没人写进文档的行为默契：系统暗自指望模型先检索再下结论，在摘要里老实保留例外条款，改代码失败后懂得换思路恢复，或者做完正事就及时收手。

开发过程中的“临时修补”，往往会悄悄把这种默契焊死成硬耦合。比方说旧模型老忘掉一条业务限制，工程师干脆在系统提示和工具说明里反反复复写了三遍。等换上一个极度听话的新模型，它真就老老实实按每条提醒各核对一遍，活生生把预算耗到超时。原本针对老毛病的局部补丁，到新模型身上反倒成了拖累。

<div class="bm-table bm-table-wide" role="region" aria-label="对照表" tabindex="0" markdown="1">

| 依赖 | 换模型后可能出现的变化 | 应在哪一层修复 |
|---|---|---|
| 输出与工具协议 | 字段缺失、停止事件不同、并行调用 | 规范消息、校验 schema，同时保留错误语义 |
| 规划与停止 | 探索更多、提前结束、过度检查 | 明确完成证据，限制执行策略的范围 |
| 上下文与记忆 | 对摘要、工具结果、示例的使用方式变化 | 保存有来源的事实与未完成义务，检验状态重建 |
| 恢复 | 重复失败动作，把业务拒绝当成服务故障 | 区分错误类型，规定哪些操作可安全重试 |
| 预算 | 推理更多、工具循环更长、尾延迟更高 | 联合衡量质量、时间和成本，适配运行档位 |
| 评测 | 新回答风格更讨评分器喜欢，却违反任务要求 | 独立终态检查，审计评分示例 |

</div>

由于 Agent 运行在多轮闭环中，微小差异会随着步数滚雪球般放大。第一步检索关键词哪怕偏了一点，召回的文档就不同，后面的规划、参数填写、累积上下文直到停止时机都会跟着分叉。只盯着单轮首答做测试，几乎一定会漏掉最要命的问题。

<figure><img loading="lazy" src="{{ '/assets/model-migration/loop-zh.svg' | relative_url }}" alt="图 1 · 换模型会改变轨迹分布。概念示意。同一初始请求可能进入不同后续状态；一份已记录轨迹只覆盖其中一条路径。"><figcaption><strong>图 1 · 换模型会改变轨迹分布。</strong>概念示意。同一初始请求可能进入不同后续状态；一份已记录轨迹只覆盖其中一条路径。</figcaption></figure>

这也正好说明了“历史回放”和“闭环实测”各司其职。把同一段录制好的历史上下文喂给两个模型，非常适合排查协议兼容或局部决策从哪一步开始分叉；但回放看不到新模型自己在真实交互里会走去哪里。诊断问题靠受控回放，评估端到端成败必须跑完整闭环。

<h2 id="evidence-zh">迁移可以成功，但不同部分并不一样</h2>

现有文献在跨模型迁移这件事上，同时给出过反例和正例。先看让人头疼的一面：Sclar 等人证明，哪怕只是调整空格、标点等完全不改语义的提示词格式，模型表现也能剧烈波动，而且一套格式在不同模型之间的优劣相关性很弱。[2](#ref-2-zh) 拿同一份提示词去比两个模型，本身就未必是一场公平竞赛。

但好的接口与结构确实能跨模型站住脚。SWE-agent 最初围绕 GPT-4 Turbo 打磨出一套 Agent–计算机交互接口（ACI），后来直接套用到 Claude 3 Opus 上依然奏效；在 SWE-bench Lite 上，这套接口比纯 shell 基线高出 10.7 个百分点。[3](#ref-3-zh) 哪怕最佳措辞和推理预算得跟着换，顺手的文件浏览、编辑保护和终端反馈机制是可以复用的。

<figure><img loading="lazy" src="{{ '/assets/model-migration/transfer-zh.svg' | relative_url }}" alt="图 2 · 冻结后的外围系统可以帮助其他模型。AHE v3，Terminal-Bench 2，89 个任务：比较初始与演化后的 harness，没有针对目标模型重新演化。源配置为 GPT-5.4 high。来源：[4]，第 4.3 节。"><figcaption><strong>图 2 · 冻结后的外围系统可以帮助其他模型。</strong>AHE v3，Terminal-Bench 2，89 个任务：比较初始与演化后的 harness，没有针对目标模型重新演化。源配置为 GPT-5.4 high。来源：[4]，第 4.3 节。</figcaption></figure>

在 AHE v3 的实验里，一套基于 GPT-5.4 high 演化出并冻结下来的 harness，迁移到其他模型家族上依然带来了 5.1 到 10.1 个百分点的提升。[4](#ref-4-zh) 但同篇工作的组件拆解也提醒了一件事：如果只把系统提示词单独搬过去，效果反而可能倒退；针对某个推理档位调好的超时与步数配置，换个档位同样会水土不服。

如果换成由强模型专门给指定弱模型“量身定制”呢？*AI4AI at Test-Time* 测了这种场景：强构建者为目标模型设计 harness 后，虽然整体平均分是涨的，但在心智理论相关的 20 组“构建者 × benchmark”配对里，更强的目标模型居然在 9 组上出现了退步。[5](#ref-5-zh) 原本已经能独立做好的能力，外面硬套一层多余脚手架反而会帮倒忙。

工程上最实用的一条划分线，就是区分**可复用的任务常识**与**针对特定模型的拐杖**。“同一笔订单绝不能重复退款”属于业务边界，换哪个模型都成立；而“在工具调用前强制让模型反思三遍”只是一种行为干预，换个模型就得重新拿数据验明正身。

<h2 id="diagnosis-zh">分开比较直接替换的影响与重新适配的空间</h2>

设想手头有两套配置：H<sub>A</sub> 围绕模型 A 调优，H<sub>B</sub> 围绕模型 B 调优。只要在相同的留出任务集上交叉跑出这四个组合，交叉项往往比单一对角线更能说明问题。

<figure><img loading="lazy" src="{{ '/assets/model-migration/matrix-zh.svg' | relative_url }}" alt="图 3 · 交叉评测分开两种决策。假设成功率，非实验结果。在 H_A 下把 A 换为 B，下降 20 个百分点；将 B 适配到 H_B，提高 25 个百分点。交互项比较相对适配程度，而非模型内在能力。"><figcaption><strong>图 3 · 交叉评测分开两种决策。</strong>假设成功率，非实验结果。在 H_A 下把 A 换为 B，下降 20 个百分点；将 B 适配到 H_B，提高 25 个百分点。交互项比较相对适配程度，而非模型内在能力。</figcaption></figure>

<div class="bm-equation">Replacement = J(B,H<sub>A</sub>) − J(A,H<sub>A</sub>)<br>Adaptation = J(B,H<sub>B</sub>) − J(B,H<sub>A</sub>)<br>Interaction = [J(B,H<sub>B</sub>) − J(B,H<sub>A</sub>)] − [J(A,H<sub>B</sub>) − J(A,H<sub>A</sub>)]</div>

按图里的假设数字，+35 个百分点的交互项说明：在当前评测条件下，把外围配置从 H<sub>A</sub> 换成 H<sub>B</sub> 对 B 的帮助明显大于对 A 的帮助。但它依然分离不出所谓脱离上下文的“纯模型实力”，也别把有限搜索预算下找到的 H<sub>B</sub> 当成理论最优解。

矩阵里这两列对应着完全不同的决策问题。固定 H<sub>A</sub> 直接换模型，测的是“今天下午切流量会掉多少”；给 B 匹配同等调优预算再看 H<sub>B</sub>，测的则是“好好适配之后能拿回多少”。只看其中一列，要么会冤枉一个本来很能打的平替模型，要么会低估切换模型所需的改造工时。

每组对照里，任务样本、工具权限、评分脚本、环境重置和资源规则都必须对齐。还要把“等额开销 / 等额延迟”的比较，与“等额 token / 等额轮次”分开算：不同分词器的 token 长度根本不对等，一轮里并发发出五次工具调用和单步只调一次工具，消耗的资源也完全不是一回事。

抠这些资源细节绝非小题大做。Anthropic 曾公开报告，哪怕 Claude 模型、harness 和题目集一个字不改，仅把运行环境从严格资源上限放开到不设限，Terminal-Bench 2.0 的成功率就差出了 6 个百分点。[6](#ref-6-zh) 很多看似模型退化的问题，追到底其实是基础设施限制变了。

<h2 id="architecture-zh">围绕真正可执行的要求解耦</h2>

套一层统一 API 包装器，解决的是请求格式、流式返回和错误码翻译；真要让行为可迁移，必须在“任务铁律”和“模型凑效的小技巧”之间划出清晰边界。

比较稳妥的做法是拆成三层：最里面是持久的业务状态与核心约束；中间是负责拦截校验并记录审计日志的执行层；最外层才是可版本化替换的模型适配层，用来调整消息组装、工具描述、上下文裁剪和推理参数。

<figure><img loading="lazy" src="{{ '/assets/model-migration/architecture-zh.svg' | relative_url }}" alt="图 4 · 分开稳定的任务要求与可替换的执行选择。建议架构。适配层可以改变请求表达方式，但不能悄悄放宽权限、成功标准或必要检查。"><figcaption><strong>图 4 · 分开稳定的任务要求与可替换的执行选择。</strong>建议架构。适配层可以改变请求表达方式，但不能悄悄放宽权限、成功标准或必要检查。</figcaption></figure>

拿客服退款举个例子：要求是对符合条件的订单只退一次款，落账，确认到账后再通知用户。模型只负责提出退款意图，工具层则依据权威订单库核验资格、附上幂等键并写下流水号；一旦请求超时，控制器必须先反查流水状态，再决定要不要重发。任务算不算完成，只看数据库里的持久化结果，不看模型嘴上有没有说“已完成”。

当然，写死的确定性代码只能兜住那些能形式化的操作边界（比如越权写库、重复扣款），它替代不了语义判断。模型到底有没有读懂含糊的用户意图、有没有挑中关键证据、回复写得是否得体，依然得靠实打实的评测去量。

<div class="bm-table bm-table-wide" role="region" aria-label="对照表" tabindex="0" markdown="1">

| 保持稳定 | 允许按模型适配 | 在边界检查 |
|---|---|---|
| 业务条件与权限 | 措辞、示例、工具描述 | 允许动作与成功条件等价 |
| 权威事实与事件历史 | 上下文窗口、摘要、检索顺序 | 来源、未完成义务、重建准确性 |
| 副作用语义 | 在依赖允许时串行或并行 | 幂等性、顺序、持久状态确认 |
| 必须达到的交付质量 | 推理档位、重试与升级阈值 | 留出质量、尾延迟、总成本 |
| 评测要求 | 模型调用与协议转换 | 答案不泄漏，评分标准稳定 |

</div>

schema 校验通过也只能说明格式没错：解析器能拦下缺少 `order_id` 的请求，却发现不了字段里的合法编号指错了另一位客户；摘要器同样能输出结构完美的 JSON，同时悄无声息漏掉一条致命例外。边界校验必须挂钩真实业务事实和执行证据，不能止步于语法合法。

Anthropic 的 Managed Agents 架构已经把这套分层做到了生命周期层面：把“模型加 harness”的大脑、执行工具以及持久会话事件日志彻底拆开。[7](#ref-7-zh) 这样哪怕外围框架崩溃重启，也能靠外部事件流续上；不过它解决的是断点续传，本身还不等于不同模型读到同一份日志后会作出完全等价的决定。

会话中途需要把请求切给另一个模型时，同理也得靠显式状态交接：当前目标、已核实的事实、已完成和挂起中的动作、尚未兑现的承诺以及引用证据，全都结构化地传过去。自然语言摘要只适合当作人类旁看的衍生视图，让两个模型都能重建同一套可执行状态，远比让新模型硬啃旧模型留下的流水账可靠得多。

<h2 id="adaptation-zh">围绕真正上线的执行器优化</h2>

像 DSPy 这类框架，核心思路正是把声明式的任务流程骨架，与面向指标编译优化出来的提示词和示例拆开。[8](#ref-8-zh) MIPRO 则更进一步，在多阶段程序里联合搜索各步的指令与演示样本。[9](#ref-9-zh) 搬到模型迁移上，道理一脉相承：保住程序想完成的状态转换，再去围绕真正上线的模型重编适配层。

做 A 到 B 迁移评测时，至少该把三个版本摆在一起：一个干净的中性基线、从 A 原封不动冻结搬过来的系统，以及给 B 配了明确预算调优后的版本。把调优预算记明尤为重要，否则很多花哨的迁移方法之所以看着惊艳，往往只是因为对照基线压根没被调优过。

至于能不能借强模型充当“教练”生成候选提示、示例或工具注释，答案是可以，但前提是筛选胜出者的裁判必须是 B 自己在开发集上的实测成绩，外加未见任务族的留出验证（同时别忘了把强模型命题的开销也记进总账）。如果拿 A 的分数挑完冠军再甩给 B 跑一次，那测的是“源模型调优后的迁移率”，不是为 B 做的适配。

更现实的情况是能力下限摆在那里。光改参数名和提示词措辞，变不出缺失的视觉输入，也补不回本就没有的工具权限或过长的上下文记忆。有时 B 需要把大任务拆细、配强检索或加上额外校验和升级兜底；要是加上这些还过不了业务的质量和成本红线，趁早放弃把这个模型用到这类场景才算清醒。

反过来看，从弱模型升到更强的模型，反而经常是做减法的好时机。不妨专门测一测删掉冗余提醒、取消强制分步规划或者精简恢复循环之后的效果。像 Agentless 用“定位—修复—补丁验证”三条固定阶段就能打下扎实基线，很值得拿来反问一句：我们手里的任务究竟需不需要那么厚重的自主编排？[10](#ref-10-zh)

<h2 id="economics-zh">最便宜的模型，未必形成最便宜的系统</h2>

单看 API 账单上的百万 token 单价很容易算错账。更便宜的模型一旦在循环里多绕几圈、触发更多二次校验、频繁升级转交给大模型甚至留下一堆人工善后，整体花销反倒可能涨上去。核算收益时，得把“单次有效完成的平均成本”和总支出、未满足率摆在一起看——少数简单题跑得又快又省，极易掩盖长尾失败拖垮的整体账单。

算一笔简单的账就清楚了。假设强模型直通路径每次请求成本是 8 个归一化单位，便宜模型是 1，加一道校验花 0.2，且校验不通过时有比例 `f` 的流量回退给强模型再花 8（这里只做归一化推演，不对应具体云厂商报价）：

<div class="bm-equation">C<sub>hybrid</sub> = 1 + 0.2 + 8f &nbsp;&nbsp; C<sub>hybrid</sub> &lt; 8 ⇔ f &lt; 0.85</div>

<div class="bm-table bm-table-wide" role="region" aria-label="对照表" tabindex="0" markdown="1">

| 回退比例 f | 混合路径期望成本 | 占直接强模型路径成本 |
|---|---|---|
| 10% | 2.0 | 25% |
| 50% | 5.2 | 65% |
| 85% | 8.0 | 100% |
| 100% | 9.2 | 115% |

</div>

这种盈亏平衡算式有个大前提：那道 0.2 的校验真的抓得住错。校验器要是宽进严出漏掉了坏结果，表面上看回退比例 `f` 压得很低，实则是在靠牺牲交付质量省钱。真要跑混合路由，误放行率、无效升级率、串行回退拖慢的尾延迟，以及回退时强模型有没有拿到干净状态（而不是继承了前一步的错误假设），一项都不能漏测。

一次性的迁移人工和算力成本 `K` 同样要摊进去算。哪怕每次请求能稳定省下正的单位成本 `Δc`，`K / Δc` 也只是在工作负载保持稳定的前提下的回本门槛；要是还没跑到这个请求量，目标模型就已经下线退役了，这趟迁移在账面上其实一直没回本。

<h2 id="migration-zh">迁移一个系统版本，而不只是改模型名</h2>

别把迁移当成改一行 `model_name` 配置，而要当作发布一个完整版本：把模型确切版本号（服务商提供修订号时务必锁死）、提示和适配层版本、工具 schema、记忆格式、资源上限、路由规则和评测器版本绑在一起记录。锁版本虽然拦不住外部服务暗中变动，却能保证出问题时手头有一份可对照的基线。

验证这个发布包时，最省事的做法是按漏斗分层推进，先用低成本测试拦住接口毛病，再跑完整的闭环对比：

<div class="bm-table bm-table-wide" role="region" aria-label="对照表" tabindex="0" markdown="1">

| 阶段 | 主要问题 | 保留的证据 |
|---|---|---|
| 接口检查 | 请求、调用、结果和错误能否有效交换？ | 解析失败、不支持的语义、丢失字段 |
| 受控回放 | 局部决策从哪里开始分化？ | 相同上下文、动作有效性、匹配扰动 |
| 闭环配对运行 | 替换后能否完成相同工作？ | 重置任务、重复试验、结果转移、副作用 |
| 留出适配测试 | 调优能否修复开发样本之外的退化？ | 任务家族隔离、冻结配置、调优成本 |
| 影子与有限流量发布 | 离线结果能否在真实流量成立？ | 有代表性的分组、尾延迟、升级处理、外部状态检查 |
| 回滚演练 | 旧系统能否安全恢复？ | 兼容状态、版本化记忆、已提交动作的核对 |

</div>

光盯着平均成功率经常会看走眼。假如旧版本在 100 个任务里过 80 个，新版本也过 80 个，表面上看毫无波动，底层却可能是修好了 10 个老错题、同时搞坏了 10 个原本稳过的核心场景。比起单次跑出的均分，把每一题反复跑几轮，看成败翻转和波动范围才有参考价值。

τ-bench 用 `pass^k`（连续 `k` 次独立试验全部通过的概率）把这种稳定性挑明在了台面上。[11](#ref-11-zh) 迁移评测既要盯着单任务的退化清单，也要量多次重复的一致性，顺便把模型本身犯的错与工具超时、沙箱故障之类基础设施噪声剥离开。

上线前的两个工程坑尤其值得多提一句：做影子流量对比时必须彻底隔离写操作，让两个退款 Agent 并发改同一笔线上订单只会把数据搅乱；另外，回滚模型配置并不会把已经退出去的钱或发出去的消息收回来，状态核对与补偿逻辑必须预先写进回滚预案。

至于最后过不过线（关键切片允许掉多少分、绝不允许哪些越权动作、成本和尾延迟卡在哪），一定要在看目标模型成绩**之前**拍板，免得看到平均分涨了两点，就忍不住替那些扎眼的尾部回归找借口。

<h2 id="research-zh">怎样把它变成实质性的研究问题？</h2>

如果把接口兼容看作工程底座，那它上面才真正站着有趣的研究问题：外围 harness 的调优成果到底能跨模型留存多少？哪些模块必须按模型重调？最少需要多少条目标模型的反馈就能补回退化？我们又能不能在全量上线之前，先用低成本探针预测迁移会不会翻车？

<div class="bm-table bm-table-wide" role="region" aria-label="对照表" tabindex="0" markdown="1">

| 研究问题 | 实验 | 会削弱主张的结果 |
|---|---|---|
| 哪些依赖可以迁移？ | 交叉模型家族，分别替换提示、工具、记忆、恢复组件 | 收益主要依赖单一源家族，或在匹配预算后消失 |
| 兼容性探测能预测闭环退化吗？ | 冻结探测规则，测试未见版本与任务家族 | 不比少量随机端到端样本更能预测退化 |
| 显式状态能减少会话中途迁移失败吗？ | 在匹配检查点切换，比较完整轨迹、摘要、结构化状态；匹配信息 | 控制信息量或交接成本后收益消失 |
| 能否降低适配成本？ | 比较质量随目标模型评测成本变化的曲线，对照简单重调 | 达到相似质量需要相当或更高总成本 |
| 通用 harness 是否优于小型适配器族？ | 比较共享 harness、轻量适配器、各自独立调优系统 | 独立调优保持明显质量优势，且维护成本可接受 |

</div>

把架构争论拆成这几张对照表后，很多模糊的感觉就变成了能被实验推翻的假设。我们追寻的终点未必是一套放之四海而皆准的“万能 harness”；更现实的答案，或许是一个坚固的稳定任务层，配上几套经过验证、轻量且可替换的模型适配层，既不用忍受硬切模型的退化，也不至于每次换模型都推倒重来。

往更深一层看，把“模型兼容性”当成一种需要像单元测试和数据库迁移一样长期维护的经验事实，可能是更关键的观念转变。代码和 schema 早就有严格的版本契约了；到 Agent 这里，我们也同样需要一组可查的证据，证明手上这套模型、记忆策略、工具接口与预算组合，依然稳稳兑现了任务约定。

一套好的系统架构，应当让换模型时更容易定位问题、更省钱地完成适配、也更安全地随时回滚。这些收益不该只停留在架构图里，而应当像任务成功率一样被直接检验。

<h2 id="sources-zh">资料与图表数据</h2>

<p class="bm-note">2026 年 10 月 8 日修订。图 2 重绘公开数据；图 1、4 为概念图；图 3 与成本表为示意计算。<a href="{{ '/assets/model-migration/figure-data.json' | relative_url }}">数据与来源</a>。</p>

<ol class="bm-references"><li id="ref-1-zh">Chen, Zaharia, and Zou. <a href="https://arxiv.org/abs/2307.09009">How is ChatGPT’s behavior changing over time?</a>. 2023 预印本；历史版本比较。</li><li id="ref-2-zh">Sclar et al. <a href="https://arxiv.org/abs/2310.11324">Quantifying Language Models’ Sensitivity to Spurious Features in Prompt Design</a>. ICLR 2024。</li><li id="ref-3-zh">Yang et al. <a href="https://arxiv.org/html/2405.15793v3">SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering</a>. NeurIPS 2024；v3，接口分析。</li><li id="ref-4-zh">Lin et al. <a href="https://arxiv.org/html/2604.25850v3">Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses</a>. 2026 预印本 v3；第 4.3 节与图 3。</li><li id="ref-5-zh">Qian et al. <a href="https://arxiv.org/html/2608.12307v1">AI4AI at Test-Time: Strong-to-Weak Capability Transfer via Harnesses</a>. 2026 预印本 v1；第 5.6 节。</li><li id="ref-6-zh">Anthropic. <a href="https://www.anthropic.com/engineering/infrastructure-noise">Quantifying infrastructure noise in agentic coding evals</a>. 工程报告，2026 年 2 月。</li><li id="ref-7-zh">Anthropic. <a href="https://www.anthropic.com/engineering/managed-agents">Scaling Managed Agents: Decoupling the brain from the hands</a>. 工程报告，2026 年 4 月。</li><li id="ref-8-zh">Khattab et al. <a href="https://arxiv.org/abs/2310.03714">DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines</a>. ICLR 2024。</li><li id="ref-9-zh">Opsahl-Ong et al. <a href="https://arxiv.org/abs/2406.11695">Optimizing Instructions and Demonstrations for Multi-Stage Language Model Programs</a>. EMNLP 2024；MIPRO。</li><li id="ref-10-zh">Xia et al. <a href="https://arxiv.org/abs/2407.01489">Agentless: Demystifying LLM-based Software Engineering Agents</a>. 2024 稿件 v2；三阶段基线。</li><li id="ref-11-zh">Yao et al. <a href="https://arxiv.org/abs/2406.12045">τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains</a>. 2024 benchmark 论文；重复运行可靠性。</li></ol>

</div>
</div>
<script src="{{ '/assets/model-migration/article.js' | relative_url }}" defer></script>
