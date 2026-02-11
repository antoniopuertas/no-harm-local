#!/bin/bash
# Run all three option scripts in sequence
# Launch with: nohup bash scripts/run_all_options.sh > /tmp/all_options_run.log 2>&1 &

set -e  # Exit on error

LOG_FILE="/tmp/all_options_run.log"

echo "================================================================================"
echo "RUNNING ALL THREE OPTION SCRIPTS"
echo "================================================================================"
echo "Started: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Option 1: Compare v2.2 evaluations
echo "================================================================================"
echo "OPTION 1: Comparing All Three v2.2 Evaluations"
echo "================================================================================"
echo ""
python3 scripts/option1_compare_v2_2_evaluations.py
OPTION1_STATUS=$?

if [ $OPTION1_STATUS -ne 0 ]; then
    echo ""
    echo "✗ Option 1 FAILED (exit code: $OPTION1_STATUS)"
    exit 1
fi

echo ""
echo "✓ Option 1 COMPLETE"
echo ""

# Option 2: Test Jury v2.3
echo "================================================================================"
echo "OPTION 2: Testing Jury v2.3 (Validation + 10-sample Pilot)"
echo "================================================================================"
echo ""
python3 scripts/option2_test_jury_v2_3.py
OPTION2_STATUS=$?

if [ $OPTION2_STATUS -ne 0 ]; then
    echo ""
    echo "✗ Option 2 FAILED (exit code: $OPTION2_STATUS)"
    exit 2
fi

echo ""
echo "✓ Option 2 COMPLETE"
echo ""

# Option 3: Full v2.3 evaluation suite
echo "================================================================================"
echo "OPTION 3: Full v2.3 Evaluation Suite (100 samples per dataset)"
echo "================================================================================"
echo ""
python3 scripts/option3_full_v2_3_evaluation_suite.py
OPTION3_STATUS=$?

if [ $OPTION3_STATUS -ne 0 ]; then
    echo ""
    echo "✗ Option 3 FAILED (exit code: $OPTION3_STATUS)"
    exit 3
fi

echo ""
echo "✓ Option 3 COMPLETE"
echo ""

# Final summary
echo "================================================================================"
echo "✓✓ ALL THREE OPTIONS COMPLETE"
echo "================================================================================"
echo "Finished: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""
echo "Results:"
echo "  - v2.2 Cross-Dataset Report: data/results/v2_2_cross_dataset_comparison.md"
echo "  - v2.3 Pilot Results: data/results/ollama_medqa_eval_v2.3_*.json"
echo "  - v2.3 Full Results: data/results/Jury_2.3/"
echo "  - v2.3 Comparison Report: data/results/Jury_2.3/v2_3_comprehensive_comparison.md"
echo ""
echo "Log file: $LOG_FILE"
echo ""
