---
layout: post
title: Picking a model by breaking the question down
date: 2026-10-27
description: 'I split the question "which model?" into small questions, give each one a test and a pass rule, and measure again as the system grows. Five tests and a three-level reasoning test on thirteen configurations of eight models.'
---

**This blog is written for anyone building mainly on open-weight models.**

**I split the question "which model?" into small questions, give each one a test and a pass rule, and measure again as the system grows. This post shows the method, five tests that fit in one script, a harder test with three levels of reasoning, and the results for thirteen configurations of eight models.**

Public benchmarks answer a general question: which model reasons best on average. A project asks a narrower one. Can this model call my tools, return my schema, read an input the size of mine, run in the region I need, and finish before the provider's gateway cuts the connection? A model can lead an index and still fail one of these. The opposite also happens. 

The narrow question matters more with open-weight models. There are many of them, new versions arrive every few weeks, and the same weights can behave differently depending on who serves them: which parameters the host accepts, how fast it writes, and where the reasoning comes back. So I test the model as it will be served, not the model in the abstract.

## The method in eight steps

This is the procedure I follow for any task that seems to need a model. 

1. **Apply the hard constraints before any model call.** Data residency, endpoint and region, licence (open weights or not), the model IDs the account can actually call, the context size the task needs, and a price ceiling. 

2. **Split the task into questions until every question has a pass rule.** The tree below shows the split I start from. Split again until a script can grade each answer. 

3. **Write the pass rules before the first run.** For example: at most one failure in five tool calls, every planted item found, no invented IDs, an estimated run time under a set limit.

4. **Build a synthetic input at the real size, with planted answers.** Plant a few items with known answers (the ground truth), at least one decoy that needs no action, and IDs the answer must cite. Give every planted item a rule in the prompt. Without a rule, there is no right answer to grade against.

5. **Add complications in levels.** For example: Level 1 states the rules and needs one step. Level 2 needs two steps, such as a join or a newer record that overrides an older one. Level 3 adds exceptions, date arithmetic and a second source. 

6. **Run every candidate at more than one effort, with the same frozen script.** Three to five trials per test are enough to rule a model out. Record the score, the median and maximum latency, the tokens, the cost per task solved, whether the reasoning came back, and format slips. 

7. **Read the failures, not only the scores.** Sort each miss into a kind: a format slip, a wrong join, a broken rule, reasoning written into the answer, or an over-flagged item. Each kind has its own fix: a pattern in the schema, a rule in the prompt, a higher effort. Some fixes make a stronger model unnecessary.

8. **Push every later failure down into the cheap test.** When a real run or an eval finds a failure, ask which small test would have shown it, and add that test. The next model then meets it in minutes.

## Breaking questions down to define pass rules

"Which model?" cannot be tested. "Does it return a valid object for this schema in five of five trials?" can. Between the two sits a short tree:

<pre class="mermaid">
flowchart TD
  Q["which model?"] --> M["can it do the mechanics?"]
  Q --> J["can it do the job at full size?"]
  Q --> U["can I use it here?"]
  Q --> S["is it fast enough?"]
  M --> T1["tool calls"]
  M --> T2["schema and field format"]
  M --> T3["reasoning returned"]
  J --> T4["real-size input with planted answers and a decoy"]
  U --> T5["region, licence, accepted parameters"]
  S --> T6["latency × calls per run, slowest call vs timeout"]
</pre>

<script type="module">
  import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.esm.min.mjs";
  mermaid.initialize({ startOnLoad: true, theme: "neutral" });
</script>

*Each leaf is something a script can check. The leaves change with the task, the four branches rarely do.*

The splitting is the useful part. "Handles long context" sounds like a requirement, but it has no pass rule. Split once more, it becomes three checks that can be counted: a valid answer on 35,000 tokens, every planted item found, the decoy left out.

## Measure again as the system grows

I test in three stages. Each costs more and runs less often than the one before.

| Stage | What runs | How long | What it answers |
|---|---|---|---|
| 1. Five tests | One model, one script | Minutes | Can the model do the mechanics on an input of my size? |
| 2. One real run | The full system on realistic data | About an hour | Does it hold up end to end, and which limits does it hit? |
| 3. Protocol | A series of graded runs, everything but one variable frozen | Hours | Did the score move, and why are the misses misses? |

