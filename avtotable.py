from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sqlite3



class MyHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        pass

    def on_created(self, event):
        if 'mp4' in event.src_path:
            sqlite_connection = sqlite3.connect('db.sqlite3')
            cursor = sqlite_connection.cursor()
            print("Подключен к SQLite")

            cursor.execute("SELECT * FROM main_avtobus")
            all_table = len(cursor.fetchall())
            id = all_table + 1
            video = event.src_path[6:]
            new = event.src_path.replace('_', '-')
            time_create = new[-21:-13]
            new = event.src_path.replace('_', ':')
            time_time = new[-12:-6] + '00'
            cat_id = event.src_path[-30]
            door_id = event.src_path[-23]
            title = f'avtobus{door_id}{id}-{time_create}-{time_time}'
            slug = id

            moreShows = [(id, title, slug, video, time_create, time_time, cat_id, door_id)]
            cursor.executemany("INSERT INTO main_avtobus VALUES (?, ?, ?, ?, ?, ?, ?, ?)", moreShows)
            cursor.execute("SELECT * FROM main_avtobus")
            # print(cursor.fetchone())
            print(id, title, slug, video, time_create, time_time, cat_id, door_id)

            sqlite_connection.commit()
            sqlite_connection.close()




    def on_deleted(self, event):
        pass

    def on_modified(self, event):
        pass

    def on_moved(self, event):
        pass


event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, path='media', recursive=True)
observer.start()





while True:
    try:
        pass
    except KeyboardInterrupt:
        observer.stop()