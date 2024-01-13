from contextlib import suppress

from aiogram import Router, F
from aiogram.client.session import aiohttp
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, URLInputFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.common import PromptsCallbackFactory, ScoresCallbackFactory
from bot.config_reader import config
from bot.db.models import UserPrompt
from bot.keyboards import generate_prompts

router = Router(name="callbacks-router")


async def post_request(prompt: str):
    async with aiohttp.ClientSession() as session:
        response = await session.post(url=f"{config.api_logo}/generate",
                                      json={"prompt": prompt})
        return await response.json()


@router.callback_query(PromptsCallbackFactory.filter(F.prompt == "Go"))
async def cb_prompt(callback: CallbackQuery, session: AsyncSession):
    db_query = await session.execute(select(UserPrompt).filter_by(id=callback.message.message_id))
    prompt: UserPrompt = db_query.scalar()
    await callback.message.answer(f'Generating logo by prompt: {prompt.prompt}')

    data = await post_request(prompt.prompt)

    image_from_url = URLInputFile(f"{config.api_logo}{data['images'][0]}")
    result = await callback.message.answer_photo(
        image_from_url,
        caption="Generated logo"
    )
    prompt.file_id = result.photo[-1].file_id
    await session.commit()
    await session.close()


@router.callback_query(PromptsCallbackFactory.filter())
async def cb_prompt(callback: CallbackQuery, session: AsyncSession):
    print(f"Prompt >>> {callback.message.message_id}")
    exists = await session.get(UserPrompt, callback.message.message_id) is not None
    if not exists:
        await session.merge(UserPrompt(id=callback.message.message_id,user_id=callback.from_user.id, prompt="Design logo for"))
        await session.commit()
    db_query = await session.execute(select(UserPrompt).filter_by(id=callback.message.message_id))
    prompt: UserPrompt = db_query.scalar()
    prompt.prompt += f" {callback.data.split(':')[-1]}"
    await session.commit()

    with suppress(TelegramBadRequest):
        await callback.message.edit_text(f"{prompt.prompt}", reply_markup=generate_prompts())


@router.callback_query(ScoresCallbackFactory.filter())
async def cb_score(callback: CallbackQuery, session: AsyncSession):
    id = int(callback.data.split(':')[-1])
    score = callback.data.split(':')[-2]
    db_query = await session.execute(select(UserPrompt).filter_by(id=id))
    prompt: UserPrompt = db_query.scalar()
    prompt.score = score
    await session.commit()
    await callback.message.answer('Thank you for the feedback')
