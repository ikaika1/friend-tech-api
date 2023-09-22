from friend_tech_api.client import FriendTechClient, FriendTechWebsocketClient
import asyncio

# WebSocketを使ってメッセージを受信する
async def receive_messages(client_websocket):
  while True:
    # メッセージを受信して表示
    message = await client_websocket.non_rest.receive() 
    print(f"{message}")

async def main():

  # REST APIクライアントを作成
  client = FriendTechClient()  

  # ユーザー情報を取得
  example_user = await client.users.by_id(100000)
  print(example_user)

  # WebSocketクライアントを作成
  client_websocket = FriendTechWebsocketClient()

  # WebSocket接続
  await client_websocket.initialize()

  # メッセージ受信タスクを作成
  asyncio.create_task(receive_messages(client_websocket))

  # Ping送信
  await client_websocket.non_rest.ping()

  # メッセージ送信
  await client_websocket.non_rest.sendMessage("A", [], "0x750add0f18b005c20cdf76236bb0f15429c7aa9a", "0xf00dbabes")

  # 60秒待機
  await asyncio.sleep(60 * 60 * 24)

# メインタスク起動  
asyncio.run(main())
