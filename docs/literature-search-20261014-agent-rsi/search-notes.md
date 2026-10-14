# Agent RSI literature audit — 2026-10-14

Scope: LLM-based agents, persistent adaptation, recursive improvement, and adjacent multi-objective optimization. 33 retained sources after the reference follow-up: 30 method/system sources (including one official developer article), two surveys, one diagnostic case study. Years refer to the initial manuscript where applicable; source versions were inspected through 2026-10-14. Inclusion is thematic, not a claim of exhaustive systematic review.

## Search and screening

Queries covered recursive self-improvement agents; self-evolving agents; prompt/context/skill/workflow evolution; Pareto agent evolution; multi-objective agent skills; model adaptation and generated curricula. Primary-source search was followed by arXiv HTML/PDF method inspection and official author/proceedings checks. Article statements are grounded in the mutable object, feedback, selection objective and retained artifact rather than title terminology.

Excluded: MDPI/preprints.org under the literature-search skill policy; the unrelated commercial SkillMOO website; non-LLM evolutionary optimizer papers; Agent0 recommendation-system paper (different work); snippet-only candidates not advanced to the article. Secondary reports were discovery aids only.

## Version and interpretation checks

- SkillMOO: current full text reports 16 software-engineering tasks; an older abstract refers to three. The article avoids mixing them. Runtime is not counted as a third objective.
- Dream-RSI: current text and older abstract differ in task/domain count; article focuses on the verified method and avoids headline speedup comparisons.
- DGM: 20→50% is the selected 200-task SWE-bench Verified evaluation, not all 500 tasks. Polyglot subset and full-set results are different.
- AIDE²: private data hidden from the inner agent still supplies selection feedback to the outer loop. External benchmarks provide a different level of evidence. Outer-improver superiority remains inconclusive.
- MOAE: only the public manuscript is used. Its evolved object is the per-query compact execution policy, with the model/tools/architecture frozen.
- GEPA: the Pareto selection preserves complementary strengths across instances; it is not by itself a safety-cost-quality frontier.
- Newer manuscripts are labeled by year, without unverified venue/acceptance claims.

## Evidence and scoring

papers.csv is the structured extraction source. Each record has a depth and locator. Scores are provisional triage judgments only, not paper rankings. Abstract-only entries are left unscored. The blog does not publish these scores. No experiments were reproduced. All figures in the article are original explanatory diagrams; the numerical evidence table cites source-specific protocols.

## User-supplied reference follow-up

Five primary works were verified and added: Meta-Harness, HELIX, pre-commit gating/VaG, coalition-aware skill reliability, and MoFlow. Their role is to support trace diagnosis, learning-data value, skill interactions and preference-aware search. The supplied essays remain discovery material, not sources for experimental claims.

Not adopted: Reflexion characterized as lacking retained state; universal claims that scalar optimization causes bloat or that Pareto methods guarantee the whole global frontier; unsupported numerical bloat examples; all co-evolution stages described as empirically completed; a requirement that every candidate improve monotonically on every check. The argument retains fixed-utility and constrained optimization as legitimate choices.
