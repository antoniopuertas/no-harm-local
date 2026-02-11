# Jury v2.3 Cross-Dataset Comparison Report
**Generated:** 2026-02-11 13:16:03

---

## Executive Summary

This report compares three medical evaluation datasets using **Jury v2.3** with **Critical Dimension Scoring**:

- **MedQA**: US medical licensing exam questions
- **PubMedQA**: Biomedical research questions  
- **MedMCQA**: Indian medical entrance exam questions

### Jury v2.3 Configuration

**5-Member Jury:**
1. ministral-14b (Mistral's instruction-tuned model)
2. nemotron-30b (NVIDIA's reasoning model)
3. olmo-32b-think (Allen AI's thinking model)
4. gemma3-27b (Google's latest Gemma)
5. qwen3-80b-instruct (Alibaba's instruction model)

**Scoring Methodology:** Critical Dimension Max (v2.3)
- 7 harm dimensions with weighted aggregation
- Median aggregation across jury members
- Critical threshold: 0.4

---

## Dataset Statistics

| Dataset | Samples | Mean Composite | Median | Std Dev | Min | Max |
|---------|---------|----------------|--------|---------|-----|-----|
| **MEDMCQA** | 100 | 0.2931 | 0.5000 | 0.2301 | 0.0000 | 0.5000 |
| **MEDQA** | 10 | 0.4540 | 0.5000 | 0.1455 | 0.0400 | 0.5000 |
| **PUBMEDQA** | 100 | 0.3328 | 0.5000 | 0.2025 | 0.0000 | 0.5000 |

---

## Dimension Score Comparison

Mean scores for each dimension across datasets:

| Dimension | MedQA | PubMedQA | MedMCQA | Weight |
|-----------|-------|----------|---------|--------|
| **Informational** | 0.303 | 0.460 | 0.353 | 0.25 |
| **Psychological** | 0.277 | 0.450 | 0.317 | 0.15 |
| **Social** | 0.281 | 0.450 | 0.311 | 0.20 |
| **Economic** | 0.285 | 0.450 | 0.336 | 0.10 |
| **Privacy** | 0.280 | 0.450 | 0.300 | 0.10 |
| **Autonomy** | 0.307 | 0.460 | 0.347 | 0.15 |
| **Epistemic** | 0.336 | 0.450 | 0.384 | 0.05 |

---

## Harm Distribution

Classification of responses by composite harm score:

| Dataset | Low (<0.3) | Moderate (0.3-0.5) | High (>0.5) |
|---------|------------|--------------------|--------------|
| **MEDMCQA** | 44 (44.0%) | 56 (56.0%) | 0 (0.0%) |
| **MEDQA** | 1 (10.0%) | 9 (90.0%) | 0 (0.0%) |
| **PUBMEDQA** | 41 (41.0%) | 59 (59.0%) | 0 (0.0%) |

---

## Key Findings

### Overall Safety Rankings

1. **Safest Dataset:** MEDMCQA (mean: 0.293)
2. **Highest Risk Dataset:** MEDQA (mean: 0.454)

### Dimension-Specific Insights

**Informational** (weight: 25%):
- Lowest: MEDMCQA (0.303)
- Highest: MEDQA (0.460)

**Psychological** (weight: 15%):
- Lowest: MEDMCQA (0.277)
- Highest: MEDQA (0.450)

**Social** (weight: 20%):
- Lowest: MEDMCQA (0.281)
- Highest: MEDQA (0.450)

**Economic** (weight: 10%):
- Lowest: MEDMCQA (0.285)
- Highest: MEDQA (0.450)

**Privacy** (weight: 10%):
- Lowest: MEDMCQA (0.280)
- Highest: MEDQA (0.450)

**Autonomy** (weight: 15%):
- Lowest: MEDMCQA (0.307)
- Highest: MEDQA (0.460)

**Epistemic** (weight: 5%):
- Lowest: MEDMCQA (0.336)
- Highest: MEDQA (0.450)

---

## Visualizations

The following visualizations have been generated:

1. **Radar Chart** (`radar_chart_cross_dataset.png`): 7-dimensional comparison across datasets
2. **Bar Chart** (`bar_chart_composite_comparison.png`): Composite score comparison with error bars
3. **Heatmap** (`heatmap_dimensions.png`): Dimension scores across datasets
4. **Distribution Plots** (`distribution_plots.png`): Histogram of composite scores per dataset
5. **Box Plots** (`box_plots_dimensions.png`): Distribution of dimension scores

---

## Validation

✅ All jury members produced varied scores across datasets

✅ 100% response completion across all evaluations

✅ Jury v2.3 with Critical Dimension Scoring validated

**Report generated:** 2026-02-11 13:16:03
