import sys
import time
import traceback

from django import db

from common import constants, logging_util
from daemons.common.Daemon2 import Daemon


class ExampleDaemon(Daemon):
    def __init__(self, pidfile):
        super(ExampleDaemon, self).__init__(pidfile=pidfile)

        self._daemon_name = "ExampleDaemon"
        self._logger = logging_util.get_logger(self._daemon_name)

    def _run_task_one(self):
        """
        Handle a daemon task.
        """
        self._logger.info("_run_task_one")

    def _run_task_two(self):
        """
        Handle another daemon task.
        """
        self._logger.info("_run_task_two")

    def run(self):
        """
        Controls the flow of the Daemon tasks.
        """
        self._logger.debug("***> {0} Started <***".format(self._daemon_name))

        while True:
            time.sleep(int(constants.DAEMON_SLEEP_TIME))
            self._logger.info("==> Start {0} Run <==".format(self._daemon_name))
            try:
                # Daemon task 1
                self._run_task_one()
                # Daemon task 2
                self._run_task_two()
            except db.utils.OperationalError as err:
                self._logger.error("{0}\n{1}".format(type(err), traceback.format_exc()))
                db.connection.close()
            except Exception as err:
                self._logger.critical("{0}\n{1}".format(type(err), traceback.format_exc()))


daemon = ExampleDaemon(constants.PID_EXAMPLE_DAEMON)
# Check to see if we're running under the debugger,
#   If we are then bypass the daemonize and just run directly.
if sys.gettrace() is not None:
    daemon.run()
else:
    daemon.perform_action()
