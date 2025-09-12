def detect_anomaly(location):
    """Return True if suspicious login (non-India)"""
    if location.lower() != "india":
        return True
    return False
