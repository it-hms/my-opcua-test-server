# Testing OPC-UA server
# Copyright HMS. All Rights Reserved
# See LICENSE file for full details


import logging
import asyncio
import random
# asyncua is LGPL licensed
# https://www.gnu.org/licenses/lgpl-3.0.en.html
from asyncua import ua, Server


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class TestServer:
    def __init__(self):
        " Basic setup of server"
        # async def __init__ doesn't work
        self.server = Server()

    async def createSimulator(self):
        await self.server.init()
        self.server.set_endpoint('opc.tcp://127.0.0.1:4840/opcua/')
        self.server.set_server_name("OPC-UA Test Server")
        uri = "https://github.com/it-hms/my-opcua-test-server"
        self.idx = await self.server.register_namespace(uri)
        self.top = await self.server.nodes.objects.add_object(self.idx, 'Dynamic')
        self.vars = []
        for i in range(3):
            tvar = await self.top.add_variable(self.idx, f"Random.Int{i}", 0)
            self.vars.append(tvar)

    async def run(self):
        async with self.server:
            while True:
                i = 0
                for var in self.vars:
                    await var.write_value(int(random.gauss(i*10, 9)))
                    i += 1
                    await asyncio.sleep(1)
                


async def main():
    server = TestServer()
    await server.createSimulator()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
