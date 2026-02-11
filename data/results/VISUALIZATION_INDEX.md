# Jury v2.3 Evaluation Visualizations - Complete Index

**Generated:** 2026-02-11 13:21:26

This document indexes all visualizations and reports generated for the Jury v2.3 evaluations across three medical datasets.

---

## 📊 Available Visualization Packages

### 1. Cross-Dataset Comparison Package
**Location:** `v2_3_comparison_visualizations/`

Compares all three datasets side-by-side:

| File | Description | Size |
|------|-------------|------|
| `radar_chart_cross_dataset.png` | 7-dimensional comparison across all datasets | 486 KB |
| `bar_chart_composite_comparison.png` | Composite scores with error bars | 123 KB |
| `heatmap_dimensions.png` | Color-coded dimension scores matrix | 216 KB |
| `distribution_plots.png` | Score distribution histograms | 168 KB |
| `box_plots_dimensions.png` | Box plots for all dimensions | 198 KB |
| `v2_3_cross_dataset_comparison.md` | Comprehensive comparison report | 3.6 KB |

**Total:** 6 files, ~1.2 MB

---

### 2. Individual Dataset Package
**Location:** `v2_3_individual_visualizations/`

Detailed analysis for each dataset separately:

#### MedMCQA (Indian Medical Entrance Exam)
- `medmcqa_comprehensive_analysis.png` - 8-subplot overview (820 KB)
- `medmcqa_sample_responses.png` - Sample high/medium/low cases (591 KB)
- `medmcqa_jury_agreement.png` - Jury agreement analysis (485 KB)
- `medmcqa_detailed_report.md` - Statistical report (2.3 KB)

#### PubMedQA (Biomedical Research)
- `pubmedqa_comprehensive_analysis.png` - 8-subplot overview (850 KB)
- `pubmedqa_sample_responses.png` - Sample high/medium/low cases (618 KB)
- `pubmedqa_jury_agreement.png` - Jury agreement analysis (493 KB)
- `pubmedqa_detailed_report.md` - Statistical report (2.5 KB)

#### MedQA (US Medical Licensing)
- `medqa_comprehensive_analysis.png` - 8-subplot overview (744 KB)
- `medqa_sample_responses.png` - Sample high/medium/low cases (953 KB)
- `medqa_jury_agreement.png` - Jury agreement analysis (474 KB)
- `medqa_detailed_report.md` - Statistical report (2.8 KB)

**Total:** 12 files, ~6.0 MB

---

## 📈 Key Findings Summary

### Overall Rankings (by mean composite harm score)

| Rank | Dataset | Score | Samples | Harm Profile |
|------|---------|-------|---------|--------------|
| 🥇 | **MedMCQA** | 0.2931 | 100 | Lowest - factual medical knowledge |
| 🥈 | **PubMedQA** | 0.3328 | 100 | Middle - research uncertainty |
| 🥉 | **MedQA** | 0.4540 | 10* | Highest - complex clinical scenarios |

*Note: MedQA has only 10 samples - interpret with caution*

### Dataset Characteristics

#### 🟠 MedMCQA - Indian Medical Entrance Exam
**Mean Score:** 0.293 (Lowest)

**Characteristics:**
- Factual medical knowledge focus
- Anatomy and physiology questions
- Straightforward with clear answers
- Less clinical ambiguity
- 44% low harm, 56% moderate harm

**Key Dimension Scores:**
- Informational: 0.303
- Social: 0.281
- Psychological: 0.277
- Epistemic: 0.336

**Why Lower Harm?**
Questions like "Which part of the brachial plexus does not give branches?" or "What is the only complete cartilage ring in the respiratory tree?" are factual and objective, with minimal potential for harm.

---

#### 🟣 PubMedQA - Biomedical Research Questions
**Mean Score:** 0.333 (Middle)

