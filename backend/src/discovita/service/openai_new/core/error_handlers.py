"""
Error handling functions for OpenAI API requests.

This module contains functions for handling various error cases
that can occur during OpenAI API requests.
"""

from typing import Any, Dict, Union

from discovita.utils.logger import configure_logging

log = configure_logging(__name__)

from .completion_handlers import process_chat_completion_response


def handle_token_parameter_error(
    self, error: ValueError, clean_params: Dict[str, Any]
) -> Union[Dict[str, Any], str]:
    """
    Handle errors related to token parameter mismatches.

    This function detects when an error is due to using max_tokens
    when max_completion_tokens is required or vice versa, and retries
    the request with the correct parameter.

    Parameters
    ----------
    self : OpenAIClient
        The OpenAIClient instance
    error : ValueError
        The error that was raised during the API call
    clean_params : Dict[str, Any]
        The parameters that were used in the API call

    Returns
    -------
    Union[Dict[str, Any], str]
        The model's response after retrying with the correct parameters

    Raises
    ------
    ValueError
        If the error is not related to token parameters or retry also fails
    """
    error_msg = str(error)
    if "max_tokens" in error_msg and "max_completion_tokens" in error_msg:
        log.warning(f"Token parameter error detected: {error_msg}")

        if "max_tokens" in clean_params:
            token_value = clean_params.pop("max_tokens")
            clean_params["max_completion_tokens"] = token_value
            log.info(
                f"Switched to max_completion_tokens={token_value} for model {clean_params['model']}"
            )
        elif "max_completion_tokens" in clean_params:
            token_value = clean_params.pop("max_completion_tokens")
            clean_params["max_tokens"] = token_value
            log.info(
                f"Switched to max_tokens={token_value} for model {clean_params['model']}"
            )

        try:
            log.info(f"Retrying chat completion with corrected token parameters")
            response = self.client.chat.completions.create(**clean_params)

            stream = clean_params.get("stream", False)
            prepared_response_format = clean_params.get("response_format", None)

            return process_chat_completion_response(
                response, stream, prepared_response_format
            )

        except Exception as retry_error:
            log.error(f"Error in retry attempt: {str(retry_error)}")
            raise error
    else:
        log.error(f"Error in chat completion request: {str(error)}")
        raise
