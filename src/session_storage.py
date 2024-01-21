import datetime

SESSION_DB = {}
SESSION_EXPIRATION_TIME = datetime.timedelta(days=1)


async def create_session(username, session_id):
    """Create a new session for the given username"""
    current_time = datetime.datetime.now()
    SESSION_DB[session_id] = {"user_id": username, "timestamp": current_time}
    expired_sessions = [session_id for session_id, session in SESSION_DB.items() if
                        current_time - session["timestamp"] > SESSION_EXPIRATION_TIME]
    for session_id in expired_sessions:
        del SESSION_DB[session_id]
    return session_id


async def validate_session(session_id):
    """Validate the given session ID"""
    session = SESSION_DB.get(session_id)
    if session is None:
        return False
    if (datetime.datetime.now() - session["timestamp"]) > SESSION_EXPIRATION_TIME:
        del SESSION_DB[session_id]
        return False
    return True


async def get_user_from_session(session_id):
    """Get the user associated with the given session ID"""
    if not await validate_session(session_id):
        return None
    return SESSION_DB[session_id]["user_id"]
