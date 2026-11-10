---
layout: default
title: "condense-eval: mitre-de-ce-rerank"
---
# condense-eval: mitre-de-ce-rerank

2026-11-10 15:44:21 UTC · 65 questions · git `43183be` · judge: skipped

## Find (65 questions, 0 errors)

| stage | level | R@1 | P@1 | C@1 | R@3 | P@3 | C@3 | R@5 | P@5 | C@5 | R@10 | P@10 | C@10 | MRR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| retrieved | doc | 0.632 | 0.683 | 0.587 | 0.836 | 0.317 | 0.810 | 0.844 | 0.203 | 0.810 | 0.952 | 0.122 | 0.921 | 0.786 |
| retrieved | chunk | 0.601 | 0.635 | 0.571 | 0.757 | 0.302 | 0.730 | 0.796 | 0.190 | 0.762 | 0.921 | 0.124 | 0.889 | 0.736 |
| final | doc | 0.815 | 0.857 | 0.778 | 0.937 | 0.402 | 0.921 | 0.944 | 0.244 | 0.937 | 0.968 | 0.127 | 0.952 | 0.904 |
| final | chunk | 0.783 | 0.810 | 0.762 | 0.905 | 0.392 | 0.873 | 0.913 | 0.238 | 0.889 | 0.929 | 0.124 | 0.905 | 0.868 |

| latency (ms) | mean | p50 | p95 | max | n |
|---|---|---|---|---|---|
| embed | 159 | 157 | 172 | 187 | 65 |
| retrieve | 26 | 25 | 28 | 80 | 65 |
| collapse | 7 | 7 | 8 | 8 | 65 |
| rerank | 46050 | 45953 | 52089 | 52718 | 65 |
| recap | 0 | 0 | 0 | 0 | 65 |
| total | 46242 | 46141 | 52277 | 52931 | 65 |

## By tag

| tag | n | find.doc_hit@1 |
|---|---|---|
| alias | 4 | 1.000 |
| ambiguous | 1 | 1.000 |
| ambiguous-domain | 1 | 1.000 |
| attribution | 2 | 1.000 |
| campaign | 15 | 0.786 |
| command | 1 | 1.000 |
| comparison | 5 | 0.600 |
| count | 1 | 1.000 |
| cross-domain | 1 | 0.000 |
| dates | 1 | 1.000 |
| de | 65 | 0.857 |
| detection | 2 | 0.500 |
| disambiguation | 1 | 0.000 |
| edge | 30 | 0.867 |
| enterprise | 38 | 0.919 |
| exact-text | 1 | 1.000 |
| explicit-unknown | 1 | 1.000 |
| false-premise | 1 | 1.000 |
| group | 9 | 1.000 |
| hierarchy | 1 | 1.000 |
| ics | 17 | 0.750 |
| id-as-name | 1 | 1.000 |
| id-lookup | 3 | 1.000 |
| list-answer | 1 | 1.000 |
| metadata | 2 | 1.000 |
| mitigation | 6 | 1.000 |
| mobile | 7 | 0.857 |
| multi-answer | 2 | 1.000 |
| multi-file | 2 | 0.500 |
| multi-hop | 4 | 1.000 |
| near-duplicate | 4 | 0.500 |
| negative-answer | 1 | 1.000 |
| nested-id | 1 | 1.000 |
| number | 4 | 1.000 |
| open-ended | 1 | 1.000 |
| procedure | 2 | 1.000 |
| punctuation | 1 | 1.000 |
| real-incident | 1 | 1.000 |
| recent | 2 | 1.000 |
| renamed | 2 | 0.500 |
| same-name-twin | 3 | 1.000 |
| set-difference | 1 | 1.000 |
| software | 7 | 0.857 |
| special-chars | 1 | 1.000 |
| sub-technique-id | 1 | 1.000 |
| tactic | 9 | 0.875 |
| technique | 16 | 0.812 |
| temporal | 1 | 0.000 |
| unanswerable | 2 | n/a |
| variant | 65 | 0.857 |
| version-sensitive | 2 | 1.000 |
| yes-no | 1 | 1.000 |
