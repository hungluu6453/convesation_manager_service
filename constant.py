INTENT_LIST = [
    'policy',
    'answer',
    'greeting',
    'confirm',
    'disagree',
    'chitchat',
]
ENTITY_LIST = [
    'policy',
    'role',
]

STATE_LIST = [
    'listen',
    'ask',
    'answer',
    'introduce',
    'greet',
    'unknow',
]

ROLE_MAP ={
    'tiến_sĩ': 'phd',
    'nghiên_cứu_sinh': 'phd',
    'thạc_sĩ': 'master',
    'sinh_viên': 'undergraduate',
    'cử_nhân': 'undergraduate',
}

RESPONSE_PATH = 'script/action_to_response.yml'
ACTION_PATH = 'script/state_to_action.yml'