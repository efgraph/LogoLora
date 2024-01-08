import random

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.common import PromptsCallbackFactory, ScoresCallbackFactory

adjectives = [
    "futuristic", "eco-friendly", "luxury", "children's", "vegan", "fitness", "pet",
    "digital", "organic", "travel", "music", "yoga", "craft", "adventure", "art",
    "home", "cybersecurity", "sustainable", "gourmet"
]

nouns = [
    "logo", "tech", "company", "nexatech", "coffee", "shop", "bean", "bliss", "brand", "green",
    "earth", "car", "elegance", "motors", "children", "book", "publisher", "little", "minds",
    "restaurant", "veggie", "delight", "fitness", "gym", "iron", "strength", "pet", "grooming",
    "service", "paws", "claws", "digital", "marketing", "agency", "pixel", "pioneers", "cosmetics",
    "nature", "glow", "travel", "wanderlust", "world", "music", "production", "melody", "makers",
    "yoga", "studio", "serenity", "space", "beer", "brewery", "hop", "haven", "adventure", "sports",
    "thrill", "seekers", "art", "gallery", "canvas", "corner", "home", "decor", "elegant", "interiors",
    "cybersecurity", "firm", "secure", "shield", "fashion", "eco", "chic", "chocolate", "choco", "indulgence"
]

prepositions = [
    "in", "and", "with", "on", "a"
]


def generate_prompts() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    p = random.sample(prepositions, 2)
    a = random.sample(adjectives, 4)
    n = random.sample(nouns, 5)
    for item in p + a + n:
        builder.button(
            text=item,
            callback_data=PromptsCallbackFactory(prompt=item).pack()
        )
    builder.button(
        text='Go',
        callback_data=PromptsCallbackFactory(prompt='Go').pack()
    )
    return builder.adjust(4, repeat=True).as_markup()


def generate_scores(id: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for i in range(5):
        builder.button(
            text=i + 1,
            callback_data=ScoresCallbackFactory(score=i + 1, id=id).pack()
        )
    return builder.adjust(5).as_markup()
