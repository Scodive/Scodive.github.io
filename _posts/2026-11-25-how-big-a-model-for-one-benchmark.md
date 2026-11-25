---
layout: default
title: "How Big Does a Model Need to Be for One Benchmark?"
title_zh: "一张考卷到底需要多大的模型？"
date: 2026-11-25
author_profile: true
excerpt: "Four complete test sets show where compact specialized models match frontier references, and why multi-step math demands a different supervision signal."
excerpt_zh: "四张完整考卷划出了小模型专精的能力边界，也解释了为什么多步数学推理不能只靠扩充题目和答案。"
topic: "Model specialization"
topic_zh: "小模型专精"
reading_time: "10 min read"
reading_time_zh: "约 10 分钟"
figure_en: "/assets/how-big-a-model-for-one-benchmark/oos-crossover-en.svg"
figure_zh: "/assets/how-big-a-model-for-one-benchmark/oos-crossover-zh.svg"
figure_alt_en: "Accuracy gap between local BGE-small and GPT-5.6 Luna across out-of-scope request shares on CLINC150"
figure_alt_zh: "CLINC150 上本地 BGE-small 与 GPT-5.6 Luna 随域外请求占比变化的准确率差值曲线"
---

<div class="blog-post-content" data-blog-article data-site-title="{{ site.title | escape }}" lang="en">
<div class="bm-topbar">
<a class="bm-back-link" href="{{ '/blogs/' | relative_url }}" data-en="All essays" data-zh="全部文章">All essays</a>
<div class="bm-language" role="tablist" aria-label="Article language / 文章语言">
<button type="button" role="tab" data-bm-language="en" aria-selected="true" aria-pressed="true" aria-controls="bm-content-en" lang="en">English</button>
<button type="button" role="tab" data-bm-language="zh" aria-selected="false" aria-pressed="false" aria-controls="bm-content-zh" lang="zh-CN">中文</button>
</div>
</div>

<div id="bm-content-en" class="bm-language-content" lang="en" markdown="1">

# How Big Does a Model Need to Be for One Benchmark?

<p class="bm-meta">{{ page.date | date: "%B %-d, %Y" }} · {{ page.topic }} · {{ page.reading_time }}<span id="vercount_container_page_pv" class="bm-meta__views" style="display:none;"> · <strong class="bm-meta__views-num" id="vercount_value_page_pv">--</strong> views</span></p>

<p class="bm-deck">{{ page.excerpt }}</p>

When a system only needs to master one domain, how small can it get? A bank ticket router has no reason to know geometry. All it must do is assign customer requests to 77 categories at a fraction of the latency and training cost of a general-purpose model. The harder question is whether that same specialization recipe carries over when we replace support tickets with math problems, supply a fresh training set, and ask a compact model to catch up.

Across four complete benchmarks trained on a single 8 GB GTX 1070, the boundary splits sharply along task structure. On CLINC150 intent routing, a 33.27M-parameter encoder adapted in 79 seconds answers 5,210 of 5,500 test queries correctly, five ahead of GPT-5.6 Luna backed by retrieved examples. On GSM8K grade-school math, starting from the same 76.96M-parameter FLAN-T5-small backbone and the same 6,725 training problems yields a completely different lesson: predicting final numbers directly gets 27 test problems right, whereas generating executable arithmetic programs jumps to 123. Both tasks emit short answers. What separates them is whether the benchmark requires routing familiar language into fixed slots or constructing a valid procedure from scratch.

<div class="bm-thesis" markdown="1">

Task specialization compresses remarkably well when a benchmark maps phrasing onto a fixed label space, though small-model leads still hinge on traffic mix and familiar wording. Once a benchmark requires compositional reasoning, adding more answer-only data stalls (`26 → 27` on GSM8K), and meaningful progress comes from changing the supervision target into executable structure (`27 → 123`).

</div>

<nav class="bm-toc" aria-label="Contents" markdown="1">

