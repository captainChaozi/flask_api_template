import random
import string
import uuid


def generate_unique(size=20):
    return ''.join([random.choice(string.ascii_letters) for _ in range(size)])


def generate_id():
    return uuid.uuid4().hex
