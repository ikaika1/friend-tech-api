import websockets
import json

from .config import API, AUTHORIZATION_TOKEN

class APIBase:

  def __init__(self) -> None:
    
    # WebSocket接続するためのヘッダーを定義
    self.session = None  

  async def connect(self):
    
    headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }
    
    # 認証トークンを付与してWebSocket接続
    self.session = await websockets.connect(f"wss://{API}/?authorization={AUTHORIZATION_TOKEN}", extra_headers=headers)

  async def disconnect(self):
    
    # セッションがあれば切断
    if self.session:
      await self.session.close()
    self.session = None

class NonRest:

  def __init__(self, api_base: APIBase):
    self.api_base = api_base

  # メッセージを受信する
  async def receive(self):
    return await self.api_base.session.recv()

  # WebSocket接続を切断
  async def close(self):
    await self.api_base.session.close()

  # Pingメッセージを送信  
  async def ping(self):
    await self.api_base.session.send(json.dumps({"action": "ping"}))

  # メッセージ送信  
  async def sendMessage(self, text: str, imagePaths: list[str], chatRoomId: str, clientMessageId: str):
    """
    メッセージ送信

    Args:
      - text : メッセージ本文
      - imagePaths: 画像URLリスト
      - chatRoomId: チャットルームID
      - clientMessageId: メッセージID
    """

    # SendメッセージをJSONで構築して送信
    await self.api_base.session.send(json.dumps({"action": "sendMessage", 
                                                 "text": f\"{text}\"",
                                                 "imagePaths": imagePaths, 
                                                 "chatRoomId": chatRoomId,
                                                 "clientMessageId": clientMessageId}))
