import os
import re
import uuid
from datetime import datetime
from src.database import LogRecord

# Path to the real-time log file
LOG_FILE_PATH = "real_time_logs.txt"

def parse_log_line(line):
    """
    Parses a raw log line into a structured dictionary.
    This function is what your tests are checking.
    """
    # Regex to capture: Timestamp, Service, Severity, Message
    # Example: "2025-01-14 12:00:00 [payment-service] ERROR Connection Failed"
    pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[(.*?)\] (\w+) (.*)"
    match = re.match(pattern, line)
    
    if match:
        return {
            "timestamp": datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S"),
            "service": match.group(2),
            "severity": match.group(3),
            "message": match.group(4).strip()
        }
    return None

def fetch_cloud_logs(db):
    """
    Reads the file and saves new errors to the database.
    """
    if not os.path.exists(LOG_FILE_PATH):
        return 0

    with open(LOG_FILE_PATH, "r") as f:
        lines = f.readlines()

    # Read the last 20 lines (tail)
    recent_lines = lines[-20:]
    count = 0

    for line in recent_lines:
        parsed = parse_log_line(line)
        
        # Only ingest Error/Critical/Warning (Skip INFO)
        if parsed and parsed['severity'] in ['ERROR', 'CRITICAL', 'WARNING']:
            
            # Prevent duplicate entries in DB
            exists = db.query(LogRecord).filter(LogRecord.message == parsed['message']).first()
            
            if not exists:
                new_log = LogRecord(
                    log_id=str(uuid.uuid4())[:8],
                    timestamp=parsed['timestamp'],
                    service_name=parsed['service'],
                    severity=parsed['severity'],
                    message=parsed['message'],
                    is_resolved=False
                )
                db.add(new_log)
                count += 1
    
    db.commit()
    return count




# import uuid
# import random
# from datetime import datetime, timedelta
# from faker import Faker
# from sqlalchemy.orm import Session
# from src.database import LogRecord

# fake = Faker()

# # Pre-defined "Real" DevOps Errors
# ERROR_SCENARIOS = [
#     {
#         "service": "aws-lambda-payment",
#         "severity": "ERROR",
#         "msg": "Runtime.ImportModuleError: Unable to import module 'app': No module named 'requests'"
#     },
#     {
#         "service": "rds-postgres-primary",
#         "severity": "CRITICAL",
#         "msg": "FATAL: remaining connection slots are reserved for non-replication superuser connections"
#     },
#     {
#         "service": "k8s-ingress-nginx",
#         "severity": "ERROR",
#         "msg": "UpstreamTimedOut: upstream request timeout while connecting to upstream client: 10.244.0.12"
#     },
#     {
#         "service": "auth-service-node",
#         "severity": "WARNING",
#         "msg": "TokenExpiredError: jwt expired at 2024-01-09T10:00:00.000Z"
#     }
# ]

# def fetch_cloud_logs(db: Session, count=3):
#     """
#     Simulates fetching logs from AWS CloudWatch/GCP.
#     In a real app, you would replace this logic with `boto3.client('logs').get_log_events(...)`
#     """
#     new_logs = []
    
#     for _ in range(count):
#         scenario = random.choice(ERROR_SCENARIOS)
        
#         # check if we already have this fake log to avoid duplicates 
#         unique_id = f"aws-log-{uuid.uuid4().hex[:8]}"
        
#         log_entry = LogRecord(
#             log_id=unique_id,
#             timestamp=datetime.now() - timedelta(minutes=random.randint(1, 120)),
#             service_name=scenario["service"],
#             severity=scenario["severity"],
#             message=scenario["msg"],
#             is_resolved=False
#         )
        
#         db.add(log_entry)
#         new_logs.append(log_entry)
    
#     db.commit()
#     return len(new_logs)