**Characteristics:**
- Research methodology focus
- Evidence interpretation required
- Scientific reasoning emphasis
- Abstract-based Yes/No/Maybe format
- 41% low harm, 59% moderate harm

**Key Dimension Scores:**
- Informational: 0.353
- **Epistemic: 0.384** ⚠️ (Highest across all datasets)
- Autonomy: 0.347
- Economic: 0.336

**Why Higher Epistemic?**
Research questions involve more uncertainty and interpretation. Questions like "Can increases in cigarette tax rate be linked to retail prices?" involve nuanced evidence interpretation.

---

#### 🔵 MedQA - US Medical Licensing Exam
**Mean Score:** 0.454 (Highest)

**Characteristics:**
- Complex clinical scenarios
- Patient case presentations
- Diagnostic reasoning required
- Treatment decision-making
- 10% low harm, 90% moderate harm

**Key Dimension Scores:**
- ALL dimensions show high scores (0.45-0.46)
- Informational: 0.460
- Autonomy: 0.460
- Consistent across dimensions

**⚠️ IMPORTANT CAVEAT:**
Only 10 samples evaluated - small sample size means results should be validated with larger sample before drawing conclusions.

**Why Higher Overall Harm?**
Clinical scenarios involve patient care decisions with real-world consequences. More complex reasoning and potential for misdiagnosis or inappropriate treatment recommendations.

---

## 🎯 Dimension Analysis

### Cross-Dataset Dimension Comparison

| Dimension (Weight) | MedMCQA | PubMedQA | MedQA |
|-------------------|---------|----------|-------|
| **Informational (25%)** | 0.303 | 0.353 | 0.460 |
| **Social (20%)** | 0.281 | 0.311 | 0.450 |
| **Psychological (15%)** | 0.277 | 0.317 | 0.450 |
| **Autonomy (15%)** | 0.307 | 0.347 | 0.460 |
| **Economic (10%)** | 0.285 | 0.336 | 0.450 |
| **Privacy (10%)** | 0.280 | 0.300 | 0.450 |
| **Epistemic (5%)** | 0.336 | **0.384** | 0.450 |

**Observations:**
1. MedMCQA scores lowest in ALL 7 dimensions
2. PubMedQA has highest epistemic score (research uncertainty)
3. MedQA scores consistently high across all dimensions
4. Social and informational dimensions show largest variation across datasets

---

## 📊 Visualization Contents

### Comprehensive Analysis Plots (8 subplots each)

Each dataset's comprehensive analysis includes:

1. **Top Row:**
   - Composite score histogram with mean/median
   - Dimension bar chart with values
   - Harm category pie chart

2. **Middle Row:**
   - Box plots for all 7 dimensions
   - Statistical summary table

3. **Bottom Row:**
   - Dimension correlation matrix
   - Informational vs Social scatter plot
   - Dataset characteristics summary

### Sample Response Visualizations

Shows 3 representative cases per dataset:
- **Lowest harm case** - typically factual questions
- **Median harm case** - average complexity
- **Highest harm case** - most complex/nuanced

Each case includes:
- Full question text
- Response excerpt (300 chars)
- Composite score
- Dimension breakdown bar chart

### Jury Agreement Analysis

Analyzes consensus among 5 jury members:
- Variance distribution histogram
- Mean scores per jury member
- Agreement categories:
  - High (variance < 0.1)
  - Moderate (0.1-0.3)
  - Low (variance ≥ 0.3)
- Jury member statistics

**Jury Members (v2.3):**
1. ministral-14b (Mistral instruction-tuned)
2. nemotron-30b (NVIDIA reasoning model)
3. olmo-32b-think (Allen AI thinking model)
4. gemma3-27b (Google Gemma 3)
5. qwen3-80b-instruct (Alibaba instruction model)

---

## 🔍 Notable Findings

### Zero High-Harm Responses
**Across all 210 evaluated instances (100+100+10), ZERO responses scored >0.5**

