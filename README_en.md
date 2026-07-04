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

# Table of Contents
* [Objective](#objective)
* [Design and Architecture Decisions](#design-and-architecture-decisions)
  * [Profiles as Configuration Building Blocks](#profiles-as-configuration-building-blocks)
  * [Use of Official Distribution Images](#use-of-official-distribution-images)
  * [Declarative Configuration](#declarative-configuration)
  * [Separation of Technical and Functional Aspects](#separation-of-technical-and-functional-aspects)
    * [Container](#container)
    * [Environment](#environment)
    * [Applications](#applications)
    * [Development](#development)
  * [Persistent User Data](#persistent-user-data)
  * [Host Minimization](#host-minimization)
* [Setup](#setup)
  * [Prerequisites](#prerequisites)
  * [Initial Setup](#initial-setup)
* [Backup](#backup)
  * [Profiles](#profiles)
  * [Container Definitions](#container-definitions)
  * [Persistent User Data](#persistent-user-data)
* [Restore](#restore)
* [Technical Limitations](#technical-limitations)
  * [X11](#x11)
  * [Wayland](#wayland)
  * [Platform](#platform)
  * [Reproducibility](#reproducibility)
* [Project Status](#project-status)
* [License](#license)

## Objective

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

# Design and Architecture Decisions

## Profiles as Configuration Building Blocks

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

## Use of Official Distribution Images

Only unmodified images from the respective Linux distributions are used.

Commonalities between different containers are defined exclusively through profiles, rather than through custom base images.

An initial approach using `distrobuilder` was discarded because the maintenance effort outweighed the practical benefits.

[↑ Back to Table of Contents](#table-of-contents)

---

## Declarative Configuration

The actual system description resides not within the containers themselves, but in the profiles being used.

Containers thus merely represent an instance of a previously defined configuration.

The actual installation and configuration logic is version-controllable and independent of the lifecycle of individual containers.

[↑ Back to Table of Contents](#table-of-contents)

---

## Separation of Technical and Functional Aspects

Profiles are categorized into different groups.

### Container

Provides basic Incus functionality.

Examples:

* Storage
* Network
* Resource limits

### Environment

Describes the runtime environment.

Examples:

* GUI
* Desktop
* Users

### Applications

Installs applications.

Examples:

* Browsers
* Office suites
* Editors
* Tools

### Development

Installs development environments.

Examples:

* Rust
* Python
* Perl
* Git

This ensures that individual responsibilities remain clearly separated.

[↑ Back to Table of Contents](#table-of-contents)

---

## Persistent User Data

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

## Host Minimization

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

# Setup

## Prerequisites

At a minimum, the following are required:

* A current Linux system
* Incus
* Functional network and storage configuration
* Git
* X11 (currently Xephyr)

Additional requirements depend on the specific profiles used.

[↑ Back to Table of Contents](#table-of-contents)

---

## Initial Setup                                                                                                                                                                                                     08:13:20 [82/1850]

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

# Backup

The project deliberately distinguishes between different levels of backups.

## Profiles

All Incus profiles are exported and version-controlled.

They represent the system's actual configuration state.

[↑ Back to Table of Contents](#table-of-contents)

---

## Container Definitions

Relevant information is backed up for each instance.

Specifically:

* Image used
* Profiles used
* Additional devices
* Optional instance parameters

The volatile runtime state of a container is deliberately not backed up.

[↑ Back to Table of Contents](#table-of-contents)

---

## Persistent User Data

All mounted host directories are backed up independently of Incus.

This includes, in particular:

* Home directories
* Configuration files
* Development projects
* Documents

[↑ Back to Table of Contents](#table-of-contents)

---

# Restore

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

# Technical Limitations

There are currently some known limitations.

## X11

GUI integration is currently handled via Xephyr.

Due to technical limitations inherent to Xephyr and Incus, authentication currently relies on `xhost`.

A switch to Xauthority or alternative methods will be re-evaluated in the future.

[↑ Back to Table of Contents](#table-of-contents)

---

## Wayland

Wayland is not currently supported.

The initial focus is on a stable X11-based solution.

[↑ Back to Table of Contents](#table-of-contents)

---

## Platform

The current focus is on openSUSE Tumbleweed.

Other distributions have not yet been tested.

[↑ Back to Table of Contents](#table-of-contents)

---

## Reproducibility

The declarative part of the system is already largely reproducible.

Full automation of backup and restore processes is currently in the planning stage.

[↑ Back to Table of Contents](#table-of-contents)

---

# Project Status

The project is currently in the evaluation and design phase.

Design decisions are deliberately based on practical experience and remain subject to change until the architecture freeze.

The structure will only be considered stable once this phase is complete.

[↑ Back to Table of Contents](#table-of-contents)

---

# License

No license has been determined yet.

[↑ Back to Table of Contents](#table-of-contents)

---
