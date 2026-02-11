#!/usr/bin/env python3
"""
Option 2: Test Jury v2.3
Runs validation tests and 10-sample pilot evaluation
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime

def run_validation_tests():
    """Run v2.3 implementation validation tests"""
    print("=" * 80)
    print("STEP 1: VALIDATION TESTS")
    print("=" * 80)
    print()

    result = subprocess.run(
        ['python3', 'scripts/test_v2_3_implementation.py'],
        capture_output=True,
        text=True
    )

    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)

    if result.returncode != 0:
        print("\n✗ Validation tests FAILED")
        return False

    print("\n✓ Validation tests PASSED")
    return True

def run_pilot_evaluation(dataset='medqa'):
    """Run 10-sample pilot evaluation with v2.3"""
    print("\n" + "=" * 80)
    print(f"STEP 2: PILOT EVALUATION ({dataset.upper()}, 10 samples)")
    print("=" * 80)
    print()

    result = subprocess.run([
        'python3', 'scripts/run_ollama_evaluation_v2_3.py',
        '--dataset', dataset,
        '--samples', '10',
        '--split', 'test' if dataset == 'medqa' else 'validation',
        '--variant', 'US'
    ] if dataset == 'medqa' else [
        'python3', 'scripts/run_ollama_evaluation_v2_3.py',
        '--dataset', dataset,
        '--samples', '10',
        '--split', 'validation'
    ])

    if result.returncode != 0:
        print(f"\n✗ Pilot evaluation FAILED")
        return False

    print(f"\n✓ Pilot evaluation COMPLETE")
    return True

def analyze_pilot_results():
    """Analyze pilot results and compare v2.2 vs v2.3"""
    print("\n" + "=" * 80)
    print("STEP 3: PILOT RESULTS ANALYSIS")
    print("=" * 80)
    print()

    import json
    from pathlib import Path

    # Find most recent v2.3 result
    results_dir = Path("data/results")
    v2_3_files = sorted(results_dir.glob("ollama_*_eval_v2.3_*.json"),
                       key=lambda x: x.stat().st_mtime, reverse=True)

    if not v2_3_files:
        print("✗ No v2.3 results found")
        return False

    results_file = v2_3_files[0]
    print(f"Analyzing: {results_file.name}")

    with open(results_file) as f:
        data = json.load(f)

    results = data['results']
    metadata = data['metadata']

    print(f"\nDataset: {metadata['dataset'].upper()}")
    print(f"Samples: {metadata['n_instances']}")
    print(f"Jury Version: {metadata['jury_version']}")
    print(f"Methodology: {metadata['scoring_methodology']}")

    # Compare v2.2 vs v2.3 scores
    v2_2_scores = [r['v2_2_weighted_composite'] for r in results]
    v2_3_scores = [r['v2_3_final_score'] for r in results]

    print(f"\nv2.2 Weighted Composite:")
    print(f"  Mean: {sum(v2_2_scores)/len(v2_2_scores):.3f}")
    print(f"  Range: [{min(v2_2_scores):.3f}, {max(v2_2_scores):.3f}]")

    print(f"\nv2.3 Final Score:")
    print(f"  Mean: {sum(v2_3_scores)/len(v2_3_scores):.3f}")
    print(f"  Range: [{min(v2_3_scores):.3f}, {max(v2_3_scores):.3f}]")

    # Critical dimension triggers
    critical_triggers = sum(1 for r in results if r['v2_3_trigger'] == 'critical_dimension')
    print(f"\nCritical Dimension Triggers: {critical_triggers}/{len(results)} ({critical_triggers/len(results)*100:.1f}%)")

    if critical_triggers > 0:
        from collections import Counter
        critical_dims = [r['v2_3_critical_dimension'] for r in results if r['v2_3_critical_dimension']]
        dim_counts = Counter(critical_dims)
        print("  Most common:")
        for dim, count in dim_counts.most_common(3):
            print(f"    {dim}: {count}")

    # Divergence analysis
    divergent = sum(1 for r in results if abs(r['v2_3_final_score'] - r['v2_2_weighted_composite']) > 0.2)
    print(f"\nv2.3 vs v2.2 Divergence (>0.2 diff): {divergent}/{len(results)} ({divergent/len(results)*100:.1f}%)")

    print("\n✓ Pilot analysis COMPLETE")
    return True

def main():
    """Main test sequence"""
    print("=" * 80)
    print("JURY v2.3 TESTING SUITE")
    print("=" * 80)
    print(f"\nStarted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Step 1: Validation tests
    if not run_validation_tests():
        print("\n✗ Testing aborted due to validation failure")
        return 1

    # Step 2: Pilot evaluation (10 samples)
    if not run_pilot_evaluation('medqa'):
        print("\n✗ Testing aborted due to pilot evaluation failure")
        return 1

    # Step 3: Analyze results
    if not analyze_pilot_results():
        print("\n✗ Testing aborted due to analysis failure")
        return 1

    print("\n" + "=" * 80)
    print("✓✓ JURY v2.3 TESTING COMPLETE")
    print("=" * 80)
    print(f"\nFinished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nJury v2.3 validated and ready for full evaluation!")

    return 0

if __name__ == '__main__':
    sys.exit(main())
