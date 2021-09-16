import os
import random
import hashlib

from model import User

pepper_letters = ["a", "b", "c", "z"]


def hash_password(password: str):
    # Ask the operating system for 32 random bytes
    salt = os.urandom(32)

    # Select a random letter and position to insert as pepper
    pep_loc = random.randint(0, len(password))
    pep_char = random.choice(pepper_letters)
    password = password[:pep_loc] + pep_char + password[pep_loc:]
    print(f"Peppered password: {password}")

    # Create a 64 byte key
    key = hashlib.pbkdf2_hmac(
        "sha256",  # The hash digest algorithm for HMAC
        password.encode("utf-8"),  # Convert the password to bytes
        salt,  # Provide the salt
        100000,  # It is recommended to use at least 100,000 iterations of SHA-256
    )

    # For an extra obfuscated step, concatenate the salt and the hash
    # An attacker would need to know the length of the salt and key to decrypt
    # Storage is of type bytes
    return salt + key


def check_password(user: User, password: str):
    # Getting the values back out
    salt = user.password[:32]  # 32 is the length of the salt
    key = user.password[32:]
    for pepper_letter in pepper_letters:
        for pep_loc in range(len(password)):
            pepper_password = password[:pep_loc] + pepper_letter + password[pep_loc:]
            print(f"Trying pepper: {pepper_password}")
            # Use the exact same setup you used to generate the key, but this time put in the password to check
            new_key = hashlib.pbkdf2_hmac(
                "sha256", pepper_password.encode("utf-8"), salt, 100000
            )  # Convert the password to bytes
            if new_key == key:
                print("Success!")
                return True

    return False


# Function to validate the password
def password_complexity(passwd):
    message = []

    if len(passwd) < 6:
        message.append("length should be at least 6<br/>")

    if len(passwd) > 20:
        message.append("length should be not be greater than 20<br/>")

    if not any(char.isdigit() for char in passwd):
        message.append("Password should have at least one numeral<br/>")

    if not any(char.isupper() for char in passwd):
        message.append("Password should have at least one uppercase letter<br/>")

    if not any(char.islower() for char in passwd):
        message.append("Password should have at least one lowercase letter<br/>")

    if message:
        return message
    else:
        return False
