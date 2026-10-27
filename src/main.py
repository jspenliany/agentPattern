from src.util.logger_singleton import logger
from src.react.agentic import get_response_prompt



if __name__ == '__main__':
    logger.info("begin to execute agent.....")
    while True:
        user_input = input("你想给我说啥。。。")
        if user_input.lower() in ["quit", "exit", "q"]:
            break

        user_message = user_input
        logger.info(user_message)
        output = get_response_prompt(user_message)
        logger.info(output)

