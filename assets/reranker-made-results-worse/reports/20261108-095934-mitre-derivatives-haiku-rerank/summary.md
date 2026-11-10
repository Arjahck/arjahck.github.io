---
layout: default
title: sift-eval — mitre-derivatives-haiku-rerank
---
# sift-eval — mitre-derivatives-haiku-rerank

2026-11-08 09:59:34 UTC · 155 questions · git `574fc23` · judge: skipped

## Find (155 questions, 0 errors)

| stage | level | R@1 | P@1 | C@1 | R@3 | P@3 | C@3 | R@5 | P@5 | C@5 | R@10 | P@10 | C@10 | MRR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| retrieved | doc | 0.600 | 0.642 | 0.563 | 0.768 | 0.307 | 0.742 | 0.808 | 0.196 | 0.781 | 0.881 | 0.110 | 0.861 | 0.734 |
| retrieved | chunk | 0.531 | 0.563 | 0.503 | 0.709 | 0.287 | 0.682 | 0.762 | 0.184 | 0.735 | 0.831 | 0.105 | 0.808 | 0.666 |
| final | doc | 0.743 | 0.788 | 0.702 | 0.848 | 0.336 | 0.821 | 0.861 | 0.208 | 0.834 | 0.887 | 0.111 | 0.868 | 0.838 |
| final | chunk | 0.634 | 0.669 | 0.603 | 0.775 | 0.309 | 0.748 | 0.801 | 0.195 | 0.775 | 0.838 | 0.106 | 0.815 | 0.744 |

| latency (ms) | mean | p50 | p95 | max | n |
|---|---|---|---|---|---|
| embed | 161 | 161 | 165 | 169 | 155 |
| retrieve | 36 | 36 | 37 | 38 | 155 |
| collapse | 8 | 8 | 9 | 10 | 155 |
| rerank | 1430 | 1234 | 2596 | 3039 | 155 |
| recap | 0 | 0 | 0 | 0 | 155 |
| total | 1636 | 1438 | 2804 | 3246 | 155 |

## By tag

| tag | n | find.doc_hit@1 |
|---|---|---|
| alias | 8 | 0.875 |
| ambiguous | 2 | 1.000 |
| ambiguous-domain | 3 | 0.333 |
| attribution | 5 | 1.000 |
| campaign | 32 | 0.833 |
| command | 2 | 0.500 |
| comparison | 10 | 0.700 |
| count | 2 | 1.000 |
| cross-domain | 2 | 1.000 |
| dates | 3 | 1.000 |
| detection | 5 | 1.000 |
| disambiguation | 2 | 1.000 |
| edge | 66 | 0.879 |
| enterprise | 91 | 0.820 |
| exact-text | 3 | 1.000 |
| explicit-unknown | 2 | 0.500 |
| false-premise | 2 | 1.000 |
| group | 22 | 0.773 |
| hierarchy | 3 | 1.000 |
| ics | 41 | 0.667 |
| id-as-name | 2 | 1.000 |
| id-lookup | 6 | 0.833 |
| keywords | 65 | 0.794 |
| list-answer | 2 | 1.000 |
| metadata | 5 | 1.000 |
| mitigation | 15 | 0.667 |
| mobile | 16 | 0.938 |
| multi-answer | 5 | 1.000 |
| multi-file | 4 | 1.000 |
| multi-hop | 9 | 0.444 |
| near-duplicate | 10 | 0.600 |
| negative-answer | 3 | 0.667 |
| nested-id | 2 | 1.000 |
| number | 9 | 0.667 |
| open-ended | 3 | 1.000 |
| paraphrase | 13 | 0.615 |
| procedure | 5 | 0.600 |
| punctuation | 2 | 1.000 |
| real-incident | 2 | 1.000 |
| recent | 4 | 0.750 |
| renamed | 4 | 1.000 |
| reword | 12 | 0.500 |
| same-name-twin | 6 | 1.000 |
| scenario | 65 | 0.873 |
| set-difference | 2 | 0.500 |
| software | 15 | 0.600 |
| special-chars | 2 | 0.500 |
| sub-technique-id | 2 | 0.500 |
| tactic | 23 | 0.857 |
| technique | 41 | 0.829 |
| temporal | 2 | 1.000 |
| unanswerable | 4 | — |
| variant | 142 | 0.804 |
| version-sensitive | 5 | 1.000 |
| yes-no | 3 | 1.000 |
