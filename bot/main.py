import discord
from discord.ext import commands
import json
import os

# 설정 파일 로드
with open('bot/config/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# 봇 설정
intents = discord.Intents.default()
intents.message_content = True  # 메시지 내용 읽기 권한 활성화
bot = commands.Bot(command_prefix=config['prefix'], intents=intents)

# Cog 로드
@bot.event
async def on_ready():
    """봇이 시작될 때 실행되는 이벤트"""
    print(f'{bot.user.name}이(가) 준비되었습니다!')
    await bot.load_extension('bot.cogs.game_commands')

# 봇 실행
bot.run(config['bot_token'])