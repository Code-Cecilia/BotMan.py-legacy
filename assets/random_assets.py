import random

ask_answers_list = ['No', 'Yes', 'Maybe', 'Perhaps', 'Why don\'t you wait and see', 'Can\'t say for sure', 'For sure!', 'Why not?', '0w0', 'hell naw', 'no, just no.']
toss_outcomes = ['Heads', 'Tails', 'Nothing']


def ask_qn(msg):
    if len(msg.split()) == 1:
        return 'You didn\'t ask the question, smartass'
    answer = random.choice(ask_answers_list)
    return f'_{answer}_'


def coin_flip():
    result = random.choice(toss_outcomes)
    return f'You tossed a coin and got... **_{result}_**.'


def roll_dice():
    result = random.randint(1, 6)
    return f'You rolled a die and got a _**{result}**_'