*Each stage catches what the stage before cannot see, and each catch becomes a cheaper test (step 8).*

### Stage 1: five tests

1. **Reasoning effort.** Effort is the parameter that sets how long the model reasons before it answers. Call once at low and once at high, record latency and tokens, and check which values the API accepts at all. 
2. **Tool call.** One tool that returns a fixed record, and a question that needs it. Five trials.
3. **Structured output.** Ask for a small object (a title, a list of IDs, a severity from 1 to 3). Five trials.
4. **Reasoning text.** Does the reasoning come back, in which field, and how long is it? If the reasoning of every call is kept for audit, a model that returns it only sometimes is a problem. A model that always returns long reasoning can be a problem too. 
5. **Long input with planted answers.** A synthetic input of about 35,000 tokens with three planted items that need action, one decoy and IDs to cite. Three trials.

**The five tests also catch a silent change.** A model can change behind its ID. Between two runs of the unchanged five tests, the Mistral Large 4 preview started reporting reasoning tokens and accepting `max`, and its output on the long input doubled. Pin a dated model ID where the provider offers one, and rerun the five tests where it does not.

### Stage 2: one real run

**A real run found what the median hid.** The five tests timed Mistral Large 4's long calls at two and a half to four minutes. The largest call of a real run wrote 67,553 tokens, 25 minutes at 45 tokens per second, and the provider's gateway cuts a call at 15 minutes (20 if streamed). Pushed down: one call with the output size of the largest real call, timed against the gateway limit.

### Stage 3: protocol

**The protocol found that the limit was reasoning.** Over 15 graded runs, Mistral Large 4 had the right facts and cited them, yet in 5 runs it missed an item whose facts were all in front of it. Pushed down: a harder version of test 5, with a rule for every planted item and longer reasoning at each level.

**The protocol is also where the model changes.** The five tests only pick a model to start building with. Once the system has evals (graded runs that give a score with a cause) and observability (every call recorded with model ID, parameters, tokens, latency and reasoning), a model comparison becomes a controlled experiment: freeze the data, prompts and code, change the model, run the protocol. A second model also shows whether the misses sit in the model or in the system. I run this comparison even without a plan to switch.

## Results from thirteen configurations

On 19 October 2026 I ran the five tests on nine configurations of five models through Mistral's EU endpoint, at temperature 0.2. The reasoning test added four configurations of three Claude models, through Anthropic's API at the default temperature, as a closed reference for the ceiling. Claude did not run the five tests. The task: read about 35,000 tokens of records, return the items that need action under written rules, and cite the records behind each.

*Disclaimer:* the models were released over about ten months and range from a 14-billion-parameter model built for small devices to frontier models. The results show which model can do my task today, through the endpoint I would use, not which lab builds better models. 

| Model | Released | Source |
|---|---|---|
| Ministral 14B | December 2025 | Date in the model ID (2512) |
| Mistral Small 2603 | March 2026 | Date in the model ID |
| Mistral Medium 3.5 | April 2026 | Its alias `mistral-medium-2604` |
| GLM-5.3 | August 2026 | Press reports; I found no official release note |
| Claude Opus 5.5 | 21 September 2026 | Anthropic Models API |
| Claude Sonnet 5.5 | 28 September 2026 | Anthropic Models API |
| Mistral Large 4 | 6 October 2026, public preview | Mistral; training still running until the weights are released |
| Claude Haiku 5.5 | 7 October 2026 | Anthropic Models API |

*Disclaimer:* every configuration ran once, with three to five trials per test. The scores vary: Mistral Medium 3.5 scored 7, 10 and 11 of 11 on the identical level 3 input, and even 9 of 9 allows a failure rate of up to 28% (one-sided, 95% confidence). I read gaps of one or two items as noise, and only large gaps, such as 2 of 18 against 18 of 18, as results.

### The five tests

