"""Database model registry and utilities."""

from typing import Dict, Type, Set
from discovita.db.models.base import DatabaseModel

class ModelRegistry:
    """Registry for database models.
    
    This class maintains a registry of all database model types that should
    be managed by the database. Models are automatically registered when
    they inherit from DatabaseModel.
    """
    
    _models: Set[Type[DatabaseModel]] = set()
    
    @classmethod
    def register(cls, model_type: Type[DatabaseModel]) -> None:
        """Register a model type.
        
        Args:
            model_type: The model class to register
        """
        if not issubclass(model_type, DatabaseModel):
            raise TypeError(
                f"Model {model_type.__name__} must inherit from DatabaseModel"
            )
        cls._models.add(model_type)
    
    @classmethod
    def get_registered_models(cls) -> Set[Type[DatabaseModel]]:
        """Get all registered model types.
        
        Returns:
            Set of registered model classes
        """
        return cls._models.copy()

# Register models by importing them
# This ensures models are registered when the module is imported
from discovita.db.models.state import StateRecord
from discovita.db.models.context import ContextRecord
from discovita.db.models.identity import IdentityRecord
from discovita.db.models.user import UserRecord

# Force registration of core models
for model in [StateRecord, ContextRecord, IdentityRecord, UserRecord]:
    ModelRegistry.register(model)
