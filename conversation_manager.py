class Conversation_Manager:
    def __init__(self, conversation_id):
        self.conversation_id = conversation_id
        self.action_list = [
            'listening',
            'introduce',
            'ask_role',
            'answer'
            'greeting',
        ]
        self.current_action = 'listening'
        self.previous_action = None

        self.current_intent = None
        self.previous_intent = None

        self.isAnswering = False
        self.entity = {'policy': '', 'role': ''}
        self.question = ''

    def act(self, intent, entity, utterance):
        print(self.isAnswering)
        self.previous_intent = self.current_intent
        self.current_intent = intent
        if intent == 'greeting':
            self.update_action('greeting')
        elif intent == 'policy':
            self.entity['role'] = self.update_role(entity['role'])
            self.entity['policy'] = entity['policy']
            self.question = utterance
            if self.entity['role'] == '':
                self.update_action('ask_role')
                self.isAnswering = True
            else:
                self.update_action('answer')
                self.isAnswering = False
        elif intent == 'answer':
            if self.isAnswering:
                self.entity['role'] = self.update_role(entity['role'])
                if self.entity['role'] == '':
                    self.update_action('ask_role')
                else:
                    self.update_action('answer')
                    self.isAnswering = False
            else:
                self.entity['role'] = self.update_role(entity['role'])
                self.update_action('listening')
        elif intent=='chitchat':
            self.update_action('introduce')
        else:
            if self.isAnswering:
                self.update_action('ask_role')
            else:
                self.update_action('listening')

    def update_action(self, action):
        self.previous_action = self.current_action
        self.current_action = action

    def update_role(self, role):
        if role in ['tiến_sĩ', 'nghiên_cứu_sinh']:
            return 'phd'
        elif role in ['thạc_sĩ']:
            return 'master'
        elif role in ['sinh_viên', 'cử_nhân']:
            return 'undergraduate'
        else:
            return ''

    def generate_response(self):
        if self.current_action == 'listening':
            return 'Xin chào, mình có thể giúp bạn giải quyết các vấn đề liên quan đến quy định.'
        if self.current_action == 'introduce':
            return 'Mình là hệ thống Chatbot hỗ trợ sinh viên, học viên các vấn đề thắc mắc đến quy định. Bạn chỉ cần hỏi mình, còn những quy định dài dòng thì cứ để mình lo.'
        if self.current_action == 'ask_role':
            return 'Bạn muốn hỏi cho cấp bậc đào tạo (sinh viên, thạc sĩ, nghiên cứu sinh, tiến sĩ) nào nhỉ?'
        if self.current_action == 'greeting':
            return 'Xin chào'
        if self.current_action == 'answer':
            return 'Câu trả lời của bạn đây: '
