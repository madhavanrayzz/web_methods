# hunt-cookie-dos

OpenCode skill for bounded, authorized assessment of cookie-related denial-of-service risks.

## Install globally
Copy the `hunt-cookie-dos` folder to `~/.config/opencode/skills/hunt-cookie-dos/`.
On Windows, the home path is typically `%USERPROFILE%\\.config\\opencode\\skills\\hunt-cookie-dos\\`.

## Install for one project
Copy the folder to `<project>/.opencode/skills/hunt-cookie-dos/`.

## Contents
- `SKILL.md` — workflow and safety/validation rules
- `references/test-matrix.md` — bounded test matrix and stop conditions
- `templates/finding-report.md` — report template
- `scripts/init-finding.sh` — creates an output folder scaffold only; it does not test targets

Restart/reload OpenCode if the skill is not discovered. The skill ID is `hunt-cookie-dos`.

The skill is designed to establish evidence safely, not to take an application offline. A single 400/431 response is not enough to claim a DoS.
