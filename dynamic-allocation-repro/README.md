# dynamicAllocation repro (2026-10-28)

YAMLs used to reproduce the prospect's "tasks never allocated" issue.
CLI: HyperExecute v0.2.363. All runs use the tests in `../tests` with a CLI-started tunnel.

Run from the repo root:

```sh
./hyperexecute --user "$LT_USERNAME" --key "$LT_ACCESS_KEY" --config dynamic-allocation-repro/<file>.yaml
```

| File | YAML | runson | Concurrency | Discovery | Job ID | Result |
|---|---|---|---|---|---|---|
| `v01-android-dynalloc-static.yaml` | 0.1 | linux | 1 | static | `a26729cb-a489-47de-a81e-c3d4ea23ca38`, `edb23220-99ba-4cdc-86b0-838f13e9d752` | COMPLETED (~1m) |
| `v01-android-dynalloc-local.yaml` | 0.1 | linux | 1 | local | `39f6d2a0-caf3-4873-99a1-48eb739c145e` | COMPLETED; CLI silently rewrote `local` to `static` |
| `v02-ios-c2-mobiledc-static.yaml` | 0.2 | ios | 2 | static | `d7619476-9998-4804-affa-ec1e298f345b` | Stuck in INITIATED, ABORTED at globalTimeout, 0s run time |
| `v02-ios-c2-nomobiledc-static.yaml` | 0.2 | ios | 2 | static | `304ac5e8-27bc-4ab7-9410-76d867883027` | Stuck in INITIATED, never RUNNING |
| `v02-ios-c2-nomobiledc-local.yaml` | 0.2 | ios | 2 | local | none | Rejected by CLI (exit 1): `ERR::YML::VAL Invalid yaml content: Dynamic allocation is only supported for static discovery` |

All files set `dynamicAllocation: true`.

## Findings

- YAML 0.2 rejects `mode: local` with `dynamicAllocation`, although the docs say it is supported. YAML 0.1 accepts it.
- The `mode: static` workaround passes validation, but the iOS 0.2 / concurrency 2 job is still never allocated a VM, with or without `region: us` / `mobileDC: true`.
- Not yet isolated: whether `dynamicAllocation`, `runson: ios`, the 0.2 `framework: appium` block or concurrency 2 is the trigger. Next run: `v02-ios-c2-nomobiledc-static.yaml` with `dynamicAllocation: false`.
- Separate CLI bug: `--no-track` with `tunnel: true` fails with `ERR::TNL::SPRT Tunnel mode is not supported with no-track-job flag.` but exits 0 (job `9c1fe6cb-a711-4d25-b06e-609377db63be`).

The iOS YAMLs list the same test twice in discovery so autosplit creates 2 tasks. The test itself opens an Android session (see `../conftest.py`), so these runs only check VM allocation, not iOS test results.
