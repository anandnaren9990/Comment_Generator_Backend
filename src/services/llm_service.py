import httpx
from ..resources.llm_prompt import prompt
from ..resources.llm_properties import llama_chat_url, model
from ..app_log import logger

async def llm_generate_comment(messages: list):
    try:
        payload = {
            "model" : model,
            "messages" : messages,
            "stream" : False
        }
        logger.info("Sending comment to LLM...")
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url = llama_chat_url,
                json = payload,
                timeout=15
            )
        response.raise_for_status()
        data = response.json()["message"]["content"]
        return data
    except httpx.HTTPError as e:
        logger.error(f"HTTP error occured: {e}")
        raise
    except httpx.ConnectError as e:
        logger.error(f"Error connecting to LLM: {e}")
        raise
    except httpx.ConnectTimeout as e:
        logger.error(f"LLM took long time to respond: {e}")
        raise
    except Exception as e:
        logger.error(f"Error occured: {e}")
        raise

    