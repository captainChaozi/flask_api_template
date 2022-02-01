import string
import random


def generate_unique(size=20):
    return ''.join([random.choice(string.ascii_letters) for _ in range(size)])
