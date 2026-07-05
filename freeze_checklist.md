# 1. Architektur-Stabilität
  - Incus als alleinige Source of Truth
    - [x] Keine externen Metadaten (user.*, DBs, Registry-Dateien)
    - [x] Alle Containerzustände über Incus Profile definiert
    - [x] Profile vollständig versioniert im Repository
    - [x] Keine parallelen Konfigurationssysteme mehr aktiv
  - Profil-System ist final strukturiert
    - [x] 00-Container_* stabil
    - [x] 01-Container_* stabil
    - [x] 10-Env_* stabil
    - [x] 20-Apps_* stabil
    - [x] 30-Dev_* stabil
    - [x] Keine experimentellen Prefixe mehr aktiv im produktiven Set
  - Klassifikationslogik ist deterministisch
    - [x] Container-Typ wird ausschließlich aus Profilen abgeleitet
    - [x] Keine heuristischen Namen mehr im Code
    - [x] Kein name.contains(...) mehr im Manager
    - [x] Klassifikation ist zentral definiert und unverändert stabil
# 2. Runtime-Stabilität
  - Desktop Launch System
    - [x] Xephyr pro Session stabil funktional
    - [x] Freie DISPLAY-Sockets zuverlässig ermittelt
    - [ ] XAUTH funktioniert ohne -ac
    - [ ] Keine Nutzung von xhost mehr erforderlich (optional Zielzustand)
  - Container Execution Model
    - [x] incus exec als alleiniger App-Startmechanismus
    - [x] GUI-Apps laufen vollständig isoliert
    - [x] Kein Host-Software-Abhängigkeitsmodell mehr
# 3. Container-Struktur
  - Standardisierte Profile-Kombinationen
    - [ ] Desktop-Container sind reproduzierbar aus Profilset
    - [x] App-Container sind eindeutig identifizierbar
    - [x] Dev-Container sind eindeutig identifizierbar
    Beispiel:
      - [x] Firefox → 10-Env_GUI + 11-Users + 20-Apps_Firefox
      - [x] Rust → 10-Env_GUI + 11-Users + 30-Dev_Rust
  - Keine „manuellen Sondercontainer“
    - [x] Kein Container existiert außerhalb des Profilschemas
    - [x] Keine „one-off hacks“
    - [x] Keine adhoc installierten Sonderrollen
# 4. Persistenzmodell
  - [x] `$HOME` Mount-Strategie stabil
  - [x] `~/.config` persistiert bewusst definiert
  - [x] Cache-Strategie bewusst entschieden (persist oder ephemeral)
  - [x] Keine impliziten Host-Abhängigkeiten
# 5. Backup / Restore Reifegrad
  - Exportfähigkeit
    - [x] Alle Profile exportierbar
    - [ ] Container-Konfigurationen exportierbar
    - [ ] Instanzen rekonstruierbar ohne manuelle Entscheidungen
  - Restore-Mechanismus
    - [ ] YAML/JSON Snapshot existiert stabil
    - [ ] Restore erzeugt identisches funktionales System
    - [x] Reihenfolge definiert:
      - Netzwerke/Storage
      - Profile
      - Container
      - Profile-Zuweisung
# 6. GUI-Stabilität
  - [x] GUI ist reine Projektion des Incus-State
  - [x] Keine eigene Persistenz
  - [x] Keine eigene Klassifikation außer Profilmapping
  - [x] Refresh ist idempotent
# 7. Operational Stability Test
System gilt als freeze-ready, wenn:
  - [ ] Ein neuer Container kann in < 5 Minuten vollständig definiert werden
  - [ ] Ein defektes System kann vollständig aus Backup rekonstruiert werden
  - [ ] Ein neuer Typ (z. B. 20-Apps_) kann ohne Codeänderung integriert werden
  - [ ] Ein Container kann 6 Monate ignoriert werden und ist danach ohne Dokumentation verständlich
