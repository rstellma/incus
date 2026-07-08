Type | Version/Name
--- | ---
Distribution Name	| OpenSuSE Leap
Distribution Version	| 16.0
Kernel Version	| 6.12.0-160000.35-default
Architecture	| x86\_64
Incus Version	| 6.23
Xephyr Version | 21.1.15
Created | 2026-07-01
Updated | 2026-07-08


# Incus Desktop & Development Environment

# Inhaltsverzeichnis
* [1. Zielsetzung](#1-zielsetzung)
* [2. Design- und Architekturentscheidungen](#2-design--und-architekturentscheidungen)
  * [2.1 Profile als Konfigurationsbausteine](#21-profile-als-konfigurationsbausteine)
  * [2.2 Verwendung offizieller Distribution-Images](#22-verwendung-offizieller-distribution-images)
  * [2.3 Deklarative Konfiguration](#23-deklarative-konfiguration)
  * [2.4 Trennung von technischen und funktionalen Aspekten](#24-trennung-von-technischen-und-funktionalen-aspekten)
    * [2.4.1 Container](#241-container)
    * [2.4.2 Environment](#242-environment)
    * [2.4.3 Applications](#243-applications)
    * [2.4.4 Development](#244-development)
  * [2.5 Persistente Benutzerdaten](#25-persistente-benutzerdaten)
  * [2.6 Minimierung des Hosts](#25-minimierung-des-hosts)
* [3. Einrichtung](#3-einrichtung)
  * [3.1 Voraussetzungen](#31-voraussetzungen)
  * [3.2 Grundinstallation](#32-grundinstallation)
  * [3.3 Incus Manager](#33-incus-manager)
* [4. Backup](#4-backup)
  * [4.1 Profile](#41-profile)
  * [4.2 Containerdefinitionen](#42-containerdefinitionen)
  * [4.3 Persistente Benutzerdaten](#43-persistente-benutzerdaten)
* [5. Restore](#5-restore)
* [6. Technische Limitierungen](#6-technische-limitierungen)
  * [6.1 X11](#61-x11)
  * [6.2 Wayland](#62-wayland)
  * [6.3 Plattform](#63-plattform)
  * [6.4 Reproduzierbarkeit](#64-reproduzierbarkeit)
* [7. Projektstatus](#7-projektstatus)
* [8. Lizenz](#8-lizenz)


# 1. Zielsetzung

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

# 2. Design- und Architekturentscheidungen

## 2.1 Profile als Konfigurationsbausteine

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

## 2.2 Verwendung offizieller Distribution-Images

Es werden ausschließlich unveränderte Images der jeweiligen Linux-Distribution verwendet.

Gemeinsamkeiten zwischen verschiedenen Containern werden nicht durch eigene Basis-Images, sondern ausschließlich über Profile beschrieben.

Ein ursprünglich evaluierter Ansatz mittels distrobuilder wurde verworfen, da der Wartungsaufwand den praktischen Nutzen überwog.

[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)

---

## 2.3 Deklarative Konfiguration

Die eigentliche Systembeschreibung befindet sich nicht innerhalb der Container, sondern in den verwendeten Profilen.

Container stellen damit lediglich eine Instanz einer zuvor definierten Konfiguration dar.

Die eigentliche Installations- und Konfigurationslogik ist versionierbar und unabhängig vom Lebenszyklus einzelner Container.

[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)

---

## 2.4 Trennung von technischen und funktionalen Aspekten

Profile werden in verschiedene Kategorien unterteilt.

### 2.4.1 Container

Stellt grundlegende Incus-Funktionalität bereit.

Beispiele:

* Storage
* Netzwerk
* Ressourcenlimits

### 2.4.2 Environment

Beschreibt die Laufzeitumgebung.

Beispiele:

* GUI
* Desktop
* Benutzer

### 2.4.3 Applications

Installiert Anwendungen.

Beispiele:

* Browser
* Office
* Editoren
* Werkzeuge

### 2.4.4 Development

Installiert Entwicklungsumgebungen.

Beispiele:

* Rust
* Python
* Perl
* Git

Dadurch bleiben einzelne Verantwortlichkeiten klar voneinander getrennt.

[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)

---

## 2.5 Persistente Benutzerdaten

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

## 2.5 Minimierung des Hosts

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

# 3. Einrichtung

## 3.1 Voraussetzungen

Benötigt werden mindestens:

* aktuelles Linux-System
* Incus
* funktionsfähige Netzwerk- und Storage-Konfiguration
* Git
* X11 (derzeit Xephyr)

Weitere Anforderungen ergeben sich aus den jeweiligen Profilen.

[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)

---

## 3.2 Grundinstallation

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

## 3.3 Incus Manager

Der Incus Manager ist kein Ersatz für die Incus-CLI oder das Incus Web UI. Er stellt bewusst nur die Funktionen bereit, die im täglichen Betrieb häufig benötigt werden. Administrative Aufgaben wie das Erstellen oder Konfigurieren von Instanzen, Netzwerken oder Storage-Pools verbleiben bei den offiziellen Incus-Werkzeugen.

Start mit:
```bash
$> python3 incus-manager/gui.py
```

[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)

---

# 4. Backup

Das Projekt unterscheidet bewusst zwischen verschiedenen Ebenen eines Backups.

## 4.1 Profile

Alle Incus-Profile werden exportiert und versioniert.

Sie stellen den eigentlichen Konfigurationsstand des Systems dar.

[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)

---

## 4.2 Containerdefinitionen

Für jede Instanz werden die relevanten Informationen gesichert.

Insbesondere:

* verwendetes Image
* verwendete Profile
* zusätzliche Devices
* optionale Instanzparameter

Der flüchtige Laufzeitzustand eines Containers wird bewusst nicht gesichert.

[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)

---

## 4.3 Persistente Benutzerdaten

Alle eingebundenen Host-Verzeichnisse werden unabhängig von Incus gesichert.

Hierzu gehören insbesondere:

* Home-Verzeichnisse
* Konfigurationsdateien
* Entwicklungsprojekte
* Dokumente

[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)

---

# 5. Restore

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

# 6. Technische Limitierungen

Derzeit sind einige Einschränkungen bekannt.

## 6.1 X11

Die GUI-Anbindung erfolgt momentan über Xephyr.

Aufgrund technischer Einschränkungen von Xephyr und Incus wird derzeit die Authentifizierung mittels `xhost` verwendet.

Ein Umstieg auf Xauthority oder alternative Verfahren wird zukünftig erneut evaluiert.

[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)

---

## 6.2 Wayland

Wayland wird derzeit nicht unterstützt.

Der Fokus liegt zunächst auf einer stabilen X11-basierten Lösung.

[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)

---

## 6.3 Plattform

Der Schwerpunkt liegt aktuell auf openSUSE Tumbleweed.

Andere Distributionen wurden bisher nicht getestet.

[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)

---

## 6.4 Reproduzierbarkeit

Der deklarative Teil des Systems ist bereits weitgehend reproduzierbar.

Die vollständige Automatisierung von Backup und Restore befindet sich noch in Planung.

[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)

---

# 7. Projektstatus

Das Projekt befindet sich derzeit in der Evaluierungs- und Entwurfsphase.

Designentscheidungen werden bewusst anhand praktischer Erfahrungen getroffen und können sich bis zum Architektur-Freeze noch ändern.

Erst nach Abschluss dieser Phase wird die Struktur als stabil betrachtet.

[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)

---

# 8. Lizenz

Das Projekt unterliegt der [MIT-Lizenz](LICENSE)

[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)

---

