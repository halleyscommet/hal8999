meows = [
    # Basic Variants
    "meow",
    "mrow",
    "miao",
    "nyan",
    "nya~",
    "miau",
    "miaow",
    "myow",

    # Stylized / Internetified
    "me0w",
    "m3ow",
    "mrowr",
    "mrow~",
    "mew~",
    "m͟e͟o͟w͟",
    "𝓂𝓇𝑜𝓌",
    "ₘₑₒw",
    "мєσω",
    "꧁meow꧂",
    "𝕄𝕣𝕠𝕨",
    "ₘɾₒ₩",

    # Elongated / Dramatic
    "meeeooooowww",
    "mrrrroooowwwww",
    "meeeeewwwww~",
    "mreeeeeeeeow",
    "mrrrRRROW!!",
    "mrrreeeowww",

    # Emotive / Roleplay
    "*meow*",
    "~mrow~",
    "*soft mrow*",
    "*angry meow*",
    ">:3 meow",
    "*purrs and meows*",
    "meow~?",
    "mrow! 🐾",
    "*tiny mew*",
    "MEOW!! 🐈",
    "mrrowl...",

    # Regional / Phonetic
    "miaou",    # French
    "miau",     # Spanish/German/Portuguese
    "nya",      # Japanese
    "meong",    # Korean
    "nyahh~",
    "mao"       # Chinese
]

def get_random_meow():
    """Return a random meow from the list."""
    import random
    return random.choice(meows)