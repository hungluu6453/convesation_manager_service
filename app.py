import logging
import uvicorn
from typing import List, Dict
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from constant import *
from conversation_manager import *

origins = [
    "http://localhost:8001",
]


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manager_list = {}


class Request_Item(BaseModel):
    conversation_id: str
    intent: str
    entity: Dict[str, str]
    utterance: str


class Response_Item(BaseModel):
    action: str
    response: str
    role: str
    question: str


@app.post("/api/v1/conversation_manage")
def conversation_manage(Request: Request_Item):
    conversation_id = Request.conversation_id
    intent = Request.intent
    entity = Request.entity
    utterance = Request.utterance

    if conversation_id not in manager_list.keys():
        manager_list[conversation_id] = Conversation_Manager(conversation_id)
    manager = manager_list[conversation_id]

    manager.act(intent, entity, utterance)
    response = manager.generate_response()

    logging.info('Intent: %s, Entity: %s', intent, entity)
    logging.info('Role: %s', manager.entity['role'])
    logging.info('Action: %s', manager.current_action)

    return Response_Item(
        action=manager.current_action,
        response=response,
        role=manager.entity['role'],
        question=manager.question,
    )


if __name__ == '__main__':
    uvicorn.run("app:app", host='0.0.0.0', port=8003)
