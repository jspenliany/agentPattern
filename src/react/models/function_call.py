from src.util.logger_singleton import logger
from src.react.models.interface.gemma4_api import llm_client
from src.util.util_json import extract_and_parse_json
import json

def process_request(message_bundle, model_name: str="gemma-4-31b-it", temperature: float=0.4) -> dict:
    logger.debug("process_request....begin")
    json_data = {
        "init": "no init"
    }
    try:
        response = llm_client.chat.completions.create(
            model=model_name,
            messages=message_bundle,
            temperature=temperature,
        )
        raw_text = response.choices[0].message.content.strip()
        json_data = extract_and_parse_json(raw_text)

    except Exception as e:
        logger.error(f"Error process_request : {e}")
    logger.debug("process_request....end")
    return json_data