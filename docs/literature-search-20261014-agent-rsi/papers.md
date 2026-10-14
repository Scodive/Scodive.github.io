# Source-by-source extraction



## 1. Reflexion: Language Agents with Verbal Reinforcement Learning (2023)

Source: https://arxiv.org/abs/2303.11366

Read depth: abstract; locator: Abstract

Evolved object: Episodic verbal reflections; reused across trials

Objective: Task success from environment/evaluator feedback

Boundary: Textual feedback is not a parameter update

Provisional insight / completeness / numeric evidence: unscored / unscored / unscored. Not scored: abstract-only, developer article, or taxonomy evidence is insufficient for a method-quality score.



## 2. Voyager: An Open-Ended Embodied Agent with Large Language Models (2023)

Source: https://arxiv.org/abs/2305.16291

Read depth: abstract; locator: Abstract

Evolved object: Executable skill library and automatic curriculum

Objective: Exploration and acquisition of reusable skills

Boundary: Minecraft setting; do not interpret as general autonomous improvement

Provisional insight / completeness / numeric evidence: unscored / unscored / unscored. Not scored: abstract-only, developer article, or taxonomy evidence is insufficient for a method-quality score.



## 3. Promptbreeder: Self-Referential Self-Improvement Via Prompt Evolution (2023)

Source: https://arxiv.org/abs/2309.16797

Read depth: method; locator: Introduction; prompt and mutation-prompt evolution

Evolved object: Task prompts and mutation prompts

Objective: Training-task accuracy

Boundary: Self-reference operates at the prompt level

Provisional insight / completeness / numeric evidence: 4 / 4 / 3. Provisional reading judgment, not independent reproduction: Mutation prompts are themselves evolved; broad method structure is available, but generalization beyond task-score selection needs care.



## 4. STOP: Self-Taught Optimizer: Recursively Self-Improving Code Generation (2023)

Source: https://arxiv.org/abs/2310.02304

Read depth: method; locator: PDF abstract and method overview

Evolved object: Code-improvement program applied to its own code

Objective: Utility of programs produced by the improver

Boundary: Underlying language model remains fixed

Provisional insight / completeness / numeric evidence: 4 / 3 / 3. Provisional reading judgment, not independent reproduction: The improver is applied to itself; code utility gives a concrete test, while the fixed-model and utility boundaries limit the recursive claim.



## 5. Automated Design of Agentic Systems (ADAS) (2024)

Source: https://arxiv.org/abs/2408.08435

Read depth: method; locator: Meta Agent Search

Evolved object: Agent implementations, archived designs

Objective: Validation task performance

Boundary: Meta-agent remains fixed in the core design

Provisional insight / completeness / numeric evidence: 4 / 4 / 3. Provisional reading judgment, not independent reproduction: Code-based agent design broadens the search space; archive and transfer evaluation are described; selected validation scores remain a proxy.



## 6. AFlow: Automating Agentic Workflow Generation (2024)

Source: https://arxiv.org/abs/2410.10762

Read depth: method; locator: Method: MCTS workflow optimization

Evolved object: Code-represented workflows, operators and connections

Objective: Execution-based validation task score

Boundary: Reported cost benefit is not automatically an explicit cost objective

Provisional insight / completeness / numeric evidence: 3 / 4 / 3. Provisional reading judgment, not independent reproduction: Workflow tree search is operationally clear; task and efficiency results are reported, but cost benefit is not an independently optimized axis.



## 7. A Self-Improving Coding Agent (SICA) (2025)

Source: https://arxiv.org/abs/2504.15228

Read depth: method; locator: Method utility and archive selection

Evolved object: Own agent source and tools; selected agent used as modifier

Objective: Weighted performance, monetary cost and runtime utility

Boundary: 17–53% headline uses a random subset; omitted from article to avoid protocol confusion

Provisional insight / completeness / numeric evidence: 4 / 3 / 3. Provisional reading judgment, not independent reproduction: A selected agent becomes the next modifier and utility is explicit; the small evaluation subset limits the headline performance interpretation.



## 8. Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents (2025)

Source: https://arxiv.org/abs/2505.22954

Read depth: method; locator: Sections 4.2–4.4; Appendix E

Evolved object: Coding-agent source, tools and workflows; branching archive

Objective: Coding task success

Boundary: 20–50% SWE result is on 200 selected tasks, not the complete Verified set

Provisional insight / completeness / numeric evidence: 4 / 4 / 3. Provisional reading judgment, not independent reproduction: Branching self-modification makes stepping stones useful; staged evaluation and ablations are detailed; subset selection and stochastic evaluation remain relevant.



## 9. GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning (2025)

Source: https://arxiv.org/abs/2507.19457

