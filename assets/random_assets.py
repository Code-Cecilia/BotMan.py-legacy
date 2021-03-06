import random

eat_reactions = ['''_{0}_, you try to eat _{1}_, but you can\'t do it.
So you leave, with the taste of failure hanging in your mouth.''',
                 '_{0}_, you try to gobble up _{1}_. They prove to be a tight fit, but you manage to eat them.',
                 '_{0}_, you advance toward _{1}_, but you turn back and run, because they want to eat you too.',
                 '_{0}_, you finish eating _{1}_, and have a long nap, the sign of a good meal.']

pet_reactions = ['_{0}_, you pet _{1}_, as they smile from your petting.',
                 '_{0}_, you try to pet _{1}_, but they hid somewhere.',
                 '_{0}_, you take your hand near _{1}_, but they bite you.',
                 '_{0}_, you try petting _{1}_ but then they hiss and run away.']

drink_reactions = ['_{0}_, you pierce {1} with a straw, as they cry out in pain.',
                   '_{0}_, you try to drink _{1}_, but you realize they aren\'t liquid.',
                   '_{0}_, you try to drink _{1}_, but they have a mirror. So now you\'re drinking yourself.']

hug_reactions = ['_{0}_, you try to hug _{1}_, but they run away because they don\'t understand your affection.',
                 '_{0}_, you hug _{1}_. and they smile, because they didn\'t know they needed it.',
                 '_{0}_, you hug _{1}_, and they hug you back, the sign of a good friendship.',
                 '_{0}_, you try to hug _{1}_, but they pull out a knife because they think you were gonna mug them.', ]

fart_reactions = ['*farting noises*', 'Toot',
                  '*Blerrrtttt*', '**no.**', '_ew_',
                  'https://tenor.com/view/dance-moves-dancing-singer-groovy-gif-17029825']

ask_answers_list = ['No', 'Yes', 'Perhaps' 'Can\'t say for sure', 'For sure!',
                    'Why not?', 'hell naw', 'no, just no.', 'Definitely 👌']

toss_outcomes = ['Heads', 'Tails', 'Nothing']

uptime_footers = ["I'm tired. I need coffee.", "Man, being a bot is a tiring job.", "I wanna take a nap.",
                  "Sometimes I wonder why I exist. Am I an insignificant creature in a vast endless space?"]

countlines_responses = ["I am made of _{0}_ lines of python code. Pretty cool, huh?",
                        r"My owner has written _{0}_ lines of code in my brain. I a-a-am ... _glitches out_",
                        "I have _{0}_ lines of python code as my insides. That's pretty cool to me, you know...",
                        "Oh no! How did _{0}_ lines of python code get inside me?\n_I'm scared..._",
                        "I am made of _{0}_ lines of python code. What can I say except 😎",
                        "Some poor soul wrote _{0}_ lines of python code to give me a life. I hope he's okay"]

spongebob_text_responses = ["You didn't enter any text, genius", "Enter some text, smartass",
                            "Look who didn't specify the text!"]

good_games = ["GTA San Andreas", "Undertale", "Cyberpunk", "[Insert a good game's title here]",
              "[Insert AAA title here]"]


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


def eat_func(author, user, bot):
    if user.id == bot.user.id:
        return '''For the record, I **DO NOT** appreciate being eaten.
Even though I am digital and you would probably get electrocuted.'''
    elif not author == user:
        return random.choice(eat_reactions).format(author.display_name, user.display_name)
    else:
        return 'You try to eat yourself, but fail miserably'


def pet_func(author, user, bot):
    if user.id == bot.user.id:
        return 'Well, what can I say? I do like people petting me :)'
    elif not author == user:
        return random.choice(pet_reactions).format(author.display_name, user.display_name)
    else:
        return 'You pet yourself. I feel you, mate'


def drink_func(author, user, bot):
    if user.id == bot.user.id:
        return 'You try to drink me, but you can\'t, because I\'m digital!'
    elif not author == user:
        return random.choice(drink_reactions).format(author.display_name, user.display_name)
    else:
        return 'You pierce yourself with a straw. Not surprisingly, it hurts.'


def fart_reaction():
    return random.choice(fart_reactions)


def hug_func(author, user, bot):
    if user.id == bot.user.id:
        return 'Even though I\'m digital, I do appreciate hugs :)'
    elif not author == user:
        return random.choice(hug_reactions).format(author.display_name, user.display_name)
    else:
        return 'You try to hug yourself, I feel you. Mind if I give you a hug?'
