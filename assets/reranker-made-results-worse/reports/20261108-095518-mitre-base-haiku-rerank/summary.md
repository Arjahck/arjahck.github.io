---
layout: default
title: "condense-eval: mitre-base-haiku-rerank"
---
# condense-eval: mitre-base-haiku-rerank

2026-11-08 09:55:18 UTC · 112 questions · git `574fc23` · judge: skipped

## Find (112 questions, 0 errors)

| stage | level | R@1 | P@1 | C@1 | R@3 | P@3 | C@3 | R@5 | P@5 | C@5 | R@10 | P@10 | C@10 | MRR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| retrieved | doc | 0.737 | 0.783 | 0.696 | 0.864 | 0.333 | 0.837 | 0.902 | 0.215 | 0.880 | 0.946 | 0.118 | 0.924 | 0.844 |
| retrieved | chunk | 0.650 | 0.685 | 0.620 | 0.799 | 0.315 | 0.772 | 0.848 | 0.207 | 0.826 | 0.891 | 0.114 | 0.870 | 0.762 |
| final | doc | 0.835 | 0.891 | 0.783 | 0.924 | 0.355 | 0.891 | 0.940 | 0.224 | 0.913 | 0.946 | 0.118 | 0.924 | 0.927 |
| final | chunk | 0.710 | 0.761 | 0.663 | 0.848 | 0.333 | 0.815 | 0.897 | 0.217 | 0.870 | 0.902 | 0.115 | 0.880 | 0.830 |

| latency (ms) | mean | p50 | p95 | max | n |
|---|---|---|---|---|---|
| embed | 162 | 162 | 166 | 171 | 112 |
| retrieve | 35 | 36 | 37 | 38 | 112 |
| collapse | 8 | 8 | 9 | 9 | 112 |
| rerank | 1379 | 1115 | 2739 | 3280 | 112 |
| recap | 0 | 0 | 0 | 0 | 112 |
| total | 1585 | 1322 | 2947 | 3491 | 112 |

## By tag

| tag | n | find.doc_hit@1 |
|---|---|---|
| alias | 4 | 0.750 |
| ambiguous | 1 | 1.000 |
| ambiguous-domain | 1 | 1.000 |
| attribution | 10 | 0.800 |
| base | 112 | 0.891 |
| campaign | 29 | 0.913 |
| command | 1 | 1.000 |
| comparison | 5 | 0.800 |
| count | 1 | 1.000 |
| cross-domain | 1 | 1.000 |
| dates | 3 | 0.667 |
| detection | 5 | 1.000 |
| disambiguation | 1 | 1.000 |
| easy | 15 | 0.867 |
| edge | 30 | 0.933 |
| enterprise | 59 | 0.920 |
| exact-text | 1 | 1.000 |
| explicit-unknown | 1 | 0.000 |
| false-premise | 1 | 1.000 |
| group | 14 | 0.727 |
| hard | 28 | 0.846 |
| has-variants | 65 | 0.905 |
| hierarchy | 1 | 1.000 |
| ics | 32 | 0.800 |
| id-as-name | 1 | 1.000 |
| id-lookup | 4 | 1.000 |
| impact | 4 | 1.000 |
| iot | 5 | 1.000 |
| list-answer | 4 | 1.000 |
| medium | 30 | 0.933 |
| metadata | 2 | 1.000 |
| mitigation | 13 | 1.000 |
| mobile | 22 | 0.842 |
| multi-answer | 2 | 1.000 |
| multi-file | 2 | 1.000 |
| multi-hop | 7 | 0.857 |
| near-duplicate | 4 | 0.750 |
| negative-answer | 2 | 1.000 |
| nested-id | 1 | 1.000 |
| nonexistent | 1 | n/a |
| number | 14 | 0.875 |
| open-ended | 1 | 1.000 |
| original | 13 | 0.923 |
| out-of-scope | 1 | n/a |
| people | 1 | n/a |
| procedure | 3 | 0.667 |
| punctuation | 1 | 1.000 |
| real-incident | 10 | 1.000 |
| recent | 6 | 0.833 |
| renamed | 2 | 1.000 |
| same-name-twin | 5 | 1.000 |
| set-difference | 1 | 1.000 |
| software | 20 | 0.800 |
| special-chars | 1 | 1.000 |
| sub-technique-id | 1 | 1.000 |
| tactic | 9 | 0.875 |
| technique | 21 | 0.950 |
| temporal | 3 | 1.000 |
| unanswerable | 20 | n/a |
| version-sensitive | 2 | 1.000 |
| very-hard | 8 | 0.875 |
| vulnerability | 1 | n/a |
| yes-no | 5 | 0.600 |
