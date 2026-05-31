from fastapi import FastAPI
from .app_log import logger
from .models.model import CommentText
from .services.llm_service import llm_generate_comment
from .resources.llm_prompt import prompt

app = FastAPI()

@app.post("/generate-comment")
async def generate_comment(comment_text: CommentText):
    try: 
        message = [{
                "role" : "system",
                "content" : prompt
                },
                {
                "role" : "user",
                "content" : comment_text.comment
                }]
        
        generated_comment = await llm_generate_comment(messages=message)
        
        return {"generated_comment" : generated_comment}
    except Exception as e:
        logger.error(f"Error occured: {e}")
        raise