1. [Four complete exams, one sharp split](#complete-tests-en)
2. [How five extra answers decide a leaderboard](#five-extra-answers-en)
3. [Parameter budgets and the wording gap](#parameter-budget-en)
4. [What a 25% training budget actually buys](#training-subsets-en)
5. [Changing the supervision target in math](#executable-solutions-en)
6. [Accounting for the real cost of specialization](#compute-cost-en)
7. [References and data sources](#references-en)

</nav>

<h2 id="complete-tests-en">Four complete exams, one sharp split</h2>

Treating each dataset as a standalone domain gives every specialized model its own weights and scores every item on the full test split. Intent models select among valid class labels; math models must output a valid number, with unparseable generations scored as incorrect. Closed-model baselines come from published runs evaluated on the exact same test sets.[1](#ref-1-en) [2](#ref-2-en) [3](#ref-3-en) [4](#ref-4-en)

<div class="bm-table bm-table-wide" role="region" aria-label="Four complete exams" tabindex="0" markdown="1">

| Complete test and local configuration | Local correct | Local accuracy | Closed reference |
| --- | ---: | ---: | ---: |
| Banking77, model chosen by overall validation accuracy | 2,866 / 3,080 | 93.05% | 93.80% |
| CLINC150, rejection threshold chosen by overall validation accuracy | 5,107 / 5,500 | 92.85% | 94.64% |
| CLINC150, equal validation weight for in-scope and out-of-scope requests | 5,210 / 5,500 | 94.73% | 94.64% |
| GSM8K, generate the number directly | 27 / 1,319 | 2.05% | 97.12% |
| GSM8K, generate and execute a program | 123 / 1,319 | 9.33% | 97.12% |
| AIME 2026, generate the number directly | 0 / 30 | 0.00% | 100.00% |

</div>

On both intent benchmarks, the reference system is GPT-5.6 Luna. Given only the 77 Banking77 category names, Luna scores 85.4%; adding 20 retrieved training examples and format constraints lifts it to 93.8%.[1](#ref-1-en) [2](#ref-2-en) Any team deploying a closed model can index that same labeled data for retrieval, which makes the retrieval-augmented number the right comparison point. The math baselines are Gemini 2.5 Pro on GSM8K and GPT-5.5 (xhigh) on AIME 2026.[3](#ref-3-en) [4](#ref-4-en) Each comparison reflects a specific system and evaluation setup rather than an exhaustive ranking of frontier models.

Running a uniform baseline across all four tasks makes the structural divide unmistakable. Starting every task from the same pretrained FLAN-T5-small weights and training for two epochs on its own training split yields **87.01%** on Banking77, **85.40%** on CLINC150, **2.05%** on GSM8K, and **0.00%** on AIME 2026. The training pipeline transfers effortlessly across benchmarks. The capability does not.

<h2 id="five-extra-answers-en">How five extra answers decide a leaderboard</h2>

CLINC150 tests two competing skills: classifying 150 known intents while rejecting out-of-scope requests.[5](#ref-5-en) Fine-tuning BGE-small on the OOS+ split (15,000 in-scope and 250 out-of-scope training examples) under two validation rules reveals why a narrow benchmark lead requires scrutiny. The first rule maximizes total validation accuracy; the second weights in-scope accuracy and out-of-scope recall equally. Both select the exact same checkpoint and differ only in the rejection threshold.

<div class="bm-table bm-table-wide" role="region" aria-label="CLINC150 threshold comparison" tabindex="0" markdown="1">

| System and threshold | In-scope correct / 4,500 | Out-of-scope correct / 1,000 | Total / 5,500 |
| --- | ---: | ---: | ---: |
| Local BGE, overall validation accuracy | 4,354 | 753 | 5,107 |
| Local BGE, equal weight for the two groups | 4,286 | 924 | 5,210 |
| GPT-5.6 Luna, retrieved examples | 4,414 | 791 | 5,205 |

</div>

Why did optimizing directly for validation accuracy forfeit 103 test answers? The validation split contains only 100 out-of-scope requests out of 3,100 (3.2%), whereas the test split jumps to 1,000 out of 5,500 (18.2%). Equal group weighting shifts the threshold to catch 171 more out-of-scope queries at a cost of 68 in-scope errors, yielding a net gain of 103.

A closer look at the 5,210 vs. 5,205 comparison with Luna shows how fragile a five-question margin can be. The local encoder gets 133 more out-of-scope items right and 128 fewer in-scope items right, meaning the two systems disagree on at least 261 items while sitting just 0.09 percentage points apart overall. Holding those within-group accuracies constant, the crossover point sits at **17.6%** out-of-scope traffic, right below the **18.2%** share in CLINC150's test set. On a service desk where only 10% of incoming queries are out of scope, those exact same rates yield 94.96% for the local model versus 96.19% for Luna. Five items settle the static benchmark ranking, but deployment traffic decides which system actually wins.

<figure>
<img src="{{ '/assets/how-big-a-model-for-one-benchmark/oos-crossover-en.svg' | relative_url }}" alt="Accuracy gap between local BGE-small and GPT-5.6 Luna across out-of-scope request shares on CLINC150" loading="lazy">
<figcaption><strong>Figure 1 · Ranking sensitivity to traffic mix on CLINC150.</strong> Accuracy difference (local BGE-small minus GPT-5.6 Luna) computed from observed in-scope and out-of-scope hit rates. The two systems cross at 17.6% out-of-scope traffic, just below the 18.2% test split share.</figcaption>
</figure>

<h2 id="parameter-budget-en">Parameter budgets and the wording gap</h2>

How much pretrained capacity does an intent router actually need? Starting completely from scratch with randomly initialized word embeddings and 2-, 3-, and 4-gram convolutions produces a Banking77 network of just **198,349 parameters**. Comparing paired runs with identical initialization and batch order, adding soft targets from a trained BGE teacher lifts three-seed accuracy from 87.69% to **88.51%** on Banking77, and from 80.86% to **83.92%** on CLINC (standard 100-OOS split). The distilled student carries zero pretraining weights and runs standalone, trading roughly five percentage points of accuracy for a 168x smaller footprint.

Even within BGE-small, model selection exposes a subtle gap between validation and test. On Banking77, freezing BGE behind a linear head yields 93.05%, while full-encoder fine-tuning reaches **2,878 / 3,080 (93.44%)**, only 11 items behind the closed reference. Yet the frozen model scored three items higher on the 1,001-item validation split, so any pre-committed validation rule would ship the frozen checkpoint rather than the fine-tuned one.

To test whether these gains reflect memorization, we can check both exact overlap and lexical similarity:

- **Exact string overlap**: Fine-tuned BGE scores 97.62% on Banking77 training, 93.91% on validation, and 93.44% on test. Removing the 22 normalized text duplicates leaves 2,856 / 3,058 (**93.39%**). On equal-weight CLINC150 (99.59% train / 95.87% val / 94.73% test), removing 19 duplicate test items leaves 5,192 / 5,481 (**94.73%**). Exact memorization contributes almost nothing to the headline score.
- **Unfamiliar phrasing**: Sorting Banking77 test items within each intent by lexical similarity to their nearest training example reveals an **8.4-point spread**: accuracy drops from **96.5%** on the 770 most familiar items to **88.1%** on the 770 least familiar items. Even when the label set is fixed, novel user phrasing remains a distinct generalization test.

All three intent architectures (CNN, frozen/fine-tuned BGE, and single-token FLAN-T5) output a category ID. For intent routing, classification completes the task. To see what breaks when a model must construct its own answer, we turn to math.

<h2 id="training-subsets-en">What a 25% training budget actually buys</h2>

If a compact model only needs one benchmark, can we also cut its training set by 75%? Using frozen BGE embeddings on question text alone, greedy k-center selection picks each new training point farthest from those already chosen, and compares against size-matched random sampling across three seeds.[6](#ref-6-en)

<figure>
<img src="{{ '/assets/how-big-a-model-for-one-benchmark/subset-coverage-en.svg' | relative_url }}" alt="Full-test accuracy difference between semantic coverage and random sampling at a 25% training budget" loading="lazy">
<figcaption><strong>Figure 2 · Semantic coverage versus random sampling at a 25% training budget.</strong> Hollow circles show individual subset seeds and dark diamonds show three-seed means on the full test split. Coverage helps on average for intent routing, swings widely on CLINC150, and hurts on GSM8K.</figcaption>
</figure>

Across the three datasets, semantic coverage behaves very differently depending on task structure:

- **Banking77 (2,250 examples)**: Both methods cover all 77 labels in every run, yet semantic coverage beats random sampling by **+24, +16, and +28** test answers (+0.74 pp mean). Choosing *which* phrasings represent each intent consistently improves generalization.
- **CLINC150 (3,775 examples)**: Outcomes swing across seeds (**+225, +171, and −119** answers; +1.68 pp mean). Reporting a single favorable seed would make diversity sampling look far more dependable than it actually is.
- **GSM8K (1,681 examples)**: Even though semantic coverage exposes a linear answer classifier to more distinct target numbers in every run, it loses by 12, loses by 16, and ties random sampling (−0.71 pp mean). Even on the full dataset, 1,226 of the 1,319 test answers appear verbatim in training, yet an answer classifier solves only 49 problems, barely above always guessing the most common answer `4` (35 right).

Testing generative FLAN-T5-small on the same 1,681-problem GSM8K budget reinforces why surface diversity backfires on reasoning. Random sampling scores 26/1,319 while embedding-based coverage drops to 13. Grouping problems by their human solution's operation sequence (such as multiplication followed by subtraction) and forcing maximum variety (1,681 unique sequences) drops accuracy further to **10**; allocating seats proportionally to training sequence frequency covers 760 patterns and recovers **27**. Maximizing sequence diversity spent 1,191 of 1,681 training slots on rare one-off patterns (versus 315 in random sampling), starving the small model of the common arithmetic patterns it actually needed to learn.

<h2 id="executable-solutions-en">Changing the supervision target in math</h2>

Because GSM8K provides worked reasoning steps alongside every final answer, the 6,725-problem split isolates the effect of *how* a small model is supervised.[7](#ref-7-en) Every variant starts from the same FLAN-T5-small weights and decodes greedily once per test question (capped at 12 tokens for direct numbers, or 72 tokens for equations and programs).

<div class="bm-table bm-table-wide" role="region" aria-label="GSM8K supervision methods" tabindex="0" markdown="1">

| GSM8K answer method | Correct / 1,319 | Accuracy |
| --- | ---: | ---: |
| Pretrained model answering directly | 9 | 0.68% |
| Train on the final number | 27 | 2.05% |
| Train on equations and the final answer | 36 | 2.73% |
| Recalculate the last equation in the model's trace | 50 | 3.79% |
| Train on a whole executable arithmetic program and run it | 123 | 9.33% |

</div>

Two qualitative failures explain why neither adding data nor patching only the final step is enough. On a problem about five pies cut into eight slices with fourteen slices remaining, the equation-trained model correctly writes `5 × 8` and `40 − 14` before emitting `21`, a pure arithmetic slip that recomputing the last equation fixes to `26`. On another problem with sixteen duck eggs (three eaten, four baked, the rest sold at two dollars each), the model hallucinates `72` eggs for sale and writes `72 × 2 = 168`; recalculating fixes the multiplication to `144`, while the true answer is `18`. Across 1,294 parseable traces, an external calculator rescues 36 answers and breaks 22 already-correct ones, netting +14.

Compiling the full training annotations into sequential arithmetic programs (where each step can reference prior intermediate variables and an external executor runs all arithmetic) produces a much larger shift. Out of 6,725 training items, 6,295 compile back to their gold targets (with 430 retaining numerical fallback). At test time, the program-trained model solves 119 problems missed by the direct-answer baseline while losing 23, netting **+96 solved problems** (with all 189 non-executing traces counted wrong). Scaling direct-answer training data fourfold from 1,681 to 6,725 examples moved accuracy by one problem (`26 → 27`). Changing the supervision target on the same 6,725 problems and offloading execution moved it to **123**.

On competition math, the floor drops to zero. Training direct-answer FLAN-T5-small on 770 historical AIME problems through 2018 (validated on 149 problems from 2019–2023) scores **0 / 30** on the 2026 AIME exams, against 100.00% averaged over four attempts by GPT-5.5 (xhigh).[4](#ref-4-en) [8](#ref-8-en) [9](#ref-9-en) No amount of short-answer memorization bridges multi-step symbolic synthesis within a 77M-parameter budget and 12-token output cap.

<h2 id="compute-cost-en">Accounting for the real cost of specialization</h2>

<div class="bm-table bm-table-wide" role="region" aria-label="Compute adaptation and latency costs" tabindex="0" markdown="1">

| Local task and system | Deployed parameters | Task adaptation | Single-query p50 / p95 |
| --- | ---: | ---: | ---: |
| Banking, randomly initialized CNN | 0.198M | 7 s | 0.7 / 1.1 ms |
| Banking, frozen BGE and linear head | 33.24M | 29 s | 11.0 / 14.7 ms |
| Banking, fine-tuned BGE | 33.24M | 59 s | 9.1 / 11.3 ms |
| CLINC OOS+, fine-tuned BGE | 33.27M | 79 s | 10.9 / 17.2 ms |
| GSM8K, FLAN generating numbers | 76.96M | 136 s | 58.7 / 64.7 ms |
| GSM8K, FLAN generating worked equations and answers | 76.96M | 176 s | 439.4 / 775.9 ms |
| GSM8K, FLAN generating programs | 76.96M | 168 s | 230.3 / 381.0 ms |

</div>

Every run above was timed end-to-end on the same 8 GB GTX 1070, including tokenization through final prediction (100 warmed-up queries for CNN and BGE; 40 for FLAN). The frozen Banking77 head optimizes just 29,645 coefficients while still shipping the BGE encoder at inference time; distilling soft targets for the 198K CNN takes an additional 18 seconds once a teacher is trained. By comparison, Luna's published median API latencies are 812 ms on Banking77 and 830 ms on CLINC (including network round-trip, excluding retrieval), with zero task-specific gradient updates.[1](#ref-1-en) Both local systems, of course, amortize the upstream pretraining of BGE-small and FLAN-T5-small that sits outside the adaptation column.[10](#ref-10-en) [11](#ref-11-en)

Prior literature points to the same mechanism. Sentence encoders enabled compact intent routing in Banking77's original release,[12](#ref-12-en) distilling step-by-step rationales let a 770M T5 surpass few-shot 540B PaLM on ANLI using 80% of the data,[13](#ref-13-en) and ILLATE's 4B specialized model reached 94.0% on Banking77 and 95.1% on CLINC.[1](#ref-1-en)

Taken together, these four exams draw a clear line between **classification compression** and **compositional synthesis**. On CLINC150, 33.27M parameters and 79 seconds of local adaptation are enough to match a retrieved closed reference, provided the traffic mix and phrasing stay near the training distribution. On GSM8K, even though 1,226 of 1,319 test answers already exist in the training set, answer prediction fails because the bottleneck is mapping prose into valid intermediate operations. The open design question for any new domain is diagnostic: before training, how can we tell from a sample of examples whether a compact model only needs sharper boundaries, or whether it must first be taught a richer intermediate representation?

<h2 id="references-en">References and data sources</h2>

<ol class="bm-references">
<li id="ref-1-en">ILLATE. <a href="https://illate.dev/luna-vs-fine-tuned-model">Luna vs. Fine-Tuned Models: Intent Evaluation Protocol, Breakdown, and Timing</a>. Benchmark report.</li>
<li id="ref-2-en">ILLATE. <a href="https://illate.dev/bakeoff.json">Reported Intent Benchmark Scores (JSON)</a>. Dataset artifact.</li>
<li id="ref-3-en">GSM8K Evaluation Reference. <a href="https://arxiv.org/abs/2602.13217">arXiv:2602.13217</a>. Closed-model baseline on GSM8K.</li>
<li id="ref-4-en">MathArena. <a href="https://matharena.ai/?comp=aime--aime_2026&amp;view=problem">AIME 2026 Evaluation Results by Problem</a>. Live benchmark leaderboard.</li>
<li id="ref-5-en">Larson et al. <a href="https://github.com/clinc/oos-eval/tree/828f8093932c8fe6ca7936c3d2e52903b1c523de/data">CLINC150 Out-of-Scope Evaluation Data and Splits</a>. GitHub repository.</li>
<li id="ref-6-en">Sener and Savarese. <a href="https://openreview.net/forum?id=H1aIuk-RW">Active Learning for Convolutional Neural Networks: A Core-Set Approach</a>. ICLR 2018 (greedy k-center selection).</li>
<li id="ref-7-en">Cobbe et al. <a href="https://github.com/openai/grade-school-math">GSM8K: Grade School Math Questions and Worked Solutions</a>. OpenAI GitHub repository.</li>
<li id="ref-8-en">Schmid, P. <a href="https://huggingface.co/datasets/philschmid/AIME_1983_2024">AIME 1983–2024 Historical Problem Dataset</a>. Hugging Face Datasets.</li>
<li id="ref-9-en">MathArena. <a href="https://huggingface.co/datasets/MathArena/aime_2026">AIME 2026 Problem Set</a>. Hugging Face Datasets.</li>
<li id="ref-10-en">BAAI. <a href="https://huggingface.co/BAAI/bge-small-en-v1.5">bge-small-en-v1.5 Pretrained Embedding Checkpoint</a>. Hugging Face Hub.</li>
<li id="ref-11-en">Google. <a href="https://huggingface.co/google/flan-t5-small">flan-t5-small Pretrained Checkpoint</a>. Hugging Face Hub.</li>
<li id="ref-12-en">Casanueva et al. <a href="https://aclanthology.org/2020.nlp4convai-1.5/">Efficient Intent Detection with Dual Sentence Encoders</a>. NLP4ConvAI 2020.</li>
<li id="ref-13-en">Hsieh et al. <a href="https://aclanthology.org/2023.findings-acl.507/">Distilling Step-by-Step! Outperforming Larger Language Models with Less Training Data and Smaller Model Sizes</a>. Findings of ACL 2023.</li>
</ol>

</div>

<div id="bm-content-zh" class="bm-language-content" lang="zh-CN" hidden markdown="1">

# 一张考卷到底需要多大的模型？

<p class="bm-meta">{{ page.date | date: "%Y 年 %-m 月 %-d 日" }} · {{ page.topic_zh }} · {{ page.reading_time_zh }}<span id="busuanzi_container_page_pv" class="bm-meta__views" style="display:none;"> · <strong class="bm-meta__views-num" id="busuanzi_value_page_pv">--</strong> 次阅读</span></p>

<p class="bm-deck">{{ page.excerpt_zh }}</p>

如果一个模型只服务于单一业务，它究竟可以缩到多小？银行的客服分流模型不需要懂平面几何，只要能把用户提问稳定分进 77 个类别，同时兼顾低延迟和低训练成本，就已经足够实用。真正棘手的问题在于：当我们把银行工单换成数学应用题，同样给它一套专属训练集，这套“小模型专精”的配方还能不能奏效？

我们在单张 8 GB 显存的 GTX 1070 上跑完了四份完整测试集，答案顺着任务结构劈成了截然不同的两半。在 CLINC150 意图识别上，一个 3,327 万参数的本地编码器仅微调 79 秒，就在 5,500 道测试题中答对 5,210 道，反超带检索样例的闭源模型 GPT-5.6 Luna（5,205 道）。然而到了 GSM8K 小学数学题，从同一个 7,696 万参数的 FLAN-T5-small 出发、训练完全相同的 6,725 道题目：直接生成最终数字只答对 27 道，改让模型生成可执行的算术程序则跃升到 123 道。两类任务的最终答案都很简短，分水岭在于：考卷考查的是把多样的表达映射进固定标签槽位，还是从零构建正确的运算步骤。

<div class="bm-thesis" markdown="1">

当任务本质是“将自然语言映射到固定标签空间”时，单任务专精能把模型压得极小，但微弱的领先仍受流量结构与措辞熟悉度左右。一旦进入“多步组合推理”，单纯堆叠“题干—最终答案”数据会迅速失效（GSM8K 从 26 道停滞在 27 道），决定上限的是把监督信号改成可执行的结构化步骤（27 道升至 123 道）。

</div>

<nav class="bm-toc" aria-label="文章目录" markdown="1">

1. [四张完整考卷划出的分水岭](#complete-tests-zh)
2. [多对五道题背后的流量陷阱](#five-extra-answers-zh)
3. [极限压缩到二十万参数，还是在“背题”？](#parameter-budget-zh)
4. [只留四分之一训练题，覆盖选样值不值](#training-subsets-zh)
5. [让数学模型输出可执行的中间结构](#executable-solutions-zh)
6. [如何估算专精模型的真实成本](#compute-cost-zh)
7. [参考资料与数据来源](#references-zh)

</nav>

<h2 id="complete-tests-zh">四张完整考卷划出的分水岭</h2>

为了严格检验专精上限，实验将每个数据集视为一个独立领域：每个任务各自训练一套独立权重，并在完整测试集上逐题计分。意图分类模型从合法类别中择一输出；数学模型必须给出明确数值，格式无法解析一律计错。闭源模型的对照成绩均取自公开评测在同一测试集上的实测结果。[1](#ref-1-zh) [2](#ref-2-zh) [3](#ref-3-zh) [4](#ref-4-zh)

<div class="bm-table bm-table-wide" role="region" aria-label="四张完整考卷" tabindex="0" markdown="1">

| 完整测试集与本地设置 | 本地答对数 | 本地准确率 | 闭源参照 |
| --- | ---: | ---: | ---: |
| Banking77，按验证集总准确率选模型 | 2,866 / 3,080 | 93.05% | 93.80% |
| CLINC150，按验证集总准确率选拒答阈值 | 5,107 / 5,500 | 92.85% | 94.64% |
| CLINC150，域内与域外请求等权选阈值 | 5,210 / 5,500 | 94.73% | 94.64% |
| GSM8K，直接生成最终数字 | 27 / 1,319 | 2.05% | 97.12% |
| GSM8K，生成可执行程序后运行 | 123 / 1,319 | 9.33% | 97.12% |
| AIME 2026，直接生成最终数字 | 0 / 30 | 0.00% | 100.00% |

</div>

两项意图测试的闭源参照均为 GPT-5.6 Luna。在 Banking77 上仅提供 77 个类别名称时，Luna 的准确率为 85.4%；接入 20 条检索示例并约束输出格式后，准确率升至 93.8%。[1](#ref-1-zh) [2](#ref-2-zh) 现实部署中，闭源系统同样可以利用这份标注数据建立检索库，因此取检索增强后的成绩作为对照更为公平。数学两卷的闭源参照分别为 Gemini 2.5 Pro 与 GPT-5.5（xhigh）。[3](#ref-3-zh) [4](#ref-4-zh) 各组数字对应各自的公开配置，并非对所有当代旗舰模型的穷举对比。

如果强行用同一套方法跨过四张考卷，结构差异会立刻显现。以完全相同的 FLAN-T5-small 预训练权重为起点，在各自主训练集上微调两轮——意图任务生成合法类别词元，数学任务直接生成最终数字——四项得分依次为 **87.01%**（Banking77）、**85.40%**（CLINC150）、**2.05%**（GSM8K）与 **0.00%**（AIME 2026）。训练流程可以原封不动地搬过去，能力却并没有随之迁移。

<h2 id="five-extra-answers-zh">多对五道题背后的流量陷阱</h2>

CLINC150 同时考验助手两项能力：识别 150 种已知业务意图，以及果断拒答超出服务范围的请求。[5](#ref-5-zh) 在 OOS+ 切分（15,000 条已知请求与 250 条域外请求）上微调 BGE-small 时，验证阶段的阈值选择规则直接改变了最终名次。第一种规则追求验证集总准确率最高；第二种将“已知意图准确率”与“域外请求召回率”各赋予 50% 权重。两种规则最终选中的是同一轮训练权重，唯一的差别仅仅在于拒答阈值。

<div class="bm-table bm-table-wide" role="region" aria-label="CLINC150 阈值对照" tabindex="0" markdown="1">

| 系统与阈值策略 | 已知请求答对 / 4,500 | 域外请求答对 / 1,000 | 合计 / 5,500 |
| --- | ---: | ---: | ---: |
| 本地 BGE，验证集总分最优 | 4,354 | 753 | 5,107 |
| 本地 BGE，域内与域外等权 | 4,286 | 924 | 5,210 |
| GPT-5.6 Luna，检索示例 | 4,414 | 791 | 5,205 |

</div>

为什么在验证集上追求总分最高，正式测试时反而少答对 103 道题？原因在于数据分布错位：验证集中域外请求只有 100 / 3,100（占比 3.2%），而正式测试集高达 1,000 / 5,500（占比 18.2%）。等权准则主动放宽了拒答门槛，多拦住 171 条域外请求，代价是多误判了 68 条域内请求，净赚恰好 103 道。

更重要的是，这 5,210 对 5,205 的胜负其实非常脆弱。与 Luna 相比，本地等权模型在域外请求上多对 133 道，在已知意图上少对 128 道。两者总分仅仅相差 5 道（0.09 个百分点），但在至少 261 道题上的对错完全相反。假设两个系统在各自子集上的命中率不变，总分相交的临界点出现在域外流量占比 **17.6%** 处——而正式测试集恰巧落在 **18.2%**。一旦放到真实客服场景，若域外请求只占 10%，同样的命中率重算后，本地小模型得分为 94.96%，Luna 则达到 96.19%。多出来的五道题能决定固定考卷上的榜首，却不足以保证换一批线上流量后谁更占优。

<figure>
<img src="{{ '/assets/how-big-a-model-for-one-benchmark/oos-crossover-zh.svg' | relative_url }}" alt="CLINC150 上本地 BGE-small 与 GPT-5.6 Luna 随域外请求占比变化的准确率差值曲线" loading="lazy">
<figcaption><strong>图 1 · CLINC150 上的排名对域外流量占比高度敏感。</strong> 按实测的域内与域外命中率重算两系统准确率差值（本地 BGE-small 减去 GPT-5.6 Luna）。两者在域外占比 17.6% 处打平，恰好贴近正式测试集的 18.2%。</figcaption>
</figure>

<h2 id="parameter-budget-zh">极限压缩到二十万参数，还是在“背题”？</h2>

如果连千万级预训练底座都去掉，意图分流最低能压到多大？以随机初始化词向量搭配宽度为 2、3、4 的一维卷积，Banking77 模型的总参数量只有 **198,349 个**（不到二十万）。在初始化权重与样本顺序完全一致的对照中，引入经过微调的 BGE 教师模型软标签进行蒸馏，三次随机种子的平均准确率从 87.69% 升至 **88.51%**；同一做法在标准 CLINC（100 条域外样本）上将准确率从 80.86% 推高至 **83.92%**。蒸馏后的卷积学生不含任何通用预训练权重，可完全独立推理，以约 5 个百分点的精度代价换来了缩小 168 倍的体积。

即便是 BGE-small 自身，在 Banking77 上也存在微调过拟合与验证集选型的张力。冻结编码器仅训练线性分类头可得 93.05%；解冻全量微调则达到 **2,878 / 3,080（93.44%）**，距离闭源参照仅差 11 道。然而冻结版在 1,001 道验证题上反而多答对 3 道。如果严格执行部署前锁定的验证集选型规则，真正被选中的反而是冻结版本。

高分究竟来自理解还是“背题”？从文本重合度与措辞相似度两个角度拆解，结论很清晰：

- **原文重复极微弱**：全量微调的 BGE 在 Banking77 训练、验证、测试集上的得分分别为 97.62%、93.91% 和 93.44%。忽略大小写与标点并剔除 22 条与训练集重复的测试题后，剩余 3,058 题仍答对 2,856 题（**93.39%**）。CLINC 等权模型（训练 99.59%、验证 95.87%、测试 94.73%）剔除 19 条重复题后，准确率依然维持在 5,192 / 5,481（**94.73%**）。
- **陌生措辞仍是硬伤**：在 Banking77 每个意图内部，按测试题与最近训练样本的词面相似度排序后，最熟悉的 770 题准确率高达 **96.5%**，而最陌生的 770 题骤降至 **88.1%**——整整相差 **8.4 个百分点**。即便类别体系完全固定，应对用户从未出现过的全新问法依然是小模型的短板。

至此，CNN、BGE 与单词元 FLAN-T5 的成功都在验证同一件事：只要目标空间是有限类别 ID，分类边界就足够解决问题。而数学考卷考验的是完全不同的能力——模型能否自己构造解法。

<h2 id="training-subsets-zh">只留四分之一训练题，覆盖选样值不值</h2>

既然模型参数可以大幅压缩，训练数据能不能也同步削减 75%？用冻结的 BGE 提取所有训练题干向量，在完全不看答案的前提下采用贪心 k-center 选样（每步挑出距离已选集合最远的样本）[6](#ref-6-zh)，并与同预算的随机抽样在三个随机种子上对比完整测试集表现。

<figure>
<img src="{{ '/assets/how-big-a-model-for-one-benchmark/subset-coverage-zh.svg' | relative_url }}" alt="在 25% 训练预算下，三次随机种子中语义覆盖选样相对随机抽样的完整测试准确率差值" loading="lazy">
<figcaption><strong>图 2 · 25% 训练预算下，语义覆盖选样与随机抽样的对照。</strong> 空心圆点代表三次单独抽样种子的测试准确率差值，深色菱形为三次均值。覆盖选样在 Banking77 上稳定有效，在 CLINC150 上方差极大，在 GSM8K 上反而帮了倒忙。</figcaption>
</figure>

结果同样按任务类型出现了明显分化：

- **Banking77（2,250 条样本）**：两种选样在三次试验中都覆盖了全部 77 个类别，但语义覆盖依然稳定多答对 **24、16、28 道**（平均 +0.74 个百分点）。同一个意图内部选哪些代表性问法，确实会影响泛化。
- **CLINC150（3,775 条样本）**：三次种子成绩波动剧烈（分别为 **+225、+171 与 −119 道**，平均 +1.68 个百分点）。如果只挑选表现最好的一次汇报，很容易高估该策略的稳定性。
- **GSM8K（1,681 条样本）**：虽然覆盖选样每次都让线性分类器见到了更多种标准答案，测试表现却两次落败（−12 道、−16 道）、一次持平（平均 −0.71 个百分点）。事实上，即便用上全部训练集（1,319 道测试题中有 1,226 道的标准数字都在训练答案里出现过），直接把数字当标签分类也只能答对 49 道，只比永远盲猜最高频数字 `4`（蒙对 35 道）强一点点。

把底层换成能逐词生成答案的 FLAN-T5-small，同样在 1,681 题预算下微调两轮，反差更加刺眼：随机抽样答对 26 道，题面语义覆盖选样却跌到 13 道。即便破例读取人工解答，将题目按“先乘后减”等运算顺序分类：强行挑满 1,681 种不同运算顺序，准确率反而跌至 **10 道**；按各类顺序在全集中的原始占比分配名额（仅覆盖 760 种常见顺序），成绩才回到 **27 道**。一味追求多样性，让 1,191 个训练名额浪费在全集中仅出现过一次的冷门解上（随机抽样仅占 315 个），反而稀释了小模型最需要反复练习的高频推理模式。

<h2 id="executable-solutions-zh">让数学模型输出可执行的中间结构</h2>

GSM8K 的训练集同时附带了解题步骤与最终数字。[7](#ref-7-zh) 从同一组 FLAN-T5-small 权重出发，在全部 6,725 道题上比较五种监督方式（测试时仅输入题干，贪心解码一次；直接输出数字限 12 个词元，输出算式或程序限 72 个词元），可以清楚看到瓶颈究竟卡在哪里。

<div class="bm-table bm-table-wide" role="region" aria-label="GSM8K 不同监督方式对照" tabindex="0" markdown="1">

| GSM8K 监督与答题方式 | 答对 / 1,319 | 准确率 |
| --- | ---: | ---: |
| 预训练底座直接作答 | 9 | 0.68% |
| 仅监督最终数字 | 27 | 2.05% |
| 监督算式与最终答案 | 36 | 2.73% |
| 用计算器重算模型输出的最后一道算式 | 50 | 3.79% |
| 监督完整可执行算术程序并交由执行器求值 | 123 | 9.33% |

</div>

看两道错题就能明白为什么单改最后一步远远不够。一题问“五个派各切八块，还剩十四块，用掉多少？”模型列对了 `5 × 8` 和 `40 − 14`，却在末尾顺手算成 21——用外部计算器重算最后一道算式即可救回 26。另一题有 16 个鸭蛋，吃掉 3 个、烘焙用掉 4 个，其余每个卖 2 美元，模型竟凭空捏造出 `72` 个待售鸭蛋，并写出 `72 × 2 = 168`。计算器能把末尾乘法修成 144，却救不了前序推理幻觉（正确答案是 18）。在 1,294 条可解析输出上，外部计算器救回 36 题的同时改错了 22 题，净增仅 14 题。

真正的跃迁来自把整套解题逻辑编译为可引用的算术程序：后一步可以调用前一步的变量名，将所有四则计算彻底外包给确定性执行器。6,725 道训练题中有 6,295 道成功编译并验证还原出标准答案（其余 430 道保留数值监督）。测试集上，程序化模型一举拿下 **123 道**——救回直接生成数字时做错的 119 道、仅丢掉 23 道，净增 **96 道**（其中 189 条无法执行的程序全部判错）。把随机选样的直接报数数据从 1,681 题翻四倍到 6,725 题，只让模型多对 1 道题（`26 → 27`）；而在同样的 6,725 题上把监督目标重构为可执行程序，成绩直接翻了四倍多。

至于难度更高的竞赛数学，小模型的容量底线更加冷酷。用截至 2018 年的 770 道历年 AIME 真题微调直接输出的 FLAN-T5-small（以 2019–2023 年 149 题做验证），在 2026 年两场全部 30 道新题上得分为 **0 / 30**，而 GPT-5.5（xhigh）同卷四次独立尝试平均达到 100.00%。[4](#ref-4-zh) [8](#ref-8-zh) [9](#ref-9-zh) 在 7,700 万参数和 12 词元的硬约束下，靠直接拟合往年答案根本无法触及长链条符号构造。

<h2 id="compute-cost-zh">如何估算专精模型的真实成本</h2>

<div class="bm-table bm-table-wide" role="region" aria-label="本地训练适配耗时与推理延迟" tabindex="0" markdown="1">

| 本地任务与方案 | 部署参数量 | 任务适配耗时 | 单条延迟 p50 / p95 |
| --- | ---: | ---: | ---: |
| Banking77，随机初始化卷积 | 19.8 万 | 7 秒 | 0.7 / 1.1 ms |
| Banking77，冻结 BGE 加线性头 | 3,324 万 | 29 秒 | 11.0 / 14.7 ms |
| Banking77，全量微调 BGE | 3,324 万 | 59 秒 | 9.1 / 11.3 ms |
| CLINC OOS+，全量微调 BGE | 3,327 万 | 79 秒 | 10.9 / 17.2 ms |
| GSM8K，FLAN 直接输出数字 | 7,696 万 | 136 秒 | 58.7 / 64.7 ms |
| GSM8K，FLAN 输出算式与答案 | 7,696 万 | 176 秒 | 439.4 / 775.9 ms |
| GSM8K，FLAN 生成可执行程序 | 7,696 万 | 168 秒 | 230.3 / 381.0 ms |

</div>

表中每一项都在同一张 8 GB GTX 1070 上独立实测。任务适配耗时包含该方案所需的训练编码、搜索或验证；单条延迟从原始文本进入分词器算起，直至输出标签或数值（预热后 CNN 与 BGE 各测 100 条，FLAN 测 40 条）。冻结版 Banking77 仅需优化 29,645 个线性系数，但部署时仍须加载完整 BGE 编码器；若计算 19.8 万参数卷积学生的蒸馏成本，还需在教师训练之外额外计入约 18 秒的软标签生成时间。作为对比，公开评测中带检索示例的 Luna 在 Banking77 与 CLINC 上的单次中位 API 延迟分别为 812 ms 与 830 ms（含网络往返，未计检索本身耗时），优势在于无需针对任务做梯度更新。[1](#ref-1-zh) 同样需要说明的是，BGE-small 与 FLAN-T5-small 的上游通用预训练成本并不在这张适配表内。[10](#ref-10-zh) [11](#ref-11-zh)

这一路径在文献中早有呼应：Casanueva 等人在提出 Banking77 时便证明了双句编码器在意图分类上的高性价比；[12](#ref-12-zh) Hsieh 等人通过分步蒸馏推理理由，让 7.7 亿参数的 T5 只用 80% 的训练数据就在 ANLI 上超越了少样本提示下的 5,400 亿参数 PaLM；[13](#ref-13-zh) 而 ILLATE 的 40 亿参数专精模型在 Banking77 和 CLINC 上分别达到了 94.0% 与 95.1%。[1](#ref-1-zh)

回看这四张完整考卷，小模型专精真正区分的是**边界压缩**与**结构构造**两类问题。在 CLINC150 上，3,327 万参数与 79 秒微调就足以在当前流量配比下追上闭源检索方案；但在 GSM8K 上，即便九成以上的标准答案早已出现在训练集里，模型缺的依然是把自然语言翻译成中间运算结构的能力。面对任何一项新任务，真正值得先问的诊断问题是：在投入算力微调之前，我们能否直接从样本中判断，一个轻量模型缺的究竟是更清晰的分类边界，还是另一种可执行的中间表示？

<h2 id="references-zh">参考资料与数据来源</h2>

<ol class="bm-references">
<li id="ref-1-zh">ILLATE. <a href="https://illate.dev/luna-vs-fine-tuned-model">Luna vs. Fine-Tuned Models: Intent Evaluation Protocol, Breakdown, and Timing</a>. 评测报告与延迟口径。</li>
<li id="ref-2-zh">ILLATE. <a href="https://illate.dev/bakeoff.json">Reported Intent Benchmark Scores (JSON)</a>. 工单测试原始分数。</li>
<li id="ref-3-zh">GSM8K Evaluation Reference. <a href="https://arxiv.org/abs/2602.13217">arXiv:2602.13217</a>. GSM8K 闭源对照基线。</li>
<li id="ref-4-zh">MathArena. <a href="https://matharena.ai/?comp=aime--aime_2026&amp;view=problem">AIME 2026 Evaluation Results by Problem</a>. 2026 年竞赛数学逐题榜单。</li>
<li id="ref-5-zh">Larson et al. <a href="https://github.com/clinc/oos-eval/tree/828f8093932c8fe6ca7936c3d2e52903b1c523de/data">CLINC150 Out-of-Scope Evaluation Data and Splits</a>. 原始数据与 OOS+ 切分。</li>
<li id="ref-6-zh">Sener &amp; Savarese. <a href="https://openreview.net/forum?id=H1aIuk-RW">Active Learning for Convolutional Neural Networks: A Core-Set Approach</a>. ICLR 2018（贪心 k-center 覆盖选样）。</li>
<li id="ref-7-zh">Cobbe et al. <a href="https://github.com/openai/grade-school-math">GSM8K: Grade School Math Questions and Worked Solutions</a>. 原始题目与分步解答。</li>
<li id="ref-8-zh">Schmid, P. <a href="https://huggingface.co/datasets/philschmid/AIME_1983_2024">AIME 1983–2024 Historical Problem Dataset</a>. 历年 AIME 训练数据集。</li>
<li id="ref-9-zh">MathArena. <a href="https://huggingface.co/datasets/MathArena/aime_2026">AIME 2026 Problem Set</a>. 2026 年 AIME 试题集。</li>
<li id="ref-10-zh">BAAI. <a href="https://huggingface.co/BAAI/bge-small-en-v1.5">bge-small-en-v1.5 Pretrained Embedding Checkpoint</a>. BGE-small 底座权重。</li>
<li id="ref-11-zh">Google. <a href="https://huggingface.co/google/flan-t5-small">flan-t5-small Pretrained Checkpoint</a>. FLAN-T5-small 底座权重。</li>
<li id="ref-12-zh">Casanueva et al. <a href="https://aclanthology.org/2020.nlp4convai-1.5/">Efficient Intent Detection with Dual Sentence Encoders</a>. NLP4ConvAI 2020（Banking77）。</li>
<li id="ref-13-zh">Hsieh et al. <a href="https://aclanthology.org/2023.findings-acl.507/">Distilling Step-by-Step! Outperforming Larger Language Models with Less Training Data and Smaller Model Sizes</a>. Findings of ACL 2023。</li>
</ol>

</div>

</div>

<script src="{{ '/assets/js/blog-article.js' | relative_url }}" defer></script>
