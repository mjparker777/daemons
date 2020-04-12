import os
import socket

# ****************************************
# Daemons
# ****************************************

DAEMON_SLEEP_TIME = 5

# pids
DAEMON_BASE_DIR = "/my_project/daemons"  # path for the daemon pids
PID_EXAMPLE_DAEMON = os.path.join(DAEMON_BASE_DIR, "example/daemon.pid")

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

SECRET_KEY = os.getenv("SECRET_KEY")
SETTINGS = "my_project.settings"
SMTP_SERVER = os.getenv("SMTP_SERVER")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")
SQL_USER = os.getenv("SQL_USER")

# Logs
LOG_DIR = "/var/log/my_project/"

# ****************************************