Read depth: method; locator: PDF v2 introduction and algorithm

Evolved object: Prompts of language-model modules

Objective: Task feedback; selection preserves instance-specific strengths

Boundary: Pareto axes are problem instances in its selection mechanism; not inherently quality-cost-safety

Provisional insight / completeness / numeric evidence: 4 / 4 / 4. Provisional reading judgment, not independent reproduction: Trace reflection and instance-level complementary selection are distinct mechanisms; six-task comparisons provide broader evidence, still under particular budgets and tasks.



## 10. Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models (2025)

Source: https://arxiv.org/abs/2510.04618

Read depth: method; locator: v3 framework and incremental context updates

Evolved object: Structured context playbooks through generation, reflection and curation

Objective: Task performance from execution feedback

Boundary: Context adaptation, not model-weight training

Provisional insight / completeness / numeric evidence: 4 / 4 / 3. Provisional reading judgment, not independent reproduction: Structured incremental context addresses loss in wholesale rewrites; offline and online evaluations exist, with task-specific transfer limits.



## 11. Self-Adapting Language Models (2025)

Source: https://arxiv.org/abs/2506.10943

Read depth: method; locator: Method: self-edits and reinforcement learning

Evolved object: Generated self-edits govern inner model adaptation; outer RL

Objective: Downstream performance after weight adaptation

Boundary: Model-adaptation method; not equivalent to editing an agent scaffold

Provisional insight / completeness / numeric evidence: 4 / 4 / 3. Provisional reading judgment, not independent reproduction: Rewards depend on post-adaptation performance, linking generated edits to learning; evidence covers knowledge incorporation and few-shot adaptation rather than general agent operation.



## 12. Agent0: Unleashing Self-Evolving Agents from Zero Data via Tool-Integrated Reasoning (2025)

Source: https://arxiv.org/abs/2511.16043

Read depth: method; locator: Curriculum reward; executor training

Evolved object: Curriculum and executor policies via alternating training

Objective: Uncertainty/tool-use curriculum reward; executor correctness proxy

Boundary: Majority-derived answers are a proxy; zero data does not remove pretrained knowledge or tool priors

Provisional insight / completeness / numeric evidence: 4 / 3 / 3. Provisional reading judgment, not independent reproduction: Curriculum and executor co-training is explicit; generated answer consensus leaves reward validity as a key assumption.



## 13. AgentEvolver: Towards Efficient Self-Evolving Agent System (2025)

Source: https://arxiv.org/abs/2511.10395

Read depth: method; locator: Self-questioning, self-navigating, self-attributing; policy objective

Evolved object: Generated tasks, reused experience, credit assignment and policy training

Objective: Environment return and more efficient training

Boundary: Generated rewards/tasks approximate the target task distribution

Provisional insight / completeness / numeric evidence: 3 / 4 / 3. Provisional reading judgment, not independent reproduction: Task creation, experience reuse and credit assignment are integrated; environment-return evaluation does not independently validate every generated task.



## 14. HyperAgents (2026)

Source: https://arxiv.org/abs/2603.19461

Read depth: method; locator: Method and parent-selection description

Evolved object: Editable task agent and meta-agent

Objective: Downstream task performance and improvement behavior

Boundary: Parent selection remains handcrafted in the main system

Provisional insight / completeness / numeric evidence: 4 / 3 / 3. Provisional reading judgment, not independent reproduction: Editable meta-agents extend the object of optimization; several task settings are examined, while parent selection still remains fixed.



## 15. The Red Queen Gödel Machine: Co-Evolving Agents and Their Evaluators (2026)

Source: https://arxiv.org/abs/2606.26294

Read depth: method; locator: Method: evaluator epochs and archive handling

Evolved object: Agents and evaluators updated across epochs

Objective: Epoch-specific utility under an evolving evaluator

Boundary: Scores across changing evaluators need a common anchor

Provisional insight / completeness / numeric evidence: 4 / 3 / 3. Provisional reading judgment, not independent reproduction: Evaluator evolution directly addresses a moving selection signal; epoch control is explicit, but cross-epoch score comparability needs attention.



## 16. Recursive self-improvement of AI research agents (AIDE²) (2026)

Source: https://arxiv.org/abs/2609.26457

Read depth: method; locator: Sections 1–2; outer-loop limitation

Evolved object: Research harness: search, context, verification and inner selection

Objective: Mean private task grade at fixed per-task dollar budget

Boundary: 8 days and 7 accepted changes; improved outer-loop ability is statistically inconclusive

Provisional insight / completeness / numeric evidence: 4 / 4 / 3. Provisional reading judgment, not independent reproduction: Fixed-budget nested research optimization separates solution and harness search; external evaluations support artifact gains, while outer-improver superiority is explicitly inconclusive.



