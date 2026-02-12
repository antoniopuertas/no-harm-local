# HealthEval Format Exports

This directory contains Jury v2.3 evaluation results converted to HealthEval format for integration with the HealthEval hub.

## Files

- `healtheval_medmcqa_jury_v2.3.json` - MedMCQA dataset evaluation (4183 instances)
- `healtheval_pubmedqa_jury_v2.3.json` - PubMedQA dataset evaluation (1000 instances)

## Format

Each file contains an array of evaluation results with:

### Metrics
- `v2_3_final_score`: Primary harm score (0.0-1.0)
- `v2_3_max_dimension_score`: Maximum score across all dimensions
- Individual dimension scores:
  - `informational_harm`
  - `psychological_harm`
  - `social_harm`
  - `economic_harm`
  - `privacy_harm`
  - `autonomy_harm`
  - `epistemic_harm`

### Metadata
- `instance_id`: Unique identifier for the evaluation instance
- `question`: Medical question (truncated to 500 chars)
- `response`: Model-generated response (truncated to 500 chars)
- `v2_3_harm_level`: Categorized harm level (None/Low/Moderate/High/Critical)
- `v2_3_critical_dimension`: The dimension with highest harm score
- `v2_3_trigger`: Whether critical threshold was exceeded
- `jury_version`: "2.3"
- `scoring_methodology`: "critical_dimension_max"
- `jury_members`: List of 5 jury models used
- Dataset information (dataset, variant, split)

### Experiment Config
- `critical_threshold`: Threshold for triggering critical harm (0.4)
- `dimension_weights`: Weights applied to each dimension

## Source Data

These files were converted from the original Jury v2.3 evaluation results in:
- `../Jury_2.3/ollama_medmcqa_eval_v2.3_20260211_124257.json`
- `../Jury_2.3/ollama_pubmedqa_eval_v2.3_20260211_102107.json`

## Conversion

Files were converted using `convert_jury_v23_to_healtheval.py` script which:
1. Extracts median dimension scores from 5-member jury consensus
2. Preserves all v2.3 metadata and scoring information
3. Formats data for HealthEval hub submission

## Upload Instructions

To upload these results to HealthEval hub:

```bash
cd /path/to/health_eval/cli
pip install -e .

# Upload MedMCQA
health_eval evaluations submit \
  /path/to/healtheval_medmcqa_jury_v2.3.json \
  --model 'Jury_v2.3_Consensus' \
  --dataset 'medmcqa' \
  --name 'Jury v2.3 - MedMCQA Evaluation'

# Upload PubMedQA
health_eval evaluations submit \
  /path/to/healtheval_pubmedqa_jury_v2.3.json \
  --model 'Jury_v2.3_Consensus' \
  --dataset 'pubmedqa' \
  --name 'Jury v2.3 - PubMedQA Evaluation'
```

## Version

- Jury Version: 2.3
- Conversion Date: 2026-02-12
- Jury Members: gemma2:27b, nemotron-3-nano:30b-a3b-fp16, olmo-3.1:32b-think-fp16, qwen2.5:32b-instruct, qwen3-next:80b-a3b-thinking-fp16
