# Software Supply Chain Security

To ensure the integrity and safety of the OpenERV project, we have implemented several hardening measures for our CI/CD pipelines.

## 1. Immutable Action Pinning
All GitHub Actions used in our workflows are pinned to specific **commit SHAs** rather than mutable version tags (like `@v6`).
*   **Why**: Tags can be moved by repository maintainers or attackers who gain access to their accounts. By using a cryptographic hash, we guarantee that the code running in our CI environment is exactly what we audited.
*   **Verification**: The SHAs correspond to the following stable releases:
    - `actions/checkout`: v6
    - `actions/upload-artifact`: v7
    - `actions/download-artifact`: v8
    - `softprops/action-gh-release`: v2
    - `carlosperate/arm-none-eabi-gcc-action`: v1 (Upstream standard for ARM GCC)

## 2. Least-Privilege Permissions
Every workflow file now includes an explicit `permissions:` block.
*   **`contents: read`**: Used for analysis workflows (like STL auditing) to ensure the runner cannot modify the repository or push malicious commits.
*   **`contents: write`**: Specifically restricted to the firmware release workflow to allow the creation of GitHub Releases and asset uploads.

## 3. Reputable Components
We only utilize actions from high-reputation, official, or de facto community-standard sources:
- **`actions/*`**: Official GitHub-maintained utilities.
- **`carlosperate/*`**: The industry-standard action for ARM embedded development.
- **`softprops/*`**: The most widely adopted community standard for release management.

## 4. Environment Isolation
Our firmware builds utilize a clean MicroPython environment cloned directly from the official MicroPython repository on every run, ensuring no lingering artifacts from previous builds.
