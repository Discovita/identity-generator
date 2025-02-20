"""Identity extraction and visualization processing."""

from typing import List, Optional, Dict
from .models import Identity, IdentityCategory

class IdentityProcessor:
    """Processes identity-related operations in coaching responses."""

    @staticmethod
    def extract_identities(response: str) -> List[Identity]:
        """Extract suggested identities from coach response."""
        identities: List[Identity] = []
        current_category = None
        lines = response.split('\n')

        for line in lines:
            line = line.strip()
            
            # Check for category markers
            if "For your" in line:
                if "Passions & Talents" in line:
                    current_category = IdentityCategory.PASSIONS
                elif "Money & Wealth" in line:
                    current_category = IdentityCategory.MONEY_MAKER
                # Add other categories as needed
                continue

            # Look for "I am" statements
            if "I am" in line:
                parts = line.split(" - ", 1)
                if len(parts) == 2:
                    name = parts[0].replace("I am", "").strip()
                    # Remove "a" or "an" prefix if present
                    if name.startswith("a "):
                        name = name[2:].strip()
                    elif name.startswith("an "):
                        name = name[3:].strip()
                    
                    # Use current category or default to PASSIONS if not in category section
                    category = current_category or IdentityCategory.PASSIONS
                    affirmation = f"I am {name} - {parts[1].strip()}"
                    
                    identity = Identity(
                        category=category,
                        name=name,
                        affirmation=affirmation,
                        visualization={
                            "setting": "Professional environment",
                            "appearance": "Confident and capable",
                            "energy": "Focused and determined"
                        }
                    )
                    identities.append(identity)

        return identities

    @staticmethod
    def generate_visualization(identities: List[Identity]) -> Optional[Dict]:
        """Generate visualization prompts for identities."""
        if not identities:
            return None

        # Create a combined visualization incorporating aspects of all identities
        settings = []
        appearances = []
        energies = []

        for identity in identities:
            if identity.visualization:
                settings.append(identity.visualization.get("setting", ""))
                appearances.append(identity.visualization.get("appearance", ""))
                energies.append(identity.visualization.get("energy", ""))

        if not settings:  # No valid visualizations found
            return None

        return {
            "setting": " and ".join(filter(None, settings)),
            "appearance": " and ".join(filter(None, appearances)),
            "energy": " and ".join(filter(None, energies))
        }
