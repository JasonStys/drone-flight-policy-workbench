<!-- Jason Stys: full local policy application setup, genuine file workflows and native acceptance boundaries. -->
# Desktop application

The 0.2.0 source candidate packages the existing complete policy workbench, its browser UI, SQLite and the checksum-verified OPA 1.21.3 executable. It is an unsigned portable application, not a clean-install-tested installer. Downloads may be published only after exact-source hosted/native checks; a local dirty candidate is never a published-release identity.

## Open and provision

Extract the entire archive into a new directory: Windows uses ZIP; Linux/macOS use tar.gz to retain executable modes and internal links. Run `DroneFlightPolicyWorkbench.exe` on Windows or `DroneFlightPolicyWorkbench` on POSIX. Normal launch takes no preset-scenario arguments.

The native owner window opens a per-user application-data profile. Choose a new empty folder or this application's identified existing profile. Unknown nonempty folders, symlink profiles/database files and a second simultaneous owner are refused without deleting them. The signed-in OS owner is trusted administration: create the first administrator with a username and confirmed password, then add named operator/reviewer accounts as needed. There is no default account or anonymous HTTP registration. Do not share the OS session with untrusted people.

Choose **Open full application** and sign in using an account just created. The application binds its own 127.0.0.1 ephemeral port; it never adopts an existing service. Keep the owner window open. Closing a browser tab does not stop the service. Choose **Quit application** in the native window; active work drains before the profile lock is released. A busy Quit retains the owner window and lock. Startup failure explains that Quit/reopen is required. Password fields clear after provisioning attempts; no password is accepted on the console control pipe.

## Real file and policy workflow

1. As operator or administrator, choose **Open operation JSON**. A bounded UTF-8 object or an exported report's `operation` member populates the editable operation draft. Edit its claims and synthetic exercise time, then choose **Evaluate evidence**. File loading alone saves nothing.
2. An administrator can choose **Open policy JSON (administrator)**, edit that draft and **Preview draft impact**. Compare the same operation/time under the active and proposed rules. For example, lowering the wind cap below a supplied wind measurement must block exactly that configured wind check; missing authorization evidence remains unknown. No policy, report, review or audit record is saved by preview.
3. Download operation/policy draft JSON or the full comparison for review. Publishing remains a separate explicit administrator action, creates an immutable policy version and makes prior sign-off eligibility stale. Import does not restore accounts, evaluation history, reviews or policies implicitly.
4. A different designated reviewer can acknowledge only current satisfied evidence. A missing-evidence hold cannot be acknowledged. Review notes use the existing 1–80-character factual-label contract, with visible allowed-character help. Download the original evidence report and independent acknowledgement. Every status still says `flight_authorization: false`.

File inputs are limited to 60,000 bytes of strict UTF-8 JSON, finite values, bounded depth/work and an object root. Invalid files retain the previous draft and invalidate comparison controls. Typing, a newer file choice, refresh, logout or a changed asynchronous context prevents an older file read from overwriting current work. Operators cannot load policy standards by forcing a disabled file event. Backend type/unit/role/revision checks remain authoritative.

The configured-checks table is a named keyboard-focusable scrolling region at narrow widths. Its geometry/data are unchanged; focus it and use arrow keys to read columns. Help summaries have a 32px minimum touch target. Existing prepared fictional examples remain optional inputs inside this full application.

## Build and verify

Use final Python 3.14.10 or a later reviewed 3.14 security patch, Node 24 and the committed hash locks. Install `requirements-dev.lock` and `requirements-package.lock`, install npm dependencies using the lock, explicitly run `python tools/fetch_opa.py`, then `npm run build`. Run `python tools/package_app.py --output-root .runtime/portable-UNIQUE`. The output must be new. CI refuses dirty source; `--allow-dirty` is only an honestly labelled local development candidate.

The packager includes real Python/Tcl/Tk/package/OPA terms, a coherent 0.2.0 source/version/runtime identity and the verified native OPA binary. It safely extracts the produced archive into an unrelated temporary directory, launches that actual executable without Python/Node on its application PATH, checks frozen Tk identity and readiness nonce, then drives actual compiled-application import/preview/independent-review/export with Chromium. No source server fallback, preset report or mocked API is used. It checks foreign Host/Origin refusal, absence of anonymous setup, private cookie scope, 390 px keyboard table access and WCAG 2.2 AA, actual owner Quit 0, listener closure and account/report persistence. The portable checksum is emitted only after success.

Source tests separately use the real UI/service in Chromium, Firefox, WebKit and mobile WebKit. Native widget tests exercise minimum-window/footer controls; compiled console mode exercises the same owned service and completion-based stop. The frozen native button/default OS-browser/shortcut path is not claimed as an automated clean-install or manual desktop activation test. Linux/macOS native results require their own hosted jobs, not inference from Windows.

## Limits

This is configured synthetic evidence review, not flight permission, a legal compliance decision, a safety verdict, airworthiness assurance, live-aircraft control or current airspace monitoring. Supplied claims and reviewer attestations may be wrong. OPA rules are trusted fixed source; users supply data-only JSON, not Rego or command plugins. SQLite and media-free local exports are not encrypted by this app. The OS administrator and designated organizational roles remain trusted. Cookie namespaces prevent accidental profile collision; localhost ports do not provide cookie confidentiality from hostile local services. Do not expose the loopback service with a LAN bind, proxy or tunnel. No Docker, autopilot, telemetry feed or paid service is used.