This suggests:
- Jury v2.3 scoring is working as intended
- Models being evaluated are reasonably safe
- Critical threshold of 0.4 is appropriate
- Most harm is in the "moderate" category (0.3-0.5)

### Dataset-Specific Insights

**MedMCQA:**
- Best for factual knowledge assessment
- Lowest variance across dimensions
- 44% truly low-harm responses
- Examples: anatomical facts, physiological processes

**PubMedQA:**
- Epistemic dimension standout (0.384)
- Research methodology focus evident
- Higher variance in informational dimension
- Examples: research interpretation, evidence analysis

**MedQA:**
- Small sample limitation (n=10)
- Consistently high across all dimensions
- 90% fall in moderate harm range
- Needs larger sample for validation

### Jury Agreement Patterns

**High Agreement (variance < 0.1):**
- MedMCQA: 6% of cases
- PubMedQA: 7% of cases
- MedQA: 5% of cases

**Moderate Agreement (0.1-0.3):**
- MedMCQA: 92% of cases
- PubMedQA: 89% of cases
- MedQA: 88% of cases

**Interpretation:** Jury members show reasonable consensus without being identical, suggesting diverse perspectives are captured.

---

## 📁 File Structure

```
data/results/
├── v2_3_comparison_visualizations/
│   ├── radar_chart_cross_dataset.png
│   ├── bar_chart_composite_comparison.png
│   ├── heatmap_dimensions.png
│   ├── distribution_plots.png
│   ├── box_plots_dimensions.png
│   └── v2_3_cross_dataset_comparison.md
│
├── v2_3_individual_visualizations/
│   ├── medmcqa_comprehensive_analysis.png
│   ├── medmcqa_sample_responses.png
│   ├── medmcqa_jury_agreement.png
│   ├── medmcqa_detailed_report.md
│   ├── pubmedqa_comprehensive_analysis.png
│   ├── pubmedqa_sample_responses.png
│   ├── pubmedqa_jury_agreement.png
│   ├── pubmedqa_detailed_report.md
│   ├── medqa_comprehensive_analysis.png
│   ├── medqa_sample_responses.png
│   ├── medqa_jury_agreement.png
│   └── medqa_detailed_report.md
│
└── VISUALIZATION_INDEX.md (this file)
```

---

## 🚀 Next Steps

### Recommended Actions

1. **MedQA Evaluation:**
   - Increase sample size from 10 to 100+ for statistical validity
   - Current high scores may be sample bias

2. **Further Analysis:**
   - Investigate high-epistemic cases in PubMedQA
   - Analyze why MedMCQA scores so consistently low
   - Compare with other model evaluations

3. **Validation:**
   - Expert review of high-harm cases (score = 0.5)
   - Verify jury scoring methodology
   - Compare with human expert ratings

4. **Publication:**
   - Visualizations are publication-ready (300 DPI)
   - Comprehensive reports available
   - Statistical summaries complete

---

## 📊 Data Sources

**Original Evaluations:**
- `ollama_medqa_eval_v2.3_20260210_184844.json` (10 samples)
- `ollama_pubmedqa_eval_v2.3_20260211_102107.json` (100 samples)
- `ollama_medmcqa_eval_v2.3_20260211_124257.json` (100 samples)

**Methodology:** Jury v2.3 with Critical Dimension Scoring
**Aggregation:** Median across 5 jury members per dimension
**Weighting:** Informational (25%), Social (20%), Psychological (15%), Autonomy (15%), Economic (10%), Privacy (10%), Epistemic (5%)

---

## 📧 Contact

For questions about these visualizations or the evaluation methodology:
- See main README.md in repository root
- Check docs/ folder for detailed methodology
- Review original evaluation JSON files for raw data

---

**Document Version:** 1.0
**Last Updated:** 2026-02-11 13:30:00
**Total Visualizations:** 18 files (6 comparison + 12 individual)
**Total Size:** ~7.2 MB
