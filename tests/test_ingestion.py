import pytest
from datetime import datetime
from src.ingestion import parse_log_line

def test_parse_valid_error_log():
    # A standard error log line
    line = "2025-01-14 12:00:00 [payment-service] ERROR Connection Failed"
    
    result = parse_log_line(line)
    
    assert result is not None
    assert result['service'] == "payment-service"
    assert result['severity'] == "ERROR"
    assert result['message'] == "Connection Failed"
    assert isinstance(result['timestamp'], datetime)

def test_parse_valid_info_log():
    # A standard info log
    line = "2025-01-14 12:05:00 [auth] INFO User logged in"
    result = parse_log_line(line)
    assert result['severity'] == "INFO"

def test_parse_invalid_log_format():
    # A junk line that shouldn't parse
    line = "This is just random text not a log"
    result = parse_log_line(line)
    assert result is None

def test_parse_empty_line():
    line = ""
    result = parse_log_line(line)
    assert result is None