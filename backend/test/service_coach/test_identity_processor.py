"""Tests for coach service identity processor."""

from discovita.service.coach.identity_processor import IdentityProcessor
from discovita.service.coach.models import Identity, IdentityCategory

def test_extract_identities_from_basic_response():
    """Test extracting identities from a simple response."""
    processor = IdentityProcessor()
    response = """
    I hear you want to be a Creative Visionary. Let's explore what that means.
    I am a Creative Visionary - I bring bold, beautiful ideas to life.
    """
    identities = processor.extract_identities(response)
    assert len(identities) == 1
    assert identities[0].category == IdentityCategory.PASSIONS
    assert identities[0].name == "Creative Visionary"
    assert "bold, beautiful ideas" in identities[0].affirmation

def test_extract_identities_with_categories():
    """Test extracting identities with their categories."""
    processor = IdentityProcessor()
    response = """
    For your Passions & Talents:
    I am a Creative Visionary - bringing ideas to life with imagination
    
    For your Money & Wealth:
    I am a Wealth Architect - building financial security with wisdom
    """
    identities = processor.extract_identities(response)
    assert len(identities) == 2
    assert identities[0].category == IdentityCategory.PASSIONS
    assert identities[0].name == "Creative Visionary"
    assert "imagination" in identities[0].affirmation
    assert identities[1].category == IdentityCategory.MONEY_MAKER
    assert identities[1].name == "Wealth Architect"
    assert "financial security" in identities[1].affirmation

def test_generate_visualization_basic():
    """Test generating visualization for a single identity."""
    processor = IdentityProcessor()
    identity = Identity(
        category=IdentityCategory.PASSIONS,
        name="Creative Visionary",
        affirmation="I bring bold ideas to life",
        visualization={
            "setting": "Creative studio",
            "appearance": "Professional attire",
            "energy": "Dynamic and inspired"
        }
    )
    visualization = processor.generate_visualization([identity])
    assert visualization is not None
    assert "Creative studio" in visualization["setting"]
    assert "Professional attire" in visualization["appearance"]
    assert "Dynamic and inspired" in visualization["energy"]

def test_generate_visualization_multiple():
    """Test generating visualization for multiple identities."""
    processor = IdentityProcessor()
    identities = [
        Identity(
            category=IdentityCategory.PASSIONS,
            name="Creative Visionary",
            affirmation="I bring bold ideas to life",
            visualization={
                "setting": "Creative studio",
                "appearance": "Professional attire",
                "energy": "Dynamic and inspired"
            }
        ),
        Identity(
            category=IdentityCategory.MONEY_MAKER,
            name="Wealth Architect",
            affirmation="I build lasting financial abundance",
            visualization={
                "setting": "Modern office",
                "appearance": "Business professional",
                "energy": "Confident and focused"
            }
        )
    ]
    visualization = processor.generate_visualization(identities)
    assert visualization is not None
    assert "Creative studio" in visualization["setting"]
    assert "Modern office" in visualization["setting"]
    assert "Professional attire" in visualization["appearance"]
    assert "Business professional" in visualization["appearance"]
    assert "Dynamic and inspired" in visualization["energy"]
    assert "Confident and focused" in visualization["energy"]

def test_generate_visualization_empty():
    """Test generating visualization with no identities."""
    processor = IdentityProcessor()
    visualization = processor.generate_visualization([])
    assert visualization is None
