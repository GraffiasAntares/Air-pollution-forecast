import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class SCSSHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".scss"):
            print(f"Изменение обнаружено: {event.src_path}")
            subprocess.run(["npx", "sass", "../front/static/css/main.scss", "../front/static/css/main.css"])

if __name__ == "__main__":
    path = "../front/static/css"
    event_handler = SCSSHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()