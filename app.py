import logging
import uvicorn
from typing import List, Dict
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from constant import *
from conversation_manager import *


logging.basicConfig(level=logging.INFO)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manager_list = {}


class Request_Item(BaseModel):
    conversation_id: str
    intent: str = None
    entity_dict: Dict[str, List]
    utterance: str


class Response_Item(BaseModel):
    action: str
    response: List
    role: str = None
    question: str = None


@app.post("/bkheart/api/conversation_update")
def conversation_update(Request: Request_Item):

    conversation_id = Request.conversation_id
    intent = Request.intent
    entity_dict = Request.entity_dict
    utterance = Request.utterance

    if conversation_id not in manager_list.keys():
        manager_list[conversation_id] = Conversation_Manager(conversation_id)
    manager = manager_list[conversation_id]

    response = manager(intent, entity_dict, utterance)

    logging.info('Intent: %s', intent)
    logging.info('Entity: %s', entity_dict)
    logging.info('Utterance: %s', utterance)
    logging.info('Role: %s', manager.role)
    logging.info('Action: %s', manager.actions)
    logging.info('Question: %s', manager.question)
    logging.info('Response: %s', response)

    return Response_Item(
        action=manager.actions[-1],
        response=response,
        role=manager.role,
        question=manager.question
    )


if __name__ == '__main__':
    uvicorn.run("app:app", host='0.0.0.0', port=8003)
