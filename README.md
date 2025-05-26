# KSC2024_summarization
[paper](paper.pdf)

exact-match : ROUGE1, 2, L <br/>
LM-based : BERTScore(F1) <br/>
LLM-based (GEval) : Faithfulness, Completeness, Conciseness <br/>

|exact-match|summary-version|ROUGE1|ROUGE2|ROUGEL|
|--------|---|-----|-----|-----|
|led-base-16k (baseline)| - | 0.247 | **0.064** | 0.179 |
|led-base-16k (lecture summarizer & baseline)| - | 0.241 | 0.062 | 0.176 |
|SciSpace (lecture summarizer & Pegasus) | - | **0.262** | 0.057 | **0.197** |
|gpt-4o-mini (1-shot)| V1 | 0.187 | 0.034 | 0.107 |
|gpt-4o-mini (lecture summarizer & 1-shot)| V1 | 0.203 | 0.034 | 0.114 |
|gpt-4o-mini (1-shot)| V2 | 0.225 | 0.033 | 0.129 |
|gpt-4o-mini (lecture summarizer & 1-shot)| V2 | 0.222 | 0.031 | 0.128 |


|LM-based|summary-version|BERTScore(F1)|
|--------|---|-----|
|led-base-16k (baseline)| - | **0.872** |
|led-base-16k (lecture summarizer & baseline)| - | 0.870 |
|SciSpace (lecture summarizer & Pegasus) | - | 0.859 |
|gpt-4o-mini (1-shot)| V1 | 0.835 | 
|gpt-4o-mini (lecture summarizer & 1-shot)| V1 | 0.840 |  
|gpt-4o-mini (1-shot)| V2 | 0.854 |
|gpt-4o-mini (lecture summarizer & 1-shot)| V2 | 0.854 |


||summary-version|ROUGE1|ROUGE2|ROUGEL|BERTScore(F1)|
|--------|---|-----|-----|-----|-----|
|led-base-16k (baseline)| - | 0.247 | **0.064** | 0.179 | **0.872** |
|led-base-16k (lecture summarizer & baseline)| - | 0.241 | 0.062 | 0.176 | 0.870 |
|SciSpace (lecture summarizer & Pegasus) | - | **0.262** | 0.057 | **0.197** | 0.859 |
|gpt-4o-mini (1-shot)| V1 | 0.187 | 0.034 | 0.107 | 0.835 | 
|gpt-4o-mini (lecture summarizer & 1-shot)| V1 | 0.203 | 0.034 | 0.114 | 0.840 | 
|gpt-4o-mini (1-shot)| V2 | 0.225 | 0.033 | 0.129 | 0.854 |
|gpt-4o-mini (lecture summarizer & 1-shot)| V2 | 0.222 | 0.031 | 0.128 | 0.854 |


--------------------------------------------------------------------------------
|summarization_V1 + GEval_V1|Faithfulness|Completeness|Conciseness|
|--------|-----|-----|-----|
|led-base-16k (baseline)| 2.161 | 1.413 | 3.066 |
|led-base-16k (lecture summarizer & baseline)| 2.134 | 1.343 | 3.303 |
|gpt-4o-mini (1-shot)| **4.660** | **4.542** | **4.243** |
|gpt-4o-mini (lecture summarizer & 1-shot)| 4.601 | 4.488 | 4.141 |


|summarization_V1 + GEval_V2|Faithfulness|Completeness|Conciseness|
|--------|-----|-----|-----|
|led-base-16k (baseline)| 2.287 | 1.961 | 2.488 |
|led-base-16k (lecture summarizer & baseline)| 2.201 | 1.851 | 2.390 |
|gpt-4o-mini (1-shot)| **3.838** | **3.999** | **3.475** |
|gpt-4o-mini (lecture summarizer & 1-shot)| 3.647 | 3.783 | 3.073 |


|summarization_V2 + GEval_V2|Faithfulness|Completeness|Conciseness|
|--------|-----|-----|-----|
|gpt-4o-mini (1-shot)| **3.737** | **3.783** | **3.624** |
|gpt-4o-mini (lecture summarizer & 1-shot)| 3.569 | 3.603 | 3.321 |


--------------------------------------------------------------------------------
|Main error category|Sub error category|Weight|Description|
|--------|-----|-----|----------|
|Faithfulness (100)| Intrinsic Information | 30 | Adding details not found in the original text, changing its meaning |
|| Extrinsic Information | 25 | Information not present in the source text is added |
|| Ambiguity | 15 | The summary is unclear or vague, leading to multiple interpretations |
|| Overgeneralization | 10 | Making broad statements that aren't supported by the original text |
|| Incorrect Implication | 10 | Suggesting conclusions that the original text does not support |
|| Inaccurate Emphasis | 10 | Misplacing importance on details that aren't central to the original message |
|Completeness (100)| Population Mismatch | 25 | When the group studied is different |
|| Intervention Mismatch | 25 | When the treatment or method differs |
|| Outcome Mismatch | 25 | When the results differ |
|| Omission of Key Facts | 25 | Important details are omitted |
|Conciseness (100)| Redundancy | 30 | Information is repeated unnecessarily |
|| Length | 25 | The inclusion of excessive or unnecessary details that lengthen the summary |
|| Lack of Focus | 25 | The inclusion of unrelated or secondary information |
|| Excessive detail | 20 | The summary includes too much detail |

--------------------------------------------------------------------------------
Explainable_Summary_Evaluation
<table>
  <tr>
    <th rowspan="2">Summary</th>
    <th colspan="3">GEval</th>
    <th colspan="3">ESE_Score</th>
  </tr>
  <tr>
    <th>Faithfulness</th>
    <th>Completeness</th>
    <th>Conciseness</th>
    <th>Faithfulness</th>
    <th>Completeness</th>
    <th>Conciseness</th>
  </tr>
  <tr>
    <td>led-base-16k</td>
    <td>2.287</td>
    <td>1.961</td>
    <td>2.488</td>
    <td>55.1731</td>
    <td>53.2734</td>
    <td>44.4916</td>
  </tr>
    <tr>
    <td>gpt-4o-mini v1</td>
    <td>3.737</td>
    <td>3.783</td>
    <td>3.624</td>
    <td>62.5646</td>
    <td>63.6654</td>
    <td>52.5365</td>
  </tr>
</table>

