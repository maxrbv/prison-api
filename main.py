from typing import Callable
import random

from aiogram import Bot, Dispatcher, BaseMiddleware
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message, Update, WebAppInfo
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from tortoise import Tortoise
import uvicorn

from settings import TEMPLATES_DIR, STATIC_DIR, DB_URL, TOKEN, WEBAPP_URL
from models.user import User


class UserMiddleware(BaseMiddleware):

    async def __call__(self, handler: Callable, event: Message, data: dict):
        username = event.from_user.username
        if not username:
            return await event.answer(text='You need to set your username.')
        user = await User.get_or_create(id=event.from_user.id, username=username)
        data['user'] = user
        return await handler(event, data)


async def lifespan(app: FastAPI):
    await bot.set_webhook(
        url=f"{WEBAPP_URL}/webhook",
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True,
    )
    await Tortoise.init(db_url=DB_URL, modules={'models': ['models.user']})
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()


bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

dp.message.middleware(UserMiddleware())

app = FastAPI(title='TON Prizon', lifespan=lifespan)
app.mount('/static', StaticFiles(directory=STATIC_DIR), name='static')
templates = Jinja2Templates(directory=TEMPLATES_DIR)


@dp.message(CommandStart())
async def start(message: Message, user: User):
    markup = (
        InlineKeyboardBuilder()
        .button(text='Hey there!', web_app=WebAppInfo(url=WEBAPP_URL))
    ).as_markup()
    await message.answer(text='Test', reply_markup=markup)


@app.get('/')
async def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.post('/webhook')
async def webhook(request: Request):
    update = Update.model_validate(await request.json(), context={'bot': bot})
    await dp.feed_update(bot, update)


@app.post('/api/v1/current_cigarettes')
async def get_current_cigarettes(request: Request, data: dict):
    user = await User.filter(id=data.get('id')).first()
    return {'cigarette_count': user.cigarettes}


@app.post('/api/v1/open_cigarettes')
async def open_cigarettes(request: Request, data: dict):
    cigarette_count = random.randint(a=10, b=50)
    user = await User.filter(id=data.get('id')).first()
    user.cigarettes += cigarette_count
    await user.save()
    return {'cigarette_count': cigarette_count}


if __name__ == '__main__':
    uvicorn.run(app)
