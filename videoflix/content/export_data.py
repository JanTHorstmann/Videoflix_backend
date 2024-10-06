import os
import sys
import django
import json

# Sicherstellen, dass der Projektpfad im Python-Pfad ist
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Django-Umgebung initialisieren
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'videoflix.settings')  # Stelle sicher, dass 'videoflix' dein Projektname ist
django.setup()

from content.admin import VideoResource  # Der Import nach dem Setup sicherstellen

def download_data():
    dataset = VideoResource().export()
    data_as_json = dataset.json

    # Pfad zum Download-Ordner ermitteln
    download_folder = os.path.join(os.path.expanduser("~"), "Downloads")

    # Pfad zur Datei im Download-Ordner
    file_path = os.path.join(download_folder, 'exported_videos.json')

    # Speichern der Daten als JSON im Download-Ordner
    with open(file_path, 'w') as json_file:
        json.dump(data_as_json, json_file)

    print(f'Datei erfolgreich im Download-Ordner gespeichert: {file_path}')
    return file_path

# Aufruf der Funktion
if __name__ == "__main__":
    result = download_data()