"""Identity checking and validation functions."""

from typing import Dict, Any, List

def has_engineer_identity(identities: List[Dict[str, Any]]) -> bool:
    """
    Check if the 'talented engineer' identity has been generated.
    
    Args:
        identities: List of identity objects
        
    Returns:
        True if the identity exists, False otherwise
    """
    for identity in identities:
        name = identity.get("name", "").lower()
        if "engineer" in name and ("talented" in name or "skilled" in name):
            return True
        
        # Also check the affirmation
        affirmation = identity.get("affirmation", "").lower()
        if "engineer" in affirmation and ("talented" in affirmation or "skilled" in affirmation):
            return True
    
    return False

def find_engineer_identity(identities: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Find and return the 'talented engineer' identity if it exists.
    
    Args:
        identities: List of identity objects
        
    Returns:
        The identity object if found, None otherwise
    """
    for identity in identities:
        name = identity.get("name", "").lower()
        affirmation = identity.get("affirmation", "").lower()
        
        if ("engineer" in name or "engineer" in affirmation) and \
           ("talented" in name or "talented" in affirmation or 
            "skilled" in name or "skilled" in affirmation):
            return identity
    
    return None

def extract_identities(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extract identities from a coach response.
    
    Args:
        response: The response from the coach API
        
    Returns:
        List of identity objects
    """
    return response.get("suggested_identities", [])
