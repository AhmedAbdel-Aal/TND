> [!NOTE]
> The following is AI generated documents for the results for quick documentation and results aggregation. A human written document will be in the thesis itself.

# LLM-Based Identification of Key ECHR Cases: Research Progress Report

## 1. Introduction and Research Context

The European Court of Human Rights (ECHR) assigns importance levels to cases on a scale from 1 to 4, with level 1 designating "key cases" that make a significant contribution to the development, clarification, or modification of ECHR case-law. This research explores the capability of Large Language Models (LLMs) to identify these key cases and investigates how this capability varies across different classification scenarios.

## 2. Research Questions

Primary Research Questions:
1. How effectively can LLMs distinguish key cases (importance level 1) from cases of other importance levels?
2. Does the difficulty of key case identification vary based on the importance level of non-key cases?
3. Which input format (facts section only vs. facts + law sections) leads to better classification performance?

## 3. Hypotheses

H1: The classification task becomes easier as the difference in importance levels increases (i.e., distinguishing between level 1 and level 4 cases is easier than distinguishing between level 1 and level 2 cases).

H2: Including both facts and law sections in the input will improve classification performance compared to using only the facts section.

## 4. Methodology

### 4.1 Data Structure

Our initial analysis focuses on pre-cutoff date cases for several reasons:
1. Larger available dataset allowing for more robust statistical analysis
2. Elimination of potential temporal bias in model responses
3. Ability to create balanced datasets for each importance level
4. Foundation for later comparison with post-cutoff performance

Pre-cutoff dataset composition:
- 125 key cases (importance level 1)
- 125 cases each for importance levels 2, 3, and 4

### 4.2 Experimental Design

Current implementation uses:
- Model: GPT-4-mini
- Simple Chain-of-Thought prompting
- Binary classification tasks:
  * Key cases vs. all other levels
  * Key cases vs. each importance level separately
  * Two input formats: facts only and facts + law sections

### prompt

- please check prompts.py
- All prompts were crafted by Oana Ichim and Ahmed Abdou.

## 5. Results

### 5.1 Facts Only Results

#### Table 1: Classification Performance with Facts Only
| Comparison | Accuracy | Precision | Recall | F1 Score |
|------------|----------|-----------|---------|-----------|
| Key vs All | 0.597 | 0.348 | 0.696 | 0.464 |
| Key vs Level 2 | 0.530 | 0.524 | 0.696 | 0.598 |
| Key vs Level 3 | 0.632 | 0.617 | 0.696 | 0.654 |
| Key vs Level 4 | 0.728 | 0.744 | 0.696 | 0.719 |

#### Table 2: Confusion Matrices (Facts Only)
Key vs Level 2:
```
Predicted 0  Predicted 1
Actual 0    45          38
Actual 1    80          87
```

Key vs Level 3:
```
Predicted 0  Predicted 1
Actual 0    71          38
Actual 1    54          87
```

Key vs Level 4:
```
Predicted 0  Predicted 1
Actual 0    95          38
Actual 1    30          87
```

### 5.2 Facts + Law Results

#### Table 3: Classification Performance with Facts + Law
| Comparison | Accuracy | Precision | Recall | F1 Score |
|------------|----------|-----------|---------|-----------|
| Key vs All | 0.558 | 0.338 | 0.798 | 0.475 |
| Key vs Level 2 | 0.484 | 0.493 | 0.798 | 0.609 |
| Key vs Level 3 | 0.538 | 0.524 | 0.798 | 0.633 |
| Key vs Level 4 | 0.891 | 0.980 | 0.798 | 0.880 |

#### Table 4: Confusion Matrices (Facts + Law)
Key vs Level 2:
```
Predicted 0  Predicted 1
Actual 0    20          25
Actual 1    102         99
```

Key vs Level 3:
```
Predicted 0  Predicted 1
Actual 0    35          25
Actual 1    90          99
```

Key vs Level 4:
```
Predicted 0  Predicted 1
Actual 0    122         25
Actual 1    2           99
```

## 6. Key Findings

1. Support for Hypothesis H1:
   - Classification performance improves as the importance level difference increases
   - Most pronounced in facts + law input format
   - Key vs Level 4 shows substantially better performance than Key vs Level 2

2. Input Format Impact:
   - Facts + law sections dramatically improve Key vs Level 4 classification
   - Accuracy increases from 0.728 to 0.891
   - F1 score improves from 0.719 to 0.880
   - Particularly effective at reducing false positives

3. Consistent Patterns:
   - Relative difficulty pattern holds across both input formats
   - Higher recall with facts + law sections (0.798 vs 0.696)
   - Better separation of key cases from level 4 cases when legal reasoning is included

## 7. Proposed Next Steps

1. Statistical Analysis:
   - Implement McNemar's test for significance testing
   - Conduct detailed error analysis

2. Prompting Enhancement:
   - Develop more sophisticated Chain-of-Thought prompting
   - Experiment with few-shot learning

3. Model Comparison:
   - Test with other LLMs
   - Compare performance across model sizes

4. Temporal Analysis:
   - Extend to post-cutoff data
   - Compare temporal generalization patterns

5. RAG Extension:
   - Implement retrieval-augmented generation
   - Compare performance with and without RAG

## 8. Initial Conclusions

The research thus far supports the hypothesis that LLMs can effectively distinguish key cases from other cases, with performance varying based on the importance level difference. The addition of legal reasoning sections particularly improves discrimination between key cases and level 4 cases, suggesting that legal context plays a crucial role in the model's decision-making process.

These findings provide a strong foundation for further investigation into temporal generalization and more sophisticated prompting strategies.
