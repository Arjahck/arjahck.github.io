---
layout: default
title: "condense-eval: mitre-base-ce-rerank"
---
# condense-eval: mitre-base-ce-rerank

2026-11-09 23:09:37 UTC · 112 questions · git `fd7e73a` · judge: skipped

## Find (112 questions, 0 errors)

| stage | level | R@1 | P@1 | C@1 | R@3 | P@3 | C@3 | R@5 | P@5 | C@5 | R@10 | P@10 | C@10 | MRR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| retrieved | doc | 0.737 | 0.783 | 0.696 | 0.864 | 0.333 | 0.837 | 0.902 | 0.215 | 0.880 | 0.946 | 0.118 | 0.924 | 0.844 |
| retrieved | chunk | 0.650 | 0.685 | 0.620 | 0.799 | 0.315 | 0.772 | 0.848 | 0.207 | 0.826 | 0.891 | 0.114 | 0.870 | 0.762 |
| final | doc | 0.824 | 0.870 | 0.783 | 0.924 | 0.370 | 0.902 | 0.929 | 0.228 | 0.913 | 0.962 | 0.123 | 0.946 | 0.909 |
| final | chunk | 0.797 | 0.837 | 0.761 | 0.902 | 0.370 | 0.880 | 0.908 | 0.228 | 0.891 | 0.935 | 0.118 | 0.913 | 0.881 |

| latency (ms) | mean | p50 | p95 | max | n |
|---|---|---|---|---|---|
| embed | 157 | 157 | 164 | 212 | 112 |
| retrieve | 26 | 26 | 29 | 61 | 112 |
| collapse | 7 | 7 | 8 | 9 | 112 |
| rerank | 45959 | 45960 | 50940 | 53705 | 112 |
| recap | 0 | 0 | 0 | 0 | 112 |
| total | 46150 | 46152 | 51130 | 53904 | 112 |

## By tag

| tag | n | find.doc_hit@1 |
|---|---|---|
| alias | 4 | 1.000 |
| ambiguous | 1 | 1.000 |
| ambiguous-domain | 1 | 1.000 |
| attribution | 10 | 0.800 |
| base | 112 | 0.870 |
| campaign | 29 | 0.870 |
| command | 1 | 1.000 |
| comparison | 5 | 0.400 |
| count | 1 | 1.000 |
| cross-domain | 1 | 1.000 |
| dates | 3 | 1.000 |
| detection | 5 | 0.250 |
| disambiguation | 1 | 0.000 |
| easy | 15 | 1.000 |
| edge | 30 | 0.900 |
| enterprise | 59 | 0.880 |
| exact-text | 1 | 1.000 |
| explicit-unknown | 1 | 1.000 |
| false-premise | 1 | 1.000 |
| group | 14 | 0.909 |
| hard | 28 | 0.692 |
| has-variants | 65 | 0.857 |
| hierarchy | 1 | 1.000 |
| ics | 32 | 0.920 |
| id-as-name | 1 | 1.000 |
| id-lookup | 4 | 1.000 |
| impact | 4 | 1.000 |
| iot | 5 | 1.000 |
| list-answer | 4 | 1.000 |
| medium | 30 | 0.900 |
| metadata | 2 | 1.000 |
| mitigation | 13 | 0.900 |
| mobile | 22 | 0.789 |
| multi-answer | 2 | 1.000 |
| multi-file | 2 | 0.500 |
| multi-hop | 7 | 1.000 |
| near-duplicate | 4 | 0.750 |
| negative-answer | 2 | 0.500 |
| nested-id | 1 | 0.000 |
| nonexistent | 1 | n/a |
| number | 14 | 1.000 |
| open-ended | 1 | 1.000 |
| original | 13 | 1.000 |
| out-of-scope | 1 | n/a |
| people | 1 | n/a |
| procedure | 3 | 1.000 |
| punctuation | 1 | 1.000 |
| real-incident | 10 | 1.000 |
| recent | 6 | 1.000 |
| renamed | 2 | 1.000 |
| same-name-twin | 5 | 1.000 |
| set-difference | 1 | 0.000 |
| software | 20 | 0.933 |
| special-chars | 1 | 1.000 |
| sub-technique-id | 1 | 1.000 |
| tactic | 9 | 1.000 |
| technique | 21 | 0.850 |
| temporal | 3 | 0.667 |
| unanswerable | 20 | n/a |
| version-sensitive | 2 | 1.000 |
| very-hard | 8 | 0.875 |
| vulnerability | 1 | n/a |
| yes-no | 5 | 1.000 |
