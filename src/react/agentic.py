from src.react.prompts.raw_prompt import tool_list, get_agent_prompt
from openai.types.chat import (
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionAssistantMessageParam,
    ChatCompletionMessageParam
)
from src.react.models.function_call import process_request

def get_response_prompt(input_text: str, context: str="") -> str:
    messages = [
        ChatCompletionSystemMessageParam(role="system", content=get_agent_prompt(tool_list)),
        ChatCompletionUserMessageParam(
            role="user",
            content=f"<context>{context}</context>\n<user_input>{input_text}</user_input>"
        ),
    ]
    json = process_request(message_bundle=messages)
    return "\n".join(json)