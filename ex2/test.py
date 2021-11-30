import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import os
import time

class Event(LoggingEventHandler):
    def dispatch(self, event):
        print(event)


if __name__ == "__main__":
    os.mkdir("./USER_PATH")