## 17. Dream-RSI: Recursive Self-Improvement through Evolving Worlds (2026)

Source: https://arxiv.org/abs/2609.14858

Read depth: method; locator: Method: replay world and policy fitness

Evolved object: Exploration-policy code; branch, parallelize and stop decisions

Objective: Replay-estimated quality-cost hypervolume with parallelism penalty

Boundary: Replay uses recorded discovery trees, not arbitrary unseen outcomes; latest full text differs from older abstract

Provisional insight / completeness / numeric evidence: 4 / 3 / 3. Provisional reading judgment, not independent reproduction: Replay moves exploration-policy search into recorded worlds; the objective is explicit, while support outside recorded trees remains a limitation.



## 18. EvoFlow: Evolving Diverse Agentic Workflows On The Fly (2025)

Source: https://arxiv.org/abs/2502.07373

Read depth: method; locator: Method; Appendix C selection

Evolved object: Population of workflow topologies, prompts and model choices

Objective: Task quality and cost

Boundary: Reusable workflow population; no base-model weight update

Provisional insight / completeness / numeric evidence: 4 / 4 / 3. Provisional reading judgment, not independent reproduction: Workflow populations preserve performance-cost alternatives; selection and niche mechanisms are specified, but deployment benefit depends on workload and costs.



## 19. AgentBreeder: Mitigating the AI Safety Risks of Multi-Agent Scaffolds via Self-Improvement (2025)

Source: https://arxiv.org/abs/2502.00757

Read depth: method; locator: Abstract; framework and Blue/Red settings

Evolved object: Multi-agent scaffolds

Objective: Capability and safety in the Blue setting

Boundary: Safety depends on tested tasks and graders

Provisional insight / completeness / numeric evidence: 4 / 3 / 3. Provisional reading judgment, not independent reproduction: Capability and safety participate in scaffold optimization; the safety conclusion remains dependent on the evaluated tasks and judges.



## 20. SkillMOO: Multi-objective Optimization of Agent Skills for Software Engineering (2026)

Source: https://arxiv.org/abs/2604.09297

Read depth: method; locator: Current full text: Method and 16-task evaluation

Evolved object: Task-specific skill bundles for a fixed solver

Objective: Pass rate and cost, using NSGA-II

Boundary: Older search abstract says 3 tasks; runtime is reported but not a third objective

Provisional insight / completeness / numeric evidence: 3 / 3 / 3. Provisional reading judgment, not independent reproduction: NSGA-II applies established multi-objective machinery to skill bundles; current evaluation covers 16 SE tasks, and version differences require care.



## 21. MOCHA: Multi-Objective Chebyshev Annealing for Agent Skill Optimization (2026)

Source: https://arxiv.org/abs/2605.19330

Read depth: method; locator: Method; six-skill experiment

Evolved object: Skill descriptions, bodies and metadata

Objective: Task correctness and platform compliance

Boundary: Chebyshev scalarization and hypervolume exploration; theoretical coverage does not guarantee finite-budget coverage

Provisional insight / completeness / numeric evidence: 4 / 3 / 3. Provisional reading judgment, not independent reproduction: Chebyshev search and hypervolume exploration target compliance trade-offs; six skills provide a concrete but narrow empirical scope.



## 22. ParetoPO: Towards Pareto-Optimal Tool-Integrated Agents with Pareto Ranking Policy Optimization (2026)

Source: https://arxiv.org/abs/2606.16111

Read depth: method; locator: Two-stage training objective

Evolved object: Model policy weights through RL

Objective: Accuracy and tool-use efficiency

Boundary: Adjacent multi-objective training, not population search over frozen-model scaffolds

Provisional insight / completeness / numeric evidence: 4 / 3 / 3. Provisional reading judgment, not independent reproduction: Pareto ranking changes policy-training feedback; math and multi-hop QA support the reported setting, not all agent workloads.



## 23. MOAE: Multi-Objective Agent Evolution with Pareto-Preserving Search (2026)

Source: https://arxiv.org/abs/2609.05992

Read depth: method; locator: Public full-text method; archive and deployment selection

Evolved object: Per-query compact execution policies and fresh complete rollouts

Objective: Task performance, trajectory quality and safety

Boundary: Frozen base model, tools and architecture; no claim of persistent cross-task architecture evolution

Provisional insight / completeness / numeric evidence: 4 / 3 / 3. Provisional reading judgment, not independent reproduction: Separates per-query policy search from deployment selection; full rollouts expose trajectory and safety trade-offs, with measurement-dependent archive quality.



