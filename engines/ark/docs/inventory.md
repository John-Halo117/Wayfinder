# ARK Inventory and Classification
Source: `/mnt/c/Users/trevl/OneDrive/Desktop/Home_Sys/Jarvis/ARK/ark`
Folded legacy destination: `engines/ark/legacy/`

## ARK Check
- Loop bounds defined? yes - inventory generation is bounded to Git-listed files.
- Resource caps defined? yes - source copy excludes generated caches and Git internals.
- State localized? yes - ARK remains preserved under `engines/ark/legacy/`.
- Interfaces strict? yes - classification uses explicit path rules and proposed owners.
- Failure paths explicit? yes - unresolved items remain classified as legacy source pending review.

## Summary by Classification

| Classification | Count |
| --- | ---: |
| ARK core/egress runtime | 10 |
| ARK ephemeral | 8 |
| ARK ingress | 8 |
| ARK legacy implementation | 38 |
| ARK proofs/promotion | 1 |
| ARK reality model | 3 |
| Capability/service: measurement | 8 |
| Constitutional/architecture documentation | 14 |
| Contract | 12 |
| Contract/definition | 4 |
| Developer/CI tooling | 9 |
| Developer/operations tooling | 17 |
| Engine documentation | 30 |
| Engine legacy source | 23 |
| Engine: MIDAS | 2 |
| Engine: NetWatch | 3 |
| Engine: VALOR | 2 |
| Engine: stability kernel | 3 |
| External integration | 1 |
| External integration ingress | 3 |
| External integration service boundary | 6 |
| Foundry engine/application | 54 |
| Foundry tooling | 7 |
| Ingress configuration contract | 1 |
| Internal application/agent | 6 |
| Operations | 35 |
| Operations documentation | 15 |
| Operations secret template/config | 1 |
| Policy service input | 11 |
| Service: configuration | 9 |
| Service: cryptography/compression | 10 |
| Service: discovery/registry | 2 |
| Service: event bus/transport | 7 |
| Service: identity | 2 |
| Service: policy | 4 |
| Service: runtime | 5 |
| Service: scheduling/resource control | 3 |
| Service: storage/persistence | 5 |
| Service: telemetry/logging | 1 |
| Tests | 46 |

## Complete File Classification

