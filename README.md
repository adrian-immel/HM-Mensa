# Projektübersicht
Dieses Projekt stellt über eine Flask-Webanwendung aktuelle Auslastungsdaten (Kapazität) von verschiedenen Mensen (LRZ-API) sowie Speisepläne (TUM-Campus-Mensa-API) bereit. Die Daten werden periodisch per Scheduler aktualisiert und über einfache HTTP-Endpoints ausgeliefert.
## Git

Das ganze Projekt kann auch auf [meinem GitHub](https://github.com/adrian-immel/HM-Mensa/tree/Abgabe) eingesehen werden.

## Installation
Installieren Sie alle Abhängigkeiten:
``` bash
   pip install --upgrade pip
   pip install -r requirements.txt
```
## Konfiguration
Legen Sie eine YAML-Datei (`config.yaml`) im Projektstamm an. Beispiel:
``` yaml
- name: "Mensa Innenstadt"
  lrz_subdistrict_id: "a"
  max_clients: 500
  access_points: ["ap1", "ap2", "ap3"]
  canteen_id: "mensa-inntenstadt"
- name: "Mensa Zweigstelle"
  lrz_subdistrict_id: "b"
  max_clients: 130
  access_points: ["ap1", "ap2"]
  canteen_id: "mensa-zweigstelle"
```
Die Datei wird beim Start automatisch von eingelesen, um die Liste der Mensastandorte zu initialisieren. `src/yaml_parser.py`
## Start der Anwendung
``` bash
python main.py
```
Standardmäßig läuft der Server unter `http://127.0.0.1:5000/`.
Beim Start werden folgende Tasks ausgeführt bzw. geplant:
- Initiales Abrufen der Kapazitätsdaten
- Initiales Abrufen der Menü-Daten
- Hintergrund-Scheduler:
    - Kapazitäts-Update alle 5 Minuten
    - Menü-Update täglich um 00:00:30

## Logs
- Logs werden in `logs/hm_mensa_YYYY-MM-DD.log` gespeichert und zusätzlich in der Konsole ausgegeben.
- Das Verzeichnis wird bei Bedarf automatisch angelegt. `logs/`

## API-Endpunkte
### 1. Statische Startseite
GET
→ liefert `/``public/index.html`
### 2. Kapazitätsdaten
GET
Optional: Query-Parameter `location` (Name der Mensa) filtern. `/api/capacity`
Beispiele:
``` bash
curl http://127.0.0.1:5000/api/capacity
curl http://127.0.0.1:5000/api/capacity?location=Mensa%20Innenstadt
```
### 3. Menüdaten
GET
Optional: Query-Parameter (Mensa-ID) filtern. `/api/menu?canteen_id=canteen_id`
Beispiele:
``` bash
curl http://127.0.0.1:5000/api/menu
curl http://127.0.0.1:5000/api/menu?canteen_id=mensa-inntenstadt
```
## Projektstruktur
```
└── HM-Mensa 
  ├── main.py                  # Entry Point, Flask-Routes & Scheduler
  ├── requirements.txt         # Alle benötigten Bibliotheken
  ├── config.yaml              # Konfigurationsdatei für Standorte
  ├── yaml_parser.py           # Läd Locations aus YAML
  ├── lrz_api_parser.py        # Abruf und Berechnung der Kapazität
  ├── trend_calculator.py      # Trendberechnung aus historischen Daten
  ├── eat_api_parser.py        # Abruf des Mensa-Menüs
  ├── json_location_model.py
  ├── menu_Api_model.py
  ├── dish_model.py
  ├── location_model.py  
  ├── public/
  │   └── index.html           # Frontend
  └── logs/                     # Logs

```
## Bibliotheken
Die wichtigsten Abhängigkeiten finden sich in : `requirements.txt`
## Technologiene
Die verwendeten Technologien/Bibliotheken sind:
- Flask
- APScheduler
- PyYAML
- requests
- numpy
- pytz
- JSON
- REST
