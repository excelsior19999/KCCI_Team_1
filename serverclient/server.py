import asyncio
import websockets

# source /home/intel/workspace/.otx/bin/activate
ServerIP = '10.10.14.203'
ServerPort = 6000

# 클라이언트들을 저장할 set
clients = set()

# client가 접속하면 실행되는 핸들러
async def serve(websocket, path):
    print(f'Server Started at {ServerIP}:{ServerPort}')
    clients.add(websocket)
    print('clients : ', clients)
    print('websocket : ', websocket)
    print('path : ', path)

    # print(dir(websocket))

    try:
        async for message in websocket:
            if not message:
                continue
            
            try:
                # 받은 스트리밍 데이터를 클라이언트들에게 중계
                for client in clients:
                    if client != websocket:
                        await client.send(message)
            except:
                print('message except')
                continue
                    
    except:
        print(f'except')
        
    finally:
        pass
        # clients.remove(websocket)
# End async def        

start_server = websockets.serve(serve, ServerIP, ServerPort, reuse_port=True)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
