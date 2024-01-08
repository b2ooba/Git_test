import asyncio
import websockets

clients = set()
pseudos = {}

async def diffuser(message, expeditaire=None, destinataire=None):
    for client, pseudo in pseudos.items():
        if destinataire is None or pseudo == destinataire:
            if client != expeditaire:
                await client.send(message)

async def gestion_connexions(websocket, path):
    pseudo = await websocket.recv()
    clients.add(websocket)
    pseudos[websocket] = pseudo
    print(f"{pseudo} a rejoint le chat")
    await websocket.send("Bienvenue dans le chat !\n")
    await diffuser(f"{pseudo} a rejoint le chat!", destinataire=pseudo)

    try:
        while True:
            message = await websocket.recv()
            if message.startswith("@"):
                destinataire, message_prive = message.split(" ", 1)
                destinataire = destinataire[1:]
                await diffuser(f"(Privé) {pseudo}: {message_prive}", expeditaire=websocket, destinataire=destinataire)
            elif message == "/exit":
                clients.remove(websocket)
                del pseudos[websocket]
                await diffuser(f"{pseudo} a quitté le chat!")
                break
            else:
                await diffuser(f"{pseudo}: {message}")
    except websockets.exceptions.ConnectionClosed:
        clients.remove(websocket)
        del pseudos[websocket]
        await diffuser(f"{pseudo} a quitté le chat!")

start_server = websockets.serve(gestion_connexions, "127.0.0.1", 6666)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
