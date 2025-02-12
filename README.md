# Discord Roblox 정보 봇

Discord에서 Roblox 게임과 유저 정보를 실시간으로 확인할 수 있는 봇입니다.

## 주요 기능

- 서버별 게임 정보 관리
- 실시간 게임 정보 확인 (1분 간격 자동 업데이트)
- 실시간 유저 정보 확인
- 직관적인 임베드 형식의 정보 표시

## 설치 방법

1. [Python 3.11](https://www.python.org/downloads/release/python-3118/) 설치
2. 필요한 패키지 설치:
```bash
pip install discord.py aiohttp
```

## 봇 설정 방법

1. [Discord Developer Portal](https://discord.com/developers/applications)에서 봇 생성
2. `bot/config/config.json` 파일에 봇 토큰 입력:
```json
{
    "bot_token": "YOUR_BOT_TOKEN",
    "prefix": "*"
}
```

3. 봇 실행:
```bash
python -m bot.main
```

## 사용 가능한 명령어

### 게임 정보 명령어
- `*게임 [게임ID]`: 서버에 게임 ID 저장
- `*게임정보`: 저장된 게임의 실시간 정보 표시
  - 활성 유저 수
  - 총 방문자 수
  - 즐겨찾기 수
  - 최대 플레이어 수
  - 게임 상태 (공개/비공개)
  - 게임 장르

### 유저 정보 명령어
- `*유저정보 [유저ID]`: 유저의 실시간 정보 표시
  - 디스플레이 닉네임
  - 사용자명
  - 소개
  - 친구 수
  - 팔로워/팔로잉 수
  - 가입일자
  - 방문한 플레이스 수

## 커스터마이징 방법

### 명령어 접두사 변경
`bot/config/config.json`의 "prefix" 값을 원하는 접두사로 변경

### 임베드 색상 변경
`bot/cogs/game_commands.py`에서 `discord.Color` 값 수정:
```python
embed = discord.Embed(
    title=title,
    color=discord.Color.blue()  # 원하는 색상으로 변경
)
```

### 표시 정보 수정
`bot/cogs/game_commands.py`의 embed.add_field() 부분을 수정하여 원하는 정보 추가/제거

### 업데이트 주기 변경
`bot/cogs/game_commands.py`의 @tasks.loop() 값 수정:
```python
@tasks.loop(seconds=60)  # 원하는 시간(초)으로 변경
```

## 주의사항

- Python 3.11 버전 사용 권장 (3.12, 3.13 버전에서는 오류 발생 가능)
- Discord 봇 토큰은 절대 공개하지 말 것
- 게임 정보는 1분 간격으로 자동 업데이트
- 유저 정보는 명령어 실행 시 실시간으로 조회

## 문제 해결

- 봇이 응답하지 않을 경우: 봇 토큰 확인
- 게임 정보가 표시되지 않을 경우: 게임 ID가 올바른지 확인
- 유저 정보가 표시되지 않을 경우: 유저 ID가 올바른지 확인

## 라이선스

MIT License - 자유롭게 수정 및 배포 가능
