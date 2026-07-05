Type | Version/Name
--- | ---
Distribution Name	| OpenSuSE Leap
Distribution Version	| 16.0
Kernel Version	| 6.12.0-160000.35-default
Architecture	| x86\_64
Incus Version	| 6.23
Xephyr Version | 21.1.15
Created | 2026-07-01
Updated | 2026-07-05


# Incus Desktop & Development Environment

# Table of Contents
* [1. Objective](#1-objective)
* [2. Design and Architecture Decisions](#2-design-and-architecture-decisions)
  * [2.1 Profiles as Configuration Building Blocks](#21-profiles-as-configuration-building-blocks)
  * [2.2 Use of Official Distribution Images](#22-use-of-official-distribution-images)
  * [2.3 Declarative Configuration](#23-declarative-configuration)
  * [2.4 Separation of Technical and Functional Aspects](#24-separation-of-technical-and-functional-aspects)
    * [2.4.1 Container](#241-container)
    * [2.4.2 Environment](#242-environment)
    * [2.4.3 Applications](#243-applications)
    * [2.4.4 Development](#244-development)
  * [2.5 Persistent User Data](#25-persistent-user-data)
  * [2.6 Host Minimization](#26-host-minimization)
* [3. Setup](#3-setup)
  * [3.1 Prerequisites](#31-prerequisites)
  * [3.2 Initial Setup](#32-initial-setup)
  * [3.3 Incus Manager](#33-incus-manager)
* [4. Backup](#4-backup)
  * [4.1 Profiles](#41-profiles)
  * [4.2 Container Definitions](#42-container-definitions)
  * [4.3 Persistent User Data](#43-persistent-user-data)
* [5. Restore](#5-restore)
* [6. Technical Limitations](#6-technical-limitations)
  * [6.1 X11](#61-x11)
  * [6.2 Wayland](#62-wayland)
  * [6.3 Platform](#63-platform)
  * [6.4 Reproducibility](#64-reproducibility)
* [7. Project Status](#7-project-status)
* [8. License](#8-license)

# 1. Objective

This project aims to provide a fully containerized work environment based on Incus.

All applications—browsers, development environments, desktop environments, and other tools—run in isolated containers. The host serves solely as a minimal runtime environment, providing the necessary resources (kernel, graphics, audio, network, and storage).

The architecture pursues several goals:

*   Separation of host and application environments
*   Minimization of dependencies on the host
*   Reproducibility of the entire system
*   Easy migration to other systems
*   Ability to update or replace applications independently of one another
*   Comprehensive system description as code ("Infrastructure as Code")

The long-term goal is to be able to recreate a complete workstation from version control at any time.

[↑ Back to Table of Contents](#table-of-contents)

---

# 2. Design and Architecture Decisions

## 2.1 Profiles as Configuration Building Blocks

Instead of providing large, monolithic container images, the system is assembled from small, clearly defined Incus profiles.

Each profile describes exactly one technical or functional aspect of a container.

Examples:

*   Storage
*   Network
*   Resource limits
*   Users
*   GUI integration
*   Development environments
*   Individual applications

This results in small, reusable building blocks that can be combined to create any desired container configuration.

[↑ Back to Table of Contents](#table-of-contents)

---

## 2.2 Use of Official Distribution Images

Only unmodified images from the respective Linux distributions are used.

Commonalities between different containers are defined exclusively through profiles, rather than through custom base images.

An initial approach using `distrobuilder` was discarded because the maintenance effort outweighed the practical benefits.

[↑ Back to Table of Contents](#table-of-contents)

---

## 2.3 Declarative Configuration

The actual system description resides not within the containers themselves, but in the profiles being used.

Containers thus merely represent an instance of a previously defined configuration.

The actual installation and configuration logic is version-controllable and independent of the lifecycle of individual containers.

[↑ Back to Table of Contents](#table-of-contents)

---

## 2.4 Separation of Technical and Functional Aspects

Profiles are categorized into different groups.

### 2.4.1 Container

Provides basic Incus functionality.

Examples:

* Storage
* Network
* Resource limits

### 2.4.2 Environment

Describes the runtime environment.

Examples:

* GUI
* Desktop
* Users

### 2.4.3 Applications

Installs applications.

Examples:

* Browsers
* Office suites
* Editors
* Tools

### 2.4.4 Development

Installs development environments.

Examples:

* Rust
* Python
* Perl
* Git

This ensures that individual responsibilities remain clearly separated.

[↑ Back to Table of Contents](#table-of-contents)

---

## 2.5 Persistent User Data

Containers remain fundamentally interchangeable.

Persistent data is mounted from the host.

This includes, for example:

* Home directory
* Configuration files
* Cache
* Git configuration
* Shell configuration

Consequently, rebuilding a container does not result in the loss of personal data.

[↑ Back to Table of Contents](#table-of-contents)

---

## 2.6 Host Minimization

The host contains as little software as possible.

Applications are generally run inside containers.

The host handles only:

* Incus
* X11/Xephyr
* Audio forwarding
* Networking
* Storage
* Startup scripts

[↑ Back to Table of Contents](#table-of-contents)

---

# 3. Setup

## 3.1 Prerequisites

At a minimum, the following are required:

* A current Linux system
* Incus
* Functional network and storage configuration
* Git
* X11 (currently Xephyr)

Additional requirements depend on the specific profiles used.

[↑ Back to Table of Contents](#table-of-contents)

---

## 3.2 Initial Setup                                                                                                                                                                                              

The setup process involves several steps.

1. Initialize Incus
2. Create storage pool
3. Configure network
4. Import profiles
5. Download images
6. Create containers
7. Create persistent directories
8. Install desktop startup scripts

The actual configuration is handled exclusively via the YAML files included in the repository.

[↑ Back to Table of Contents](#table-of-contents)

---

## 3.3 Incus Manager

Incus Manager is not a substitute for the Incus CLI or the Incus Web UI. It deliberately provides only those functions frequently required for daily operations. Administrative tasks—such as creating or configuring instances, networks, or storage pools—remain the domain of the official Incus tools.

Start with:
```bash
$> python3 incus-manager/gui.py
```

[↑ Back to Table of Contents](#table-of-contents)

---


# 4. Backup

The project deliberately distinguishes between different levels of backups.

## 4.1 Profiles

All Incus profiles are exported and version-controlled.

They represent the system's actual configuration state.

[↑ Back to Table of Contents](#table-of-contents)

---

## 4.2 Container Definitions

Relevant information is backed up for each instance.

Specifically:

* Image used
* Profiles used
* Additional devices
* Optional instance parameters

The volatile runtime state of a container is deliberately not backed up.

[↑ Back to Table of Contents](#table-of-contents)

---

## 4.3 Persistent User Data

All mounted host directories are backed up independently of Incus.

This includes, in particular:

* Home directories
* Configuration files
* Development projects
* Documents

[↑ Back to Table of Contents](#table-of-contents)

---

# 5. Restore

The restoration process is carried out in stages.

1. Restore storage
2. Restore network
3. Import profiles
4. Deploy images
5. Import container definitions
6. Create containers
7. Mount persistent data

A tool to fully automate this process is planned for the future.

[↑ Back to Table of Contents](#table-of-contents)

---

# 6. Technical Limitations

There are currently some known limitations.

## 6.1 X11

GUI integration is currently handled via Xephyr.

Due to technical limitations inherent to Xephyr and Incus, authentication currently relies on `xhost`.

A switch to Xauthority or alternative methods will be re-evaluated in the future.

[↑ Back to Table of Contents](#table-of-contents)

---

## 6.2 Wayland

Wayland is not currently supported.

The initial focus is on a stable X11-based solution.

[↑ Back to Table of Contents](#table-of-contents)

---

## 6.3 Platform

The current focus is on openSUSE Tumbleweed.

Other distributions have not yet been tested.

[↑ Back to Table of Contents](#table-of-contents)

---

## 6.4 Reproducibility

The declarative part of the system is already largely reproducible.

Full automation of backup and restore processes is currently in the planning stage.

[↑ Back to Table of Contents](#table-of-contents)

---

# 7. Project Status

The project is currently in the evaluation and design phase.

Design decisions are deliberately based on practical experience and remain subject to change until the architecture freeze.

The structure will only be considered stable once this phase is complete.

[↑ Back to Table of Contents](#table-of-contents)

---

# 8. License

The project is licensed under the [MIT License](LICENSE).

[↑ Back to Table of Contents](#table-of-contents)

---
