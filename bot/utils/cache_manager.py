import json
import time
from pathlib import Path
from .roblox_api import get_game_info
import asyncio

class GameCache:
    def __init__(self):
        self.cache_file = Path('bot/config/game_cache.json')
        self.games_file = Path('bot/config/games.json')
        self.update_interval = 60  # 1분
        self._ensure_cache_exists()
        self.last_update = 0

    def _ensure_cache_exists(self):
        """캐시 파일이 존재하지 않으면 생성"""
        if not self.cache_file.exists():
            self.cache_file.write_text(json.dumps({
                "last_update": 0,
                "games": {}
            }))

    async def update_cache(self):
        """캐시 데이터 업데이트"""
        try:
            current_time = time.time()
            
            # 마지막 업데이트로부터 1분이 지났는지 확인
            if current_time - self.last_update < self.update_interval:
                return False

            # 서버별 게임 ID 로드
            if not self.games_file.exists():
                return False

            with open(self.games_file, 'r', encoding='utf-8') as f:
                servers = json.load(f)

            with open(self.cache_file, 'r', encoding='utf-8') as f:
                cache = json.load(f)

            updated = False
            # 각 게임의 정보 업데이트
            for server_id, game_id in servers.items():
                game_info = await get_game_info(game_id)
                if game_info:
                    cache["games"][str(game_id)] = {
                        "data": game_info,
                        "last_update": current_time
                    }
                    updated = True

            if updated:
                cache["last_update"] = current_time
                self.last_update = current_time
                
                # 캐시 파일 업데이트
                with open(self.cache_file, 'w', encoding='utf-8') as f:
                    json.dump(cache, f, indent=4, ensure_ascii=False)
                
                print(f"캐시 업데이트 완료: {time.strftime('%Y-%m-%d %H:%M:%S')}")
                return True

        except Exception as e:
            print(f"캐시 업데이트 중 오류 발생: {e}")
        return False

    def get_game_info(self, game_id):
        """캐시된 게임 정보 반환"""
        try:
            if not self.cache_file.exists():
                return None

            with open(self.cache_file, 'r', encoding='utf-8') as f:
                cache = json.load(f)
            
            game_data = cache["games"].get(str(game_id))
            if game_data:
                return game_data["data"]
            return None
        except Exception as e:
            print(f"게임 정보 조회 중 오류 발생: {e}")
            return None