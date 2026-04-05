# AGENTS.md - GitHub Actions Engineering Standards

This document defines the foundational mandates and expert workflows for managing GitHub Actions within this repository. Adhere to these standards to ensure high-performance, secure, and maintainable CI/CD pipelines.

## 1. Runtime & Security Mandates
- **Node.js 24 Transition:** All JavaScript actions MUST use versions compatible with the Node.js 24 runtime (Standard for 2026).
    - Prefer `actions/checkout@v6`, `actions/upload-artifact@v7`, and `actions/download-artifact@v8`.
    - Avoid `node20` based actions to prevent deprecation failures and security warnings.
- **Credential Isolation:** Use the `actions/checkout@v6` pattern of persisting credentials in `$RUNNER_TEMP` rather than `.git/config` to prevent accidental credential leakage in containerized steps.
- **Permission Scoping:** Always define explicit `permissions:` blocks (e.g., `contents: read` or `contents: write`) at the job or workflow level to follow the principle of least privilege.

## 2. Performance & Caching Strategy
- **Multi-Stage Caching (Prepare-Build Pattern):** For complex builds (e.g., MicroPython, C++ toolchains), separate the environment preparation from the actual artifact compilation.
    - **Prepare Job:** Performs heavy lifting (cloning submodules, building compilers) and saves to `actions/cache@v5`.
    - **Build Jobs:** Use `actions/cache/restore@v5` with `fail-on-cache-miss: true` to ensure a consistent, pre-validated environment across parallel matrix runs.
- **Dependency Caching:**
    - For Python, use `actions/setup-python@v5` with `cache: 'pip'`.
    - For multi-job sharing, standardize cache keys (e.g., `${{ runner.os }}-submodules-${{ env.VERSION }}`) to avoid hashing discrepancies between different job contexts.
- **Path Filtering:** Use `dorny/paths-filter@v4` to prevent unnecessary builds. If a change only affects documentation, firmware jobs should be skipped automatically.

## 3. Workflow Architecture
- **Matrix Builds:** Utilize `strategy: matrix` for parallelizing builds across different hardware models (e.g., `tw4`, `wm12`) or environments.
- **Dynamic Branch Triggers:** Use `branches: [ "**" ]` combined with `workflow_dispatch` to allow testing of any feature branch without hardcoding branch names into the YAML.
- **Artifact Management:**
    - Use `actions/upload-artifact@v7` with `archive: false` for reports or logs intended for direct browser viewing.
    - Standardize artifact naming (e.g., `OpenERV_${{ matrix.model }}_Firmware`) to facilitate reliable downloading in the `release` stage.

## 4. Validation Workflow
- **Surgical Verification:** After modifying a workflow, verify it triggers on the target branch immediately.
- **Log Auditing:** If a job fails with `exit code 128` (Git), verify `fetch-depth` and submodule initialization logic. MicroPython specifically requires `submodules: 'true'` in `actions/checkout`.
- **Artifact Integrity:** Always verify that the produced `.uf2`, `.bin`, or `.csv` files exist and are named according to project conventions before considering a workflow change successful.
