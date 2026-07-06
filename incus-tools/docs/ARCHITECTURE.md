# ARCHITECTURE

## Ziel

Der **Incus Instance Launcher** ist ein Management- und Orchestrierungswerkzeug für eine deklarative, profilbasierte Incus-Umgebung.

Ziel des Projekts ist **nicht** die Verwaltung beliebiger Incus-Installationen.

Ziel ist die Verwaltung **eines klar definierten Systemmodells**, dessen vollständiger Zustand jederzeit reproduzierbar ist.

Der **Backup & Restore Manager** soll ermöglichen, dass eine Arbeitsumgebung ohne manuelle Nacharbeiten auf einem beliebigen kompatiblen System erneut aufgebaut werden kann.

---

# Architekturprinzipien

## Declarative over Imperative

Das System beschreibt **was existieren soll**, nicht **wie es Schritt für Schritt erzeugt wird**.

Exportierte Spezifikationen beschreiben den Soll-Zustand.

Der Backup & Restore Manager sorgt dafür, dass dieser Soll-Zustand auf einem Zielsystem erreicht wird.

---

## Single Source of Truth

Weder der Incus Instance Launcher noch der Incus Backup & Restore Manager besitzen einen eigenen dauerhaften Zustand.

Alle Informationen befinden sich entweder
* in Incus selbst oder
* in den exportierten Spezifikationen.

Der Backup & Restore Manager erzeugt oder interpretiert ausschließlich diesen Zustand.

---

## No Hidden State

Ein System gilt nur dann als vollständig beschrieben, wenn sämtliche für seine Reproduktion notwendigen Informationen explizit vorhanden sind.

Nicht dokumentierte Annahmen, manuelle Nacharbeiten oder implizite Abhängigkeiten gelten als Architekturfehler.

---

## Profile First

Profile bilden die Grundlage der gesamten Systemarchitektur.

Sie definieren
* Infrastruktur
* Laufzeitumgebung
* installierte Software
* Entwicklungsumgebungen

Profile sind die primäre semantische Steuerungsebene für Container.

---

## Deterministic Behaviour

Identische Eingaben müssen stets identische Ergebnisse erzeugen.

Ein Export eines Systems muss ausreichen, um denselben funktionalen Zustand auf einem anderen Rechner erneut bereitzustellen.

---

## Minimal Host

Der Host stellt die notwendige Infrastruktur für Container-Ausführung und Interaktion bereit.

Dazu gehören insbesondere:
* Netzwerk
* Storage
* optional: GUI-Integration

Anwendungen werden grundsätzlich innerhalb von Containern ausgeführt.

---

# Systemmodell

Das System besteht aus zwei Ebenen.

## Infrastruktur

Diese Objekte existieren unabhängig von Containern.

Beispiele:
* Projekte
* Storage Pools
* Netzwerke
* Profile

---

## Laufzeitobjekte

Diese Objekte repräsentieren konkrete Arbeitsumgebungen.

Beispiele:
* Container
* Virtuelle Maschinen

---

# Profilmodell

Die gesamte Funktionalität wird aus Profilen zusammengesetzt.

Die Profilstruktur folgt festen Präfixen.

```
00-Container_*

01-Container_*

10-Env_*

20-Apps_*

21-Apps_*

22-Apps_*

30-Dev_*
```

Diese Struktur bildet die Grundlage für sämtliche Klassifizierungen.

---

# Containerklassifikation

Container werden ausschließlich anhand ihrer Profile klassifiziert.

Es existieren keine zusätzlichen Typinformationen.

Beispielsweise:
* Desktop
* Application
* Development

werden vollständig aus den Profilen abgeleitet.

---

# Rolle des Incus Instance Launchers

Der Launcher stellt die zentrale Verwaltungsoberfläche der Instanzen dar.

Er bietet ausschließlich grafische Funktionen.

Die eigentliche Logik existiert ausschließlich im Core.

---

# Rolle des Incus Backup & Restore Managers

Der Backup & Restore Manager stellt den zentralen Einstiegspunkt für geskriptete Backups und Wiederherstellungen dar .

Er bietet ausschließlich skriptfähige Funktionen.

Die eigentliche Logik existiert ausschließlich im Core.

---

# Export

Ein Export beschreibt den vollständigen deklarativen Soll-Zustand des Systems.

Er stellt kein Backup von Nutzdaten dar.

Exportiert wird der reproduzierbare Systemzustand, nicht nur Verwaltungsmetadaten.

---

# Import

Import bedeutet nicht automatisch "Restore".

Import bedeutet: 
> Anwendung einer deklarativen Systembeschreibung auf ein Incus-System.

Restore bedeutet:
> Rekonstruktion eines zuvor exportierten Systemzustands.

Ein Import kann sowohl auf einem leeren als auch auf einem bereits bestehenden System ausgeführt werden.

---

# Architekturgrenzen

Weder der Incus Instance Launcher noch der Incus Backup & Restore Manager sind allgemeine Incus-Werkzeuge.

Beide setzen die in diesem Projekt definierte Profilstruktur voraus.

Beide versuchen ausdrücklich nicht, beliebige Incus-Konfigurationen automatisch zu interpretieren.

---

# Entwicklungsprinzipien

Neue Funktionen müssen sich an folgenden Fragen messen lassen:
* Macht diese Änderung das System reproduzierbarer?
* Reduziert sie implizites Wissen?
* Vereinfacht sie das Deployment?
* Vermeidet sie Sonderfälle?
* Lässt sich ihre Funktion vollständig exportieren?

Kann eine dieser Fragen nicht eindeutig mit "Ja" beantwortet werden, sollte die Änderung kritisch hinterfragt werden.

---

# Langfristige Vision

Ziel ist ein deklaratives Arbeitsumgebungssystem auf Basis von Incus, dessen vollständiger Zustand jederzeit reproduzierbar, nachvollziehbar und versionierbar ist.
