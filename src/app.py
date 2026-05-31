from fastapi import FastAPI
from .app_log import logger
from .models.model import CommentText
from .services.llm_service import llm_generate_comment
from .resources.llm_prompt import prompt
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://github.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/improve")
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