---
layout: default
title: sift-eval — mitre-derivatives-ce-rerank
---
# sift-eval — mitre-derivatives-ce-rerank

2026-11-10 09:29:16 UTC · 155 questions · git `43183be` · judge: skipped

## Find (155 questions, 0 errors)

| stage | level | R@1 | P@1 | C@1 | R@3 | P@3 | C@3 | R@5 | P@5 | C@5 | R@10 | P@10 | C@10 | MRR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| retrieved | doc | 0.600 | 0.642 | 0.563 | 0.768 | 0.307 | 0.742 | 0.808 | 0.196 | 0.781 | 0.881 | 0.110 | 0.861 | 0.734 |
| retrieved | chunk | 0.531 | 0.563 | 0.503 | 0.709 | 0.287 | 0.682 | 0.762 | 0.184 | 0.735 | 0.831 | 0.105 | 0.808 | 0.666 |
| final | doc | 0.746 | 0.781 | 0.715 | 0.877 | 0.351 | 0.854 | 0.894 | 0.221 | 0.874 | 0.924 | 0.118 | 0.907 | 0.844 |
| final | chunk | 0.703 | 0.728 | 0.682 | 0.854 | 0.351 | 0.834 | 0.868 | 0.221 | 0.848 | 0.901 | 0.117 | 0.881 | 0.800 |

| latency (ms) | mean | p50 | p95 | max | n |
|---|---|---|---|---|---|
| embed | 156 | 157 | 168 | 192 | 155 |
| retrieve | 23 | 23 | 27 | 30 | 155 |
| collapse | 7 | 7 | 8 | 9 | 155 |
| rerank | 43955 | 44045 | 49100 | 51207 | 155 |
| recap | 0 | 0 | 0 | 0 | 155 |
| total | 44141 | 44231 | 49305 | 51397 | 155 |

## By tag

| tag | n | find.doc_hit@1 |
|---|---|---|
| alias | 8 | 0.875 |
| ambiguous | 2 | 1.000 |
| ambiguous-domain | 3 | 1.000 |
| attribution | 5 | 0.800 |
| campaign | 32 | 0.800 |
| command | 2 | 1.000 |
| comparison | 10 | 0.500 |
| count | 2 | 1.000 |
| cross-domain | 2 | 0.500 |
| dates | 3 | 1.000 |
| detection | 5 | 0.400 |
| disambiguation | 2 | 0.500 |
| edge | 66 | 0.848 |
| enterprise | 91 | 0.798 |
| exact-text | 3 | 1.000 |
| explicit-unknown | 2 | 1.000 |
| false-premise | 2 | 0.500 |
| group | 22 | 0.864 |
| hierarchy | 3 | 1.000 |
| ics | 41 | 0.718 |
| id-as-name | 2 | 1.000 |
| id-lookup | 6 | 1.000 |
| keywords | 65 | 0.873 |
| list-answer | 2 | 1.000 |
| metadata | 5 | 1.000 |
| mitigation | 15 | 0.867 |
| mobile | 16 | 0.812 |
| multi-answer | 5 | 0.800 |
| multi-file | 4 | 0.500 |
| multi-hop | 9 | 0.889 |
| near-duplicate | 10 | 0.500 |
| negative-answer | 3 | 0.667 |
| nested-id | 2 | 0.500 |
| number | 9 | 1.000 |
| open-ended | 3 | 1.000 |
| paraphrase | 13 | 0.692 |
| procedure | 5 | 0.600 |
| punctuation | 2 | 1.000 |
| real-incident | 2 | 1.000 |
| recent | 4 | 1.000 |
| renamed | 4 | 0.750 |
| reword | 12 | 0.583 |
| same-name-twin | 6 | 1.000 |
| scenario | 65 | 0.746 |
| set-difference | 2 | 0.500 |
| software | 15 | 0.800 |
| special-chars | 2 | 1.000 |
| sub-technique-id | 2 | 1.000 |
| tactic | 23 | 0.810 |
| technique | 41 | 0.707 |
| temporal | 2 | 0.000 |
| unanswerable | 4 | — |
| variant | 142 | 0.790 |
| version-sensitive | 5 | 1.000 |
| yes-no | 3 | 1.000 |
