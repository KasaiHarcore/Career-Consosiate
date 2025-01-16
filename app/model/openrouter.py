"""
Interfacing with Openrouter cloud.
"""

import os
import sys
from typing import Literal

import litellm
from litellm.utils import Choices, Message, ModelResponse
from openai import BadRequestError
from tenacity import retry, stop_after_attempt, wait_random_exponential

from app.log import log_and_print
from app.model import common
from app.model.common import Model


class OPModel(Model):
    """
    Base class for creating Singleton instances of OP models.
    We use native API from OpenRouter through LiteLLM.
    """
    _instances = {}

    def __new__(cls):
        if cls not in cls._instances:
            cls._instances[cls] = super().__new__(cls)
            cls._instances[cls]._initialized = False
        return cls._instances[cls]

    def __init__(
        self, 
        name: str, 
        cost_per_input: float, 
        cost_per_output: float,
        parallel_tool_call: bool = False,
    ):
        if self._initialized:
            return
        super().__init__(name, cost_per_input, cost_per_output, parallel_tool_call)
        self._initialized = True

    def setup(self) -> None:
        """
        Check OpenRouter API key.
        """
        self.check_api_key()

    def check_api_key(self) -> str:
        """
        Check for the OPENROUTER_API_KEY environment variable.
        """
        key = os.environ.get("OPENROUTER_API_KEY")
        if not key:
            log_and_print("Please set the OPENROUTER_API_KEY env var")
            sys.exit(1)
        return key

    def extract_resp_content(self, chat_message: Message) -> str:
        """
        Given a chat completion message, extract the content from it.
        """
        content = chat_message.content
        if content is None:
            return ""
        else:
            return content


    @retry(wait=wait_random_exponential(min=30, max=600), stop=stop_after_attempt(5))
    def call(
        self,
        messages: list[dict],
        top_p: float = 1,
        tools = None,
        response_format: Literal["text", "json_object"] = "text",
        chat_mode: Literal[True, False] = False,
        **kwargs,
    ):
        """
        Calls the API to generate completions for the given inputs.
        """
        
        # FIXME: ignore tools field since we don't use tools now
        try:
            # groq models - prefilling response with { increase the success rate
            # of producing json output
            prefill_content = "{"
            if response_format == "json_object":  # prefill
                messages.append({"role": "assistant", "content": prefill_content})

            response = litellm.completion(
                model=self.name,
                messages=messages,
                temperature=common.MODEL_TEMP,
                max_tokens=4096,
                top_p=top_p,
                stream=False,
            )
            assert isinstance(response, ModelResponse)
            resp_usage = response.usage
            assert resp_usage is not None
            input_tokens = int(resp_usage.prompt_tokens)
            output_tokens = int(resp_usage.completion_tokens)
            cost = self.calc_cost(input_tokens, output_tokens)

            common.thread_cost.process_cost += cost
            common.thread_cost.process_input_tokens += input_tokens
            common.thread_cost.process_output_tokens += output_tokens

            first_resp_choice = response.choices[0]
            assert isinstance(first_resp_choice, Choices)
            resp_msg: Message = first_resp_choice.message
            content = self.extract_resp_content(resp_msg)
            if response_format == "json_object":
                # prepend the prefilled character
                if not content.startswith(prefill_content):
                    content = prefill_content + content
            return content, cost, input_tokens, output_tokens

        except BadRequestError as e:
            if e.code == "context_length_exceeded":
                log_and_print("Context length exceeded")
            raise e
        
class GPT4(OPModel):
    def __init__(self):
        super().__init__(
            "openrouter/openai/gpt-4", 0.00000005, 0.00000010, parallel_tool_call=True
        )
        self.note = "GPT-4 model from OpenAI"
        
class Llama31_405B_Instruct(OPModel):
    def __init__(self):
        super().__init__(
            "openrouter/meta-llama/llama-3.1-405b-instruct:free", 0, 0, parallel_tool_call=True
        )
        self.note = "Llama 3.1 405B Instruct model"