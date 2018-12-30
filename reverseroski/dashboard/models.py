from ..models import struct, Client, Command

class ClientTable(struct):
    headers=None
    client=None

    def get_body(self):
        return zip(*([
            c.__getattribute__(header)
            for header in self.headers
        ] for c in self.client.get_all_commands()))
