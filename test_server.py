# Testing OPC-UA server
# Copyright HMS. All Rights Reserved
# See LICENSE file for full details


import logging
import asyncio
import random
# asyncua is LGPL licensed
# https://www.gnu.org/licenses/lgpl-3.0.en.html
from asyncua import Server


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# server ip 127.0.0.1 for localhost
SERVER_IP = '0.0.0.0'
LOCAL_HOST = '127.0.0.1'
PORT = "4840"
PATH = "opcua/"

MAX_TAG = 1032


class TestServer:
    def __init__(self):
        " Basic setup of server"
        # async def __init__ doesn't work
        self.server = Server()
        self.idx = None
        self.top = None
        self.vars = []

    async def create_simulator(self):
        await self.server.init()
        self.server.set_endpoint(f'opc.tcp://{LOCAL_HOST}:{PORT}/{PATH}')
        self.server.set_server_name("OPC-UA Test Server")
        uri = "https://github.com/it-hms/my-opcua-test-server"
        self.idx = await self.server.register_namespace(uri)
        self.top = await self.server.nodes.objects.add_object(self.idx, 'Dynamic')
        for i in range(MAX_TAG + 1):
            t_var = await self.top.add_variable(self.idx, f"Random.Float{i}", 0)
            self.vars.append(t_var)

    async def run(self):
        async with self.server:
            while True:
                i = 0
                for var in self.vars:
                    await var.write_value(random.gauss(i*10, 9))
                    i += 1
                await asyncio.sleep(2)


async def main():
    server = TestServer()
    await server.create_simulator()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
