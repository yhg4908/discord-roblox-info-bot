import discord
from discord.ext import commands, tasks
import json
import os
from bot.utils.roblox_api import get_game_info, get_user_info  # 상대 경로 대신 절대 경로 사용
from ..utils.cache_manager import GameCache
from datetime import datetime

class GameCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games_file = 'bot/config/games.json'
        self.cache = GameCache()
        self.update_cache.start()  # 캐시 업데이트 작업 시작
        # games.json 파일이 없다면 생성
        if not os.path.exists(self.games_file):
            with open(self.games_file, 'w') as f:
                json.dump({}, f)

    def cog_unload(self):
        """Cog가 언로드될 때 실행되는 메서드"""
        self.update_cache.cancel()

    @tasks.loop(seconds=60)  # 1분마다 실행
    async def update_cache(self):
        """게임 정보 캐시 업데이트"""
        try:
            updated = await self.cache.update_cache()
            if updated:
                print("캐시가 성공적으로 업데이트되었습니다.")
        except Exception as e:
            print(f"캐시 업데이트 중 오류 발생: {e}")

    @update_cache.before_loop
    async def before_update_cache(self):
        """캐시 업데이트 전에 봇이 준비될 때까지 대기"""
        await self.bot.wait_until_ready()

    @commands.command(name="게임")
    async def set_game(self, ctx, game_id: int):
        """게임 ID를 서버에 저장하는 명령어
        
        Args:
            ctx: 명령어 컨텍스트
            game_id: 저장할 로블록스 게임 ID
        """
        # 게임 정보 확인
        game_info = await get_game_info(game_id)
        
        if game_info is None:
            await ctx.reply("존재하지 않는 게임 ID입니다!")
            return

        # 게임 ID 저장
        with open(self.games_file, 'r', encoding='utf-8') as f:
            games = json.load(f)
        
        games[str(ctx.guild.id)] = game_id
        
        with open(self.games_file, 'w', encoding='utf-8') as f:
            json.dump(games, f, indent=4, ensure_ascii=False)
        
        await ctx.reply(f"게임 ID가 성공적으로 저장되었습니다! (ID: {game_id})")

    @commands.command(name="게임정보")
    async def game_info(self, ctx):
        """저장된 게임의 정보를 보여주는 명령어"""
        # 저장된 게임 ID 확인
        with open(self.games_file, 'r', encoding='utf-8') as f:
            games = json.load(f)
        
        game_id = games.get(str(ctx.guild.id))
        if not game_id:
            await ctx.reply("저장된 게임이 없습니다! *게임 명령어로 먼저 게임을 저장해주세요.")
            return

        # 캐시에서 게임 정보 가져오기
        game_info = self.cache.get_game_info(game_id)
        if game_info is None:
            await ctx.reply("게임 정보를 가져오는데 실패했습니다.")
            return

        # 임베드 생성
        embed = discord.Embed(
            title=game_info.get("name", "알 수 없음"),
            description="실시간 게임 정보",  # 실시간 정보임을 표시
            color=discord.Color.blue(),
            timestamp=ctx.message.created_at  # 정보 조회 시간 표시
        )
        
        # 안전하게 데이터 가져오기
        embed.add_field(name="활성 유저 수", value=game_info.get("playing", 0), inline=True)
        embed.add_field(name="총 방문자 수", value=game_info.get("visits", 0), inline=True)
        embed.add_field(name="즐겨찾기 수", value=game_info.get("favoritedCount", 0), inline=True)
        embed.add_field(name="최대 플레이어 수", value=game_info.get("maxPlayers", 0), inline=True)
        # 게임 상태 로직 수정 - 비공개 상태 확인 개선
        embed.add_field(name="게임 상태", 
                       value="비공개" if game_info.get("createVipServersAllowed", False) else "공개", 
                       inline=True)
        embed.add_field(name="장르", value=game_info.get("genre", "알 수 없음"), inline=True)
        
        # 마지막 업데이트 시간 표시
        embed.set_footer(text="마지막 업데이트")

        await ctx.reply(embed=embed)

    @commands.command(name="유저정보")
    async def user_info(self, ctx, user_id: int):
        """로블록스 유저 정보를 보여주는 명령어
        
        Args:
            ctx: 명령어 컨텍스트
            user_id: 조회할 로블록스 유저 ID
        """
        # 유저 정보 가져오기
        user_info = await get_user_info(user_id)
        if user_info is None:
            await ctx.reply("유저 정보를 가져오는데 실패했습니다.")
            return

        # 가입일 변환
        created_date = datetime.fromisoformat(user_info["created"].replace('Z', '+00:00'))
        kr_date = created_date.strftime("%Y년 %m월 %d일")

        # 임베드 생성
        embed = discord.Embed(
            title=user_info.get("displayName", "알 수 없음"),
            description=user_info.get("description", "소개 없음"),
            color=discord.Color.green(),
            timestamp=ctx.message.created_at
        )
        
        embed.add_field(name="사용자명", value=user_info.get("name", "알 수 없음"), inline=True)
        embed.add_field(name="가입일", value=kr_date, inline=True)
        embed.add_field(name="방문한 플레이스", value=f"{user_info.get('placeVisits', 0):,}개", inline=True)
        embed.add_field(name="친구 수", value=f"{user_info.get('friendCount', 0):,}명", inline=True)
        embed.add_field(name="팔로워 수", value=f"{user_info.get('followerCount', 0):,}명", inline=True)
        embed.add_field(name="팔로잉 수", value=f"{user_info.get('followingCount', 0):,}명", inline=True)

        # 프로필 이미지 추가
        embed.set_thumbnail(url=f"https://www.roblox.com/headshot-thumbnail/image?userId={user_id}&width=420&height=420&format=png")
        
        await ctx.reply(embed=embed)

async def setup(bot):
    """Cog를 봇에 로드"""
    await bot.add_cog(GameCommands(bot))