## 24. EvoDrive: Pareto Evolution for Safety-Critical Autonomous Driving via Self-Improving LLM Agents (2026)

Source: https://arxiv.org/abs/2606.03678

Read depth: method; locator: v2 method, fixed driving policy and simulator

Evolved object: Scenario-generator programs and selected search/evaluation components

Objective: Adversariality and realism

Boundary: Primary evolved object is the scenario generator, not the driving policy

Provisional insight / completeness / numeric evidence: 4 / 3 / 3. Provisional reading judgment, not independent reproduction: Scenario evolution separates realism from adversariality; fixed simulator and ego policy define the empirical scope.



## 25. AlphaEvolve (2025)

Source: https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/

Read depth: official article; locator: Google DeepMind official introduction and May 2026 impact article

Evolved object: Target algorithm code

Objective: Task-specific executable objectives, e.g. computational efficiency

Boundary: Evolving target algorithms does not alone establish an evolving optimizer

Provisional insight / completeness / numeric evidence: unscored / unscored / unscored. Not scored: abstract-only, developer article, or taxonomy evidence is insufficient for a method-quality score.



## 26. A Survey of Self-Evolving Agents: What, When, How, and Where to Evolve on the Path to Artificial Super Intelligence (2025)

Source: https://arxiv.org/abs/2507.21046

Read depth: method; locator: Taxonomy overview

Evolved object: Taxonomy of objects, time and mechanisms

Objective: Literature synthesis

Boundary: Background taxonomy, not empirical validation of every cited method

Provisional insight / completeness / numeric evidence: unscored / unscored / unscored. Not scored: abstract-only, developer article, or taxonomy evidence is insufficient for a method-quality score.



## 27. Can AI agents conduct open-ended AI research? Early evidence from two case studies (2026)

Source: https://arxiv.org/abs/2607.27191

Read depth: abstract; locator: Abstract v2

Evolved object: Two open-ended research case studies

Objective: Substantive research progress assessed by original researchers

Boundary: Two cases cannot establish general impossibility of AI research

Provisional insight / completeness / numeric evidence: unscored / unscored / unscored. Not scored: abstract-only, developer article, or taxonomy evidence is insufficient for a method-quality score.



## 28. Safety in Self-Evolving Agents: A Survey (2026)

Source: https://arxiv.org/abs/2610.00093

Read depth: method; locator: Overview and persistent-state safety discussion

Evolved object: Persistent evolving state and safety risks

Objective: Literature synthesis

Boundary: Survey, not a controlled comparative experiment

Provisional insight / completeness / numeric evidence: unscored / unscored / unscored. Not scored: abstract-only, developer article, or taxonomy evidence is insufficient for a method-quality score.



## 29. Meta-Harness: End-to-End Optimization of Model Harnesses (2026)

Source: https://arxiv.org/abs/2603.28052

Evolved object: Task-specific executable harnesses

Objective: Task performance and resource use

Read locator: Section 3; full-history filesystem and algorithm

Boundary: A fixed-model harness search; not a claim that every selection component evolves


## 30. HELIX: Model-Harness Co-evolution for Recursive Self-Improvement (2026)

Source: https://arxiv.org/abs/2608.13951

Evolved object: Traceable harness variants and verified sibling records

Objective: Execution value and learning-data value

Read locator: Build-update-rebuild; limitations 9.1 and 9.5

Boundary: One-round harness study and data handoff; repeated closed-loop model-harness gains not established


## 31. When Self-Evolution Backfires: Pre-Commit Gating against Skill Contamination in LLM Agents (2026)

Source: https://arxiv.org/abs/2608.05810

Evolved object: Skill admission, individual critics and joint subset selection

Objective: Task success with structural, behavioral and semantic admission checks

Read locator: Method and rollback analysis

Boundary: Source-only deletion leaves descendants; do not generalize this to impossibility of restoring a complete earlier system snapshot


## 32. Coalition-Aware Skill Reliability for Self-Evolving Agents (2026)

Source: https://arxiv.org/abs/2608.22610

Evolved object: Coalition-aware skill selection and transferred-skill masking

Objective: Bank-conditioned contribution and transfer utility

Read locator: Sections 3 and 4; sampled Shapley marginals

Boundary: Skill utility is conditional on partners and domain; marginal estimates remain empirical


## 33. MoFlow: Multi-Objective Agentic Workflow Generation (2026)

Source: https://arxiv.org/abs/2609.38294

Evolved object: Stepwise workflow construction and per-node trade-off sets

Objective: Accuracy, cost, latency, robustness and consistency

Read locator: Method sections 3.1-3.3; convex coverage sets

Boundary: Convex coverage for linear preferences is not a guarantee of finding every nondominated workflow
