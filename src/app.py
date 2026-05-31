from fastapi import FastAPI
from .app_log import logger
from .models.model import CommentText
from .services.llm_service import llm_generate_comment
from .resources.llm_prompt import prompt

app = FastAPI()

message_history = [
    {
        "role" : "system",
        "content" : prompt
    }
]

@app.post("/generate-comment")
async def generate_comment(comment_text: CommentText):
    try: 
        message = {
                "role" : "user",
                "content" : comment_text.comment
                }

        message_history.append(message)
        system_message = message_history[0]
        recent_messages = message_history[-9:]
        payload_message = [system_message, *recent_messages]

        generated_comment = await llm_generate_comment(messages=payload_message)
        return {"generated_comment" : generated_comment}
    except Exception as e:
        logger.error(f"Error occured: {e}")
        raise