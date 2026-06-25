import os
import json
import time
import uuid
from datetime import datetime
from functools import wraps

LOG_DIR = "logs"

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)


def _get_timestamp():
    return datetime.utcnow().isoformat()


def _write_log(filename, data):
    file_path = os.path.join(LOG_DIR, filename)
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(data) + "\n")


class Observability:
    def __init__(self, service_name="AI_Service"):
        self.service_name = service_name

    # Base event logger
    def log_event(self, event_type, payload):
        log_entry = {
            "id": str(uuid.uuid4()),
            "timestamp": _get_timestamp(),
            "service": self.service_name,
            "event_type": event_type,
            "payload": payload
        }
        _write_log(f"{event_type}.log", log_entry)
        return log_entry

    # Request logging
    def log_request(self, endpoint, method, user_id=None):
        return self.log_event("request", {
            "endpoint": endpoint,
            "method": method,
            "user_id": user_id
        })

    # User query logging
    def log_query(self, user_id, query):
        return self.log_event("user_query", {
            "user_id": user_id,
            "query": query
        })

    # Tool call logging
    def log_tool_call(self, tool_name, input_data, status="started"):
        return self.log_event("tool_call", {
            "tool_name": tool_name,
            "input": input_data,
            "status": status
        })

    # Agent action logging
    def log_agent_action(self, agent_name, action, metadata=None):
        return self.log_event("agent_action", {
            "agent_name": agent_name,
            "action": action,
            "metadata": metadata or {}
        })

    # Error logging
    def log_error(self, error_message, context=None):
        return self.log_event("error", {
            "error": error_message,
            "context": context or {}
        })


# -----------------------------
# Decorator for auto-tracing
# -----------------------------
def trace_function(observability: Observability, name=None):
    def decorator(func):
        func_name = name or func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()

            observability.log_event("function_start", {
                "function": func_name,
                "args": str(args),
                "kwargs": str(kwargs)
            })

            try:
                result = func(*args, **kwargs)

                observability.log_event("function_success", {
                    "function": func_name,
                    "duration_ms": round((time.time() - start) * 1000, 2)
                })

                return result

            except Exception as e:
                observability.log_error(str(e), {
                    "function": func_name
                })
                raise

        return wrapper
    return decorator