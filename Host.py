import hashlib
import time

class Host:
    class HostLog:
        def __init__(self, hostname):
            self._hostname=hostname
            self._logfile='logs/{}.log'.format(self._sha256(hostname))

        def __call__(self, msg):
            self.log(msg)

        def log(self, msg):
            open(self._logfile, 'a').write(
                '{} : {} : {}'.format(
                    self._utcnow(),
                    self._hostname,
                    msg,
                )
            )

        @staticmethod
        def _utcnow():
            return str(int(time.time()))

        @staticmethod
        def _sha256(s):
            return hashlib.sha256(s.encode()).hexdigest()

    def __init__(self, hostname, uname):
        self.hostname=hostname
        self.uname=uname
        
        self._hostlog=self.HostLog(hostname)
        self.pending_cmds=list()
        
        self.log('[+] registering client : {}'.format(hostname))

    def log(self, msg):
        self._hostlog(msg)

    def add_cmd(self, cmd):
        self.pending_cmds.append(cmd)
        self.log('"{}" command submitted')

    def get_pending(self):
        ret=dict()
        ret['cmds']=self.pending_cmds.copy()
        self.pending_cmds.clear()
        return ret
