from conversation_manager import Conversation_Manager

manager = Conversation_Manager(0)
intent = 'policy'
entity = {
    'policy':None,
    'role': None
}
print(manager.generate_response(), manager.current_action, manager.current_intent)
manager.act(intent, entity)
print(manager.generate_response(), manager.current_action, manager.current_intent)
intent = 'answer'
entity = {
    'policy':None,
    'role': None
}
manager.act(intent, entity)
print(manager.generate_response(), manager.current_action, manager.current_intent)
intent = 'answer'
entity = {
    'policy':None,
    'role': ''
}
manager.act(intent, entity)
print(manager.generate_response(), manager.current_action, manager.current_intent)