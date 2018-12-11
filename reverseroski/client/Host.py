from datetime import datetime
from db import DB_NAME
import sqlite3
import hashlib
import time
import json
import art

class Host:
    class _Host_Exception(Exception):
        pass

    class Commands:
        def __init__(self, hostid):
            self.commands=list()
            self._load_command_state(hostid)

        def __enter__(self):
            return self

        def __del__(self):
            pass

        def __exit__(self, *_):
            pass

        def __iter__(self):
            return iter(self.commands)

        def _load_command_state(self, hostid):
            with sqlite3.connect(DB_NAME) as db:
                commands=db.execute(
                    'SELECT command, commandid, hostid, stdout, pending ' + \
                    'FROM Commands WHERE hostid = ?;',
                    (hostid,)
                ).fetchall()
                for command in commands:
                    self.commands.append(self.Command(*command))

        def dump_state(self):
            with sqlite3.connect(DB_NAME) as db:
                for command in self:
                    db.execute(*command.dumps())
                db.commit()

    class Command:
        _DUMP_SQL=open('sql/command_dump.sql').read()
        def __init__(self, command,  commandid, hostid, stdout=None, pending=True, timestamp=None):
            self.command=command
            self.commandid=commandid
            self.hostid=hostid
            self.timestamp=timestamp if timestamp is not None else str(datetime.utcnow())
            self.stdout='' if stdout is None else stdout
            self.pending=bool(pending)

        def __enter__(self):
            return self

        def submit_stdout(self, stdout):
            assert self.pending
            self.pending=False
            self.stdout=stdout

        def dumps(self):
            return self._DUMP_SQL, (
                self.command,
                self.pending,
                self.stdout,
                self.commandid,
                self.hostid,
            )

        def state(self):
            return [
                self.commandid,
                self.pending,
                self.timestamp,
                self.command,
                self.stdout,
            ]

        @staticmethod
        def _utcnow():
            return str(int(time.time()))

    _DUMP_SQL=open('sql/host_dump.sql').read()
    def __init__(self, hostid, hostname, uname):
        self.hostid=hostid
        self.hostname=hostname
        self.uname=uname
        self.commands=list()
        self._load_command_state()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.dump_state()

    def __del__(self):
        self.dump_state()


    def dump_command_state(self, n=None):
        raise DeprecationWarning()
        with sqlite3.connect(DB_NAME) as db:
            if n is None:
                for sql, args in (command.dumps() for command in self.commands):
                    db.execute(sql, args)
            else:
                db.execute(*self.commands[n].dumps())
            db.commit()

    def dumps(self):
        return self._DUMP_SQL, (
            self.hostid,self.hostname,self.uname,
        )

    def dump_state(self):
        with sqlite3.connect(DB_NAME) as db:
            sql, args = self.dumps()
            db.execute(sql, args)
            db.commit()

    def add_command(self, command):        
        self.commands.append(
            self.Command(command, self.hostid, len(self.commands))
        )

    def submit_pending_command(self, commandid, stdout):
        assert self.commands[commandid].pending
        self.commands[commandid].submit_stdout(stdout)

    def get_pending(self):
        for i in self.commands:
            print(i.state())
        return list(map(
            lambda command: (command.commandid, command.command,), filter(
                lambda command: command.pending,
                self.commands
            )
        ))


class Hosts:
    def __init__(self):
        with sqlite3.connect(DB_NAME) as db:
            size=db.execute(
                'SELECT MAX(hostid) FROM Hosts;'
            ).fetchone()[0]
            self.size=size+1 if size is not None else 0
            print('siz:', self.size)

    def __iter__(self):
        for hostid in range(self.size):
            yield self.load_state(hostid)

    def __len__(self):
        return self.size

    def __contains__(self, item):
        for host in self:
            if item == host.hostname or item == host:
                return True
        else:
            return False

    def get(self, hostid):
        return self.load_state(hostid)

    def set(self, host, new=False):
        host.dump_state()
        if new:
            self.size+=1

    @staticmethod
    def load_state(hostid):
        with sqlite3.connect(DB_NAME) as db:
            hostdata=db.execute(
                'SELECT hostid, hostname, uname FROM Hosts ' + \
                'WHERE hostid = ?;',
                (hostid,)
            ).fetchone()
            return Host(*hostdata)

# def load_state():
#     print(art.star, 'loading state...', end='\r')
#     with sqlite3.connect('rev.db') as db:
#         hosts_data=db.execute(
#             'SELECT hostid, hostname, uname FROM Hosts;'
#         ).fetchall()
#     hosts_data=list(sorted(
#         hosts_data,
#         key=lambda host: host[0]
#     ))
#     print(art.plus, 'loaded state' + ' '*10)
#     return [
#         Host(*data)
#         for data in hosts_data
#     ]

# def dump_state(hosts):
#     print(hosts)
#     print(art.star, 'Dumping hosts state into database...')
#     for index in range(len(hosts)):
#         host[index].dumps_state()
#     print(art.plus, 'Successfully dumped hosts state!')
