import os
import pathlib
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


DIRECTORY_TO_WATCH = pathlib.Path(os.getenv("NOTESDIR")) / "02-notes"


def run():
    observer = Observer()
    event_handler = Handler()

    observer.schedule(event_handler, DIRECTORY_TO_WATCH, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(5)
    except:
        observer.stop()
    observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print("Received created event - %s." % event.src_path)

        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            print("Received modified event - %s." % event.src_path)
