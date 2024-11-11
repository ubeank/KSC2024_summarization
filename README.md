# KSC2024_summarization
exact-match : ROUGE1, 2, L <br/>
LM-based : BERTScore(F1) <br/>
LLM-based (GEval) : Faithfulness, Completeness, Conciseness <br/>


|exact-match| summarization-version | ROUGE1|ROUGE2|ROUGEL|
|--------|-----|-----|-----|
|led-base-16k (baseline)| | 0.247 | 0.064 | 0.179 |
|led-base-16k (lecture summarizer & baseline)| | 0.241 | 0.062 | 0.176 |
|SciSpace (lecture summarizer & Pegasus) | | 0.262 | 0.057 | 0.197 |
|gpt-4o-mini (1-shot)| summarization_V1 | 0.187 | 0.034 | 0.107 |
|gpt-4o-mini (lecture summarizer & 1-shot)| summarization_V1 | 0.203 | 0.034 | 0.114 |


|summarization_V2|ROUGE1|ROUGE2|ROUGEL|
|--------|-----|-----|-----|
|gpt-4o-mini (1-shot)|  |  |  |
|gpt-4o-mini (lecture summarizer & 1-shot)|  |  |  |


|summarization_V1|BERTScore(F1)|
|--------|-----|
|led-base-16k (baseline)| 0.872 |
|led-base-16k (lecture summarizer & baseline)| 0.870 |
|SciSpace (lecture summarizer & Pegasus) | 0.859 |
|gpt-4o-mini (1-shot)| 0.835 | 
|gpt-4o-mini (lecture summarizer & 1-shot)| 0.840 |


|summarization_V2|BERTScore(F1)|
|--------|-----|
|gpt-4o-mini (1-shot)|  | 
|gpt-4o-mini (lecture summarizer & 1-shot)|  |


|summarization_V1 + GEval_V1|Faithfulness|Completeness|Conciseness|
|--------|-----|-----|-----|
|led-base-16k (baseline)| 2.161 | 1.413 | 3.066 |
|led-base-16k (lecture summarizer & baseline)| 2.134 | 1.343 | 3.303 |
|gpt-4o-mini (1-shot)| 4.660 | 4.542 | 4.243 |
|gpt-4o-mini (lecture summarizer & 1-shot)| 4.601 | 4.488 | 4.141 |


|summarization_V1 + GEval_V2|Faithfulness|Completeness|Conciseness|
|--------|-----|-----|-----|
|led-base-16k (baseline)| 2.287 | 1.961 | 2.488 |
|led-base-16k (lecture summarizer & baseline)| 2.201 | 1.851 | 2.390 |
|gpt-4o-mini (1-shot)| 3.838 | 3.999 | 3.475 |
|gpt-4o-mini (lecture summarizer & 1-shot)| 3.647 | 3.783 | 3.073 |


|summarization_V2 + GEval_V2|Faithfulness|Completeness|Conciseness|
|--------|-----|-----|-----|
|led-base-16k (baseline)|  |  |  |
|led-base-16k (lecture summarizer & baseline)|  |  |  |
|gpt-4o-mini (1-shot)|  |  |  |
|gpt-4o-mini (lecture summarizer & 1-shot)|  |  |  |