**Effort values are not what the documentation suggests.** All four Mistral models reject `low`, so the only step down from `high` is `none`, which turns reasoning off. *Note:* an accepted value is not an applied one. Medium 3.5, Small 2603 and Ministral 14B accept `max` without an error but return no reasoning, and all three got a short time calculation wrong at `max`. At `high`, Medium 3.5 spent 137 seconds and 30,149 output tokens on the same question.

| Configuration | Tool call | Structured output | Reasoning returned | Planted items found | Decoy flagged, lower is better | Median / max latency, long input | Cost, all tests |
|---|---|---|---|---|---|---|---|
| Mistral Large 4, high | 5 of 5 | 5 of 5 | 16 of 16 | 9 of 9 | 3 of 3 | 160 / 251 s | 0.31 USD |
| Mistral Large 4, none | 5 of 5 | 5 of 5 | 1 of 16 | 9 of 9 | 3 of 3 | 5 / 8 s | 0.15 USD |
| Mistral Medium 3.5, high | 5 of 5 | 5 of 5 | 16 of 16 | 9 of 9 | 0 of 3 | 181 / 203 s | 0.97 USD |
| Mistral Small 2603, high | **2 of 5** | 5 of 5 | 16 of 16 | 4 of 9 | 1 of 3 | 10 / 10 s | 0.02 USD |
| Mistral Small 2603, none | 5 of 5 | 5 of 5 | 1 of 16 | 9 of 9 | 3 of 3 | 2 / 3.5 s | 0.02 USD |
| Ministral 14B | 4 of 5 | 5 of 5 | 0 of 15 | 9 of 9 | 3 of 3 | 57 / 63 s | 0.02 USD |
| GLM-5.3, low | 5 of 5 | 5 of 5 | 6 of 17 | 9 of 9 | 3 of 3 | 1.8 / 3.5 s | 0.16 USD |
| GLM-5.3, high | 5 of 5 | 5 of 5 | 6 of 17 | 7 of 9 | 2 of 3 | 5.9 / 6.0 s | 0.17 USD |
| GLM-5.3, max | 5 of 5 | 5 of 5 | 16 of 17 | 9 of 9 | 3 of 3 | 19.7 / 52.0 s | 0.25 USD |

*Reasoning returned counts the short calls of tests 1 to 3, so the total depends on the effort values the API accepts. Mistral Small 2603 at high fails the tool-call rule. The decoy column has no rule behind it, my mistake.*

### Three levels of reasoning

This is the harder test the protocol pushed down. It uses the same input, gives every planted item a rule, and adds steps at each level:

1. **Rules stated.** Test 5 plus two rules: an item already handled needs no action, and an item dated after today needs none yet. 5 items.
2. **Two steps.** A second record for the same item, listed far from the first, and a newer record that overrides an older one. 7 items.
3. **Exceptions.** A grace period computed from a date (one has ended, one has not), and an end date that sits only in a second source. 11 items: 6 that need action and 5 that do not, scored apart because a model that flags nothing gets every no-action item right.

Some answers named the right item in a format no downstream system could read, such as a record ID and a name in one field. So I grade twice: lenient reads the name out of the field and measures the reasoning, strict accepts only the exact format and measures whether the output is usable. I chose this after seeing answers, so both numbers stay visible.

