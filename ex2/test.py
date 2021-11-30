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
    modified = time.ctime(os.path.getmtime("./Users/users.txt")).split(" ")
    print(modified[4] + str(time.strptime(modified[1],'%b').tm_mon) +
     modified[2] + modified[3].split(":")[0]
     + modified[3].split(":")[1] + modified[3].split(":")[2])
