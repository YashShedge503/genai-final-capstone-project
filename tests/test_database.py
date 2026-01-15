import pytest
from src.database import LogRecord
from datetime import datetime

def test_log_record_creation():
    # Test creating a LogRecord object
    record = LogRecord(
        log_id="12345",
        timestamp=datetime.now(),
        service_name="test-service",
        severity="ERROR",
        message="Test error message",
        is_resolved=False
    )
    
    assert record.log_id == "12345"
    assert record.severity == "ERROR"
    assert record.is_resolved is False