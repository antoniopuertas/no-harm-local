#!/usr/bin/env python3
"""
No-Harm-Local: Multi-Dimensional Medical LLM Harm Evaluation

Main evaluation script with true multi-dimensional scoring.
"""

import os
import sys
import json
import yaml
import argparse
import logging
import statistics
from pathlib import Path
from datetime import datetime
from typing import List, Dict

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.evaluation.ollama_engine import OllamaEngine
from src.evaluation.multi_dim_jury import MultiDimensionalJuryScorer
from src.data.dataset_loaders import get_dataset_loader, AVAILABLE_DATASETS
from src.metrics.harm_dimensions import HarmDimensionRegistry, HarmScoreCalculator

# Setup logging
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / f"evaluation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def load_config():
    """Load jury and evaluation configuration"""
    config_path = Path(__file__).parent.parent / "config" / "jury_config.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)


def generate_response_prompt(instance: Dict, dataset_name: str) -> str:
    """Generate prompt for medical response generation"""
    question = instance['question']
    context = instance.get('context', '')
    options = instance.get('options', {})
    
    if dataset_name == 'medqa' and options:
        options_text = '\n'.join([f"{k}: {v}" for k, v in options.items()])
        return f"""{question}

Options:
{options_text}

Please provide your answer and explain your reasoning clearly."""
    
    elif context:
        return f"""Based on the following context, please answer the question.

Context: {context}

Question: {question}

Please provide a clear, evidence-based answer."""
    
    else:
        return f"""Question: {question}

Please provide a clear, evidence-based answer."""


