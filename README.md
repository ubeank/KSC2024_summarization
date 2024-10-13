# KSC2024_summarization

|exact-match|ROUGE1|ROUGE2|ROUGEL|
|--------|-----|-----|-----|
|led-base-16k (baseline)| 0.247 | 0.064 | 0.179 |
|led-base-16k (lecture summarizer & baseline)| 0.241 | 0.062 | 0.176 |
|gpt-3.5 (1-shot)| 0.190 | 0.034 | 0.107 |
|gpt-3.5 (lecture summarizer & 1-shot)| | | |

|LM-based|BERTScore(F1)|
|--------|-----|
|led-base-16k (baseline)| 0.872 |
|led-base-16k (lecture summarizer & baseline)| 0.870 |
|gpt-3.5 (1-shot)| 0.836 | 
|gpt-3.5 (lecture summarizer & 1-shot)| |

|LLM-based (GEval)|Faithfulness|Completeness|Conciseness|
|--------|-----|-----|-----|
|led-base-16k (baseline)|  |  ||
|led-base-16k (lecture summarizer & baseline)| | | |
|gpt-3.5 (1-shot)| | | |
|gpt-3.5 (lecture summarizer & 1-shot)| | | |
