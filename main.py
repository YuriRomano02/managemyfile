import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Path to the download folder (example with fictional path)
folder_to_track = r"C:\Users\john_doe\Downloads"

# Dictionary mapping file extensions to destination folder names
extensions_map = {
    '.jpg': 'Immagini', '.jpeg': 'Immagini', '.png': 'Immagini', '.gif': 'Immagini',
    '.pdf': 'Documenti', '.docx': 'Documenti', '.txt': 'Documenti', '.xlsx': 'Documenti',
    '.mp4': 'Video', '.mkv': 'Video', '.mov': 'Video',
    '.mp3': 'Musica', '.wav': 'Musica',
    '.zip': 'Archivi', '.rar': 'Archivi', '.7z': 'Archivi',
    '.exe': 'Programmi', '.msi': 'Programmi'
}

class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        try:
            for filename in os.listdir(folder_to_track):
                source = os.path.join(folder_to_track, filename)
                
                # Skip if it's a directory
                if os.path.isdir(source):
                    continue
                
                # Get file extension in lowercase
                extension = os.path.splitext(filename)[1].lower()
                
                # Check if extension is in our mapping
                if extension in extensions_map:
                    dest_folder_name = extensions_map[extension]
                    dest_path = os.path.join(folder_to_track, dest_folder_name)
                    destination = os.path.join(dest_path, filename)

                    # Create destination folder if it doesn't exist
                    if not os.path.exists(dest_path):
                        os.makedirs(dest_path)

                    try:
                        # Small pause to ensure the download is complete
                        time.sleep(1)
                        shutil.move(source, destination)
                        print(f"Moved: {filename} -> {dest_folder_name}")
                    except (OSError, PermissionError) as e:
                        # File might still be in use, skip for now
                        print(f"Could not move {filename}: {e}")
        except Exception as e:
            print(f"Error during file processing: {e}")

# --- STARTUP ---
event_handler = MoverHandler()
observer = Observer()
observer.schedule(event_handler, folder_to_track, recursive=False)
observer.start()

print(f"Monitoring active on: {folder_to_track}")
try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    observer.stop()
observer.join()
