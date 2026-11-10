---
layout: default
title: "condense-eval: mitre-de-haiku-rerank"
---
# condense-eval: mitre-de-haiku-rerank

2026-11-08 10:01:15 UTC · 65 questions · git `574fc23` · judge: skipped

## Find (65 questions, 0 errors)

| stage | level | R@1 | P@1 | C@1 | R@3 | P@3 | C@3 | R@5 | P@5 | C@5 | R@10 | P@10 | C@10 | MRR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| retrieved | doc | 0.632 | 0.683 | 0.587 | 0.836 | 0.317 | 0.810 | 0.844 | 0.203 | 0.810 | 0.952 | 0.122 | 0.921 | 0.786 |
| retrieved | chunk | 0.601 | 0.635 | 0.571 | 0.757 | 0.302 | 0.730 | 0.796 | 0.190 | 0.762 | 0.921 | 0.124 | 0.889 | 0.736 |
| final | doc | 0.815 | 0.873 | 0.762 | 0.915 | 0.354 | 0.873 | 0.921 | 0.222 | 0.889 | 0.952 | 0.122 | 0.921 | 0.915 |
| final | chunk | 0.696 | 0.746 | 0.651 | 0.852 | 0.344 | 0.810 | 0.889 | 0.216 | 0.857 | 0.921 | 0.124 | 0.889 | 0.822 |

| latency (ms) | mean | p50 | p95 | max | n |
|---|---|---|---|---|---|
| embed | 162 | 162 | 165 | 176 | 65 |
| retrieve | 36 | 36 | 38 | 38 | 65 |
| collapse | 8 | 8 | 9 | 9 | 65 |
| rerank | 1299 | 1067 | 2546 | 2948 | 65 |
| recap | 0 | 0 | 0 | 0 | 65 |
| total | 1506 | 1272 | 2756 | 3151 | 65 |

## By tag

| tag | n | find.doc_hit@1 |
|---|---|---|
| alias | 4 | 0.750 |
| ambiguous | 1 | 1.000 |
| ambiguous-domain | 1 | 1.000 |
| attribution | 2 | 1.000 |
| campaign | 15 | 0.929 |
| command | 1 | 1.000 |
| comparison | 5 | 0.800 |
| count | 1 | 1.000 |
| cross-domain | 1 | 1.000 |
| dates | 1 | 1.000 |
| de | 65 | 0.873 |
| detection | 2 | 1.000 |
| disambiguation | 1 | 1.000 |
| edge | 30 | 0.867 |
| enterprise | 38 | 0.919 |
| exact-text | 1 | 1.000 |
| explicit-unknown | 1 | 0.000 |
| false-premise | 1 | 1.000 |
| group | 9 | 0.889 |
| hierarchy | 1 | 1.000 |
| ics | 17 | 0.688 |
| id-as-name | 1 | 1.000 |
| id-lookup | 3 | 1.000 |
| list-answer | 1 | 0.000 |
| metadata | 2 | 1.000 |
| mitigation | 6 | 0.833 |
| mobile | 7 | 1.000 |
| multi-answer | 2 | 1.000 |
| multi-file | 2 | 1.000 |
| multi-hop | 4 | 0.750 |
| near-duplicate | 4 | 0.750 |
| negative-answer | 1 | 0.000 |
| nested-id | 1 | 1.000 |
| number | 4 | 0.750 |
| open-ended | 1 | 1.000 |
| procedure | 2 | 1.000 |
| punctuation | 1 | 1.000 |
| real-incident | 1 | 1.000 |
| recent | 2 | 0.500 |
| renamed | 2 | 1.000 |
| same-name-twin | 3 | 1.000 |
| set-difference | 1 | 1.000 |
| software | 7 | 0.571 |
| special-chars | 1 | 1.000 |
| sub-technique-id | 1 | 1.000 |
| tactic | 9 | 0.750 |
| technique | 16 | 1.000 |
| temporal | 1 | 1.000 |
| unanswerable | 2 | n/a |
| variant | 65 | 0.873 |
| version-sensitive | 2 | 1.000 |
| yes-no | 1 | 1.000 |
