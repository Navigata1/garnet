# Garnet Converter Assist Plan

Source file: `C:\Users\IslandDevCrew\Desktop\Garnet Opus 4.7 final\garnet\apps\garnet-studio\src\main.ts`
Language: **TypeScript** (`planned`)
Status: **active-assist-plan**

Current truth: this is not active conversion. It is deterministic, provider-optional planning evidence for Garnet-aware migration.

## Boundaries

- Provider required: false
- Model required: false
- Network required: false
- Source execution allowed: false
- Conversion active: false
- Deterministic converter available: false

## Risk Inventory

- **actor or async orchestration mapping** -> actor/orchestration mappings. Evidence: async, await, promise. Map concurrent control flow to Garnet orchestration constructs before emitting runnable code.
- **network or external capability boundary** -> CapCaps/capability boundaries. Evidence: file, exec. Declare capability boundaries and keep external effects behind explicit CapCaps.
- **type and ownership modeling** -> safe-mode ownership candidates. Evidence: class, interface, record. Inventory type shapes before choosing managed-mode or safe-mode ownership boundaries.

## Required Gates

- lineage per emitted node
- @sandbox default
- migrate_todo evidence
- garnet check
- dogfood readiness bundle
- human audit before unquarantine

## Next Steps

- Treat TypeScript as planned-only until a deterministic frontend, corpus tests, and CI gates land.
- Keep any future emitted Garnet output @sandbox by default.
- Preserve lineage per emitted node before treating output as conversion evidence.
- Emit migrate_todo evidence for unsupported constructs.
- Run `garnet check` before claiming translated source is valid.
- Preserve a dogfood readiness bundle for the attempted migration.
- Require human audit before unquarantine.

Do not treat this plan as an LLM-backed converter, broad-language frontend, or replacement for lineage, sandboxing, `garnet check`, dogfood readiness, and human audit.
