"""Identity checking and validation functions."""

from typing import Dict, Any, List, Optional

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

def find_engineer_identity(identities: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
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

def is_engineer_identity(identity: Dict[str, Any]) -> bool:
    """
    Check if a single identity is a 'talented engineer' identity.
    
    Args:
        identity: An identity object
        
    Returns:
        True if the identity is a talented engineer, False otherwise
    """
    if not identity:
        return False
        
    name = identity.get("name", "").lower()
    affirmation = identity.get("affirmation", "").lower()
    
    return (("engineer" in name or "engineer" in affirmation) and 
            ("talented" in name or "talented" in affirmation or 
             "skilled" in name or "skilled" in affirmation))

def extract_identities(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extract all identities from a coach response.
    
    Args:
        response: The response from the coach API
        
    Returns:
        List of identity objects
    """
    all_identities = []
    
    # Add proposed identity if present
    proposed = response.get("proposed_identity")
    if proposed:
        all_identities.append(proposed)
    
    # Add confirmed identity if present
    confirmed = response.get("confirmed_identity")
    if confirmed:
        all_identities.append(confirmed)
    
    return all_identities
