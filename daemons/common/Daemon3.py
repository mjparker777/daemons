"""
Python 3

This was created using several examples from the net.
Here is where they all started:
http://web.archive.org/web/20131025230048/http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/
"""
from abc import ABCMeta
from abc import abstractmethod
import atexit
import errno
import os
from signal import SIGTERM
import sys
import time


class Daemon(object):
    """
    A generic daemon class for Python 3.x.x

    Usage: subclass the Daemon class and override the run() method
    """
    __metaclass__ = ABCMeta

    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.pidfile = pidfile
        self.stderr = stderr
        self.stdin = stdin
        self.stdout = stdout

    def daemonize(self):
        """
        Do the UNIX double-fork magic, see Stevens' "Advanced
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError as err:
            sys.stderr.write("Attempt to fork 1st time failed: {} ({})\n".format(err.errno, err.strerror))
            sys.exit(1)

        # Decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)

        # Do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                sys.exit(0)
        except OSError as err:
            sys.stderr.write("Attempt to fork 2nd time failed: {} ({})\n".format(err.errno, err.strerror))
            sys.exit(1)

        # Redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = open(self.stdin, 'r')
        so = open(self.stdout, 'a+')
        se = open(self.stderr, 'a+')
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # Write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        with open(self.pidfile, 'w+') as f:
            f.write(pid + '\n')

    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        """
        Start the daemon
        """
        # Check for a pidfile to see if the daemon is already running
        try:
            with open(self.pidfile, 'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if pid:
            message = "The daemon may already be running. The pidfile ({}) already exists.\n".format(self.pidfile)
            sys.stderr.write(message)
            sys.exit(1)

        # Start the daemon
        print("Attempting to start {} as a daemon.".format(sys.argv[0]))
        self.daemonize()
        self.run()

    def stop(self):
        """
        Stop the daemon
        """
        # Get the pid from the pidfile
        try:
            with open(self.pidfile, 'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if not pid:
            message = "The daemon may not be running. The pidfile ({}) does not exist.\n".format(self.pidfile)
            sys.stderr.write(message)
            return  # not an error in a restart

        # Try killing the daemon process
        print("Attempting to shutdown daemon process {}".format(pid))
        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
        except OSError as err:
            e = str(err.args)
            if e.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print(str(err.args))
                sys.exit(1)

    def restart(self):
        """
        Restart the daemon
        """
        self.stop()
        self.start()

    def status(self):
        """
        Get the status of the daemon
        """
        # Check for a pidfile to see if the daemon is already running
        try:
            with open(self.pidfile, 'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if not pid:
            message = "The daemon may not be running. The pidfile ({}) does not exist.\n".format(self.pidfile)
            sys.stderr.write(message)
            sys.exit(1)

        try:
            os.kill(pid, 0)
        except OSError as err:
            if err.errno == errno.EPERM:
                # EPERM clearly means there's a process to deny access to
                sys.stdout.write("The process with the PID {} is running but denied access.\n".format(pid))
                sys.exit(0)
            else:
                sys.stderr.write("There is not a process with the PID {} specified in {}\n".format(pid, self.pidfile))
                sys.exit(1)

        sys.stdout.write("The process with the PID {} is running\n".format(pid))
        sys.exit(0)

    def perform_action(self):
        """
        Process the command line parameters and perform the start, stop, restart, or status operations.
        """
        if len(sys.argv) == 2:
            if 'start' == sys.argv[1]:
                self.start()
            elif 'stop' == sys.argv[1]:
                self.stop()
            elif 'restart' == sys.argv[1]:
                self.restart()
            elif 'status' == sys.argv[1]:
                self.status()
            else:
                print("Unknown command")
                sys.exit(2)
            sys.exit(0)
        else:
            print("Usage: {} start | stop | restart | status".format(sys.argv[0]))
            sys.exit(2)

    @abstractmethod
    def run(self):
        """
        Override this method when you subclass Daemon.
        It will be called after the process has been daemonized by start() or restart().
        """
        raise NotImplementedError
