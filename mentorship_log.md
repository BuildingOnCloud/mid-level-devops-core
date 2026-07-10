# DevOps Mentorship Log

## 📦 Phase 1: Containerization Milestone

### Technical Hurdles & Resolutions

#### 1. Homebrew Binary Conflicts (`/usr/local/bin/`)
* **Problem:** `brew install --cask docker` repeatedly failed due to pre-existing, unmanaged binaries like `kubectl.docker` and credential helpers blocking the script paths.
* **Resolution:** Triage paths manually by forcing an explicit cleanup using `sudo rm` to let Homebrew cleanly take ownership of symlinks.

#### 2. Python PEP 668 Host Environment Restrictions
* **Problem:** Attempting to install requirements via `pip` globally triggered an `externally-managed-environment` error.
* **Resolution:** Implemented host environment isolation by instantiating a local Python virtual environment (`python3 -m venv .venv`), mapping our IDE LSP configs locally, and shifting runtime compilation entirely to an isolated Docker multi-stage environment.

### Architectural Patterns Applied
* **Multi-stage Isolation:** Reduced the footprint of the container from over 500MB down to **163MB** by stripping out pip caches and build tools.
* **Process Signal Handling:** Wired `tini` as `PID 1` alongside custom Python OS hooks to cleanly intercept `SIGTERM` events, allowing a 3-second application traffic drain window to guarantee zero-downtime rolling updates.