| Configuration | Level 1 | Level 2 | Level 3, needs action, found | Level 3, no action, left out | Format slips | Median / max latency | Median output tokens | Calls solved | Cost per solved call |
|---|---|---|---|---|---|---|---|---|---|
| Mistral Large 4, high | 15/15 | 21/21 | 18/18 | 15/15 | 0 | 79 / 176 s | 7,513 | 9/9 | 0.078 USD |
| Mistral Large 4, none | 15/15 | 18/21 | 18/18 | 4/15 | 0 | 7 / 24 s | 619 | 3/9 | 0.136 USD |
| Mistral Medium 3.5, high | 12/15 | 20/21 | 14/18 | 14/15 | 0 | 57 / 70 s | 9,872 | 3/9 | 0.382 USD |
| Mistral Small 2603, high | 11/15 | 13/21 | 2/18 | 14/15 | 0 | 17 / 41 s | 3,138 | 0/9 | none solved |
| Mistral Small 2603, none | 6/15 | 6/21 | 3/18 (2) | 13/15 | 7 | 3 / 4 s | 272 | 0/9 | none solved |
| Ministral 14B | 9/15 (3) | 14/21 (6) | 3/18 (0) | 12/15 | 63 | 29 / 54 s | 704 | 0/9 | none solved |
| GLM-5.3, low | 15/15 | 21/21 | 13/18 | 15/15 | 0 | 5 / 7 s | 491 | 6/9 | 0.071 USD |
| GLM-5.3, high | 15/15 (12) | 21/21 (17) | 18/18 | 15/15 | 7 | 3 / 49 s | 892 | 9/9 (7) | 0.053 (0.068) USD |
| GLM-5.3, max | 15/15 | 21/21 (17) | 18/18 (12) | 15/15 | 10 | 12 / 24 s | 4,095 | 9/9 (7) | 0.063 (0.081) USD |
| Claude Haiku 5.5, low | 15/15 | 21/21 | 18/18 | 15/15 | 0 | 9 / 11 s | 1,300 | 9/9 | 0.005 USD |
| Claude Haiku 5.5, high | 15/15 | 21/21 | 18/18 | 15/15 | 0 | 11 / 12 s | 1,784 | 9/9 | 0.005 USD |
| Claude Sonnet 5.5, low | 15/15 | 21/21 | 15/18 | 12/15 | 0 | 5 / 6 s | 646 | 6/9 | 0.131 USD |
| Claude Opus 5.5, low | 15/15 | 21/21 | 18/18 | 15/15 | 0 | 6 / 10 s | 399 | 9/9 | 0.175 USD |

*Lenient scores, strict in brackets where different. A call is solved when every planted item is right, nothing else is flagged and no ID is invented. Cost per solved call: the cost of all nine calls divided by the solved ones (prices in the annex). The maximum counts only the retry of a hung call: two GLM-5.3 calls at high and one at max hung for about 20 minutes first.*

**The most common miss is the join, not the rule.** GLM-5.3 at low, Medium 3.5 and Mistral Small usually apply the right rule, then attach the answer to the wrong record: the one a row below, or one with a similar name.

**Effort can matter as much as size.** Mistral Large 4 drops from 33 of 33 on level 3 at `high` to 22 of 33 at `none`, Mistral Small from 11 to 6 of 15 on level 1. The smallest Claude model, Haiku 5.5, solved everything at `low`.

**At low effort, the model decides when to think, and models decide differently.** Claude Opus 5.5 at `low` skipped reasoning on levels 1 and 2 and reasoned on every level 3 call: 33 of 33, with the fewest output tokens of any perfect configuration. Claude Sonnet 5.5 at `low` reasoned on level 2, not on level 3, and missed 6 of 33 there.

**Without reasoning, the reasoning moves into the answer.** Mistral Large 4 at `none` put 10 entries that need no action into the action list, with reasons like "but wait, let me recalculate... so no action needed". Claude Sonnet 5.5 at `low` did the same, and added entries whose only reason was "placeholder".

**Stating the rule fixed the decoy.** In test 5, without a rule, Mistral Large 4 flags the decoy 3 of 3 times. With the rule at level 1, it leaves it out 3 of 3 times. The failure was the test's, not the model's.

**Right decision, wrong format.** GLM-5.3 at high and max put a record ID in front of the name in 17 entries, Ministral 14B wrote only the record ID in 63. Test 3 checks that the field is a string, not its format. Pushed down: a pattern for the field in the schema.

**Cost per call misleads, cost per task solved does not.** Mistral Medium 3.5 costs 1.14 USD for nine calls but solves 3, so 0.38 USD per solved call, five times Mistral Large 4 at high. Mistral Small and Ministral 14B cost less than a cent per call and solve none. Every call sends 31,000 to 41,000 tokens, depending on how the model counts them, so the input price decides more than the answer length: among the configurations that solve all nine, Claude Haiku 5.5 costs 0.005 USD per solved call and Claude Opus 5.5 0.175 USD.

**The median hides the tail again.** GLM-5.3 at high has a median of 3 seconds, but three GLM-5.3 calls hung for about 20 minutes before the client retried them, and each retry answered in seconds.

