Type | Version/Name
--- | ---
Distribution Name	| OpenSuSE Leap
Distribution Version	| 16.0
Kernel Version	| 6.12.0-160000.35-default
Architecture	| x86\_64
Incus Version	| 6.23
Xephyr Version | 21.1.15
Created | 2026-07-01
Updated | 2026-07-03


# Incus Desktop & Development Environment

# Inhaltsverzeichnis
* [Zielsetzung](#zielsetzung)
* [Design- und Architekturentscheidungen](#design--und-architekturentscheidungen)
  * [Profile als Konfigurationsbausteine](#profile-als-konfigurationsbausteine)
  * [Verwendung offizieller Distribution-Images](#verwendung-offizieller-distribution-images)
  * [Deklarative Konfiguration](#deklarative-konfiguration)
  * [Trennung von technischen und funktionalen Aspekten](#trennung-von-technischen-und-funktionalen-aspekten)
    * [Container](#container)
    * [Environment](#environment)
    * [Applications](#applications)
    * [Development](#development)
  * [Persistente Benutzerdaten](#persistente-benutzerdaten)
  * [Minimierung des Hosts](#minimierung-des-hosts)
* [Einrichtung](#einrichtung)
  * [Voraussetzungen](#voraussetzungen)
  * [Grundinstallation](#grundinstallation)
* [Backup](#backup)
  * [Profile](#profile)
  * [Containerdefinitionen](#containerdefinitionen)
  * [Persistente Benutzerdaten](#persistente-benutzerdaten-1)
* [Restore](#restore)
* [Technische Limitierungen](#technische-limitierungen)
  * [X11](#x11)
  * [Wayland](#wayland)
  * [Plattform](#plattform)
  * [Reproduzierbarkeit](#reproduzierbarkeit)
* [Projektstatus](#projektstatus)
* [Lizenz](#lizenz)


## Zielsetzung

Dieses Projekt verfolgt das Ziel, eine vollständig containerisierte Arbeitsumgebung auf Basis von Incus bereitzustellen.

Sämtliche Anwendungen – Browser, Entwicklungsumgebungen, Desktopumgebungen und weitere Werkzeuge – werden in voneinander getrennten Containern betrieben. Der Host übernimmt ausschließlich die Rolle einer minimalen Laufzeitumgebung und stellt die notwendigen Ressourcen (Kernel, Grafik, Audio, Netzwerk und Storage) zur Verfügung.

Die Architektur verfolgt dabei mehrere Ziele:

* Trennung von Host- und Anwendungsumgebung
* Minimierung von Abhängigkeiten auf dem Host
* Reproduzierbarkeit des Gesamtsystems
* einfache Migration auf andere Systeme
* Möglichkeit, Anwendungen unabhängig voneinander zu aktualisieren oder auszutauschen
* möglichst vollständige Beschreibung des Systems als Code ("Infrastructure as Code")

Das langfristige Ziel ist es, einen vollständigen Arbeitsplatz jederzeit aus einer Versionsverwaltung reproduzierbar neu erzeugen zu können.

[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)
---

# Design- und Architekturentscheidungen

## Profile als Konfigurationsbausteine

Anstatt große, monolithische Container-Images bereitzustellen, wird das System aus kleinen, klar abgegrenzten Incus-Profilen zusammengesetzt.

Jedes Profil beschreibt genau einen technischen oder funktionalen Aspekt eines Containers.

Beispiele:

* Storage
* Netzwerk
* Ressourcenlimits
* Benutzer
* GUI-Anbindung
* Entwicklungsumgebungen
* einzelne Anwendungen

Dadurch entstehen kleine, wiederverwendbare Bausteine, aus denen beliebige Container zusammengesetzt werden können.

[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)
---

## Verwendung offizieller Distribution-Images

Es werden ausschließlich unveränderte Images der jeweiligen Linux-Distribution verwendet.

Gemeinsamkeiten zwischen verschiedenen Containern werden nicht durch eigene Basis-Images, sondern ausschließlich über Profile beschrieben.

Ein ursprünglich evaluierter Ansatz mittels distrobuilder wurde verworfen, da der Wartungsaufwand den praktischen Nutzen überwog.

[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)
---

## Deklarative Konfiguration

Die eigentliche Systembeschreibung befindet sich nicht innerhalb der Container, sondern in den verwendeten Profilen.

Container stellen damit lediglich eine Instanz einer zuvor definierten Konfiguration dar.

Die eigentliche Installations- und Konfigurationslogik ist versionierbar und unabhängig vom Lebenszyklus einzelner Container.

[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)
---

## Trennung von technischen und funktionalen Aspekten

Profile werden in verschiedene Kategorien unterteilt.

### Container

Stellt grundlegende Incus-Funktionalität bereit.

Beispiele:

* Storage
* Netzwerk
* Ressourcenlimits

### Environment

Beschreibt die Laufzeitumgebung.

Beispiele:

* GUI
* Desktop
* Benutzer

### Applications

Installiert Anwendungen.

Beispiele:

* Browser
* Office
* Editoren
* Werkzeuge

### Development

Installiert Entwicklungsumgebungen.

Beispiele:

* Rust
* Python
* Perl
* Git

Dadurch bleiben einzelne Verantwortlichkeiten klar voneinander getrennt.

[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)
---

## Persistente Benutzerdaten

Container bleiben grundsätzlich austauschbar.

Persistente Daten werden über Mounts vom Host eingebunden.

Dazu gehören beispielsweise:

* Home-Verzeichnis
* Konfigurationsdateien
* Cache
* Git-Konfiguration
* Shell-Konfiguration

Ein Neuaufbau eines Containers führt dadurch nicht zum Verlust persönlicher Daten.

[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)
---

## Minimierung des Hosts

Der Host enthält möglichst wenig Software.

Anwendungen werden grundsätzlich innerhalb von Containern ausgeführt.

Der Host übernimmt lediglich:

* Incus
* X11/Xephyr
* Audio-Weiterleitung
* Netzwerk
* Storage
* Startskripte

[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)
---

# Einrichtung

## Voraussetzungen

Benötigt werden mindestens:

* aktuelles Linux-System
* Incus
* funktionsfähige Netzwerk- und Storage-Konfiguration
* Git
* X11 (derzeit Xephyr)

Weitere Anforderungen ergeben sich aus den jeweiligen Profilen.

[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)
---

## Grundinstallation

Die Einrichtung erfolgt in mehreren Schritten.

1. Incus initialisieren
2. Storage-Pool anlegen
3. Netzwerk konfigurieren
4. Profile importieren
5. Images herunterladen
6. Container erzeugen
7. Persistente Verzeichnisse anlegen
8. Desktop-Startskripte installieren

Die eigentliche Konfiguration erfolgt ausschließlich über die im Repository enthaltenen YAML-Dateien.

[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)
---

# Backup

Das Projekt unterscheidet bewusst zwischen verschiedenen Ebenen eines Backups.

## Profile

Alle Incus-Profile werden exportiert und versioniert.

Sie stellen den eigentlichen Konfigurationsstand des Systems dar.

[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)
---

## Containerdefinitionen

Für jede Instanz werden die relevanten Informationen gesichert.

Insbesondere:

* verwendetes Image
* verwendete Profile
* zusätzliche Devices
* optionale Instanzparameter

Der flüchtige Laufzeitzustand eines Containers wird bewusst nicht gesichert.

[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)
---

## Persistente Benutzerdaten

Alle eingebundenen Host-Verzeichnisse werden unabhängig von Incus gesichert.

Hierzu gehören insbesondere:

* Home-Verzeichnisse
* Konfigurationsdateien
* Entwicklungsprojekte
* Dokumente

[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)
---

# Restore

Die Wiederherstellung erfolgt schrittweise.

1. Storage wiederherstellen
2. Netzwerk wiederherstellen
3. Profile importieren
4. Images bereitstellen
5. Containerdefinitionen importieren
6. Container erzeugen
7. Persistente Daten einbinden

Langfristig ist ein Werkzeug geplant, das diesen Vorgang vollständig automatisiert.

[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)
---

# Technische Limitierungen

Derzeit sind einige Einschränkungen bekannt.

## X11

Die GUI-Anbindung erfolgt momentan über Xephyr.

Aufgrund technischer Einschränkungen von Xephyr und Incus wird derzeit die Authentifizierung mittels `xhost` verwendet.

Ein Umstieg auf Xauthority oder alternative Verfahren wird zukünftig erneut evaluiert.

[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)
---

## Wayland

Wayland wird derzeit nicht unterstützt.

Der Fokus liegt zunächst auf einer stabilen X11-basierten Lösung.

[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)
---

## Plattform

Der Schwerpunkt liegt aktuell auf openSUSE Tumbleweed.

Andere Distributionen wurden bisher nicht getestet.

[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)
---

## Reproduzierbarkeit

Der deklarative Teil des Systems ist bereits weitgehend reproduzierbar.

Die vollständige Automatisierung von Backup und Restore befindet sich noch in Planung.

[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)
---

# Projektstatus

Das Projekt befindet sich derzeit in der Evaluierungs- und Entwurfsphase.

Designentscheidungen werden bewusst anhand praktischer Erfahrungen getroffen und können sich bis zum Architektur-Freeze noch ändern.

Erst nach Abschluss dieser Phase wird die Struktur als stabil betrachtet.

[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)
---

# Lizenz

Derzeit ist noch keine Lizenz festgelegt.

[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)
---
