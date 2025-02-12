import aiohttp
import asyncio

async def get_game_info(place_id: int):
    """로블록스 게임 정보를 가져오는 함수"""
    try:
        async with aiohttp.ClientSession() as session:
            # 먼저 place ID로 universe ID 가져오기
            async with session.get(f"https://apis.roblox.com/universes/v1/places/{place_id}/universe") as resp:
                if resp.status == 200:
                    universe_data = await resp.json()
                    universe_id = universe_data.get("universeId")
                else:
                    return None

            # universe ID로 게임 정보 가져오기
            async with session.get(f"https://games.roblox.com/v1/games?universeIds={universe_id}") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if not data["data"]:
                        return None
                    game_data = data["data"][0]
                else:
                    return None

            # 즐겨찾기 수 가져오기
            async with session.get(f"https://games.roblox.com/v1/games/{universe_id}/favorites/count") as resp:
                if resp.status == 200:
                    favorites_data = await resp.json()
                    game_data["favoritedCount"] = favorites_data.get("favoritesCount", 0)
                else:
                    game_data["favoritedCount"] = 0

            # 현재 플레이어 수 가져오기
            async with session.get(f"https://games.roblox.com/v1/games/{place_id}/playing") as resp:
                if resp.status == 200:
                    playing_data = await resp.json()
                    game_data["playing"] = playing_data
                else:
                    game_data["playing"] = 0

        return game_data
    except Exception as e:
        print(f"Error fetching game info: {e}")
        return None

async def get_user_info(user_id: int):
    """로블록스 유저 정보를 가져오는 함수"""
    try:
        async with aiohttp.ClientSession() as session:
            # 기본 유저 정보 가져오기
            async with session.get(f"https://users.roblox.com/v1/users/{user_id}") as resp:
                if resp.status != 200:
                    return None
                user_data = await resp.json()

            # 팔로워/팔로잉 수 가져오기
            async with session.get(f"https://friends.roblox.com/v1/users/{user_id}/followers/count") as resp:
                if resp.status == 200:
                    followers_data = await resp.json()
                    user_data["followerCount"] = followers_data.get("count", 0)

            async with session.get(f"https://friends.roblox.com/v1/users/{user_id}/followings/count") as resp:
                if resp.status == 200:
                    following_data = await resp.json()
                    user_data["followingCount"] = following_data.get("count", 0)

            # 친구 수 가져오기
            async with session.get(f"https://friends.roblox.com/v1/users/{user_id}/friends/count") as resp:
                if resp.status == 200:
                    friends_data = await resp.json()
                    user_data["friendCount"] = friends_data.get("count", 0)

            # 방문 수 가져오기
            async with session.get(f"https://www.roblox.com/users/profile/profileheader-json?userId={user_id}") as resp:
                if resp.status == 200:
                    profile_data = await resp.json()
                    user_data["placeVisits"] = profile_data.get("PlaceVisits", 0)

            return user_data

    except Exception as e:
        print(f"Error fetching user info: {e}")
        return None

def fetch_game_info(game_id):
    """로블록스 API를 통해 게임 정보를 가져옵니다."""
    import requests

    url = f"https://api.roblox.com/games/{game_id}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def is_game_valid(game_id):
    """게임 ID가 유효한지 확인합니다."""
    game_info = fetch_game_info(game_id)
    return game_info is not None

def get_active_users(game_id):
    """활성 유저 수를 가져옵니다."""
    game_info = fetch_game_info(game_id)
    if game_info:
        return game_info.get("playing", 0)
    return 0

def get_total_visits(game_id):
    """총 방문자 수를 가져옵니다."""
    game_info = fetch_game_info(game_id)
    if game_info:
        return game_info.get("visits", 0)
    return 0

def get_favorites(game_id):
    """즐겨찾기 수를 가져옵니다."""
    game_info = fetch_game_info(game_id)
    if game_info:
        return game_info.get("favorites", 0)
    return 0

def get_game_recommendations(game_id):
    """게임 추천 수를 가져옵니다."""
    game_info = fetch_game_info(game_id)
    if game_info:
        return game_info.get("recommendations", 0)
    return 0

def is_game_public(game_id):
    """게임이 공개인지 비공개인지 확인합니다."""
    game_info = fetch_game_info(game_id)
    if game_info:
        return game_info.get("isPublic", False)
    return False

def get_active_servers(game_id):
    """현재 활성 서버 수를 가져옵니다."""
    game_info = fetch_game_info(game_id)
    if game_info:
        return game_info.get("activeServers", 0)
    return 0