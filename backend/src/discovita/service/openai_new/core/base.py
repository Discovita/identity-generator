"""
Base OpenAIClient class for interacting with the OpenAI API.

This module contains the main OpenAIClient class which provides
a simplified interface to OpenAI's API.
"""

from typing import Annotated, Optional

from discovita.utils.logger import configure_logging
from openai import OpenAI

from ..utils.model_utils import check_dependency_versions

log = configure_logging(__name__)


class OpenAIClient:
    """
    A helper class for interacting with the OpenAI API.

    Provides methods for creating chat completions with support for:
    - Basic text responses
    - Image inputs
    - JSON mode
    - Structured outputs using JSON schema
    - Pydantic model parsing
    - Beta structured outputs with automatic parsing

    This class initializes the OpenAI client with your API key and
    organization, and provides methods to interact with the API.
    """

    def __init__(
        self,
        api_key: Annotated[str, "The OpenAI API Key you wish to use"],
        organization: Optional[str] = None,
    ):
        """
        Initialize the OpenAI helper with your API key and organization.

        Parameters
        ----------
        api_key : str - Your OpenAI API key
        organization : str - Your OpenAI organization ID
        """
        self.client = OpenAI(
            api_key=api_key, organization=organization if organization else None
        )

        check_dependency_versions()