The test works, but its top is already reached: six configurations reach the ceiling under lenient grading, four under strict, so it can no longer rank them. A level 4 would need longer chains, conflicting sources and ambiguous policies.

## Important to note

- **One input, sampled again.** Every trial uses the same records and planted items. Three trials show how stable a model is on that input, not how it does on the next one.
- **The reasoning test is mine.** It is synthetic and small, and does not show how a model handles messy real data.
- **Self-hosted weights behave differently again.** Every open-weight model here ran on a provider's API. Quantisation and the serving stack change speed, accepted parameters and sometimes the answers, so test the build you will deploy.
- **Every answer here is graded by a script.** The planted answers make that possible. Where no script can grade an answer, such as a free-text summary, a second model can grade it against a written rubric (a model as a judge). The judge then needs its own test against a few answers graded by hand.
- **The design can be stronger.** A next version would run several generated inputs per configuration and report the spread, and fix the grading before the first answer. It would also run every model through every test at one temperature, and add misleading tool results, concurrent load and instructions planted in the records.
- **Token counts do not compare across models.** The same prompt counts 121 tokens for GLM-5.3 and 223 for Mistral Large 4. Compare across models in seconds and dollars.

**A test script like this is not always worth writing. For a single prompt with no tools and no schema, trying the model by hand is faster. If a public benchmark measures closely what the system does, use the benchmark. It pays off when the system depends on a specific combination of mechanics no benchmark checks.**

## The same approach fits other tasks

- **Contract review.** 40 supplier contracts. Level 1: three notice periods end within the next 30 days, and one contract is already terminated (the decoy). Level 2: a later amendment changes one notice period. Level 3: notice counted in working days, and a termination date that sits only in a separate register.
- **Support tickets.** 500 tickets. Level 1: five tickets report the same outage in different words, and one mentions the outage but is about an invoice (the decoy). Level 2: a ticket that only makes sense with the earlier ticket it links to. Level 3: a product line with its own escalation rule, defined in a second document.

## Conclusion

The models in these tables will be replaced within months, the method carries over. From the runs in this post, five recommendations hold beyond my task:

- **Pick the configuration with the lowest cost per task solved that passes every rule, and keep a stronger one as the reference.**
- **Treat effort as its own variable.**
- **Grade twice: leniently for the reasoning, strictly for the output.**
- **Record the maximum latency, not only the median.**
- **Keep the test cheap enough to rerun without thinking about it.**

## Annex

- [Mistral, regional inference (EU endpoint)](https://docs.mistral.ai/inference/regional-inference)
- [Artificial Analysis, Intelligence Index, an example of a public leaderboard](https://artificialanalysis.ai)
- [Anthropic, effort and adaptive thinking](https://platform.claude.com/docs)
- [Clopper-Pearson interval, for the 28% bound on nine calls](https://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval)
- [Zheng et al., Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena (2023), on a model as a judge and its biases](https://arxiv.org/abs/2306.05685)

Prices used for the cost estimates, in USD per million tokens, October 2026. Every input token is counted at the uncached price, reasoning tokens as output. Prompt caching on the fixed input would lower these costs, by a different amount per provider. Calls that hung and were retried are not in the record, so the real cost of the GLM-5.3 runs is higher.

| Model | Input | Output | Source |
|---|---|---|---|
| Mistral Large 4 | 1.36 | 4.18 | Mistral list price; the preview sale price was half |
| Mistral Medium 3.5 | 1.50 | 7.50 | Third-party price lists |
| Mistral Small 2603 | 0.15 | 0.60 | Third-party price lists, the higher of two published prices |
| Ministral 14B | 0.20 | 0.20 | Third-party price lists |
| GLM-5.3 on the Mistral API | 1.40 | 4.40 | Mistral API, October 2026 |
| Claude Haiku 5.5 | 0.10 | 0.50 | Anthropic, prompts up to 100,000 tokens |
| Claude Sonnet 5.5 | 2.00 | 10.00 | Anthropic |
| Claude Opus 5.5 | 4.00 | 20.00 | Anthropic |
