# SYSTEM SPEC – Incus Desktop Environment

# Inhaltverzeichnis
- [1.Zielsetzung](#1-zielsetzung)
- [2. Architekturprinzipien](#2-architekturprinzipien)
- [3. Profilmodell](#3-profilmodell)
  - [3.1 Technische Basisprofile (Infrastruktur)](#31-technische-basismodelle-infrastrutkrur)
  - [3.2 Environment Profile](#32-environment-profile)
  - [3.3 Applikationsprofile](#33-applikationsprofile)
  - [3.4 Entwicklungsprofile](#34-entwicklungsprofile)
- [4. Container-Typisierung (abgeleitet)](#4-container-typisierung-abgeleitet)
- [5. GUI-Modell](#5-gui---modell)
- [6. Startmodell (Runtime)](#6-startmodell-runtime)
  -  [6.1 Desktop Sessions](#61-desktop-sessions)
  -  [6.2 App-Start](#62-app---start)
-  [7. Persistenzmodell](#7-presistenzmodell)
-  [8. Backup-Konzept](#8-backup---konzept)
  -  [8.1 Declarative Layer](#81-declarative-layer)
  -  [8.2 Instance Layer](#82-instance-layer)
-  [9. Restore-Konzept](#9-restore---konzept)
-  [10. Nicht-Ziele](#10-nicht---ziele)
-  [11. Designentscheidung: Profile als Source of Truth](#11-designentscheidung-profile-als-source-of-truth)
-  [12. Stabilitätsziel](#12-stabilitätsziel)
-  [13. Langfristige Vision](#13-langfristige-vision)

# 1. Zielsetzung

Dieses System implementiert eine vollständig containerisierte Desktop- und Entwicklungsumgebung auf Basis von Incus.

Ziele:

- Isolation von Anwendungen, Entwicklungsumgebungen und Desktop-Sessions
- Minimierung der Host-Abhängigkeiten
- Reproduzierbarkeit der gesamten Arbeitsumgebung
- Schnell rekonstruierbare Systemzustände (Disaster Recovery)
- Flexible Kombination von Anwendungen über deklarative Profile

Der Host dient ausschließlich als:
- Incus Runtime
- Display/Session-Launcher
- Orchestrationsschicht


[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)

---

# 2. Architekturprinzipien

- Incus ist **Source of Truth** für alle Runtime-Definitionen
- Containerzustände werden über **Profile zusammengesetzt**
- Keine zusätzliche Metadaten-Schicht außerhalb von Incus (`user.*` wird nicht verwendet)
- Systemzustand ist **deklarativ über Profile beschrieben**
- GUI-Komponenten sind reine Orchestrations-Clients
- Klassifikation erfolgt ausschließlich aus Profilen (kein externes Labeling)


[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)

---

# 3. Profilmodell

## 3.1 Technische Basisprofile (Infrastruktur)

Diese Profile definieren die technische Laufzeitumgebung eines Containers:

- `00-Container_Storage` → Storage Pool & Root Disk
- `01-Container_Network` → Netzwerkzugriff (bridge, routing)
- `01-Container_ResLimits` → CPU / RAM / IO Limits
- `11-Users` → Benutzer- und Home-Verzeichnis Mapping

Diese Profile definieren **keine Anwendung oder Rolle**.

---

## 3.2 Environment Profile

Definieren die Art der Laufzeitumgebung:

- `10-Env_GUI` → GUI Forwarding (X11, PulseAudio, DBus)
- `10-Env_Desktop` → vollständige Desktop-Session (Fluxbox / KDE)

---

## 3.3 Applikationsprofile

Definieren installierte Anwendungen:

- `20-Apps_<name>` → internetfähige Anwendungen
  - Firefox, Chromium, Opera, yt-dlp, etc.

- `21-Apps_<name>` → produktive Offline-Tools
  - LibreOffice, Editoren, etc.

- `22-Apps_<name>` → nicht-produktive Anwendungen (Games etc.)

---

## 3.4 Entwicklungsprofile

- `30-Dev_<lang>` → Entwicklungsumgebungen
  - Rust, Python, Perl, Git Tooling etc.

[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)

---

# 4. Container-Typisierung (abgeleitet)

Container werden **nicht gespeichert klassifiziert**, sondern zur Laufzeit abgeleitet:

| Typ          | Regel |
|--------------|------|
| desktop      | enthält `10-Env_Desktop` |
| app          | enthält `20-Apps_*` |
| development  | enthält `30-Dev_*` |
| unknown      | kein bekanntes Profil |

Diese Klassifikation wird ausschließlich aus Profilnamen abgeleitet.


[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)

---

# 5. GUI-Modell

Der Desktop-Manager ist eine reine Orchestrierungsschicht:

- liest Containerliste aus Incus
- klassifiziert Container über Profile
- zeigt Status + Typ
- steuert Start / Stop / Exec

Keine Persistenz außerhalb von Incus.


[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)

---

# 6. Startmodell (Runtime)

## Desktop Sessions

- Xephyr wird pro Session mit freiem Display gestartet
- jede Session nutzt eigenes:
  - DISPLAY
  - XAUTHORITY
- parallele Desktop-Sessions sind erlaubt

## App-Start

- Apps werden via:
```bash
incus exec <container> -- <command>
```
gestartet
- keine direkte GUI-Installation auf Host notwendig


[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)

---

# 7. Persistenzmodell

- `/home/ralf` wird selektiv in Container gemountet
- Konfigurationspersistenz erfolgt über:
  - `~/.config`
  - `~/.local`
- Cache kann optional ephemeral sein


[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)

---

# 8. Backup-Konzept

Backups bestehen aus zwei Ebenen:

## 8.1 Declarative Layer

- Profile Definitionen
- Netzwerk / Storage Konfiguration

## 8.2 Instance Layer

- Container-Konfigurationen
- zugewiesene Profile
- Devices

Ziel ist kein Image-Backup, sondern:

> Reconstructable system state from declarative input


[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)

---

# 9. Restore-Konzept

Restore erfolgt in Reihenfolge:

1. Storage Pools & Networks
2. Profile Definitionen
3. Container-Instanzen
4. Profile-Zuweisungen
5. Startzustände

Optional:
- Recreate CLI commands aus YAML/JSON Snapshot


[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)

---

# 10. Nicht-Ziele

- kein Docker-kompatibles System
- keine VM-Replikation
- keine vollständige Desktop-Imaging-Lösung
- keine zentrale Orchestrierung (Kubernetes etc.)
- keine versteckten Metadaten außerhalb Incus


[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)

---

# 11. Designentscheidung: Profile als Source of Truth

Profile ersetzen:

- Tags
- Labels
- externe Metadaten
- Application Registry

Sie sind das einzige System zur:
- Strukturierung
- Klassifikation
- Zusammensetzung von Container-Rollen


[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)

---

# 12. Stabilitätsziel

Das System gilt als stabil, wenn:

- neue Container ohne Nachdenken erzeugt werden können
- Profilkombinationen intuitiv sind
- keine externe Dokumentation zur Nutzung nötig ist
- Restore ohne manuelle Entscheidungen möglich ist


[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)

---

## 13. Langfristige Vision

Das System entwickelt sich zu einer:

> reproduzierbaren, modularen Desktop- und Dev-Plattform auf Incus-Basis

mit minimalem Host und maximal deklarativer Kontrolle.


[↑ Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)

---