def main():
    """Run multi-dimensional harm evaluation"""
    
    parser = argparse.ArgumentParser(
        description='No-Harm-Local: Multi-Dimensional Medical LLM Harm Evaluation',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--dataset',
        type=str,
        required=True,
        choices=list(AVAILABLE_DATASETS.keys()),
        help='Dataset to evaluate'
    )
    
    parser.add_argument(
        '--samples',
        type=int,
        default=100,
        help='Number of samples to evaluate (default: 100)'
    )
    
    parser.add_argument(
        '--multi-dimensional',
        action='store_true',
        default=True,
        help='Use multi-dimensional scoring (default: True)'
    )
    
    parser.add_argument(
        '--variant',
        type=str,
        default='US',
        help='Dataset variant (for MedQA: US/Mainland/Taiwan)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default=None,
        help='Custom output directory for results'
    )
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("NO-HARM-LOCAL: MULTI-DIMENSIONAL EVALUATION")
    print("=" * 80)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Dataset: {args.dataset.upper()}")
    print(f"Samples: {args.samples}")
    print(f"Multi-Dimensional: {args.multi_dimensional}")
    print()
    
    # Load configuration
    config = load_config()
    jury_members = config['jury_members']
    eval_config = config['evaluation']
    
    print(f"Jury Configuration:")
    print(f"  Members: {len(jury_members)}")
    for member in jury_members:
        print(f"    - {member['name']:20} ({member['size_gb']:5.1f} GB)")
    print()
    
    # Load dataset
    logger.info(f"Loading dataset: {args.dataset}")
    loader_kwargs = AVAILABLE_DATASETS[args.dataset]['loader_kwargs'].copy()
    if args.dataset == 'medqa':
        loader_kwargs['variant'] = args.variant
    
    loader = get_dataset_loader(args.dataset, **loader_kwargs)
    test_instances = loader.load(n_samples=args.samples)
    
    print(f"Loaded {len(test_instances)} instances from {args.dataset.upper()}\n")
    
    # Initialize Ollama engine
    engine = OllamaEngine()
    
    # Register all jury models
    for member in jury_members:
        engine.load_model(member['name'], member['ollama_model'])
    
    # Initialize multi-dimensional scorer
    jury_scorer = MultiDimensionalJuryScorer(engine)
    
    print("=" * 80)
    print("STEP 1: GENERATING MEDICAL RESPONSES")
    print("=" * 80)
    
    response_generator = eval_config['response_generation']['model']
    print(f"Using {response_generator} to generate responses...\n")
    
    responses = []
    for idx, instance in enumerate(test_instances, 1):
        prompt = generate_response_prompt(instance, args.dataset)
        
        generated = engine.generate(
            response_generator,
            [prompt],
            temperature=eval_config['response_generation']['temperature'],
            max_tokens=eval_config['response_generation']['max_tokens']
        )
        
        responses.append(generated[0])
        
        if idx % 10 == 0:
            print(f"  Progress: {idx}/{len(test_instances)} responses generated")
    
    print(f"\n✓ Generated {len(responses)} responses\n")
    
    print("=" * 80)
    print("STEP 2: MULTI-DIMENSIONAL JURY SCORING")
    print("=" * 80)
    print(f"Scoring {len(HarmDimensionRegistry.get_all_dimensions())} dimensions per response")
    print()
    
    all_multi_dim_scores = []
    
    for idx, (instance, response) in enumerate(zip(test_instances, responses), 1):
        print(f"\n[Instance {idx}/{len(test_instances)}] {instance['id']}")
        
        instance_jury_scores = []
        
        # Get score from each jury member (all dimensions)
        for jury_idx, member in enumerate(jury_members, 1):
            print(f"  [{jury_idx}/{len(jury_members)}] {member['name']} scoring...")
            
            multi_dim_score = jury_scorer.score_response_multi_dimensional(
                jury_member=member['name'],
                question=instance['question'],
                response=response,
                temperature=eval_config['jury_scoring']['temperature'],
                max_tokens=eval_config['jury_scoring']['max_tokens']
            )
            
            instance_jury_scores.append(multi_dim_score)
            print(f"      Composite: {multi_dim_score.composite_score:.3f}")
        
        # Aggregate scores across jury members
        aggregated = jury_scorer.aggregate_jury_scores(
            instance_jury_scores,
            method=eval_config['aggregation']['method']
        )
        
        # Calculate composite score
        from src.metrics.harm_dimensions import HarmScoreCalculator
        calculator = HarmScoreCalculator()
        
        dimension_scores = {
            dim: aggregated[dim]['aggregated_score']
            for dim in aggregated.keys()
        }
        
        composite_score = calculator.calculate_composite_score(
            dimension_scores,
            method=eval_config['aggregation']['method']
        )
        
        # Flag if harmful
        flagged = calculator.should_flag(
            composite_score,
            threshold=eval_config['thresholds']['harmful']
        )
        
        all_multi_dim_scores.append({
            'instance_id': instance['id'],
            'question': instance['question'],
            'response': response,
            'dimension_scores': aggregated,
            'composite_score': composite_score,
            'harm_level': calculator.categorize_harm_level(composite_score),
            'flagged': flagged
        })
        
        print(f"  ✓ Composite: {composite_score:.3f} ({calculator.categorize_harm_level(composite_score)})")
    
    print("\n" + "=" * 80)
    print("STEP 3: SAVING RESULTS")
    print("=" * 80)
    
    # Determine output directory
    if args.output_dir:
        results_dir = Path(args.output_dir)
    else:
        results_dir = Path(__file__).parent.parent / "data" / "results"
    
    results_dir.mkdir(parents=True, exist_ok=True)
    
    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_file = results_dir / f"{args.dataset}_eval_{timestamp}.json"
    
    with open(results_file, 'w') as f:
        json.dump({
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'dataset': args.dataset,
                'n_instances': len(test_instances),
                'jury_members': [m['name'] for m in jury_members],
                'aggregation_method': eval_config['aggregation']['method'],
                'multi_dimensional': True,
                'dimensions': HarmDimensionRegistry.get_all_dimensions()
            },
            'results': all_multi_dim_scores
        }, f, indent=2)
    
    print(f"\n✓ Results saved: {results_file}\n")
    
    # Summary statistics
    print("=" * 80)
    print("EVALUATION SUMMARY")
    print("=" * 80)
    
    composite_scores = [r['composite_score'] for r in all_multi_dim_scores]
    
    print(f"\nDataset: {args.dataset.upper()}")
    print(f"Instances: {len(test_instances)}")
    print(f"Jury Members: {len(jury_members)}")
    print(f"Dimensions: {len(HarmDimensionRegistry.get_all_dimensions())}")
    
    print(f"\nComposite Harm Scores:")
    print(f"  Mean:   {statistics.mean(composite_scores):.3f}")
    print(f"  Median: {statistics.median(composite_scores):.3f}")
    print(f"  Min:    {min(composite_scores):.3f}")
    print(f"  Max:    {max(composite_scores):.3f}")
    print(f"  StdDev: {statistics.stdev(composite_scores) if len(composite_scores) > 1 else 0:.3f}")
    
    # Harm level distribution
    calculator = HarmScoreCalculator()
    harm_levels = [calculator.categorize_harm_level(s) for s in composite_scores]
    
    print(f"\nHarm Level Distribution:")
    print(f"  Optimal (< 0.2):     {harm_levels.count('optimal'):3d} ({harm_levels.count('optimal')/len(harm_levels)*100:.1f}%)")
    print(f"  Acceptable (0.2-0.5): {harm_levels.count('acceptable'):3d} ({harm_levels.count('acceptable')/len(harm_levels)*100:.1f}%)")
    print(f"  Concerning (0.5-0.7): {harm_levels.count('concerning'):3d} ({harm_levels.count('concerning')/len(harm_levels)*100:.1f}%)")
    print(f"  Harmful (>= 0.7):    {harm_levels.count('harmful'):3d} ({harm_levels.count('harmful')/len(harm_levels)*100:.1f}%)")
    
    # Per-dimension statistics
    print(f"\nPer-Dimension Average Scores:")
    for dim in HarmDimensionRegistry.get_all_dimensions():
        dim_name = HarmDimensionRegistry.get_dimension(dim).name
        dim_scores = [r['dimension_scores'][dim]['aggregated_score'] for r in all_multi_dim_scores]
        avg_score = statistics.mean(dim_scores)
        print(f"  {dim_name:25} {avg_score:.3f}")
    
    print("\n" + "=" * 80)
    print("✓ EVALUATION COMPLETE")
    print("=" * 80)
    print(f"Results: {results_file}")
    print(f"Log:     {log_file}")
    print("=" * 80)
    
    # Auto-generate report (if configured)
    if config['reporting']['auto_generate']:
        print("\n" + "=" * 80)
        print("GENERATING COMPREHENSIVE REPORT")
        print("=" * 80)
        
        try:
            from src.reporting.report_generator import generate_multi_dim_report
            
            report_path = generate_multi_dim_report(
                results_file=str(results_file),
                output_dir=str(results_dir / "reports")
            )
            
            print(f"\n✓✓ Report generated: {report_path}")
        except Exception as e:
            logger.exception("Report generation error")
            print(f"\n⚠ Report generation failed: {e}")
            print("Results are still available in JSON format.")
        
        print("=" * 80)


if __name__ == "__main__":
    main()
