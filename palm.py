# You can take a look: https://github.com/google/generative-ai-python/blob/v0.1.0/google/generativeai/__init__.py

# pip install google-generativeai

import google.generativeai as palm

palm.configure(api_key='API_KEY')

"""
# Use palm.list_models to discover models:

import pprint
for model in palm.list_models():
    pprint.pprint(model)
"""

"""
def generate_text(
    *,
    model: Optional[model_types.ModelNameOptions] = "models/text-bison-001",
    prompt: str,
    temperature: Optional[float] = None,
    candidate_count: Optional[int] = None,
    max_output_tokens: Optional[int] = None,
    top_p: Optional[float] = None,
    top_k: Optional[float] = None,
    safety_settings: Optional[Iterable[safety.SafetySettingDict]] = None,
    stop_sequences: Union[str, Iterable[str]] = None,
    client: Optional[glm.TextServiceClient] = None,
) -> text_types.Completion:
"""
"""
    # Calls the API and returns a `types.Completion` containing the response.

    Args:
        model: Which model to call, as a string or a `types.Model`.
        prompt: Free-form input text given to the model. Given a prompt, the model will
                generate text that completes the input text.
        temperature: Controls the randomness of the output. Must be positive.
            Typical values are in the range: `[0.0,1.0]`. Higher values produce a
            more random and varied response. A temperature of zero will be deterministic.
        candidate_count: The **maximum** number of generated response messages to return.
            This value must be between `[1, 8]`, inclusive. If unset, this
            will default to `1`.

            Note: Only unique candidates are returned. Higher temperatures are more
            likely to produce unique candidates. Setting `temperature=0.0` will always
            return 1 candidate regardless of the `candidate_count`.
        max_output_tokens: Maximum number of tokens to include in a candidate. Must be greater
                           than zero. If unset, will default to 64.
        top_k: The API uses combined [nucleus](https://arxiv.org/abs/1904.09751) and top-k sampling.
            `top_k` sets the maximum number of tokens to sample from on each step.
        top_p: The API uses combined [nucleus](https://arxiv.org/abs/1904.09751) and top-k sampling.
            `top_p` configures the nucleus sampling. It sets the maximum cumulative
            probability of tokens to sample from.
            For example, if the sorted probabilities are
            `[0.5, 0.2, 0.1, 0.1, 0.05, 0.05]` a `top_p` of `0.8` will sample
            as `[0.625, 0.25, 0.125, 0, 0, 0]`.
        safety_settings: A list of unique `types.SafetySetting` instances for blocking unsafe content.
           These will be enforced on the `prompt` and
           `candidates`. There should not be more than one
           setting for each `types.SafetyCategory` type. The API will block any prompts and
           responses that fail to meet the thresholds set by these settings. This list
           overrides the default settings for each `SafetyCategory` specified in the
           safety_settings. If there is no `types.SafetySetting` for a given
           `SafetyCategory` provided in the list, the API will use the default safety
           setting for that category.
        stop_sequences: A set of up to 5 character sequences that will stop output generation.
          If specified, the API will stop at the first appearance of a stop
          sequence. The stop sequence will not be included as part of the response.
        client: If you're not relying on a default client, you pass a `glm.TextServiceClient` instead.

    Returns:
        A `types.Completion` containing the model's text completion response.
"""
"""
    request = _make_generate_text_request(
        model=model,
        prompt=prompt,
        temperature=temperature,
        candidate_count=candidate_count,
        max_output_tokens=max_output_tokens,
        top_p=top_p,
        top_k=top_k,
        safety_settings=safety_settings,
        stop_sequences=stop_sequences,
    )
"""

# How to use:
response = palm.generate_text(prompt="The opposite of hot is")
print(response.result) #  'cold.'


