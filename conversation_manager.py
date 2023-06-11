import logging
import random
import yaml
import constant

class Conversation_Manager:
    def __init__(self, conversation_id):
        self.conversation_id = conversation_id

        self.response_map = self.read_yaml(constant.RESPONSE_PATH)
        self.action_map = self.read_yaml(constant.ACTION_PATH)

        self.isAsking = 'notAsking'
        self.role = None
        self.policy = None
        
        self.state = 'listening'

    def __call__(self, intent, entity, question):
        self.update_state(intent, entity, question)
        self.actions = self.act(self.state, self.isAsking)
        reponses = [self.respone(action, self.policy) for action in self.actions]
        return reponses

    def read_yaml(self, path):
        with open(path, 'r') as file:
            return yaml.safe_load(file)

    def update_policy(self, entity):
        policy_value = [x[0] for x in entity]
        if len(entity) != 0:
            self.policy = ', '.join(policy_value)

    def update_role(self, role):
        if len(role) == 0:
            self.role_type = None
            return
        # Currently only use the first role value
        role_value = role[0][0]

        if role_value not in constant.ROLE_MAP.keys():
            self.role = None
            return
        
        self.role = constant.ROLE_MAP[role_value]

    def update_state(self, intent, entity, question):
        self.update_role(entity['role'])
        isUnknow = intent is None or (intent == 'policy' and len(entity['policy'])==0)

        if self.isAsking == 'notAsking': 
            self.question = None
            if intent == 'greeting':
                self.state = 'greet'
            elif intent=='chitchat':
                self.state = 'introduce'
            elif intent == 'answer':
                self.state = 'update'
            elif isUnknow:
                self.state = 'unknow'
            elif intent == 'policy':
                self.update_policy(entity['policy'])  
                self.question = question
                if self.role is None:
                    self.state = 'ask'
                    self.isAsking = 'isAsking'
                else:                    
                    self.state = 'answer'
                    self.isAsking = 'notAsking'
            else:
                self.state = 'introduce'
        
        elif self.isAsking == 'isAsking':
            if intent == 'policy' and len(entity['policy'])!=0:
                self.state = 'processing'
            if intent == 'answer' and self.role is not None:
                self.state = 'answer'
                self.isAsking = 'notAsking'

    def act(self, state, isAskng):
        return self.action_map[isAskng][state]

    def respone(self, action, format_value=None):
        response = random.choice(self.response_map[action])

        if '{}' in response:
            if format_value is None:
                raise "Need value for response"            
            return response.format(format_value)
        
        return response
