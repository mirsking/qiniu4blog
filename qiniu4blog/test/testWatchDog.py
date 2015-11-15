import time
import sys
import threading
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

class MyHandler(PatternMatchingEventHandler):
    ignore_directories = True
    threads = []
    def process(self, event):
        #print event.src_path, event.event_type  # print now only for degug
        if event.event_type == 'created':
            threadCreated = myThread(2, "created-Thread", event.src_path)
            threadCreated.start()
        if event.event_type == 'modified':
            threadModified = myThread(2, "modified-Thread", event.src_path)
            threadModified.start()

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)

def run1(filePath):
    print "in run1"
    print filePath

class myThread (threading.Thread):
    def __init__(self, threadID, name, filePath):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.filePath = filePath
    def run(self):
        print "Starting " + self.name
        #run1(self.filePath)

        print "Exiting " + self.name


if __name__ == '__main__':
    args = sys.argv[1:]
    observer = Observer()
    observer.schedule(MyHandler(), path=args[0] if args else '.',recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()