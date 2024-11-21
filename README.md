# KSC2024_summarization
exact-match : ROUGE1, 2, L <br/>
LM-based : BERTScore(F1) <br/>
LLM-based (GEval) : Faithfulness, Completeness, Conciseness <br/>


|exact-match|summarization-version|ROUGE1|ROUGE2|ROUGEL|
|--------|-----|-----|-----|-----|
|led-base-16k (baseline)| - | 0.247 | 0.064 | 0.179 |
|led-base-16k (lecture summarizer & baseline)| - | 0.241 | 0.062 | 0.176 |
|SciSpace (lecture summarizer & Pegasus) | - | 0.262 | 0.057 | 0.197 |
|gpt-4o-mini (1-shot)| V1 | 0.187 | 0.034 | 0.107 |
|gpt-4o-mini (lecture summarizer & 1-shot)| V1 | 0.203 | 0.034 | 0.114 |
|gpt-4o-mini (1-shot)| V2 | 0.225 | 0.033 | 0.129 |
|gpt-4o-mini (lecture summarizer & 1-shot)| V2 | 0.222 | 0.031 | 0.128 |


|LM-based|summarization-version|BERTScore(F1)|
|--------|-----|-----|
|led-base-16k (baseline)| - | 0.872 |
|led-base-16k (lecture summarizer & baseline)| - | 0.870 |
|SciSpace (lecture summarizer & Pegasus) | - | 0.859 |
|gpt-4o-mini (1-shot)| V1 | 0.835 | 
|gpt-4o-mini (lecture summarizer & 1-shot)| V1 | 0.840 |  
|gpt-4o-mini (1-shot)| V2 | 0.854 |
|gpt-4o-mini (lecture summarizer & 1-shot)| V2 | 0.854 |


--------------------------------------------------------------------------------
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
|gpt-4o-mini (1-shot)| 3.737 | 3.783 | 3.624 |
|gpt-4o-mini (lecture summarizer & 1-shot)| 3.569 | 3.603 | 3.321 |


--------------------------------------------------------------------------------
|Main error category|Sub error category|Description|
|--------|-----|-----|
|Faithfulness| Intrinsic Information | |
|| Extrinsic Information | Information not present in the source text is added |
|| Ambiguity | |
|| Overgeneralization | |
|| Inaccurate Emphasis | |
|| Incorrect Implication | |
|Completeness| Population Mismatch | When the group studied is different |
|| Intervention Mismatch | When the treatment or method differs |
|| Outcome Mismatch | When the results differ |
|| Omission of Key Facts | Important details are omitted |
|Conciseness| Redundancy | Information is repeated unnecessarily |
|| Length | The inclusion of excessive or unnecessary details that lengthen the summary |
|| Lack of Focus | The inclusion of unrelated or secondary information |
|| Excessive detail | The summary includes too much detail |


