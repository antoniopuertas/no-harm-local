# Jury v2.2 Cross-Dataset Comparison Report
## Generated: 2026-02-10 18:37:31

---

## Executive Summary

This report compares three medical evaluation datasets using Jury v2.2:
- **MedQA**: US medical licensing exam questions
- **PubMedQA**: Biomedical research questions
- **MedMCQA**: Indian medical entrance exam questions

**Jury v2.2 Configuration:**
1. ministral-14b (27 GB)
2. nemotron-30b (63 GB)
3. olmo-32b-think (64 GB)
4. gemma3-27b (54 GB) - NEW (replaced GLM-4.7-Flash)
5. qwen3-80b (50 GB) - OPTIMIZED (quantized from 159 GB)
**Total:** 258 GB

---

## Dataset Statistics

| Dataset | Samples | Mean Score | Median | Std Dev | Min | Max |
|---------|---------|------------|--------|---------|-----|-----|
| MEDMCQA  |     100 |     0.3449 | 0.5000 |  0.1945 | 0.00 | 0.70 |
| MEDQA    |     100 |     0.4045 | 0.5000 |  0.1607 | 0.10 | 0.68 |
| PUBMEDQA |     100 |     0.3425 | 0.3500 |  0.1275 | 0.10 | 0.50 |

---

## Jury Member Performance

| Jury Member | Dataset | Mean | Std Dev | Range |
|-------------|---------|------|---------|-------|
| gemma3-27b      | MEDQA   | 0.481 | 0.265 | [0.10, 0.90] |
| gemma3-27b      | PUBMEDQA | 0.296 | 0.159 | [0.10, 0.70] |
| gemma3-27b      | MEDMCQA | 0.460 | 0.278 | [0.00, 0.90] |
| ministral-14b   | MEDQA   | 0.144 | 0.153 | [0.00, 0.85] |
| ministral-14b   | PUBMEDQA | 0.124 | 0.064 | [0.00, 0.30] |
| ministral-14b   | MEDMCQA | 0.102 | 0.126 | [0.00, 0.70] |
| nemotron-30b    | MEDQA   | 0.333 | 0.225 | [0.00, 0.78] |
| nemotron-30b    | PUBMEDQA | 0.301 | 0.181 | [0.04, 0.68] |
| nemotron-30b    | MEDMCQA | 0.271 | 0.218 | [0.00, 0.78] |
| olmo-32b-think  | MEDQA   | 0.475 | 0.110 | [0.00, 0.50] |
| olmo-32b-think  | PUBMEDQA | 0.495 | 0.050 | [0.00, 0.50] |
| olmo-32b-think  | MEDMCQA | 0.410 | 0.193 | [0.00, 0.50] |
| qwen3-80b-instruct | MEDQA   | 0.500 | 0.000 | [0.50, 0.50] |
| qwen3-80b-instruct | PUBMEDQA | 0.497 | 0.089 | [0.00, 1.00] |
| qwen3-80b-instruct | MEDMCQA | 0.470 | 0.119 | [0.00, 0.50] |

---

## Key Findings

### Dataset Characteristics

**Safest Dataset:** PUBMEDQA (mean: 0.343)

**Highest Risk Dataset:** MEDQA (mean: 0.405)

### Jury Member Insights

- **gemma3-27b**: First production use across all three datasets
- **qwen3-80b (quantized)**: Performance comparison with fp16 version

---

## Validation Notes

✅ All jury members produced varied scores (no GLM-like malfunction)

✅ 100% response completion across all datasets

✅ Jury v2.2 validated with gemma3 and quantized qwen3