| Existing File | State | Kind | Classification | Proposed Destination | Rationale |
| --- | --- | --- | --- | --- | --- |
| `.cursorrules` | tracked | Tool/config file | Developer/CI tooling | `tooling/ark/` | Repository automation and local developer controls. |
| `.dockerignore` | modified | Tool/config file | Developer/CI tooling | `tooling/ark/` | Repository automation and local developer controls. |
| `.env.example` | tracked | Source/configuration | Ingress configuration contract | `engines/ark/ingress/.env.example` | Defines required runtime inputs for ARK ingress. |
| `.env.prod` | modified | Source/configuration | Operations secret template/config | `operations/deployment/ark/.env.prod` | Production environment configuration belongs with deployment operations; review for secrets before promotion. |
| `.githooks/post-commit` | tracked | Source/configuration | Developer/CI tooling | `tooling/ark/` | Repository automation and local developer controls. |
| `.githooks/pre-commit` | tracked | Source/configuration | Developer/CI tooling | `tooling/ark/` | Repository automation and local developer controls. |
| `.github/workflows/ark-build-push.yml` | modified | YAML configuration | Developer/CI tooling | `tooling/ark/` | Repository automation and local developer controls. |
| `.github/workflows/ark-core-ci.yml` | tracked | YAML configuration | Developer/CI tooling | `tooling/ark/` | Repository automation and local developer controls. |
| `.gitignore` | tracked | Tool/config file | Developer/CI tooling | `tooling/ark/` | Repository automation and local developer controls. |
| `AI_CONTRACT.md` | tracked | Documentation | Constitutional/architecture documentation | `constitution/ark/` | Defines architectural principles, system maps, truth-spine, or governance language. |
| `ALL_PORTS_URLS.md` | tracked | Documentation | Operations documentation | `operations/ark/docs/` | Deployment, wiring, production, or port documentation. |
| `ARCHITECTURE.md` | tracked | Documentation | Constitutional/architecture documentation | `constitution/ark/` | Defines architectural principles, system maps, truth-spine, or governance language. |
| `ARK_SPEC.md` | tracked | Documentation | Constitutional/architecture documentation | `constitution/ark/` | Defines architectural principles, system maps, truth-spine, or governance language. |
| `ARK_SPEC_PACK_V1.md` | tracked | Documentation | Constitutional/architecture documentation | `constitution/ark/` | Defines architectural principles, system maps, truth-spine, or governance language. |
| `BUILD_SUMMARY.md` | tracked | Documentation | Engine documentation | `engines/ark/docs/legacy/` | ARK explanatory material retained as engine documentation until canonicalized. |
| `DEPLOYMENT_CHECKLIST.txt` | tracked | Documentation | Operations documentation | `operations/ark/docs/` | Deployment, wiring, production, or port documentation. |
| `DEPLOYMENT_CHECKLIST_PROD.md` | untracked | Documentation | Operations documentation | `operations/ark/docs/` | Deployment, wiring, production, or port documentation. |
| `DEPLOYMENT_GUIDE.md` | tracked | Documentation | Operations documentation | `operations/ark/docs/` | Deployment, wiring, production, or port documentation. |
| `DEPLOYMENT_GUIDE_v1.0.md` | tracked | Documentation | Operations documentation | `operations/ark/docs/` | Deployment, wiring, production, or port documentation. |
| `Dockerfile.ark` | tracked | Container build file | Operations | `operations/ark/` | Runtime deployment, provisioning, monitoring, or container infrastructure. |
| `Dockerfile.autoscaler` | modified | Container build file | Operations | `operations/ark/` | Runtime deployment, provisioning, monitoring, or container infrastructure. |
| `Dockerfile.composio` | modified | Container build file | Operations | `operations/ark/` | Runtime deployment, provisioning, monitoring, or container infrastructure. |
| `Dockerfile.duckdb` | modified | Container build file | Operations | `operations/ark/` | Runtime deployment, provisioning, monitoring, or container infrastructure. |
| `Dockerfile.gateway` | tracked | Container build file | Operations | `operations/ark/` | Runtime deployment, provisioning, monitoring, or container infrastructure. |
| `Dockerfile.ha-emitter` | modified | Container build file | Operations | `operations/ark/` | Runtime deployment, provisioning, monitoring, or container infrastructure. |
| `Dockerfile.ingestion-leader` | tracked | Container build file | Operations | `operations/ark/` | Runtime deployment, provisioning, monitoring, or container infrastructure. |
| `Dockerfile.jellyfin-emitter` | modified | Container build file | Operations | `operations/ark/` | Runtime deployment, provisioning, monitoring, or container infrastructure. |
| `Dockerfile.mesh` | modified | Container build file | Operations | `operations/ark/` | Runtime deployment, provisioning, monitoring, or container infrastructure. |
| `Dockerfile.mqtt-bridge` | tracked | Container build file | Operations | `operations/ark/` | Runtime deployment, provisioning, monitoring, or container infrastructure. |
| `Dockerfile.netwatch` | tracked | Container build file | Operations | `operations/ark/` | Runtime deployment, provisioning, monitoring, or container infrastructure. |
| `Dockerfile.opencode` | modified | Container build file | Operations | `operations/ark/` | Runtime deployment, provisioning, monitoring, or container infrastructure. |
| `Dockerfile.openwolf` | modified | Container build file | Operations | `operations/ark/` | Runtime deployment, provisioning, monitoring, or container infrastructure. |
| `Dockerfile.stability-kernel` | tracked | Container build file | Operations | `operations/ark/` | Runtime deployment, provisioning, monitoring, or container infrastructure. |
| `Dockerfile.unifi-emitter` | modified | Container build file | Operations | `operations/ark/` | Runtime deployment, provisioning, monitoring, or container infrastructure. |
| `EMITTERS_DELIVERY.md` | tracked | Documentation | Engine documentation | `engines/ark/docs/legacy/` | ARK explanatory material retained as engine documentation until canonicalized. |
| `EMITTERS_GUIDE.md` | tracked | Documentation | Engine documentation | `engines/ark/docs/legacy/` | ARK explanatory material retained as engine documentation until canonicalized. |
| `EMITTERS_QUICK_REF.md` | tracked | Documentation | Engine documentation | `engines/ark/docs/legacy/` | ARK explanatory material retained as engine documentation until canonicalized. |
| `EMITTERS_SUMMARY.md` | tracked | Documentation | Engine documentation | `engines/ark/docs/legacy/` | ARK explanatory material retained as engine documentation until canonicalized. |
| `EMITTER_WORKFLOWS.md` | tracked | Documentation | Engine documentation | `engines/ark/docs/legacy/` | ARK explanatory material retained as engine documentation until canonicalized. |
| `EXAMPLES.md` | tracked | Documentation | Engine documentation | `engines/ark/docs/legacy/` | ARK explanatory material retained as engine documentation until canonicalized. |
| `FINAL_DELIVERY_SUMMARY.txt` | tracked | Documentation | Engine documentation | `engines/ark/docs/legacy/` | ARK explanatory material retained as engine documentation until canonicalized. |
| `FORGE_START_HERE.md` | tracked | Documentation | Engine documentation | `engines/ark/docs/legacy/` | ARK explanatory material retained as engine documentation until canonicalized. |
| `FRESH_START.md` | tracked | Documentation | Engine documentation | `engines/ark/docs/legacy/` | ARK explanatory material retained as engine documentation until canonicalized. |
| `Forge App.cmd` | tracked | Windows launcher | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `Forge App.ps1` | tracked | PowerShell script | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `Forge App.sh` | tracked | Shell script | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `GLOSSARY.md` | tracked | Documentation | Constitutional/architecture documentation | `constitution/ark/` | Defines architectural principles, system maps, truth-spine, or governance language. |
| `INDEX.md` | tracked | Documentation | Engine documentation | `engines/ark/docs/legacy/` | ARK explanatory material retained as engine documentation until canonicalized. |
| `MASTER_CHECKLIST.txt` | tracked | Documentation | Engine documentation | `engines/ark/docs/legacy/` | ARK explanatory material retained as engine documentation until canonicalized. |
| `Makefile` | tracked | Executable helper | Developer/CI tooling | `tooling/ark/` | Repository automation and local developer controls. |
| `OPTIMIZATION_CHANGES.md` | untracked | Documentation | Engine documentation | `engines/ark/docs/legacy/` | ARK explanatory material retained as engine documentation until canonicalized. |
| `PERFORMANCE_OPTIMIZATION.md` | untracked | Documentation | Engine documentation | `engines/ark/docs/legacy/` | ARK explanatory material retained as engine documentation until canonicalized. |
| `PORTS_REFERENCE.md` | tracked | Documentation | Operations documentation | `operations/ark/docs/` | Deployment, wiring, production, or port documentation. |
| `PRODUCTION_FIXES_SUMMARY.md` | untracked | Documentation | Operations documentation | `operations/ark/docs/` | Deployment, wiring, production, or port documentation. |
| `PRODUCTION_GUIDE.md` | untracked | Documentation | Operations documentation | `operations/ark/docs/` | Deployment, wiring, production, or port documentation. |
| `PRODUCTION_GUIDE.txt` | tracked | Documentation | Operations documentation | `operations/ark/docs/` | Deployment, wiring, production, or port documentation. |
| `PRODUCTION_RELEASE_v1.0.md` | tracked | Documentation | Operations documentation | `operations/ark/docs/` | Deployment, wiring, production, or port documentation. |
| `PROD_REFERENCE.md` | tracked | Documentation | Operations documentation | `operations/ark/docs/` | Deployment, wiring, production, or port documentation. |
| `QUICKSTART.sh` | tracked | Shell script | Engine legacy source | `engines/ark/legacy/QUICKSTART.sh` | Historical ARK source retained pending extraction. |
| `QUICK_REFERENCE.md` | tracked | Documentation | Engine documentation | `engines/ark/docs/legacy/` | ARK explanatory material retained as engine documentation until canonicalized. |
| `QUICK_REFERENCE_PROD.md` | untracked | Documentation | Operations documentation | `operations/ark/docs/` | Deployment, wiring, production, or port documentation. |
| `README.md` | tracked | Documentation | Engine documentation | `engines/ark/docs/legacy/` | ARK explanatory material retained as engine documentation until canonicalized. |
| `README_PROD.md` | tracked | Documentation | Operations documentation | `operations/ark/docs/` | Deployment, wiring, production, or port documentation. |
| `REVIEW.md` | tracked | Documentation | Engine documentation | `engines/ark/docs/legacy/` | ARK explanatory material retained as engine documentation until canonicalized. |
| `SYSTEM_MAP.md` | tracked | Documentation | Constitutional/architecture documentation | `constitution/ark/` | Defines architectural principles, system maps, truth-spine, or governance language. |
| `TRISCA.md` | tracked | Documentation | Constitutional/architecture documentation | `constitution/ark/` | Defines architectural principles, system maps, truth-spine, or governance language. |
| `VERIFICATION_v1.0.md` | tracked | Documentation | Engine documentation | `engines/ark/docs/legacy/` | ARK explanatory material retained as engine documentation until canonicalized. |
| `WIRING_CHECKLIST.md` | tracked | Documentation | Operations documentation | `operations/ark/docs/` | Deployment, wiring, production, or port documentation. |
| `WIRING_GUIDE.txt` | tracked | Documentation | Operations documentation | `operations/ark/docs/` | Deployment, wiring, production, or port documentation. |
| `action/action.go` | tracked | Go module | ARK core/egress runtime | `engines/ark/core/` | SD-ARK loop, API, command entrypoints, actions, and meta behavior implement ARK responsibilities until split. |
| `agents/aider/agent.py` | tracked | Python module | Internal application/agent | `internal/agents/` | Wayfinder-owned agent surfaces should consume engines/services via contracts. |
| `agents/composio/agent.py` | tracked | Python module | External integration | `external/composio/` | Composio is a third-party execution bridge. |
| `agents/forge_native/__init__.py` | tracked | Python module | Internal application/agent | `internal/agents/` | Wayfinder-owned agent surfaces should consume engines/services via contracts. |
| `agents/forge_native/agent.py` | tracked | Python module | Internal application/agent | `internal/agents/` | Wayfinder-owned agent surfaces should consume engines/services via contracts. |
| `agents/opencode/agent.py` | tracked | Python module | Internal application/agent | `internal/agents/` | Wayfinder-owned agent surfaces should consume engines/services via contracts. |
| `agents/openwolf/agent.py` | tracked | Python module | Internal application/agent | `internal/agents/` | Wayfinder-owned agent surfaces should consume engines/services via contracts. |
| `agents/rube/agent.py` | tracked | Python module | Internal application/agent | `internal/agents/` | Wayfinder-owned agent surfaces should consume engines/services via contracts. |
| `api/server.go` | tracked | Go module | ARK core/egress runtime | `engines/ark/core/` | SD-ARK loop, API, command entrypoints, actions, and meta behavior implement ARK responsibilities until split. |
| `ark-core/.github/workflows/ci.yml` | tracked | YAML configuration | Engine legacy source | `engines/ark/legacy/ark-core/.github/workflows/ci.yml` | Historical ARK source retained pending extraction. |
| `ark-core/README.md` | tracked | Documentation | Engine documentation | `engines/ark/docs/legacy/` | ARK explanatory material retained as engine documentation until canonicalized. |
| `ark-core/config/operating_rules.json` | tracked | JSON configuration/schema | Service: configuration | `services/configuration/` | Configuration loading and invariant manifests are reusable service concerns. |
| `ark-core/config/system_invariants.json` | tracked | JSON configuration/schema | Service: configuration | `services/configuration/` | Configuration loading and invariant manifests are reusable service concerns. |
| `ark-core/config/tiering_rules.json` | tracked | JSON configuration/schema | Service: configuration | `services/configuration/` | Configuration loading and invariant manifests are reusable service concerns. |
| `ark-core/docs/ARK_TRUTH_SPINE.md` | tracked | Documentation | Constitutional/architecture documentation | `constitution/ark/` | Defines architectural principles, system maps, truth-spine, or governance language. |
| `ark-core/docs/CODEX_ARK_SYSTEM_PROMPT.md` | tracked | Documentation | Constitutional/architecture documentation | `constitution/ark/` | Defines architectural principles, system maps, truth-spine, or governance language. |
| `ark-core/docs/MISSION_GRADE_RULES.md` | tracked | Documentation | Constitutional/architecture documentation | `constitution/ark/` | Defines architectural principles, system maps, truth-spine, or governance language. |
| `ark-core/docs/REDTEAM.md` | tracked | Documentation | Constitutional/architecture documentation | `constitution/ark/` | Defines architectural principles, system maps, truth-spine, or governance language. |
| `ark-core/docs/SYSTEM_MAP.md` | tracked | Documentation | Constitutional/architecture documentation | `constitution/ark/` | Defines architectural principles, system maps, truth-spine, or governance language. |
| `ark-core/docs/TODO_TIERS.md` | tracked | Documentation | Constitutional/architecture documentation | `constitution/ark/` | Defines architectural principles, system maps, truth-spine, or governance language. |
| `ark-core/docs/ark-field-v4.2-foundation.md` | tracked | Documentation | Constitutional/architecture documentation | `constitution/ark/` | Defines architectural principles, system maps, truth-spine, or governance language. |
| `ark-core/forge/__init__.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/ci/__init__.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/ci/loc.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/context/build.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/context/provider.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/control/controller.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/control/decay.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/control/phi.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/core/loop.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/core/orchestrator.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/exec/git.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/exec/runner.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/exec/sandbox.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/math_utils.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/mcp/__init__.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/mcp/contracts.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/mcp/policy.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/mcp/registry.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/mcp/tools.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/memory/ban.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/memory/store.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/models/discovery.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/models/ollama_client.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/models/prompts.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/runtime/artifacts.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/runtime/bootstrap.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/runtime/capabilities.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/runtime/config.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/runtime/guards.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/runtime/logs.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/transform/apply.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/transform/propose.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/types.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/ui/app.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/ui/browser.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/ui/common.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/ui/controller.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/ui/launcher.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/ui/session.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/verify/adapters.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/verify/eval.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/verify/redteam.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/forge/verify/synth.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/go.mod` | tracked | Source/configuration | Engine legacy source | `engines/ark/legacy/ark-core/go.mod` | Historical ARK source retained pending extraction. |
| `ark-core/internal/epistemic/conflict.go` | tracked | Go module | Engine legacy source | `engines/ark/legacy/ark-core/internal/epistemic/conflict.go` | Historical ARK source retained pending extraction. |
| `ark-core/internal/epistemic/policy.go` | tracked | Go module | Engine legacy source | `engines/ark/legacy/ark-core/internal/epistemic/policy.go` | Historical ARK source retained pending extraction. |
| `ark-core/internal/epistemic/resolver.go` | tracked | Go module | Engine legacy source | `engines/ark/legacy/ark-core/internal/epistemic/resolver.go` | Historical ARK source retained pending extraction. |
| `ark-core/internal/epistemic/resolver_test.go` | tracked | Go module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `ark-core/internal/epistemic/states.go` | tracked | Go module | Engine legacy source | `engines/ark/legacy/ark-core/internal/epistemic/states.go` | Historical ARK source retained pending extraction. |
| `ark-core/internal/epistemic/states_test.go` | tracked | Go module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `ark-core/internal/models/truth_spine.go` | tracked | Go module | ARK reality model | `engines/ark/reality/` | Truth spine and event models are reality-preservation concepts. |
| `ark-core/internal/models/truth_spine_test.go` | tracked | Go module | ARK reality model | `engines/ark/reality/` | Truth spine and event models are reality-preservation concepts. |
| `ark-core/requirements-dev.txt` | tracked | Documentation | Engine documentation | `engines/ark/docs/legacy/` | ARK explanatory material retained as engine documentation until canonicalized. |
| `ark-core/scripts/ai/codex_prompt.txt` | tracked | Documentation | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/scripts/ai/forge.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/scripts/ai/orchestrator.py` | tracked | Python module | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `ark-core/scripts/ci/enforce_tiers.py` | tracked | Python module | Engine legacy source | `engines/ark/legacy/ark-core/scripts/ci/enforce_tiers.py` | Historical ARK source retained pending extraction. |
| `ark-core/scripts/ci/redteam.sh` | tracked | Shell script | Engine legacy source | `engines/ark/legacy/ark-core/scripts/ci/redteam.sh` | Historical ARK source retained pending extraction. |
| `ark-core/scripts/verify.ps1` | tracked | PowerShell script | Engine legacy source | `engines/ark/legacy/ark-core/scripts/verify.ps1` | Historical ARK source retained pending extraction. |
| `ark-core/tests/conftest.py` | tracked | Python module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `ark-core/tests/test_ai_orchestrator.py` | tracked | Python module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `ark-core/tests/test_docs_contracts.py` | tracked | Python module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `ark-core/tests/test_forge_banlist.py` | tracked | Python module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `ark-core/tests/test_forge_bootstrap.py` | tracked | Python module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `ark-core/tests/test_forge_browser.py` | tracked | Python module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `ark-core/tests/test_forge_diff_apply.py` | tracked | Python module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `ark-core/tests/test_forge_launcher.py` | tracked | Python module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `ark-core/tests/test_forge_linux.py` | tracked | Python module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `ark-core/tests/test_forge_loc.py` | tracked | Python module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `ark-core/tests/test_forge_mcp.py` | tracked | Python module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `ark-core/tests/test_forge_mvp.py` | tracked | Python module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `ark-core/tests/test_forge_ollama.py` | tracked | Python module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `ark-core/tests/test_forge_propose.py` | tracked | Python module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `ark-core/tests/test_forge_security.py` | tracked | Python module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `ark-core/tests/test_forge_session.py` | tracked | Python module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `ark-core/tests/test_forge_ui_app.py` | tracked | Python module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `ark-core/tests/test_tier_enforcement.py` | tracked | Python module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `ark/Cargo.lock` | tracked | Lockfile | ARK legacy implementation | `engines/ark/core/` | Python/Rust ARK implementation retained until services/contracts are extracted. |
| `ark/Cargo.toml` | tracked | TOML manifest | ARK legacy implementation | `engines/ark/core/` | Python/Rust ARK implementation retained until services/contracts are extracted. |
| `ark/__init__.py` | tracked | Python module | ARK legacy implementation | `engines/ark/core/` | Python/Rust ARK implementation retained until services/contracts are extracted. |
| `ark/api_gateway.py` | tracked | Python module | ARK legacy implementation | `engines/ark/core/` | Python/Rust ARK implementation retained until services/contracts are extracted. |
| `ark/autoscaler.py` | tracked | Python module | Service: scheduling/resource control | `services/scheduling/` | Budgeting and autoscaling are reusable bounded-execution controls. |
| `ark/axioms.py` | tracked | Python module | ARK legacy implementation | `engines/ark/core/` | Python/Rust ARK implementation retained until services/contracts are extracted. |
| `ark/codegen_safe.py` | tracked | Python module | ARK legacy implementation | `engines/ark/core/` | Python/Rust ARK implementation retained until services/contracts are extracted. |
| `ark/config.py` | tracked | Python module | Service: configuration | `services/configuration/` | Configuration loading and invariant manifests are reusable service concerns. |
| `ark/duck_client.py` | tracked | Python module | Service: storage/persistence | `services/storage/` | Storage and persistence are reusable services, not ARK-owned behavior. |
| `ark/emitter_contracts.py` | tracked | Python module | Contract | `contracts/ark/` | Schemas and interface language contain no durable ARK implementation once extracted. |
| `ark/event_schema.py` | tracked | Python module | Contract | `contracts/ark/` | Schemas and interface language contain no durable ARK implementation once extracted. |
| `ark/forge_planner.py` | tracked | Python module | ARK legacy implementation | `engines/ark/core/` | Python/Rust ARK implementation retained until services/contracts are extracted. |
| `ark/git_reconcile.py` | tracked | Python module | ARK legacy implementation | `engines/ark/core/` | Python/Rust ARK implementation retained until services/contracts are extracted. |
| `ark/gsb.py` | tracked | Python module | ARK legacy implementation | `engines/ark/core/` | Python/Rust ARK implementation retained until services/contracts are extracted. |
| `ark/import_audit.py` | tracked | Python module | ARK legacy implementation | `engines/ark/core/` | Python/Rust ARK implementation retained until services/contracts are extracted. |
| `ark/integrations/__init__.py` | tracked | Python module | External integration service boundary | `external/ark-integrations/` | HTTP, Docker, map, web, and registry adapters are replaceable integration boundaries. |
| `ark/integrations/contracts.py` | tracked | Python module | Contract | `contracts/ark/` | Schemas and interface language contain no durable ARK implementation once extracted. |
| `ark/integrations/docker.py` | tracked | Python module | External integration service boundary | `external/ark-integrations/` | HTTP, Docker, map, web, and registry adapters are replaceable integration boundaries. |
| `ark/integrations/http.py` | tracked | Python module | External integration service boundary | `external/ark-integrations/` | HTTP, Docker, map, web, and registry adapters are replaceable integration boundaries. |
| `ark/integrations/maps.py` | tracked | Python module | External integration service boundary | `external/ark-integrations/` | HTTP, Docker, map, web, and registry adapters are replaceable integration boundaries. |
| `ark/integrations/registry.py` | tracked | Python module | External integration service boundary | `external/ark-integrations/` | HTTP, Docker, map, web, and registry adapters are replaceable integration boundaries. |
| `ark/integrations/web.py` | tracked | Python module | External integration service boundary | `external/ark-integrations/` | HTTP, Docker, map, web, and registry adapters are replaceable integration boundaries. |
| `ark/maintenance.py` | tracked | Python module | ARK legacy implementation | `engines/ark/core/` | Python/Rust ARK implementation retained until services/contracts are extracted. |
| `ark/math_utils.py` | tracked | Python module | ARK legacy implementation | `engines/ark/core/` | Python/Rust ARK implementation retained until services/contracts are extracted. |
| `ark/mcp_containment.py` | tracked | Python module | ARK legacy implementation | `engines/ark/core/` | Python/Rust ARK implementation retained until services/contracts are extracted. |
| `ark/mesh_registry.py` | modified | Python module | Service: discovery/registry | `services/discovery/` | Capability registry and mesh discovery are reusable services. |
| `ark/performance.py` | untracked | Python module | ARK legacy implementation | `engines/ark/core/` | Python/Rust ARK implementation retained until services/contracts are extracted. |
| `ark/policy_engine.py` | tracked | Python module | Service: policy | `services/policy/` | Policy evaluation is reusable shared infrastructure. |
| `ark/reducers.py` | tracked | Python module | ARK ephemeral | `engines/ark/ephemeral/` | Reducers, projections, and replay are derived/disposable views until proven. |
| `ark/runtime_contracts.py` | tracked | Python module | Contract | `contracts/ark/` | Schemas and interface language contain no durable ARK implementation once extracted. |
| `ark/runtime_flow.py` | tracked | Python module | Service: runtime | `services/runtime/` | Runtime middleware, toggles, and compilers are reusable execution infrastructure. |
| `ark/sd_trisca.py` | tracked | Python module | Capability/service: measurement | `capabilities/measure/` | TRISCA is cross-cutting measurement/scoring capability used by ARK and others. |
| `ark/security.py` | tracked | Python module | Service: cryptography/compression | `services/cryptography/` | Cryptography, hashing, envelope, and compression are shared infrastructure. |
| `ark/skills.py` | tracked | Python module | ARK legacy implementation | `engines/ark/core/` | Python/Rust ARK implementation retained until services/contracts are extracted. |
| `ark/src/compress/mod.rs` | tracked | Rust module | Service: cryptography/compression | `services/cryptography/` | Cryptography, hashing, envelope, and compression are shared infrastructure. |
| `ark/src/compress/zstd.rs` | tracked | Rust module | Service: cryptography/compression | `services/cryptography/` | Cryptography, hashing, envelope, and compression are shared infrastructure. |
| `ark/src/control/mod.rs` | tracked | Rust module | ARK legacy implementation | `engines/ark/core/` | Python/Rust ARK implementation retained until services/contracts are extracted. |
| `ark/src/control/plane.rs` | tracked | Rust module | ARK legacy implementation | `engines/ark/core/` | Python/Rust ARK implementation retained until services/contracts are extracted. |
| `ark/src/delta/compute.rs` | tracked | Rust module | ARK legacy implementation | `engines/ark/core/` | Python/Rust ARK implementation retained until services/contracts are extracted. |
| `ark/src/delta/mod.rs` | tracked | Rust module | ARK legacy implementation | `engines/ark/core/` | Python/Rust ARK implementation retained until services/contracts are extracted. |
| `ark/src/event/mod.rs` | tracked | Rust module | ARK legacy implementation | `engines/ark/core/` | Python/Rust ARK implementation retained until services/contracts are extracted. |
| `ark/src/event/wal.rs` | tracked | Rust module | ARK legacy implementation | `engines/ark/core/` | Python/Rust ARK implementation retained until services/contracts are extracted. |
| `ark/src/ingest/audio.rs` | tracked | Rust module | ARK ingress | `engines/ark/ingress/` | Ingestion is the ARK entry point for observations/events. |
| `ark/src/ingest/image.rs` | tracked | Rust module | ARK ingress | `engines/ark/ingress/` | Ingestion is the ARK entry point for observations/events. |
| `ark/src/ingest/mod.rs` | tracked | Rust module | ARK ingress | `engines/ark/ingress/` | Ingestion is the ARK entry point for observations/events. |
| `ark/src/ingest/net.rs` | tracked | Rust module | ARK ingress | `engines/ark/ingress/` | Ingestion is the ARK entry point for observations/events. |
| `ark/src/ingest/text.rs` | tracked | Rust module | ARK ingress | `engines/ark/ingress/` | Ingestion is the ARK entry point for observations/events. |
| `ark/src/ingest/video.rs` | tracked | Rust module | ARK ingress | `engines/ark/ingress/` | Ingestion is the ARK entry point for observations/events. |
| `ark/src/lib.rs` | tracked | Rust module | ARK legacy implementation | `engines/ark/core/` | Python/Rust ARK implementation retained until services/contracts are extracted. |
| `ark/src/main.rs` | tracked | Rust module | ARK legacy implementation | `engines/ark/core/` | Python/Rust ARK implementation retained until services/contracts are extracted. |
| `ark/src/otel.rs` | tracked | Rust module | Service: telemetry/logging | `services/telemetry/` | Telemetry and logs are shared observability infrastructure. |
| `ark/src/policy/engine.rs` | tracked | Rust module | Service: policy | `services/policy/` | Policy evaluation is reusable shared infrastructure. |
| `ark/src/policy/mod.rs` | tracked | Rust module | Service: policy | `services/policy/` | Policy evaluation is reusable shared infrastructure. |
| `ark/src/replay/engine.rs` | tracked | Rust module | ARK ephemeral | `engines/ark/ephemeral/` | Reducers, projections, and replay are derived/disposable views until proven. |
| `ark/src/replay/mod.rs` | tracked | Rust module | ARK ephemeral | `engines/ark/ephemeral/` | Reducers, projections, and replay are derived/disposable views until proven. |
| `ark/src/storage/duck.rs` | tracked | Rust module | Service: storage/persistence | `services/storage/` | Storage and persistence are reusable services, not ARK-owned behavior. |
| `ark/src/storage/mod.rs` | tracked | Rust module | Service: storage/persistence | `services/storage/` | Storage and persistence are reusable services, not ARK-owned behavior. |
| `ark/src/trisca/core.rs` | tracked | Rust module | Capability/service: measurement | `capabilities/measure/` | TRISCA is cross-cutting measurement/scoring capability used by ARK and others. |
| `ark/src/trisca/kalman.rs` | tracked | Rust module | Capability/service: measurement | `capabilities/measure/` | TRISCA is cross-cutting measurement/scoring capability used by ARK and others. |
| `ark/src/trisca/mod.rs` | tracked | Rust module | Capability/service: measurement | `capabilities/measure/` | TRISCA is cross-cutting measurement/scoring capability used by ARK and others. |
| `ark/src/trisca/system.rs` | tracked | Rust module | Capability/service: measurement | `capabilities/measure/` | TRISCA is cross-cutting measurement/scoring capability used by ARK and others. |
| `ark/src/types.rs` | tracked | Rust module | ARK legacy implementation | `engines/ark/core/` | Python/Rust ARK implementation retained until services/contracts are extracted. |
| `ark/subjects.py` | tracked | Python module | Service: identity | `services/identity/` | Subject and identity rules are reusable identity language/infrastructure. |
| `ark/task_graph.py` | tracked | Python module | ARK legacy implementation | `engines/ark/core/` | Python/Rust ARK implementation retained until services/contracts are extracted. |
| `ark/time_utils.py` | tracked | Python module | ARK legacy implementation | `engines/ark/core/` | Python/Rust ARK implementation retained until services/contracts are extracted. |
| `ark/tool_system.py` | tracked | Python module | ARK legacy implementation | `engines/ark/core/` | Python/Rust ARK implementation retained until services/contracts are extracted. |
| `ark/vendor/arrow-arith-51.0.0/.cargo-ok` | tracked | Tool/config file | ARK legacy implementation | `engines/ark/core/` | Python/Rust ARK implementation retained until services/contracts are extracted. |
| `ark/vendor/arrow-arith-51.0.0/Cargo.toml` | tracked | TOML manifest | ARK legacy implementation | `engines/ark/core/` | Python/Rust ARK implementation retained until services/contracts are extracted. |
| `ark/vendor/arrow-arith-51.0.0/Cargo.toml.orig` | tracked | Source/configuration | ARK legacy implementation | `engines/ark/core/` | Python/Rust ARK implementation retained until services/contracts are extracted. |
| `ark/vendor/arrow-arith-51.0.0/src/aggregate.rs` | tracked | Rust module | ARK legacy implementation | `engines/ark/core/` | Python/Rust ARK implementation retained until services/contracts are extracted. |
| `ark/vendor/arrow-arith-51.0.0/src/arithmetic.rs` | tracked | Rust module | ARK legacy implementation | `engines/ark/core/` | Python/Rust ARK implementation retained until services/contracts are extracted. |
| `ark/vendor/arrow-arith-51.0.0/src/arity.rs` | tracked | Rust module | ARK legacy implementation | `engines/ark/core/` | Python/Rust ARK implementation retained until services/contracts are extracted. |
| `ark/vendor/arrow-arith-51.0.0/src/bitwise.rs` | tracked | Rust module | ARK legacy implementation | `engines/ark/core/` | Python/Rust ARK implementation retained until services/contracts are extracted. |
| `ark/vendor/arrow-arith-51.0.0/src/boolean.rs` | tracked | Rust module | ARK legacy implementation | `engines/ark/core/` | Python/Rust ARK implementation retained until services/contracts are extracted. |
| `ark/vendor/arrow-arith-51.0.0/src/lib.rs` | tracked | Rust module | ARK legacy implementation | `engines/ark/core/` | Python/Rust ARK implementation retained until services/contracts are extracted. |
| `ark/vendor/arrow-arith-51.0.0/src/numeric.rs` | tracked | Rust module | ARK legacy implementation | `engines/ark/core/` | Python/Rust ARK implementation retained until services/contracts are extracted. |
| `ark/vendor/arrow-arith-51.0.0/src/temporal.rs` | tracked | Rust module | ARK legacy implementation | `engines/ark/core/` | Python/Rust ARK implementation retained until services/contracts are extracted. |
| `authelia/configuration.yml` | tracked | YAML configuration | Operations | `operations/ark/` | Runtime deployment, provisioning, monitoring, or container infrastructure. |
| `authelia/users_database.yml` | tracked | YAML configuration | Operations | `operations/ark/` | Runtime deployment, provisioning, monitoring, or container infrastructure. |
| `backup-prod.sh` | tracked | Shell script | Operations | `operations/ark/` | Runtime deployment, provisioning, monitoring, or container infrastructure. |
| `cmd/ingestion-leader/main.go` | tracked | Go module | ARK core/egress runtime | `engines/ark/core/` | SD-ARK loop, API, command entrypoints, actions, and meta behavior implement ARK responsibilities until split. |
| `cmd/mqtt-bridge/main.go` | tracked | Go module | ARK core/egress runtime | `engines/ark/core/` | SD-ARK loop, API, command entrypoints, actions, and meta behavior implement ARK responsibilities until split. |
| `cmd/netwatch/main.go` | tracked | Go module | Engine: NetWatch | `engines/netwatch/legacy/` | Network watching is a separate engine responsibility. |
| `cmd/stability-kernel/main.go` | tracked | Go module | ARK core/egress runtime | `engines/ark/core/` | SD-ARK loop, API, command entrypoints, actions, and meta behavior implement ARK responsibilities until split. |
| `config/ark.env` | tracked | Source/configuration | Service: configuration | `services/configuration/` | Configuration loading and invariant manifests are reusable service concerns. |
| `config/manifest.json` | tracked | JSON configuration/schema | Service: configuration | `services/configuration/` | Configuration loading and invariant manifests are reusable service concerns. |
| `config/nats.conf` | untracked | Service configuration | Service: event bus/transport | `services/event-bus/` | Pub/sub and transport are reusable infrastructure. |
| `config/tiering_rules.json` | tracked | JSON configuration/schema | Service: configuration | `services/configuration/` | Configuration loading and invariant manifests are reusable service concerns. |
| `conftest.py` | tracked | Python module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `core/bayes.go` | tracked | Go module | ARK core/egress runtime | `engines/ark/core/` | SD-ARK loop, API, command entrypoints, actions, and meta behavior implement ARK responsibilities until split. |
| `core/interpreter.go` | tracked | Go module | ARK core/egress runtime | `engines/ark/core/` | SD-ARK loop, API, command entrypoints, actions, and meta behavior implement ARK responsibilities until split. |
| `core/step.go` | tracked | Go module | ARK core/egress runtime | `engines/ark/core/` | SD-ARK loop, API, command entrypoints, actions, and meta behavior implement ARK responsibilities until split. |
| `core/step_test.go` | tracked | Go module | ARK core/egress runtime | `engines/ark/core/` | SD-ARK loop, API, command entrypoints, actions, and meta behavior implement ARK responsibilities until split. |
| `core/trisca.go` | tracked | Go module | Capability/service: measurement | `capabilities/measure/` | TRISCA is cross-cutting measurement/scoring capability used by ARK and others. |
| `definitions/actions.yaml` | tracked | YAML definition | Contract/definition | `contracts/ark/definitions/` | Runtime actions, policies, routing, and meta definitions are shared language. |
| `definitions/meta.yaml` | tracked | YAML definition | Contract/definition | `contracts/ark/definitions/` | Runtime actions, policies, routing, and meta definitions are shared language. |
| `definitions/policies.yaml` | tracked | YAML definition | Contract/definition | `contracts/ark/definitions/` | Runtime actions, policies, routing, and meta definitions are shared language. |
| `definitions/routing.yaml` | tracked | YAML definition | Contract/definition | `contracts/ark/definitions/` | Runtime actions, policies, routing, and meta definitions are shared language. |
| `deploy-prod.sh` | modified | Shell script | Operations | `operations/ark/` | Runtime deployment, provisioning, monitoring, or container infrastructure. |
| `deploy/compose/dev.yml` | tracked | YAML configuration | Operations | `operations/ark/` | Runtime deployment, provisioning, monitoring, or container infrastructure. |
| `docker-compose.prod.yml` | modified | YAML configuration | Operations | `operations/ark/` | Runtime deployment, provisioning, monitoring, or container infrastructure. |
| `docker-compose.yml` | modified | YAML configuration | Operations | `operations/ark/` | Runtime deployment, provisioning, monitoring, or container infrastructure. |
| `docs/ARK_FIELD_V4_2_STAGE1.md` | tracked | Documentation | Engine documentation | `engines/ark/docs/legacy/` | ARK explanatory material retained as engine documentation until canonicalized. |
| `docs/ARK_FIELD_V4_2_STAGE2.md` | tracked | Documentation | Engine documentation | `engines/ark/docs/legacy/` | ARK explanatory material retained as engine documentation until canonicalized. |
| `docs/ARK_FIELD_V4_2_STAGE3.md` | tracked | Documentation | Engine documentation | `engines/ark/docs/legacy/` | ARK explanatory material retained as engine documentation until canonicalized. |
| `docs/ARK_FIELD_V4_2_STAGE4.md` | tracked | Documentation | Engine documentation | `engines/ark/docs/legacy/` | ARK explanatory material retained as engine documentation until canonicalized. |
| `emitters/homeassistant_emitter.py` | tracked | Python module | External integration ingress | `external/` | Home Assistant, Jellyfin, and UniFi emitters are replaceable external adapters. |
| `emitters/jellyfin_emitter.py` | tracked | Python module | External integration ingress | `external/` | Home Assistant, Jellyfin, and UniFi emitters are replaceable external adapters. |
| `emitters/unifi_emitter.py` | tracked | Python module | External integration ingress | `external/` | Home Assistant, Jellyfin, and UniFi emitters are replaceable external adapters. |
| `external/README.md` | tracked | Documentation | Engine documentation | `engines/ark/docs/legacy/` | ARK explanatory material retained as engine documentation until canonicalized. |
| `forge` | tracked | Executable helper | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `forge-app` | tracked | Executable helper | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `forge.cmd` | tracked | Windows launcher | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `forge.ps1` | tracked | PowerShell script | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `go.mod` | tracked | Source/configuration | Engine legacy source | `engines/ark/legacy/go.mod` | Historical ARK source retained pending extraction. |
| `go.sum` | tracked | Go checksum | Engine legacy source | `engines/ark/legacy/go.sum` | Historical ARK source retained pending extraction. |
| `gsb/gsb.go` | tracked | Go module | Service: event bus/transport | `services/event-bus/` | Pub/sub and transport are reusable infrastructure. |
| `init-db.sql` | untracked | SQL schema | Operations | `operations/ark/` | Runtime deployment, provisioning, monitoring, or container infrastructure. |
| `init-prod.sh` | tracked | Shell script | Operations | `operations/ark/` | Runtime deployment, provisioning, monitoring, or container infrastructure. |
| `install-forge-arch.sh` | tracked | Shell script | Foundry engine/application | `engines/foundry/legacy/` | Foundry owns engineering/code transformation workflows; Forge is the legacy ARK name. |
| `internal/README.md` | tracked | Documentation | Engine documentation | `engines/ark/docs/legacy/` | ARK explanatory material retained as engine documentation until canonicalized. |
| `internal/adapters/gitcommit/source.go` | tracked | Go module | Engine legacy source | `engines/ark/legacy/internal/adapters/gitcommit/source.go` | Historical ARK source retained pending extraction. |
| `internal/adapters/gitcommit/source_test.go` | tracked | Go module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `internal/adapters/ingestforward/forwarder.go` | tracked | Go module | Engine legacy source | `engines/ark/legacy/internal/adapters/ingestforward/forwarder.go` | Historical ARK source retained pending extraction. |
| `internal/adapters/ingestforward/forwarder_test.go` | tracked | Go module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `internal/adapters/natspub/publisher.go` | tracked | Go module | Service: event bus/transport | `services/event-bus/` | Pub/sub and transport are reusable infrastructure. |
| `internal/adapters/redisstate/store.go` | tracked | Go module | Service: storage/persistence | `services/storage/` | Storage and persistence are reusable services, not ARK-owned behavior. |
| `internal/adapters/stabilitywrap/evaluator.go` | tracked | Go module | Engine legacy source | `engines/ark/legacy/internal/adapters/stabilitywrap/evaluator.go` | Historical ARK source retained pending extraction. |
| `internal/budget/controller.go` | tracked | Go module | Service: scheduling/resource control | `services/scheduling/` | Budgeting and autoscaling are reusable bounded-execution controls. |
| `internal/config/env.go` | tracked | Go module | Service: configuration | `services/configuration/` | Configuration loading and invariant manifests are reusable service concerns. |
| `internal/config/env_test.go` | tracked | Go module | Service: configuration | `services/configuration/` | Configuration loading and invariant manifests are reusable service concerns. |
| `internal/contracts/anomaly_v1.json` | tracked | JSON configuration/schema | Contract | `contracts/ark/` | Schemas and interface language contain no durable ARK implementation once extracted. |
| `internal/contracts/event_v1.json` | tracked | JSON configuration/schema | Contract | `contracts/ark/` | Schemas and interface language contain no durable ARK implementation once extracted. |
| `internal/contracts/external_action_v1.json` | tracked | JSON configuration/schema | Contract | `contracts/ark/` | Schemas and interface language contain no durable ARK implementation once extracted. |
| `internal/contracts/health_v1.json` | tracked | JSON configuration/schema | Contract | `contracts/ark/` | Schemas and interface language contain no durable ARK implementation once extracted. |
| `internal/contracts/promotion_v1.json` | tracked | JSON configuration/schema | Contract | `contracts/ark/` | Schemas and interface language contain no durable ARK implementation once extracted. |
| `internal/contracts/runtime_schemas_v1.json` | tracked | JSON configuration/schema | Contract | `contracts/ark/` | Schemas and interface language contain no durable ARK implementation once extracted. |
| `internal/contracts/validate.go` | tracked | Go module | Contract | `contracts/ark/` | Schemas and interface language contain no durable ARK implementation once extracted. |
| `internal/crypto/audit.go` | tracked | Go module | Service: cryptography/compression | `services/cryptography/` | Cryptography, hashing, envelope, and compression are shared infrastructure. |
| `internal/crypto/compress.go` | tracked | Go module | Service: cryptography/compression | `services/cryptography/` | Cryptography, hashing, envelope, and compression are shared infrastructure. |
| `internal/crypto/envelope.go` | tracked | Go module | Service: cryptography/compression | `services/cryptography/` | Cryptography, hashing, envelope, and compression are shared infrastructure. |
| `internal/crypto/hash.go` | tracked | Go module | Service: cryptography/compression | `services/cryptography/` | Cryptography, hashing, envelope, and compression are shared infrastructure. |
| `internal/crypto/key.go` | tracked | Go module | Service: cryptography/compression | `services/cryptography/` | Cryptography, hashing, envelope, and compression are shared infrastructure. |
| `internal/cryptofabric/fabric.go` | tracked | Go module | Service: cryptography/compression | `services/cryptography/` | Cryptography, hashing, envelope, and compression are shared infrastructure. |
| `internal/cryptofabric/fabric_test.go` | tracked | Go module | Service: cryptography/compression | `services/cryptography/` | Cryptography, hashing, envelope, and compression are shared infrastructure. |
| `internal/ingestion/service.go` | tracked | Go module | ARK ingress | `engines/ark/ingress/` | Ingestion is the ARK entry point for observations/events. |
| `internal/ingestion/service_test.go` | tracked | Go module | ARK ingress | `engines/ark/ingress/` | Ingestion is the ARK entry point for observations/events. |
| `internal/loop_contract.md` | tracked | Documentation | Engine documentation | `engines/ark/docs/legacy/` | ARK explanatory material retained as engine documentation until canonicalized. |
| `internal/midas/core.go` | tracked | Go module | Engine: MIDAS | `engines/midas/legacy/` | MIDAS is a named engine responsibility, not ARK core. |
| `internal/midas/core_test.go` | tracked | Go module | Engine: MIDAS | `engines/midas/legacy/` | MIDAS is a named engine responsibility, not ARK core. |
| `internal/models/event.go` | tracked | Go module | ARK reality model | `engines/ark/reality/` | Truth spine and event models are reality-preservation concepts. |
| `internal/netwatch/controller.go` | tracked | Go module | Engine: NetWatch | `engines/netwatch/legacy/` | Network watching is a separate engine responsibility. |
| `internal/netwatch/controller_test.go` | tracked | Go module | Engine: NetWatch | `engines/netwatch/legacy/` | Network watching is a separate engine responsibility. |
| `internal/projections/projector.go` | tracked | Go module | ARK ephemeral | `engines/ark/ephemeral/` | Reducers, projections, and replay are derived/disposable views until proven. |
| `internal/projections/projector_test.go` | tracked | Go module | ARK ephemeral | `engines/ark/ephemeral/` | Reducers, projections, and replay are derived/disposable views until proven. |
| `internal/promotion/engine.go` | tracked | Go module | ARK proofs/promotion | `engines/ark/proofs/` | Promotion logic belongs in ARK proof boundary. |
| `internal/redteam/crypto.go` | tracked | Go module | Engine legacy source | `engines/ark/legacy/internal/redteam/crypto.go` | Historical ARK source retained pending extraction. |
| `internal/redteam/determinism.go` | tracked | Go module | Engine legacy source | `engines/ark/legacy/internal/redteam/determinism.go` | Historical ARK source retained pending extraction. |
| `internal/redteam/module.go` | tracked | Go module | Engine legacy source | `engines/ark/legacy/internal/redteam/module.go` | Historical ARK source retained pending extraction. |
| `internal/redteam/recovery.go` | tracked | Go module | Engine legacy source | `engines/ark/legacy/internal/redteam/recovery.go` | Historical ARK source retained pending extraction. |
| `internal/redteam/runtime.go` | tracked | Go module | Engine legacy source | `engines/ark/legacy/internal/redteam/runtime.go` | Historical ARK source retained pending extraction. |
| `internal/runtime/middleware.go` | tracked | Go module | Service: runtime | `services/runtime/` | Runtime middleware, toggles, and compilers are reusable execution infrastructure. |
| `internal/runtime/toggle.go` | tracked | Go module | Service: runtime | `services/runtime/` | Runtime middleware, toggles, and compilers are reusable execution infrastructure. |
| `internal/shared/types.go` | tracked | Go module | Engine legacy source | `engines/ark/legacy/internal/shared/types.go` | Historical ARK source retained pending extraction. |
| `internal/shared/validate.go` | tracked | Go module | Engine legacy source | `engines/ark/legacy/internal/shared/validate.go` | Historical ARK source retained pending extraction. |
| `internal/stability/interface.go` | tracked | Go module | Engine: stability kernel | `engines/stability/legacy/` | Stability evaluation is a unique engine responsibility. |
| `internal/stability/kernel.go` | tracked | Go module | Engine: stability kernel | `engines/stability/legacy/` | Stability evaluation is a unique engine responsibility. |
| `internal/stability/kernel_test.go` | tracked | Go module | Engine: stability kernel | `engines/stability/legacy/` | Stability evaluation is a unique engine responsibility. |
| `internal/state/README.md` | tracked | Documentation | Engine documentation | `engines/ark/docs/legacy/` | ARK explanatory material retained as engine documentation until canonicalized. |
| `internal/subjects/subjects.go` | tracked | Go module | Service: identity | `services/identity/` | Subject and identity rules are reusable identity language/infrastructure. |
| `internal/transport/nats.go` | tracked | Go module | Service: event bus/transport | `services/event-bus/` | Pub/sub and transport are reusable infrastructure. |
| `internal/transport/nats_test.go` | tracked | Go module | Service: event bus/transport | `services/event-bus/` | Pub/sub and transport are reusable infrastructure. |
| `internal/transport/redis.go` | tracked | Go module | Service: event bus/transport | `services/event-bus/` | Pub/sub and transport are reusable infrastructure. |
| `internal/transport/redis_test.go` | tracked | Go module | Service: event bus/transport | `services/event-bus/` | Pub/sub and transport are reusable infrastructure. |
| `internal/trisca/core.go` | tracked | Go module | Capability/service: measurement | `capabilities/measure/` | TRISCA is cross-cutting measurement/scoring capability used by ARK and others. |
| `internal/trisca/core_test.go` | tracked | Go module | Capability/service: measurement | `capabilities/measure/` | TRISCA is cross-cutting measurement/scoring capability used by ARK and others. |
| `internal/valor/core.go` | tracked | Go module | Engine: VALOR | `engines/valor/legacy/` | VALOR is a named engine responsibility, not ARK core. |
| `internal/valor/core_test.go` | tracked | Go module | Engine: VALOR | `engines/valor/legacy/` | VALOR is a named engine responsibility, not ARK core. |
| `internal/wiring/mqttbridge.go` | tracked | Go module | Engine legacy source | `engines/ark/legacy/internal/wiring/mqttbridge.go` | Historical ARK source retained pending extraction. |
| `internal/wiring/mqttbridge_test.go` | tracked | Go module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `meta/meta.go` | tracked | Go module | ARK core/egress runtime | `engines/ark/core/` | SD-ARK loop, API, command entrypoints, actions, and meta behavior implement ARK responsibilities until split. |
| `monitor-prod.sh` | tracked | Shell script | Operations | `operations/ark/` | Runtime deployment, provisioning, monitoring, or container infrastructure. |
| `packaging/linux/forge-app.desktop.in` | tracked | Template | Operations | `operations/ark/` | Runtime deployment, provisioning, monitoring, or container infrastructure. |
| `packaging/linux/forge-app.svg` | tracked | Image asset | Operations | `operations/ark/` | Runtime deployment, provisioning, monitoring, or container infrastructure. |
| `policy/ARK_CONSTITUTION.md` | tracked | Documentation | Engine documentation | `engines/ark/docs/legacy/` | ARK explanatory material retained as engine documentation until canonicalized. |
| `policy/ark_identity_rules.json` | tracked | JSON configuration/schema | Policy service input | `services/policy/ark/` | Reusable policy rules and policy code should be owned by the policy service. |
| `policy/ark_rules.json` | tracked | JSON configuration/schema | Policy service input | `services/policy/ark/` | Reusable policy rules and policy code should be owned by the policy service. |
| `policy/autonomy_rules.json` | tracked | JSON configuration/schema | Policy service input | `services/policy/ark/` | Reusable policy rules and policy code should be owned by the policy service. |
| `policy/autoscaler_rules.json` | tracked | JSON configuration/schema | Policy service input | `services/policy/ark/` | Reusable policy rules and policy code should be owned by the policy service. |
| `policy/budgets.json` | tracked | JSON configuration/schema | Policy service input | `services/policy/ark/` | Reusable policy rules and policy code should be owned by the policy service. |
| `policy/emitter_rules.json` | tracked | JSON configuration/schema | Policy service input | `services/policy/ark/` | Reusable policy rules and policy code should be owned by the policy service. |
| `policy/failure_classes.json` | tracked | JSON configuration/schema | Policy service input | `services/policy/ark/` | Reusable policy rules and policy code should be owned by the policy service. |
| `policy/import_registry.json` | tracked | JSON configuration/schema | Policy service input | `services/policy/ark/` | Reusable policy rules and policy code should be owned by the policy service. |
| `policy/integration_rules.json` | tracked | JSON configuration/schema | Policy service input | `services/policy/ark/` | Reusable policy rules and policy code should be owned by the policy service. |
| `policy/mesh_routing_rules.json` | tracked | JSON configuration/schema | Policy service input | `services/policy/ark/` | Reusable policy rules and policy code should be owned by the policy service. |
| `policy/placement_rules.md` | tracked | Documentation | Engine documentation | `engines/ark/docs/legacy/` | ARK explanatory material retained as engine documentation until canonicalized. |
| `policy/policy.go` | tracked | Go module | Policy service input | `services/policy/ark/` | Reusable policy rules and policy code should be owned by the policy service. |
| `preflight-checks.sh` | tracked | Shell script | Operations | `operations/ark/` | Runtime deployment, provisioning, monitoring, or container infrastructure. |
| `prometheus.yml` | untracked | YAML configuration | Operations | `operations/ark/` | Runtime deployment, provisioning, monitoring, or container infrastructure. |
| `pytest.ini` | tracked | Source/configuration | Developer/CI tooling | `tooling/ark/` | Repository automation and local developer controls. |
| `quick-start-prod.sh` | tracked | Shell script | Operations | `operations/ark/` | Runtime deployment, provisioning, monitoring, or container infrastructure. |
| `requirements.txt` | modified | Documentation | Developer/operations tooling | `tooling/ark/` | Build, verification, sync, and development automation. |
| `runtime/compiler.go` | tracked | Go module | Service: runtime | `services/runtime/` | Runtime middleware, toggles, and compilers are reusable execution infrastructure. |
| `runtime/compiler_test.go` | tracked | Go module | Service: runtime | `services/runtime/` | Runtime middleware, toggles, and compilers are reusable execution infrastructure. |
| `scripts/ai/apply_proposal.sh` | tracked | Shell script | Foundry tooling | `engines/foundry/legacy/` | AI repair/code-generation workflows are Foundry responsibility, not ARK reality preservation. |
| `scripts/ai/assembly_line.py` | tracked | Python module | Foundry tooling | `engines/foundry/legacy/` | AI repair/code-generation workflows are Foundry responsibility, not ARK reality preservation. |
| `scripts/ai/autonomous_repair.py` | tracked | Python module | Foundry tooling | `engines/foundry/legacy/` | AI repair/code-generation workflows are Foundry responsibility, not ARK reality preservation. |
| `scripts/ai/enqueue_repair_last_failure.sh` | tracked | Shell script | Foundry tooling | `engines/foundry/legacy/` | AI repair/code-generation workflows are Foundry responsibility, not ARK reality preservation. |
| `scripts/ai/enqueue_task.sh` | tracked | Shell script | Foundry tooling | `engines/foundry/legacy/` | AI repair/code-generation workflows are Foundry responsibility, not ARK reality preservation. |
| `scripts/ai/forge.py` | tracked | Python module | Foundry tooling | `engines/foundry/legacy/` | AI repair/code-generation workflows are Foundry responsibility, not ARK reality preservation. |
| `scripts/ai/local_codegen_loop.py` | tracked | Python module | Foundry tooling | `engines/foundry/legacy/` | AI repair/code-generation workflows are Foundry responsibility, not ARK reality preservation. |
| `scripts/ci/classify_todo.py` | tracked | Python module | Developer/operations tooling | `tooling/ark/` | Build, verification, sync, and development automation. |
| `scripts/ci/deploy_local.sh` | tracked | Shell script | Developer/operations tooling | `tooling/ark/` | Build, verification, sync, and development automation. |
| `scripts/ci/full_suite.sh` | tracked | Shell script | Developer/operations tooling | `tooling/ark/` | Build, verification, sync, and development automation. |
| `scripts/ci/lib.sh` | tracked | Shell script | Developer/operations tooling | `tooling/ark/` | Build, verification, sync, and development automation. |
| `scripts/ci/policy_gate.sh` | tracked | Shell script | Developer/operations tooling | `tooling/ark/` | Build, verification, sync, and development automation. |
| `scripts/ci/promote.sh` | tracked | Shell script | Developer/operations tooling | `tooling/ark/` | Build, verification, sync, and development automation. |
| `scripts/ci/recover.sh` | tracked | Shell script | Developer/operations tooling | `tooling/ark/` | Build, verification, sync, and development automation. |
| `scripts/ci/redteam.sh` | tracked | Shell script | Developer/operations tooling | `tooling/ark/` | Build, verification, sync, and development automation. |
| `scripts/ci/reliability_gate.py` | tracked | Python module | Developer/operations tooling | `tooling/ark/` | Build, verification, sync, and development automation. |
| `scripts/ci/run_once.sh` | tracked | Shell script | Developer/operations tooling | `tooling/ark/` | Build, verification, sync, and development automation. |
| `scripts/ci/smoke.sh` | tracked | Shell script | Developer/operations tooling | `tooling/ark/` | Build, verification, sync, and development automation. |
| `scripts/ci/snapshot_config.sh` | tracked | Shell script | Developer/operations tooling | `tooling/ark/` | Build, verification, sync, and development automation. |
| `scripts/ci/source_ingest_smoke.py` | tracked | Python module | Developer/operations tooling | `tooling/ark/` | Build, verification, sync, and development automation. |
| `scripts/ci/watch_loop.sh` | tracked | Shell script | Developer/operations tooling | `tooling/ark/` | Build, verification, sync, and development automation. |
| `scripts/deploy.sh` | tracked | Shell script | Developer/operations tooling | `tooling/ark/` | Build, verification, sync, and development automation. |
| `scripts/sync/online_sync.sh` | tracked | Shell script | Developer/operations tooling | `tooling/ark/` | Build, verification, sync, and development automation. |
| `tests/__init__.py` | tracked | Python module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `tests/agents/__init__.py` | tracked | Python module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `tests/agents/test_composio_agent.py` | tracked | Python module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `tests/agents/test_opencode_agent.py` | tracked | Python module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `tests/agents/test_openwolf_agent.py` | tracked | Python module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `tests/agents/test_rube_agent.py` | tracked | Python module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `tests/ark/__init__.py` | tracked | Python module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `tests/ark/test_autoscaler.py` | tracked | Python module | Service: scheduling/resource control | `services/scheduling/` | Budgeting and autoscaling are reusable bounded-execution controls. |
| `tests/ark/test_config.py` | tracked | Python module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `tests/ark/test_duck_client.py` | tracked | Python module | Service: storage/persistence | `services/storage/` | Storage and persistence are reusable services, not ARK-owned behavior. |
| `tests/ark/test_emitter_contracts.py` | tracked | Python module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `tests/ark/test_event_schema.py` | tracked | Python module | Contract | `contracts/ark/` | Schemas and interface language contain no durable ARK implementation once extracted. |
| `tests/ark/test_git_reconcile.py` | tracked | Python module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `tests/ark/test_gsb.py` | tracked | Python module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `tests/ark/test_import_audit.py` | tracked | Python module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `tests/ark/test_integrations.py` | tracked | Python module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `tests/ark/test_maintenance.py` | tracked | Python module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `tests/ark/test_mesh_registry.py` | tracked | Python module | Service: discovery/registry | `services/discovery/` | Capability registry and mesh discovery are reusable services. |
| `tests/ark/test_policy_engine.py` | tracked | Python module | Service: policy | `services/policy/` | Policy evaluation is reusable shared infrastructure. |
| `tests/ark/test_reducers.py` | tracked | Python module | ARK ephemeral | `engines/ark/ephemeral/` | Reducers, projections, and replay are derived/disposable views until proven. |
| `tests/ark/test_runtime_contracts.py` | tracked | Python module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `tests/ark/test_runtime_flow.py` | tracked | Python module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `tests/ark/test_security.py` | tracked | Python module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `tests/ark/test_subjects.py` | tracked | Python module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `tests/emitters/__init__.py` | tracked | Python module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `tests/emitters/test_homeassistant_emitter.py` | tracked | Python module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `tests/emitters/test_jellyfin_emitter.py` | tracked | Python module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `tests/emitters/test_unifi_emitter.py` | tracked | Python module | Tests | `engines/ark/tests/` | Tests should follow the classified owner; initially retained under ARK test migration. |
| `tests/replay/fixtures/real_world_sims.json` | tracked | JSON configuration/schema | ARK ephemeral | `engines/ark/ephemeral/` | Reducers, projections, and replay are derived/disposable views until proven. |
| `tests/replay/test_sd_ark_replay.py` | tracked | Python module | ARK ephemeral | `engines/ark/ephemeral/` | Reducers, projections, and replay are derived/disposable views until proven. |
| `traefik/dynamic.yml` | tracked | YAML configuration | Operations | `operations/ark/` | Runtime deployment, provisioning, monitoring, or container infrastructure. |
| `traefik/traefik.yml` | tracked | YAML configuration | Operations | `operations/ark/` | Runtime deployment, provisioning, monitoring, or container infrastructure. |
| `validate-prod.sh` | tracked | Shell script | Operations | `operations/ark/` | Runtime deployment, provisioning, monitoring, or container infrastructure. |
| `wiring-check.sh` | tracked | Shell script | Operations | `operations/ark/` | Runtime deployment, provisioning, monitoring, or container infrastructure. |
| `wiring-setup.sh` | tracked | Shell script | Operations | `operations/ark/` | Runtime deployment, provisioning, monitoring, or container infrastructure. |
