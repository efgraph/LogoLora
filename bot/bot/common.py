from aiogram.filters.callback_data import CallbackData


class PromptsCallbackFactory(CallbackData, prefix='prompt'):
    prompt: str


class ScoresCallbackFactory(CallbackData, prefix='score'):
    score: int
    id: int

