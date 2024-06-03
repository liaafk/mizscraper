# [Musikinformationszentrums (MIZ)]([url](https://miz.org/de/kurse))-Scraper

Dieses einfache Python-Skript habe ich geschrieben, um keine [interessante Musikworkshops]([url](https://miz.org/de/kurse)) mehr zu verpassen.

## Voraussetzungen

Um dieses Skript auszuführen, muss Python auf deinem System installiert sein. Zusätzlich müssen die folgenden Python-Bibliotheken installiert sein:

- `requests`
- `beautifulsoup4`
- `smtplib`
- `configparser`

Du kannst diese Bibliotheken mit pip installieren:

```sh
pip install requests beautifulsoup4 configparser
```

## Konfiguration

Erstelle eine config.ini Datei im gleichen Verzeichnis wie dein Skript. Diese Datei sollte deine E-Mail-Konfigurationsdetails enthalten. Hier ist ein Beispiel für die Konfiguration:

```sh
[EMAIL]
SMTP_SERVER = smtp.example.com
SMTP_PORT = 587
FROM_EMAIL = your-email@example.com
TO_EMAIL = recipient@example.com
SMTP_USER = your-email@example.com
SMTP_PASSWORD = your-email-password
```

## Verwendung

URLs aktualisieren: Aktualisiere die URLS Liste im Skript mit den URLs, die du durchsuchen möchtest.
Skript ausführen: Führe das Skript mit Python aus:

```sh
python scrape.py
```

Selbstverständlich kann einen CRON-Job hierfür errichtet werden.
