import logging
import logging.handlers
import os
import sys

from daemon import runner
import subprocess

cmd = os.getcwd()

class App():

    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = '/tmp/foo.pid'
        self.pidfile_timeout = 5

    def run(self):
        logs = logging.getLogger('MyLogger')
        logs.setLevel(logging.DEBUG)
        fh = logging.handlers.RotatingFileHandler(
            '/tmp/test.log', maxBytes=10000000, backupCount=5)
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter(u'%(asctime)s [%(levelname)s] %(message)s')
        fh.setFormatter(formatter)
        logs.addHandler(fh)
        print(cmd)
        sys.argv = [cmd + '/manage.py', 'runserver', '0.0.0.0:8000']
        import manage
        manage.main()


app = App()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()
