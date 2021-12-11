from json import dumps, loads

from aiogram import Dispatcher, Bot, executor
from aiogram.types import Message, InputFile

from shazamio import Shazam

from aiofiles import open
from aiofiles.os import remove

from aiohttp import ClientSession


bot = Bot("1029672277:AAG0C6w6yhKuznyhM_4SdLuGjYXITnu3ZDY")
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: Message):
    await message.answer("Ovozli xabar yuboring...")

@dp.message_handler(content_types=['voice', 'audio'])
async def get_voice(message: Message):
    voice = message.voice.file_id if message.voice else message.audio.file_id
    file_info = await dp.bot.get_file(voice)
    file_path = file_info.file_path
    async with ClientSession() as session:
        url = f"https://api.telegram.org/file/bot{bot._token}/{file_path}"
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await open(file_path, mode='wb')
                await f.write(await resp.read())
                await f.close()
                
    shazam = Shazam()
    out = await shazam.recognize_song(file_path)
    
    track = out.get('track', None)
    if track is None:
        await message.answer("Musiqa topilmadi!")
        return
    actions = track.get('hub').get('actions')
    for action in actions:
        if action.get('type') == 'uri':
            caption = f"{track.get('subtitle')} — {track.get('title')}"
            audio_url = action['uri']
            async with ClientSession() as session:
                async with session.get(audio_url) as resp:
                    if resp.status == 200:
                        audio_path = f"{message.from_user.id}.{message.date.timestamp()}.mp3"
                        f = await open(audio_path, mode='wb')
                        await f.write(await resp.read())
                        await f.close()
                    await message.answer_audio(InputFile(audio_path),
                    title=caption, performer='@TilonCodes', caption="<b>" +caption+ "</b>", parse_mode='html')
                    await remove(audio_path)
    
    await remove(file_path)
    
executor.start_polling(dp)