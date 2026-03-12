import time
import datetime
import os
import json
from experiment.toolkits.configs import Addresses
from experiment.toolkits.configs import LabscriptSettings
from concurrent.futures import ThreadPoolExecutor, Future
import threading
import functools

_timer_information = {}
_absolute_time_information = {}

_TIMER_LOCK = threading.RLock()
_TIMER_IO_EXECUTOR = ThreadPoolExecutor(max_workers=1)

FLAG_TIMER_ENABLED = LabscriptSettings.flag_timer_enabled

def thread_safe_timer_method(fn):
    """Decorator to make Timer static methods atomic w.r.t shared timer dicts."""
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        if not FLAG_TIMER_ENABLED:
            return
        with _TIMER_LOCK:
            return fn(*args, **kwargs)
    return wrapper


class Timer:
    @staticmethod
    @thread_safe_timer_method
    def register_absolute_time(name: str):
        if name in _absolute_time_information:
            Timer.flush()  # safe (also locked)
            print(f"Register absolute time -- Duplicate name found: {name}")
            return
        _t = time.time_ns()
        _absolute_time_information[name] = {"time": _t}

    @staticmethod
    @thread_safe_timer_method
    def start_timer(name: str):
        if name in _timer_information:
            Timer.flush()
            print(f"Start timer -- Duplicate name found: {name}")
            return
        _timer_information[name] = {"start": time.time_ns()}

    @staticmethod
    @thread_safe_timer_method
    def stop_timer(name: str):
        info = _timer_information.get(name)
        if info is None:
            Timer.flush()
            print(f"End timer -- Name not found: {name}")
            return
        stop = time.time_ns()
        info["stop"] = stop
        info["duration"] = stop - info["start"]

    @staticmethod
    @thread_safe_timer_method
    def save_and_flush(path: str, process_name: str, executor: ThreadPoolExecutor = _TIMER_IO_EXECUTOR) -> Future:
        file_name = os.path.splitext(os.path.basename(path))[0]
        time_tag = os.path.basename(os.path.dirname(os.path.dirname(path))).split("-")[0]
        date_tag = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(path))))

        directory = os.path.join(Addresses.labscript_log_file, f"{date_tag}@{time_tag}@{process_name}")
        os.makedirs(directory, exist_ok=True)

        fileaddress = os.path.join(directory, f"{file_name}.json")

        # Snapshot + clear under lock, but DO NOT do disk I/O under lock:
        with _TIMER_LOCK:  # or whatever your thread_safe_timer_method uses
            d = {
                "durations": dict(_timer_information),
                "times": dict(_absolute_time_information),
            }
            _timer_information.clear()
            _absolute_time_information.clear()

        def _write_json(addr: str, payload: dict):
            with open(addr, "w") as f:
                json.dump(payload, f)
            return addr

        return executor.submit(_write_json, fileaddress, d)

    @staticmethod
    @thread_safe_timer_method
    def flush():
        _timer_information.clear()
        _absolute_time_information.clear()