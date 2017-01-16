import os
import socket

# ****************************************
# Server
# ****************************************

HOST_NAME = socket.gethostname()
BETA_BOXES = []
LIVE_BOXES = []
if HOST_NAME in LIVE_BOXES:
    DEBUG = False
else:
    DEBUG = True

SECRET_KEY = os.getenv("REPORTS_SECRET_KEY")
SQL_PASSWORD = os.getenv("REPORTS_SQL_PASSWORD")
SQL_USER = os.getenv("REPORTS_SQL_USER")
SMTP_SERVER = os.getenv("SMTP_SERVER")

# Logs
LOG_DIR = "/var/log/my_project/"

# ****************************************
# Daemons
# ****************************************

DAEMON_SLEEP_TIME = 5

# pids
DAEMON_BASE_DIR = "/x/local/my_project/daemons"  # path for the daemon pids
# noinspection PyUnresolvedReferences
PID_EXAMPLE_DAEMON = os.path.join(DAEMON_BASE_DIR, "example/daemon.pid")

# ****************************************
