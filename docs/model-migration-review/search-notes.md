# Research notes · 2026-10-08

Purpose: primary-source support for a bilingual blog about cross-model agent-system portability. No novelty verdict or experimental efficacy claim.

## Search and screening

Public query clusters: agent-computer interface ablations; ChatGPT behavior across snapshots; cross-model harness transfer; prompt-format sensitivity; declarative LM programs; agent infrastructure noise; builder versus target models.

Screened 17 distinct primary candidates: the 11 references used in the article, plus Automated Design of Agentic Systems (2408.08435), AFlow (2410.10762), Gödel Agent (2410.04444), τ²-Bench (2506.07982), GEPA (2507.19457), and Building Effective Agents (Anthropic). These six are adjacent background rather than evidence required by this article. Primary records opened; no claim of full-paper review for every screened candidate.

Primary papers, official proceedings, and official engineering reports only. MDPI excluded by skill policy; search-engine comments and aggregators not used as evidence. Queries used public research terms, not private draft paragraphs.

## Evidence quality

papers.csv scores use the skill 1–5 rubric as provisional prioritization from inspected sections; they are not simulated peer-review verdicts. Abstract-only inspections have narrower coverage. AHE transfer and ablation sections, AI4AI target comparisons, SWE-agent interface sections, τ-bench reliability discussion, and official infrastructure/lifecycle reports received focused reads.

AHE figure uses explicitly pinned v3, not an unspecified latest version; v4 abstract has the same headline transfer range. No fabricated confidence intervals. AI4AI's builder-target experiment is distinguished from direct transfer of an A-tuned harness. No private experimental data used. The crossed matrix and cost table are labeled hypothetical / normalized examples.

## Positioning

Interface engineering already demonstrates transfer; DSPy and MIPRO separate programs from target-specific optimization. AHE and AI4AI make generic claims that scaffolding can transfer insufficient as novelty. The remaining direction pursued in the essay is measurable adaptation cost, matched-information handoff, regression prediction, and model-by-component interaction under fixed task contracts.

Useful carriers: SWE-bench / Terminal-Bench for executable workflows; τ-bench for stateful, repeated user interaction. Their public scores are not deployment guarantees. The essay proposes experiments; it does not claim to have run them.

## Boundaries

No inferred training-data or RLHF explanations for opaque version changes. No universal deterministic-agent guarantee. No universal ranking from a fixed-harness comparison. No publishing or deployment in this task.
