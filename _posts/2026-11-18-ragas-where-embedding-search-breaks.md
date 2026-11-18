---
layout: post
title: Using RAGAS to understand and measure RAG and understand what RAGAS metrics can't see
date: 2026-11-18
description: 'I scored 306 answers from my RAG with RAGAS and two LLM judges. One answer named the wrong malware and still scored 0.56 on answer correctness, the only metric that compares it with the reference answer.'
---

When a model answers with information from a RAG (retrieval-augmented generation) system, there's a risk that its answers are hallucinated. It's therefore critical to actively measure such a setup by analyzing its answers for things like relevance, context and, most importantly, quality.

It's important to note that RAG systems are often used in applications where the generated text has to be factually consistent with the sources.


## RAGAS

RAGAS (Retrieval Augmented Generation Assessment) is a framework that measures the quality of generated content fully automatically.
The idea behind the automation is basically to use an LLM as a judge (AI-as-a-judge) and focus on measuring three quality aspects over a dataset:

- **Faithfulness:** how well is the answer grounded in the context? (key to avoiding hallucinations)

  How to measure: An LLM breaks the answer down into statements and then rates each one against the context (1 if valid, 0 if not). The number of valid statements is then divided by the total number of statements.

  Formula: `F = |V| / |S|`, V the valid statements, S all statements.

- **Answer Relevance:** does the generated answer address the actual question?

  How to measure: An LLM reverse-generates questions from the answer being measured. Those questions are embedded, and the cosine similarity with the original question is calculated and averaged.

  Formula: `AR = (1/n) · Σ sim(q, q_i)`, q the original question, q_i the n generated questions, sim the cosine similarity.

- **Context Relevance:** how focused is the retrieved context (does it contain as little irrelevant information as possible)?

  How to measure: An LLM extracts every sentence from the context that is needed to answer the question. The number of extracted sentences is then divided by the total number of sentences in the context.

  Formula: `CR = extracted sentences / all sentences in the context`

