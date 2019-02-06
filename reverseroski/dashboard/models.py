from ..models import struct, Client, Command


class ClientTable(struct):
    class ClientTableRow(struct):
        data=None
        link=None

        def __iter__(self):
            return (i for i in self.data)
    headers=None
    client=None

    def get_body(self):
        return [self.ClientTableRow(
            data=([
                c.__getattribute__(header)
                for header in self.headers
            ]),
            link='/dashboard/command/{id}'.format(id=c.id)
        ) for c in self.client.get_all_commands()]
