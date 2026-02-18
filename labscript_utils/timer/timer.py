import time
import datetime
import os
import json
from experiment.toolkits.configs import Addresses

FLAG_TIMER_ENABLED = True

_timer_information = {}
_absolute_time_information = {}

class Timer:

    @staticmethod
    def register_absolute_time(name: str):
        if name in _absolute_time_information:
            raise Exception(f"Register absolute time -- Duplicate name found: {name}")
        _t = time.perf_counter_ns()
        _absolute_time_information[f'{name}'] = {
            "time": _t
        }

    @staticmethod
    def start_timer(name: str):
        if name in _timer_information:
            raise Exception(f"Start timer -- Duplicate name found: {name}")
        _timer_information[name] = {"start": time.perf_counter_ns()}

    @staticmethod
    def stop_timer(name: str):
        if name not in _timer_information:
            raise Exception(f"End timer -- Name not found: {name}")
        _timer_information[name]["stop"] = time.perf_counter_ns()
        _timer_information[name]["duration"] = _timer_information[name]["stop"] - _timer_information[name]["start"]

    @staticmethod
    def save_and_flush(filename: str, date_tag: str, time_tag: str):
        if not FLAG_TIMER_ENABLED:
            return
        directory = os.path.join(Addresses.labscript_log_file, f'{date_tag}@{time_tag}')
        os.makedirs(directory, exist_ok=True)
        
        fileaddress = os.path.join(directory, f'{filename}.json')
        with open(fileaddress, "w") as file:
            d = {
                "durations": _timer_information,
                "times": _absolute_time_information
            }
            json.dump(d, file)

        _timer_information.clear()
        _absolute_time_information.clear()