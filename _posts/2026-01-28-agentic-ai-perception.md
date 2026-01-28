---
title: "The Commitment Gap: Why LLMs Struggle with System 2 Reasoning and the Case for a Cognitive Kernel"
date: 2026-01-28
layout: default
author_profile: true
---
# The Commitment Gap: Why LLMs Struggle with System 2 Reasoning and the Case for a Cognitive Kernel

Large Language Models have become extremely good at fast, fluent, intuitive generation. This looks like what cognitive science often calls System 1: quick pattern matching that produces plausible answers with little explicit deliberation. However, when we push LLMs into complex software engineering, scientific workflows, and long-horizon decision making, a recurring failure mode becomes hard to ignore. Bigger models and more data improve average performance, but they do not reliably produce the kind of structured, reversible, constraint-respecting reasoning we expect from System 2.

This essay argues that the gap is not only about model size or training data. It is about the structure of inference. We should stop treating an LLM as a standalone brain and instead treat it as a probabilistic proposer inside a deterministic control loop that enforces commitments, checks constraints, and manages working memory. I call this control loop a **Cognitive Kernel**.

## 1. The fallacy of incremental commitment

Autoregressive generation factorizes language as a sequence of conditional predictions, selecting the next token based on the current prefix. The issue is not that the model is Markovian. It is conditioned on the full history. The issue is that the decoding process is incremental and locally committed.

Once the model commits to a token, that decision becomes part of the context for every future token. If the decision was slightly wrong, the model has two options. It can correct itself explicitly, which is hard because it must admit inconsistency while preserving coherence. Or it can maintain surface coherence by constructing a plausible continuation that retroactively supports the earlier choice. In long-horizon settings, the second option is often easier. This is one root of hallucination and reasoning after commitment.

A useful way to name the problem is the **Commitment Gap**. LLM decoding commits locally, while System 2 reasoning often behaves as if it can postpone commitment until enough evidence has been gathered.

## 2. System 2 is not a prompt, it is a process

System 2 is often described as slow, attention-demanding, and resource-intensive. But what matters for engineering is not the metaphor. What matters is the process shape.

System 2-like behavior usually includes at least three properties.

First, it represents constraints explicitly and checks them against candidate actions.  
Second, it can compare alternatives before finalizing a decision.  
Third, it can revise or backtrack when verification fails.

A plain LLM prompt does not guarantee these properties. A chain-of-thought prompt may encourage longer deliberation, but it does not create an explicit mechanism that enforces verification or reversible search. Fluency can increase without increasing correctness.

## 3. The Cognitive Kernel: a minimal architecture

The Cognitive Kernel is a control loop around the LLM that separates proposing from committing. The LLM remains valuable because it is a strong generator of hypotheses, plans, and candidate actions. The kernel adds the missing structure: verification, memory scheduling, and commitment control.

At minimum, the kernel has three components.

### 3.1 The Shell: a constrained interface to the world

The kernel does not let the LLM interact with the environment through raw text alone. Instead, the shell exposes a small set of structured operations.

A task is represented as objectives and constraints. Actions are represented as tool calls or state updates. The shell ensures that proposals are evaluated in a consistent format, rather than being mixed with free-form narrative.

This is not about prompt engineering. It is about enforcing a stable interface so downstream checks are possible.

### 3.2 The Scheduler: working memory is not a flat context window

Large context windows help, but they are not the same as working memory. A long window is a passive buffer. Working memory is an active process that decides what to keep, what to retrieve, and what to foreground.

The scheduler selects which evidence enters the active context at a given step. It can use retrieval, summarization, or task-specific indexing. The key design is that selection is explicit and revisable, rather than being an accidental artifact of what happened to be written earlier.

### 3.3 The Verifier: proposal-verification loop

This is the core. The verifier is a module that produces an explicit pass or fail signal for a proposed action, with a reason anchored in constraints or checks.

The verifier can be implemented in multiple ways.

For code, it might run unit tests, type checks, or static analyzers.  
For math, it might call a symbolic checker, or validate intermediate steps against known invariants.  
For tool-using agents, it might check whether the proposal violates declared constraints or contradicts observed environment state.

The most important shift is that verification happens before commitment. If a proposal fails verification, the kernel forces a revision step.

## 4. A concrete example: code patching with enforced verification

Consider a task: fix a bug in a function that parses dates.

A plain LLM often produces a patch quickly, but the patch can be subtly wrong. With a Cognitive Kernel, the loop looks like this.

The proposer generates a patch candidate.  
The shell applies the patch in a sandbox.  
The verifier runs tests and a linter.  
If tests fail, the scheduler retrieves the failing test case and relevant function signature.  
The proposer generates a revised patch conditioned on the failure evidence.  
The kernel repeats until a patch passes or a budget limit is reached.

This loop is simple, but it changes failure dynamics. The system no longer relies on the model to be honest in text. It relies on explicit verification signals.

## 5. Two minimal equations, and what they mean

The kernel selects actions that are both useful and compliant by combining a utility signal with a verification signal.

### 5.1 Verification-conditioned acceptance

Let `a` be a proposed action at state `s`. Let `V(a,s)` be the verifier pass or fail.

The kernel only commits if the verifier passes.

\[
Commit(a \mid s) = \mathbb{1}[V(a,s)=1]
\]

### 5.2 Utility under constraints

When multiple passing actions exist, choose the best one under the verifier constraint.

\[
a^{*} = \arg\max_{a \in \mathcal{A}(s)} U(a,s) \quad \text{s.t.} \quad V(a,s)=1
\]

## 6. Why this changes scaling

Scaling training compute improves the proposer. Adding a kernel scales inference structure. You can trade time for reliability by exploring multiple proposals and rejecting those that fail verification.

The practical lesson is that strong reasoning in real workflows is a system property. It cannot be reduced to a single model call.

## Closing

LLMs are powerful proposers, but System 2-like reliability requires more than fluent chain-of-thought. It requires a mechanism that controls commitment, manages working memory, and enforces verification before actions become final.

The Cognitive Kernel is one way to formalize that mechanism. The future may look less like a chatbot and more like a probabilistic engine running inside an operating system for reasoning.