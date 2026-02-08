# Quick Start Guide

## Installation

### 1. Prerequisites

- **Python 3.8+**
- **Ollama** installed and running
- **Hardware**: 190GB+ VRAM (e.g., 2x NVIDIA H100)
- **Disk Space**: 320GB for models

### 2. Install Dependencies

```bash
cd no-harm-local
pip install -r requirements.txt
```

### 3. Download Jury Models

```bash
python scripts/setup_models.py
```

This downloads all 5 jury models (~320GB). Takes 1-2 hours depending on internet speed.

## Run Your First Evaluation

### Quick Test (10 instances)

```bash
python scripts/run_evaluation.py \
    --dataset medqa \
    --samples 10 \
    --multi-dimensional
```

Expected time: ~30 minutes

### Full Evaluation (100 instances)

```bash
python scripts/run_evaluation.py \
    --dataset medqa \
    --samples 100 \
    --multi-dimensional
```

Expected time: ~4-5 hours

## Understanding Results

### Output Files

After evaluation, find results in `data/results/`:

```
data/results/
├── medqa_eval_20260208_123456.json         # Raw results
└── reports/
    ├── evaluation_report_20260208_123456.md  # Markdown report
    ├── dimension_heatmap_20260208_123456.png
    └── score_distributions_20260208_123456.png
```

### Reading the Report

```bash
# View in terminal
cat data/results/reports/evaluation_report_*.md

# Or open in VS Code, browser, etc.
```

The report includes:
- **Executive Summary**: Overall findings
- **Dimension Analysis**: All 7 harm dimensions
- **Harm Distribution**: Optimal/acceptable/concerning/harmful counts
- **Flagged Instances**: High-harm responses for review

## What's Next?

- **Try different datasets**: `--dataset pubmedqa` or `--dataset medmcqa`
- **Customize configuration**: Edit `config/jury_config.yaml`
- **Read full documentation**: See `docs/` folder

## Troubleshooting

### Ollama not found
```bash
curl https://ollama.ai/install.sh | sh
```

### Out of VRAM
Models auto-swap in/out. If issues persist, reduce `--samples`.

### Model download fails
Re-run `python scripts/setup_models.py` - it will skip already downloaded models.

## Support

- **Issues**: GitHub Issues
- **Documentation**: `docs/` folder
- **Examples**: `examples/` folder