More details can be found in the [RAGAS paper](https://arxiv.org/pdf/2309.15217).

*Note:* All three metrics return a value between 0 and 1, with 1 being the best.


## System 

Condense is a self-hosted search engine for a folder of documents. It's a RAG (retrieval-augmented generation) system that first retrieves the passages that match a question, then lets a language model write from them. Condense works in two phases. A first "ingest" phase, turns every file into searchable chunks. A second "find" phase, runs for every question and returns a single result: the best-matching file and page.

A more detailed description of the system can be found in the [System section](https://arjahck.github.io/2026/11/09/reranker-made-results-worse/#system) of my previous post.

To implement RAGAS into a separate evaluation tool called "condense-eval". It's part of the Condense repository and runs every question of the dataset through the same pipeline as the product, with fix configuration. This lets it see what the API hides: the full ranking, the exact passages the LLM read before answering, and how long each stage took.

For RAGAS, the important part is the answer. Find returns a file and page, but in addition, an LLM writes a short answer from the first three passages, the "recap". The tool records this answer together with the passages it was written from. It then hands both to RAGAS, together with the question and the reference answer from the dataset. RAGAS uses an LLM as the judge and returns one score per metric and question. Finally, the tool averages the scores per question set and per tag.

*Note:* The retrieval metrics of the previous post (precision@k, recall@k, MRR) are computed directly from the ranking and need no judge.

In my case, the same answers were judged twice: once by Mistral Small 4 and once by Claude Haiku 5.5.


## Data

MITRE ATT&CK (version 20.1) has been chosen as test data because of its complexity, depth and security topic.
The dataset is made out of 332 questions: 112 question/answer (reference) pairs of various difficulties (easy to very hard, plus edge cases) and 220 derivatives of them (keywords, scenario, paraphrase, reword and German). 26 of them are unanswerable, which leaves 306 answerable questions.

How the dataset was created is described in the [Data section](https://arjahck.github.io/2026/11/09/reranker-made-results-worse/#data) of my previous post.

## Measurement

In the previous post, I used question m03 to explain the retrieval metrics. For RAGAS, I picked its harder version, vh01. It asks about the same malware, but needs several steps to answer:

> Several of Cozy Bear's malware families leaned on Twitter as a backup command channel. Which one was only in use from 2013 to 2015, and how does ATT&CK classify its Twitter use differently from CozyCar's?

The right answer is OnionDuke.

ATT&CK classifies OnionDuke's Twitter use as T1102.003 Web Service: One-Way Communication, and CozyCar's as T1102.002 Web Service: Bidirectional Communication. To get there, the system has to resolve the alias Cozy Bear to APT29, pick out OnionDuke by its years (APT29 / Cozy Bear also used MiniDuke and CozyCar with Twitter, both from 2010 to 2015), and then compare two files.

This is exactly where the embedding search breaks. APT29's own file, which lists Cozy Bear as an alias, isn't among the 30 candidates. Instead, the CozyCar file takes ranks 1 and 2, probably because it lists "CozyBear" as one of its aliases. The OnionDuke file, the only one with the years 2013 to 2015, lands on rank 10. After the rerank, the recap reads three passages:

1. a part of the T1102.003 technique file that lists OnionDuke, UPSTYLE and other malware, without any years
2. the first part of the CozyCar file (aliases, description, "used by APT29 from 2010 to 2015")
3. the second part of the CozyCar file, which classifies its Twitter use as T1102.002.

The answer is only half right:

> **UPSTYLE** was only in use from 2013 to 2015, and ATT&CK classifies its Twitter use as **T1102.003 Web Service: One-Way Communication**, whereas CozyCar's Twitter use is classified under **T1102.002 Web Service: Bidirectional Communication**.
>
> - UPSTYLE's timeframe is not explicitly stated in the passages, but it is the only malware family listed alongside OnionDuke, Metamorfo, EVILNUM, and Sagerunex as using Twitter for C2 in passage [1], which focuses on T1102.003.
> - CozyCar's Twitter use is explicitly classified under **T1102.002** in passage [3].


The two classifications are right, but the malware is wrong. According to passage 1, UPSTYLE doesn't even use Twitter (it "parses encoded commands from error logs"), and the recap itself admits that the years aren't in the passages.

Now that we have the answer for the question vh01 we use the "condense-eval" AI-as-a-judge to measure the result. For this we use the following prompt structure: an instruction, a JSON schema for the output, one or more worked examples and finally the input (question, answer, passages and/or reference answer). 

I only show the instruction below. The judge is Mistral Small 4.


### Faithfulness

**Judge prompt:** Faithfulness uses two prompts. The first one splits the answer into statements:

> Given a question and an answer, analyze the complexity of each sentence in the answer. Break down each sentence into one or more fully understandable statements. Ensure that no pronouns are used in any statement.

The second one checks every statement against the context (all three passages, joined into one text):

> Your task is to judge the faithfulness of a series of statements based on a given context. For each statement you must return verdict as 1 if the statement can be directly inferred based on the context or 0 if the statement can not be directly inferred based on the context.

**Output:** The judge splits the answer into seven statements and rejects three of them:

| # | Statement | Verdict |
|---|---|---|
| 1 | UPSTYLE malware was only in use from 2013 to 2015. | 0 |
| 2 | ATT&CK classifies UPSTYLE's Twitter use as T1102.003 Web Service: One-Way Communication. | 0 |
| 3 | ATT&CK classifies CozyCar's Twitter use as T1102.002 Web Service: Bidirectional Communication. | 1 |
| 4 | UPSTYLE's timeframe is not explicitly stated in the passages. | 1 |
| 5 | UPSTYLE is the only malware family listed alongside OnionDuke, Metamorfo, EVILNUM, and Sagerunex as using Twitter for C2 in the passage. | 0 |
| 6 | The passage focuses on T1102.003 for UPSTYLE's Twitter use. | 1 |
| 7 | CozyCar's Twitter use is explicitly classified under T1102.002 in the passage. | 1 |
{: .center}

**Measurement:** 4 valid statements / 7 statements = 0.57.

The judge catches the main error, statement 1: "The context does not provide any information about the timeframe when UPSTYLE was in use." It also rejects statement 2, because the passage never names T1102.003 (the judge only sees the text of a passage, not its file name). Strangely, it accepts statement 6, which makes almost the same claim. Statement 4 counts as faithful, because the answer is honest that the years are missing.

For me, this shows two limits of the metric: 
- A wrong answer still scores above 0.5, because the true statements around the error count as much as the error itself. 
- the judge isn't consistent: statements 2 and 6 get different verdicts.

### Answer Relevance

**Judge prompt:** The prompt runs three times, and each time it generates one question from the answer. The judge only sees the answer, not the original question:

> Generate a question for the given answer and identify if the answer is noncommittal. Give noncommittal as 1 if the answer is noncommittal (evasive, vague, or ambiguous) and 0 if the answer is substantive. Examples of noncommittal answers: "I don't know", "I'm not sure", "It depends".

**Output:** Each generated question is embedded with bge-m3 and compared with the original question by cosine similarity:

| Generated question | Cosine similarity |
|---|---|
| Which malware families used Twitter for C2 under the ATT&CK technique T1102.003? | 0.698 |
| Which malware families used Twitter for C2 under the ATT&CK technique T1102.003? | 0.698 |
| Which malware families used Twitter for C2 communication according to the passages? | 0.635 |
{: .center}

**Measurement:** (0.698 + 0.698 + 0.635) / 3 = 0.68. 

The generated questions describe what the answer talks about, a list of malware in T1102.003, and not what was asked: one malware picked by its years, and a comparison with CozyCar. Still, the wrong answer gets a decent 0.68. 

Answer relevance measures how close the generated questions are to the original question, not if the answer is actually correct.


### Context Utilization

condense-eval doesn't compute context relevance as described in the paper but context utilization: for every passage, the judge decides if it was useful for the answer. A useful passage on a high rank counts more than one further down.

Formula: `CU = Σ (precision@k · v_k) / Σ v_k`, v_k the verdict for the passage at rank k (0 or 1), precision@k the share of useful passages in the first k.

**Judge prompt:** The prompt runs once per passage:

> Given question, answer and context verify if the context was useful in arriving at the given answer. Give verdict as "1" if useful and "0" if not with json output.

**Output:**

| Rank | Passage | Verdict | Reason (shortened) |
|---|---|---|---|
| 1 | T1102.003 (list of malware) | 1 | "The answer correctly identifies UPSTYLE as the malware family in use from 2013 to 2015" |
| 2 | S0046_cozycar.md (first part) | 0 | "does not mention UPSTYLE or its timeframe (2013-2015) [...] It only describes CozyCar and its attributes" |
| 3 | S0046_cozycar.md (second part) | 1 | "explicitly mentions CozyCar's use of Twitter as a backup C2 channel under T1102.002" |
{: .center}

**Measurement:**  (1 + 0.67) / 2 = 0.83.

The judge checks if a passage was useful for the answer that was given, not for the right answer. Passage 2 holds exactly what is needed to rule out CozyCar ("used by APT29 from 2010 to 2015"), but the wrong answer doesn't use it, so it counts as not useful. Worse, the judge even calls the wrong answer correct in its reason for passage 1.

### Answer Correctness

Answer correctness is the only metric in this post that compares the answer with the reference answer. An LLM sorts the statements of both into true positives (TP), false positives (FP) and false negatives (FN). The F1 score is then combined with the cosine similarity of the two texts.

Formula: `AC = 0.75 · F1 + 0.25 · sim(a, r)`, with `F1 = |TP| / (|TP| + 0.5 · (|FP| + |FN|))`, a the answer, r the reference answer.

> **Reference answer:** OnionDuke (S0052). ATT&CK classes its Twitter backup C2 as T1102.003 Web Service: One-Way Communication, while CozyCar's Twitter backup channel is T1102.002 Web Service: Bidirectional Communication.

**Measurement:** 3 TP, 3 FP and 3 FN give F1 = 0.50. With a similarity of 0.74: AC = 0.75 · 0.50 + 0.25 · 0.74 = 0.56.

The main error, UPSTYLE instead of OnionDuke, counts as a true positive twice: the judge reads it as "OnionDuke (likely a reference to UPSTYLE)". Even with the reference answer, the judge misses the one fact that matters.

### Two judges

The same answer, scored by both judges (recorded runs). The Mistral values differ from the walkthrough above, which comes from re-scoring the same answer: the judge isn't deterministic (see Limitations).

| Metric | Mistral Small 4 | Claude Haiku 5.5 |
|---|---|---|
| Faithfulness | 0.43 | 0.38 |
| Answer relevance | 0.66 | 0.69 |
| Context utilization | 0.83 | 0.00 |
| Answer correctness | 0.56 | 0.58 |
{: .center}

The two judges agree that the answer is mostly not grounded in the passages. However, they disagree completely on the passages. Haiku rates none of the three as useful.

In the end, the wrong malware costs the answer little: answer correctness, the only metric that checks the answer against the reference, still gives it 0.56 and 0.58.

## Evaluation

The following tables sum up the runs. The answers are the same in both tables, only the judge changes. They show the average of the three RAGAS metrics for the Find recap answers, over all answerable questions of a question set (number in brackets). 

**Judge: Mistral Small 4**

| Metric | Golden (92) | English derivatives (151) | German (63) |
|---|---|---|---|
| Faithfulness | 0.92 | 0.89 | 0.92 |
| Answer relevance | 0.75 | 0.71 | 0.78 |
| Context utilization | 0.86 | 0.86 | 0.84 |
{: .center}

**Judge: Claude Haiku 5.5**

| Metric | Golden (92) | English derivatives (151) | German (63) |
|---|---|---|---|
| Faithfulness | 0.83 | 0.75 | 0.81 |
| Answer relevance | 0.79 | 0.73 | 0.82 |
| Context utilization | 0.75 | 0.80 | 0.79 |
{: .center}

**Differences between the judges:** 

- **Haiku is stricter on faithfulness:** Its averages are 0.09 to 0.14 lower. Out of all answers scored, Mistral gave the higher faithfulness score 116 times, Haiku only 29 times. My guess: Mistral Small 4 also wrote the answers, and models tend to grade their own answers generously.
- **The averages hide large differences on single answers:** On some answers, the two judges disagree completely, e.g. context utilization for vh01.
- **The values only make sense under the same judge:** For faithfulness and answer relevance, both rank the question sets in the same order, but the values differ (max 0.14). For context utilization, even the order flips. Two runs can therefore only be compared under the same judge.
- **Mistral generates the same question several times.** RAGAS sends a temperature of 0.01 to Mistral, so its three generated questions are often identical (as in vh01). Haiku runs with the API's default temperature (Claude reject the 0.01 temperature setting).

**When the retrieval fails:** Combining the retrieval data with the judges finally shows where the answers break. For 37 of the 306 answerable questions, the right file isn't among the three passages the recap reads:

| Metric (Mistral / Haiku) | Right file in the passages (269) | Right file missing (37) |
|---|---|---|
| Faithfulness | 0.92 / 0.83 | 0.78 / 0.51 |
| Answer relevance | 0.74 / 0.76 | 0.73 / 0.77 |
| Context utilization | 0.87 / 0.81 | 0.73 / 0.56 |
{: .center}

- **Answer relevance doesn't move at all (pretty useless here)** 
- **Faithfulness drops a little with Mistral and a lot with Haiku**

## What I learned

- RAGAS allows to turn subjective checks of RAG outputs into more objective, repeatable metrics. Allowing to diagnose whether poor answers come from bad document retrieval or model hallucination (or both in my case).
- RAGAS is an automated and scalable way to measure the quality of answers. However, its three core metrics never compare the answer with a reference answer, so a wrong answer can still score well (vh01). Answer correctness does compare, but the judge still counted the wrong malware as correct.
- Using the same LLM to write and to judge the answers risks a generous judge (my guess: Mistral Small 4 scored its own answers higher).
- Swapping the judge changes the results. Runs can only be compared under the same judge.
- Answer relevance can't see a retrieval failure.


## Limitations

- **Judge bias:** LLM judges tend to favor longer, more detailed answers. In faithfulness, extra true statements also dilute an error (vh01).
- **One judge run:** The judge isn't deterministic: re-scoring vh01 changed its faithfulness from 0.43 to 0.57.
- **Public data:** MITRE ATT&CK is very likely part of the training data of both judges.

## Appendix

**Resources:**

- [Condense](https://github.com/AetherisAI/condense): the RAG system used in this post, including the evaluation harness "condense-eval"
- [RAGAS](https://github.com/explodinggradients/ragas): the evaluation framework used by "condense-eval" (version 0.4.3)
- [MITRE ATT&CK](https://attack.mitre.org): the knowledge base used as test data (version 20.1)
- [Mistral Small 4](https://docs.mistral.ai): the reranker, the recap writer and the first judge (API name mistral-small-latest, currently mistral-small-2603)
- [Claude Haiku 5.5 and Opus 5.5](https://docs.anthropic.com/en/docs/about-claude/models): the second judge, and the model used to create the dataset

**Reports and data:**

Every run has a report with more data than this post shows, including metrics left out here (e.g. answer recall). Both judges scored the same answers.

| Question set | Judge: Mistral Small 4 | Judge: Claude Haiku 5.5 |
|---|---|---|
| Golden | [report](/assets/reranker-made-results-worse/reports/20261107-130230-mitre-base/summary/) | [report](/assets/ragas-where-embedding-search-breaks/reports/20261107-130230-mitre-base-judge-haiku/summary/) |
| English derivatives | [report](/assets/reranker-made-results-worse/reports/20261107-160648-mitre-derivatives/summary/) | [report](/assets/ragas-where-embedding-search-breaks/reports/20261107-160648-mitre-derivatives-judge-haiku/summary/) |
| German | [report](/assets/reranker-made-results-worse/reports/20261107-173114-mitre-de/summary/) | [report](/assets/ragas-where-embedding-search-breaks/reports/20261107-173114-mitre-de-judge-haiku/summary/) |
{: .center}

- Golden and silver dataset: [silver.jsonl](/assets/reranker-made-results-worse/silver.jsonl)
