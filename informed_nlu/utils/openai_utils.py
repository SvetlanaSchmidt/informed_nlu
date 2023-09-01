from typing import List, Union, Tuple, Optional
import tiktoken

API_COSTS_PROMPT = {"gpt-4": 0.03, "gpt-4-32k": 0.06, "gpt-3.5-turbo": 0.0015}
API_COSTS_COMPLETION = {"gpt-4": 0.06, "gpt-4-32k": 0.12, "gpt-3.5-turbo": 0.002}

def calculate_api_call_len_and_price(
    prompt_text: str, model_name: str, max_tokens: int, output_text: Optional[str]=None
) -> Tuple[int, float]:
    """Calculates the prompt length and maximum API call cost, assuming the model generates up to max_tokens.

    Args:
        prompt_text: The formatted prompt text (containing the prompt input).
        model: The OpenAI model wrapper.

    Returns:
        Prompt length and API Call price as tuple.
    """
    tokenizer = tiktoken.encoding_for_model(model_name)
    prompt_len = len(tokenizer.encode(text=prompt_text))
    prompt_cost = prompt_len / 1000 * API_COSTS_PROMPT[model_name]
    if output_text is None:
        output_cost = API_COSTS_COMPLETION[model_name] * max_tokens / 1000
    else:
        output_len = len(tokenizer.encode(text=output_text))
        output_cost = output_len / 1000 * API_COSTS_COMPLETION[model_name]
    max_expected_cost = prompt_cost + output_cost
    return prompt_len + max_tokens if output_text is None else prompt_len + output_len, max_expected_cost
