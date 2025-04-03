import secrets
import string


def generate_win_password(length=18):
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digits = string.digits
    symbols = '~!@#$%^&*_-+=(){}[]|,.:;<>?/'

    password = [
        secrets.choice(uppercase),
        secrets.choice(lowercase),
        secrets.choice(digits),
        secrets.choice(symbols)
    ]

    all_chars = uppercase + lowercase + digits + symbols
    password += [secrets.choice(all_chars) for _ in range(length - 4)]

    secrets.SystemRandom().shuffle(password)

    return ''.join(password)
