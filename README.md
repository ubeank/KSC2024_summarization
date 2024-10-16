# KSC2024_summarization

|exact-match|ROUGE1|ROUGE2|ROUGEL|
|--------|-----|-----|-----|
|led-base-16k (baseline)| 0.247 | 0.064 | 0.179 |
|led-base-16k (lecture summarizer & baseline)| 0.241 | 0.062 | 0.176 |
|gpt-4o-mini (1-shot)| 0.187 | 0.034 | 0.107 |
|gpt-4o-mini (lecture summarizer & 1-shot)| 0.203 | 0.034 | 0.114 |

|LM-based|BERTScore(F1)|
|--------|-----|
|led-base-16k (baseline)| 0.872 |
|led-base-16k (lecture summarizer & baseline)| 0.870 |
|gpt-4o-mini (1-shot)| 0.835 | 
|gpt-4o-mini (lecture summarizer & 1-shot)| 0.840 |

|LLM-based (GEval)|Faithfulness|Completeness|Conciseness|
|--------|-----|-----|-----|
|led-base-16k (baseline)| 2.161 | 1.413 | 3.066 |
|led-base-16k (lecture summarizer & baseline)| 2.134 | 1.343 | 3.303 |
|gpt-4o-mini (1-shot)| 4.660 | 4.542 | 4.243 |
|gpt-4o-mini (lecture summarizer & 1-shot)| 4.601 | 4.488 | 4.141 |
