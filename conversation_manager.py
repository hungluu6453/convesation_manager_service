import logging

class Conversation_Manager:
    def __init__(self, conversation_id):
        self.conversation_id = conversation_id
        self.action_list = [
            'asking',
            'answering',
            'introducing',
            'greeting',
            'wondering',
        ]
        self.current_action = None
        self.previous_action = None

        self.current_intent = None
        self.previous_intent = None

        self.current_entity = None
        self.previous_entity = None

        self.role_type = None
        self.current_policy = None

        self.question = None

        self.isAsking = False
        

    def transit(self, intent, entity, question):

        self.previous_intent = self.current_intent
        self.current_intent = intent
        self.current_entity = self.previous_entity
        self.previous_entity = entity
        
        self.update_role_type(entity['role'])
        self.update_policy(entity['policy'])

        if not self.isAsking:
            if intent == 'greeting':
                self.update_action('greeting')

            elif intent=='chitchat':
                self.update_action('introducing')
            
            elif intent is None or (intent == 'policy' and len(entity['policy'])==0):
                self.update_action('wondering')

            elif intent == 'policy':
                self.question = question
                if self.role_type is None:
                    self.update_action('asking')
                    self.isAsking = True
                else:
                    self.update_action('answering')
                    self.isAsking = False

            else:
                self.update_action('introducing')

        if self.isAsking:
            if intent == 'answer' and self.role_type is not None:
                self.update_action('answering')
                self.isAsking = False


    def update_action(self, action):
        self.previous_action = self.current_action
        self.current_action = action

    def update_policy(self, entity):
        entity_value = [x[0] for x in entity]
        if len(entity) != 0:
            self.current_policy = ', '.join(entity_value)

    def update_role_type(self, role):
        if len(role) == 0:
            self.role_type = None
            return

        role_value = role[0][0]
        if role_value in ['tiến_sĩ', 'nghiên_cứu_sinh']:
            self.role_type = 'phd'
        elif role_value in ['thạc_sĩ']:
            self.role_type = 'master'
        elif role_value in ['sinh_viên', 'cử_nhân']:
            self.role_type = 'undergraduate'
        else:
            self.role_type = None

    def act(self):
        # 'Xin chào, mình có thể giúp bạn giải quyết các vấn đề liên quan đến quy định.'
        
        if self.current_action == 'greeting':
            return 'Xin chào'
        
        if self.current_action == 'introducing':
            return 'Mình là hệ thống Chatbot hỗ trợ sinh viên, học viên các vấn đề thắc mắc đến quy định. Bạn chỉ cần hỏi mình, còn những quy định dài dòng thì cứ để mình lo.'
        
        if self.current_action == 'asking':
            return 'Bạn muốn hỏi cho cấp bậc đào tạo nào nhỉ? (sinh viên, thạc sĩ, nghiên cứu sinh, tiến sĩ)'
        
        if self.current_action == 'wondering':
            return 'Xin lỗi nha, mình chưa hiểu ý bạn lắm. Bạn có thể để lại lời góp ý để giúp mình thông minh hơn đó.'
        
        if self.current_action == 'answering':
            return 'Câu trả lời của bạn liên quan đến [{}] đây:'.format(self.current_policy)
