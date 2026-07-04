# Table of Contents

- [1. Objective](#1-objective)
- [2. Architectural Principles](#2-architectural-principles)
- [3. Profiles Model](#3-profiles-model)
  - [3.1 Technical Base Profiles (Infrastructure)](#31-technical-base-profiles-infrastructure)
  - [3.2 Environment Profiles](#32-environment-profiles)
  - [3.3 Application Profiles](#33-application-profiles)
  - [3.4 Development Profiles](#34-development-profiles)
- [4. Container Classification (Derived)](#4-container-classification-derived)
- [5. GUI Model](#5-gui-model)
- [6. Startup Model (Runtime)](#6-startup-model-runtime)
  - [6.1 Desktop Sessions](#61-desktop-sessions)
  - [6.2 App Launch](#62-app-launch)
- [7. Persistence Model](#7-persistence-model)
- [8. Backup Concept](#8-backup-concept)
  - [8.1 Declarative Layer](#81-declarative-layer)
  - [8.2 Instance Layer](#82-instance-layer)
- [9. Restore Concept](#9-restore-concept)
- [10. Non-Goals](#10-non-goals)
- [11. Design Decision: Profiles as the Source of Truth](#11-design-decision-profiles-as-the-source-of-truth)
- [12. Stability Goal](#12-stability-goal)
- [13. Long-Term Vision](#13-long-term-vision)

# 1. Objective

This system implements a fully containerized desktop and development environment based on Incus.

Objectives:

- Isolation of applications, development environments, and desktop sessions
- Minimization of host dependencies
- Reproducibility of the entire working environment
- Rapidly reconstructible system states (disaster recovery)
- Flexible combination of applications via declarative profiles

The host serves exclusively as:

- Incus runtime
- Display/session launcher
- Orchestration layer

[↑ Back to Table of Contents](#table-of-contents)

---

# 2. Architectural Principles

- Incus is the **source of truth** for all runtime definitions
- Container states are **assembled via profiles**
- No additional metadata layer outside of Incus (`user.*` is not used)
- System state is **described declaratively via profiles**
- GUI components are pure orchestration clients
- Classification is derived exclusively from profiles (no external labeling)

[↑ Back to Table of Contents](#table-of-contents)

---

# 3. Profiles Model

## 3.1 Technical Base Profiles (Infrastructure)

These profiles define the technical runtime environment of a container:

- `00-Container_Storage` → Storage pool & root disk
- `01-Container_Network` → Network access (bridge, routing)
- `01-Container_ResLimits` → CPU / RAM / IO limits
- `11-Users` → User and home directory mapping

These profiles **do not define an application or role**. ---

## 3.2 Environment Profiles

Define the type of runtime environment:

- `10-Env_GUI` → GUI forwarding (X11, PulseAudio, DBus)
- `10-Env_Desktop` → Full desktop session (Fluxbox / KDE)

---

## 3.3 Application Profiless

Define installed applications:

- `20-Apps_<name>` → Internet-enabled applications
- Firefox, Chromium, Opera, yt-dlp, etc.

- `21-Apps_<name>` → Productivity/offline tools
- LibreOffice, editors, etc.

- `22-Apps_<name>` → Non-productivity applications (games, etc.)

---

## 3.4 Development Profiles

- `30-Dev_<lang>` → Development environments
- Rust, Python, Perl, Git tooling, etc.

[↑ Back to Table of Contents](#table-of-contents)

---

# 4. Container Classification (Derived)

Containers are **not classified via stored metadata**, but rather derived at runtime:

| Type         | Rule |
|--------------|------|
| desktop      | contains `10-Env_Desktop` |
| app          | contains `20-Apps_*` |
| development  | contains `30-Dev_*` |
| unknown      | no known profile |

This classification is derived exclusively from profile names.

[↑ Back to Table of Contents](#table-of-contents)

---

# 5. GUI Model

The desktop manager acts purely as an orchestration layer:

- reads the container list from Incus
- classifies containers based on profiles
- displays status and type
- controls start / stop / exec operations

No persistence outside of Incus.

[↑ Back to Table of Contents](#table-of-contents)

---

# 6. Startup Model (Runtime)

## 6.1 Desktop Sessions

- Xephyr is launched per session using an available display
- Each session uses its own:
- DISPLAY
- XAUTHORITY
- Parallel desktop sessions are permitted

## 6.2 App Launch

- Apps are launched via:
```bash
incus exec <container> -- <command>
```
- No direct GUI installation required on the host


[↑ Back to Table of Contents](#table-of-contents)

---

# 7. Persistence Model

- `/home/ralf` is selectively mounted into the container
- Configuration persistence is handled via:
- `~/.config`
- `~/.local`
- Cache can optionally be ephemeral


[↑ Back to Table of Contents](#table-of-contents)

---

# 8. Backup Concept

Backups consist of two layers:

## 8.1 Declarative Layer

- Profile definitions
- Network / storage configuration

## 8.2 Instance Layer

- Container configurations
- Assigned profiles
- Devices

The goal is not an image backup, but rather:

> Reconstructable system state from declarative input


[↑ Back to Table of Contents](#table-of-contents)

---

# 9. Restore Concept

Restoration proceeds in this order:

1. Storage Pools & Networks
2. Profile Definitions
3. Container Instances
4. Profile Assignments
5. Startup States

Optional:
- Recreate CLI commands from YAML/JSON snapshot

[↑ Back to Table of Contents](#table-of-contents)

---

# 10. Non-Goals

- Not a Docker-compatible system
- No VM replication
- Not a full desktop imaging solution
- No central orchestration (Kubernetes, etc.)
- No hidden metadata outside of Incus

[↑ Back to Table of Contents](#table-of-contents)

---

# 11. Design Decision: Profiles as the Source of Truth

Profiles replace:

- Tags
- Labels
- External metadata
- Application registry

They serve as the sole system for:
- Structuring
- Classification
- Composition of container roles

[↑ Back to Table of Contents](#table-of-contents)

---

# 12. Stability Goal

The system is considered stable when:

- new containers can be created without any thought
- profile combinations are intuitive
- no external documentation is required for use
- restore is possible without manual decisions

[↑ Back to Table of Contents](#tableofcontents)

---

## 13. Long-Term Vision

The system is evolving into a:

> reproducible, modular desktop and development platform based on Incus

with minimal host and maximum declarative control.

[↑ Back to Table of Contents](#tableofcontents)

---
