import random
import string

def generate_random_username():
    """ Generates nonsense usernames that sound AI-generated """
    prefixes = ["Cyber", "AI", "Bot", "Robo", "Neural", "Quantum"]
    suffixes = ["Master", "2000", "Genius", "Coder", "X", "42"]
    return f"{random.choice(prefixes)}{random.randint(100, 999)}{random.choice(suffixes)}"

def generate_network_links(users):
    """ Creates nonsense social network URLs """
    return {user: f"https://fakenetwork.com/profile/{user.lower()}" for user in users}
