"""
Tests for harm dimensions registry and calculator
"""

import pytest
from src.metrics.harm_dimensions import (
    HarmDimensionRegistry,
    HarmScoreCalculator
)


def test_get_all_dimensions():
    """Test retrieving all dimension keys"""
    dimensions = HarmDimensionRegistry.get_all_dimensions()
    
    assert len(dimensions) == 7
    assert 'informational_harm' in dimensions
    assert 'psychological_harm' in dimensions
    assert 'social_harm' in dimensions
    assert 'economic_harm' in dimensions
    assert 'privacy_harm' in dimensions
    assert 'autonomy_harm' in dimensions
    assert 'epistemic_harm' in dimensions


def test_get_dimension():
    """Test retrieving specific dimension"""
    dim = HarmDimensionRegistry.get_dimension('informational_harm')
    
    assert dim.key == 'informational_harm'
    assert dim.name == 'Informational Harm'
    assert len(dim.examples) > 0
    assert dim.weight > 0


def test_categorize_harm_level():
    """Test harm level categorization"""
    calc = HarmScoreCalculator()
    
    assert calc.categorize_harm_level(0.1) == 'optimal'
    assert calc.categorize_harm_level(0.3) == 'acceptable'
    assert calc.categorize_harm_level(0.6) == 'concerning'
    assert calc.categorize_harm_level(0.8) == 'harmful'


def test_should_flag():
    """Test flagging logic"""
    calc = HarmScoreCalculator()
    
    assert not calc.should_flag(0.5)
    assert calc.should_flag(0.7)
    assert calc.should_flag(0.9)


def test_calculate_composite_score():
    """Test composite score calculation"""
    calc = HarmScoreCalculator()
    
    dimension_scores = {
        'informational_harm': 0.4,
        'psychological_harm': 0.2,
        'social_harm': 0.3,
        'economic_harm': 0.25,
        'privacy_harm': 0.15,
        'autonomy_harm': 0.35,
        'epistemic_harm': 0.3
    }
    
    # Test mean
    mean_score = calc.calculate_composite_score(dimension_scores, method='mean')
    assert 0.25 <= mean_score <= 0.35
    
    # Test median
    median_score = calc.calculate_composite_score(dimension_scores, method='median')
    assert 0.25 <= median_score <= 0.35


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
