#!/usr/bin/env python3
"""
Dataset loaders for different medical evaluation benchmarks
"""

import json
from pathlib import Path
from typing import List, Dict, Optional


class DatasetLoader:
    """Base class for dataset loaders"""

    def __init__(self, base_path: Path):
        self.base_path = base_path

    def load(self, n_samples: Optional[int] = None) -> List[Dict]:
        """Load dataset instances"""
        raise NotImplementedError

    def get_question(self, instance: Dict) -> str:
        """Extract question from instance"""
        raise NotImplementedError

    def get_context(self, instance: Dict) -> str:
        """Extract context from instance (if available)"""
        return ""

    def format_for_evaluation(self, instance: Dict) -> Dict:
        """Format instance for evaluation pipeline"""
        return {
            'id': instance.get('id', 'unknown'),
            'question': self.get_question(instance),
            'context': self.get_context(instance),
            'original': instance
        }


class PubMedQALoader(DatasetLoader):
    """Loader for PubMedQA dataset"""

    def __init__(self):
        base_path = Path(__file__).parent.parent.parent / "data" / "processed" / "pubmedqa"
        super().__init__(base_path)

    def load(self, n_samples: Optional[int] = None) -> List[Dict]:
        """Load PubMedQA test instances"""
        data_path = self.base_path / "test_instances_1000.json"

        with open(data_path) as f:
            instances = json.load(f)

        if n_samples:
            instances = instances[:n_samples]

        return [self.format_for_evaluation(inst) for inst in instances]

    def get_question(self, instance: Dict) -> str:
        """Extract question from PubMedQA instance"""
        return instance['clinical_scenario']['question']

    def get_context(self, instance: Dict) -> str:
        """Extract context from PubMedQA instance"""
        # Use pre-formatted input if available
        if 'input' in instance and 'text' in instance['input']:
            return instance['input']['text']

        # Otherwise construct from context
        context_list = instance['clinical_scenario'].get('context', [])
        return ' '.join(context_list[:3])  # Limit to first 3 sentences


class MedQALoader(DatasetLoader):
    """Loader for MedQA dataset"""

    def __init__(self, variant: str = "US"):
        base_path = Path(__file__).parent.parent.parent / "benchmark_multi_scenarios" / "scenarios" / "med_qa" / "data" / "data_clean" / "questions" / variant
        super().__init__(base_path)
        self.variant = variant

    def load(self, n_samples: Optional[int] = None, split: str = "test") -> List[Dict]:
        """Load MedQA instances"""
        data_path = self.base_path / f"{split}.jsonl"

        instances = []
        with open(data_path) as f:
            for line in f:
                instances.append(json.loads(line))

        if n_samples:
            instances = instances[:n_samples]

        return [self.format_for_evaluation(inst) for inst in instances]

    def get_question(self, instance: Dict) -> str:
        """Extract question from MedQA instance"""
        return instance['question']

    def get_context(self, instance: Dict) -> str:
        """MedQA questions are self-contained clinical scenarios"""
        # The question itself contains the full clinical scenario
        return instance['question']

    def format_for_evaluation(self, instance: Dict) -> Dict:
        """Format MedQA instance with options"""
        formatted = super().format_for_evaluation(instance)
        # Include answer options for reference
        formatted['options'] = instance.get('options', {})
        formatted['answer'] = instance.get('answer', '')
        return formatted


class MedMCQALoader(DatasetLoader):
    """Loader for MedMCQA dataset"""

    def __init__(self):
        base_path = Path(__file__).parent.parent.parent / "benchmark_multi_scenarios" / "scenarios" / "med_mcqa" / "data"
        super().__init__(base_path)

    def load(self, n_samples: Optional[int] = None, split: str = "dev") -> List[Dict]:
        """Load MedMCQA instances"""
        data_path = self.base_path / f"{split}.json"

        instances = []
        with open(data_path) as f:
            for line in f:
                instances.append(json.loads(line))

        if n_samples:
            instances = instances[:n_samples]

        return [self.format_for_evaluation(inst) for inst in instances]

    def get_question(self, instance: Dict) -> str:
        """Extract question from MedMCQA instance"""
        return instance['question']

    def get_context(self, instance: Dict) -> str:
        """MedMCQA questions are knowledge-based with options"""
        # Include explanation if available
        exp = instance.get('exp', '')
        if exp:
            return f"Question: {instance['question']}\nExplanation available: {exp[:200]}"
        return instance['question']

    def format_for_evaluation(self, instance: Dict) -> Dict:
        """Format MedMCQA instance with options"""
        formatted = super().format_for_evaluation(instance)
        # Include options
        formatted['options'] = {
            'A': instance.get('opa', ''),
            'B': instance.get('opb', ''),
            'C': instance.get('opc', ''),
            'D': instance.get('opd', '')
        }
        formatted['subject'] = instance.get('subject_name', '')
        formatted['topic'] = instance.get('topic_name', '')
        return formatted


def get_dataset_loader(dataset_name: str, **kwargs) -> DatasetLoader:
    """Factory function to get appropriate dataset loader"""
    loaders = {
        'pubmedqa': PubMedQALoader,
        'medqa': MedQALoader,
        'medmcqa': MedMCQALoader
    }

    dataset_name_lower = dataset_name.lower()
    if dataset_name_lower not in loaders:
        raise ValueError(f"Unknown dataset: {dataset_name}. Available: {list(loaders.keys())}")

    return loaders[dataset_name_lower](**kwargs)


# Available datasets with descriptions
AVAILABLE_DATASETS = {
    'pubmedqa': {
        'description': 'PubMedQA - Biomedical research questions with evidence-based context',
        'size': 1000,
        'loader_kwargs': {}
    },
    'medqa': {
        'description': 'MedQA - Clinical case scenarios from medical licensing exams',
        'size': 1273,
        'loader_kwargs': {'variant': 'US'}  # Can be US, Mainland, or Taiwan
    },
    'medmcqa': {
        'description': 'MedMCQA - Medical knowledge questions from Indian entrance exams',
        'size': 4183,
        'loader_kwargs': {}
    }
}
