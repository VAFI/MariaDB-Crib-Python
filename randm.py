import random
import string

def strng(lenght:int):
    letters = string.ascii_lowercase
    return ''.join([random.choice(letters) for i in range(lenght)]).title()

def num():
    return random.randint(1,33)
