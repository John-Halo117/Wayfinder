# ARK Forge to Foundry Normalization

The ARK fold identified Forge-labeled engineering and self-coding material. Wayfinder canonical ownership names this responsibility Foundry.

## Source

- Historical source: `engines/ark/legacy/`
- Canonical owner: `engines/foundry/`
- Compatibility source copy: `engines/foundry/legacy/`

## Compatibility Rule

Legacy executable names such as `forge`, `forge-app`, `forge.cmd`, `forge.ps1`, and `Forge App.*` are preserved as historical compatibility entrypoints. They are not renamed in this phase.

Canonical Foundry entrypoints have been added beside them:

- `foundry`
- `foundry-app`
- `foundry.cmd`
- `foundry.ps1`
- `install-foundry-arch.sh`
- `packaging/linux/foundry-app.desktop.in`
- `packaging/linux/foundry-app.svg`
- `Foundry App.cmd`
- `Foundry App.ps1`
- `Foundry App.sh`

The root Wayfinder launcher exposes these through `wf foundry`, `wf foundry-app`,
and `wf foundry-cli`.

## Copied Files

- `FORGE_START_HERE.md`
- `Forge App.cmd`
- `Forge App.ps1`
- `Forge App.sh`
- `agents/forge_native/__init__.py`
- `agents/forge_native/agent.py`
- `ark-core/forge/__init__.py`
- `ark-core/forge/ci/__init__.py`
- `ark-core/forge/ci/loc.py`
- `ark-core/forge/context/build.py`
- `ark-core/forge/context/provider.py`
- `ark-core/forge/control/controller.py`
- `ark-core/forge/control/decay.py`
- `ark-core/forge/control/phi.py`
- `ark-core/forge/core/loop.py`
- `ark-core/forge/core/orchestrator.py`
- `ark-core/forge/exec/git.py`
- `ark-core/forge/exec/runner.py`
- `ark-core/forge/exec/sandbox.py`
- `ark-core/forge/math_utils.py`
- `ark-core/forge/mcp/__init__.py`
- `ark-core/forge/mcp/contracts.py`
- `ark-core/forge/mcp/policy.py`
- `ark-core/forge/mcp/registry.py`
- `ark-core/forge/mcp/tools.py`
- `ark-core/forge/memory/ban.py`
- `ark-core/forge/memory/store.py`
- `ark-core/forge/models/discovery.py`
- `ark-core/forge/models/ollama_client.py`
- `ark-core/forge/models/prompts.py`
- `ark-core/forge/runtime/artifacts.py`
- `ark-core/forge/runtime/bootstrap.py`
- `ark-core/forge/runtime/capabilities.py`
- `ark-core/forge/runtime/config.py`
- `ark-core/forge/runtime/guards.py`
- `ark-core/forge/runtime/logs.py`
- `ark-core/forge/transform/apply.py`
- `ark-core/forge/transform/propose.py`
- `ark-core/forge/types.py`
- `ark-core/forge/ui/app.py`
- `ark-core/forge/ui/browser.py`
- `ark-core/forge/ui/common.py`
- `ark-core/forge/ui/controller.py`
- `ark-core/forge/ui/launcher.py`
- `ark-core/forge/ui/session.py`
- `ark-core/forge/verify/adapters.py`
- `ark-core/forge/verify/eval.py`
- `ark-core/forge/verify/redteam.py`
- `ark-core/forge/verify/synth.py`
- `ark-core/scripts/ai/codex_prompt.txt`
- `ark-core/scripts/ai/forge.py`
- `ark-core/scripts/ai/orchestrator.py`
- `ark/forge_planner.py`
- `forge`
- `forge-app`
- `forge.cmd`
- `forge.ps1`
- `install-forge-arch.sh`
- `scripts/ai/apply_proposal.sh`
- `scripts/ai/assembly_line.py`
- `scripts/ai/autonomous_repair.py`
- `scripts/ai/enqueue_repair_last_failure.sh`
- `scripts/ai/enqueue_task.sh`
- `scripts/ai/forge.py`
- `scripts/ai/local_codegen_loop.py`

## Canonical Foundry App Files

- `Foundry App.cmd`
- `Foundry App.ps1`
- `Foundry App.sh`
- `foundry`
- `foundry-app`
- `foundry.cmd`
- `foundry.ps1`

## Missing Files

None.
