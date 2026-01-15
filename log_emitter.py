import time
import random
import logging
from datetime import datetime

# file where logs will be written
LOG_FILE = "real_time_logs.txt"

# setup logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s [%(name)s] %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# 1. THE MENU OF ERRORS (Pre-defined scenarios that match our RAG manual)
ERROR_SCENARIOS = [
    ("auth-service-node", "ERROR", "TokenExpiredError: jwt expired at 2024-01-09T10:00:00.000Z"),
    ("rds-postgres-primary", "CRITICAL", "FATAL: remaining connection slots are reserved for non-replication superuser connections"),
    ("aws-lambda-payment", "ERROR", "Runtime.ImportModuleError: Unable to import module 'app': No module named 'requests'"),
    ("k8s-ingress-nginx", "WARNING", "504 Gateway Time-out - Upstream server not responding")
]

SUCCESS_MESSAGES = [
    "User login successful", 
    "Payment processed", 
    "Health check passed", 
    "Cache refreshed"
]

print(f" Simulation Server Started! Writing logs to {LOG_FILE}...")
print("Press Ctrl+C to stop.\n")

try:
    while True:
        # 70% chance of "Normal" traffic (INFO), 30% chance of ERROR
        if random.random() < 0.7:
            msg = random.choice(SUCCESS_MESSAGES)
            # Format: YYYY-MM-DD HH:MM:SS [service] LEVEL Message
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"{timestamp} [app-server] INFO {msg}"
            
            with open(LOG_FILE, "a") as f:
                f.write(log_entry + "\n")
            print(f" {msg}")
            
        else:
            # Pick a random error from our menu
            service, level, msg = random.choice(ERROR_SCENARIOS)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"{timestamp} [{service}] {level} {msg}"
            
            with open(LOG_FILE, "a") as f:
                f.write(log_entry + "\n")
            print(f" [GENERATED ERROR]: {msg}")

        # Wait 3 seconds before the next log
        time.sleep(3)

except KeyboardInterrupt:
    print("\n Server stopped.")