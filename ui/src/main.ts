/** @file Jason Stys: private local policy workflow, safe DOM rendering and stale-request guards; lines: docs/SOURCE_MAP.md. */
import "./style.css";
import {
  type User,
  type Report,
  type Result,
  canReview,
  counts,
  statusLabel,
  reasonLabel,
} from "./view";
interface Rule {
  id: string;
  title: string;
  fact: string;
  source_url: string;
  reference: string;
  comparator: string;
  expected: boolean | number;
  when_fact: string | null;
}
interface Policy {
  name: string;
  rules: Rule[];
}
interface Workspace {
  version: number;
  policy: Policy;
  history: { id: number; version: number; creator: string; created: string }[];
  audit: { actor: string; event: string; version: number; at: string }[];
}
const root = document.querySelector<HTMLDivElement>("#app")!;
// Fixed template only. Imported values are appended as text nodes or validated HTTPS links.
root.innerHTML = `<header><a class="brand" href="#main">F / P <span>DRONE FLIGHT<br>POLICY WORKBENCH</span></a><span class="tag">EVIDENCE BEFORE ASSUMPTION</span></header>
<main id="main"><section class="intro"><p class="eyebrow">PREFLIGHT / GOVERNANCE / ETHICAL USE</p><h1>Make every hold<br>explainable.</h1><p>Review configured evidence, understand what is missing, and preserve the policy version behind each decision.</p></section><aside class="notice"><strong>Synthetic review lab — never flight permission.</strong> These are example organizational checks, not a complete ruleset, legal advice, airworthiness assessment or FAA authorization. Real approvals must be verified through official services.</aside>
<section id="login-panel" class="panel login"><h2>Private local workspace</h2><p>No public registration. A workstation administrator provisions operator, reviewer and administrator accounts through the local CLI.</p><form id="login-form"><label for="username">Username</label><input id="username" autocomplete="username" required minlength="3" maxlength="40"/><label for="password">Password</label><input id="password" type="password" autocomplete="current-password" required maxlength="128"/><button>Sign in</button></form></section>
<p id="message" role="status" aria-live="polite">Sign in to review synthetic evidence.</p>
<div id="workspace" hidden><div class="identity"><span id="identity"></span><div><button id="refresh" class="secondary">Refresh workspace</button><button id="logout" class="secondary">Sign out</button></div></div>
<section class="summary panel"><div><p class="eyebrow">ACTIVE POLICY</p><h2 id="policy-name"></h2><p id="version"></p></div><div id="outcome"><h2>No current assessment</h2><p>Edit or load an operation, then evaluate.</p></div></section>
<section class="columns"><div class="panel"><div class="panel-head"><h2>Operation evidence</h2><span class="tag">SYNTHETIC CLOCK / SI UNITS</span></div><label for="scenario">Example case</label><select id="scenario"><option value="inspection">Infrastructure inspection</option><option value="missing-approval">Flood survey — missing approval evidence</option><option value="privacy-hold">Sensitive inspection — privacy hold</option><option value="expired-record">Emergency exercise — expired record</option></select><label for="operation">Operation JSON</label><textarea id="operation" rows="15" spellcheck="false"></textarea><div class="buttons"><button id="evaluate">Evaluate evidence</button><button id="export" class="secondary" disabled>Export evidence</button></div><p class="muted">Claims marked attested are supplied by a person, not independently verified by this application. Unknown facts remain unknown.</p></div>
<div class="panel"><div class="panel-head"><h2>Versioned policy</h2><span id="policy-role" class="tag"></span></div><label for="policy">Policy JSON</label><textarea id="policy" rows="15" spellcheck="false"></textarea><div class="buttons"><button id="publish" class="secondary">Publish policy version</button></div><p class="muted">Only administrators can publish. Previous versions and reports remain immutable. Publishing invalidates prior sign-off eligibility; it never rewrites history.</p><details><summary>How to interpret this workbench</summary><p>Use the four fictional examples or edit their bounded JSON. Time values are an explicit synthetic exercise clock, not current legal status. Source links are research references, not evidence that a specific approval exists.</p><p>Satisfied means the configured subset of evidence checks passed. Blocked means a configured check failed or evidence expired. Requires review means context or evidence is missing, conflicting, unknown, stale, future-dated or unattested. No status authorizes a flight.</p><p>Conditional checks also require current evidence. If a condition is unknown, the requirement remains under review. Administrators publish data-only rules; arbitrary Rego, scripts, files and URLs to fetch are not accepted.</p><p>Operators see their own reports. Designated reviewers and administrators can access organizational reports. Only a different reviewer can acknowledge current, satisfied evidence. Acknowledgement is a record of review, not a government approval.</p></details></div></section>
<section class="panel evidence"><div class="panel-head"><h2>Check-by-check evidence</h2><span id="report-label">No report selected</span></div><p id="report-state" class="muted"></p><div class="table-scroll"><table><caption>Configured checks and source references</caption><thead><tr><th scope="col">Check</th><th scope="col">Outcome</th><th scope="col">Reason</th><th scope="col">Research reference</th></tr></thead><tbody id="checks"></tbody></table></div><div id="review-controls"><label for="review-note">Review note — short factual acknowledgement</label><input id="review-note" maxlength="80" value="Synthetic evidence reviewed"/><div class="buttons"><button id="acknowledge" disabled>Acknowledge evidence</button><button id="reject" class="secondary" disabled>Record rejection</button></div></div></section>
<section class="columns history"><div class="panel"><h2>Immutable evaluation history</h2><ul id="history"></ul></div><div class="panel"><h2>Organizational audit</h2><ul id="audit"></ul></div></section></div>
<details class="panel help"><summary>Setup, privacy and help</summary><p>Build the UI, install the checksum-verified OPA runtime, initialize a local workspace, then provision accounts through the documented CLI. The source repository includes setup, API, test, security and recovery guides.</p><p>The service stays on loopback. Passwords are Argon2id hashes; opaque sessions are stored hashed. No analytics, remote scripts, ads, cloud AI or third-party runtime requests. SQLite and local exports must be protected by your workstation permissions; an OS administrator is trusted. Do not expose this lab on a network or enter sensitive operational data.</p></details></main>
<footer><span>Designed & engineered by <strong>Jason Stys</strong></span><a href="https://github.com/JasonStys/drone-flight-policy-workbench" rel="noreferrer">Source & help</a><a href="https://github.com/JasonStys" rel="noreferrer">GitHub / Contact</a><a href="https://www.linkedin.com/in/jason-stys-31b30b351/" rel="noreferrer">LinkedIn</a></footer>`;
/** Resolve only fixed application elements. */
function el<T extends HTMLElement>(id: string): T {
  return document.getElementById(id) as T;
}
/** Render arbitrary server/text content as inert text. */
function text(tag: string, value: string): HTMLElement {
  const node = document.createElement(tag);
  node.textContent = value;
  return node;
}
let user: User | null = null;
let workspace: Workspace | null = null;
let report: Report | null = null;
let templates: Record<string, unknown> = {};
let revision = 0;
let policyDraftVersion = 0;
let busy = false;
/** All writes include the server-issued CSRF token; browser supplies the exact Origin. */
async function api(path: string, body?: unknown): Promise<unknown> {
  const response = await fetch(path, {
    method: body === undefined ? "GET" : "POST",
    headers:
      body === undefined
        ? {}
        : {
            "Content-Type": "application/json",
            "X-CSRF-Token": user?.csrf ?? "",
          },
    body: body === undefined ? undefined : JSON.stringify(body),
    signal: AbortSignal.timeout(15000),
  });
  const result = await response.json();
  if (!response.ok) throw new Error(result.detail ?? "Request failed");
  return result;
}
/** Never leave old evidence downloadable/reviewable after edits or failed work. */
function invalidate(): void {
  revision += 1;
  report = null;
  el<HTMLButtonElement>("export").disabled = true;
  el<HTMLButtonElement>("acknowledge").disabled = true;
  el<HTMLButtonElement>("reject").disabled = true;
  el("checks").replaceChildren();
  el("outcome").replaceChildren(
    text("h2", "No current assessment"),
    text("p", "Inputs changed or no report selected."),
  );
  el("report-label").textContent = "No report selected";
  el("report-state").textContent = "";
}
/** One UI mutation at a time; explicit progress avoids old completion messages during work. */
async function action(task: () => Promise<void>): Promise<void> {
  if (busy) return;
  busy = true;
  el("message").textContent = "Working…";
  ["evaluate", "publish", "refresh", "logout", "acknowledge", "reject"].forEach(
    (id) => (el<HTMLButtonElement>(id).disabled = true),
  );
  try {
    await task();
  } catch (error) {
    el("message").textContent =
      `Request failed: ${error instanceof Error ? error.message : "unknown error"}`;
  } finally {
    busy = false;
    permissions();
  }
}
/** Restore controls according to current server identity and selected report; backend enforces again. */
function permissions(): void {
  el<HTMLButtonElement>("evaluate").disabled = !user;
  el<HTMLButtonElement>("refresh").disabled = !user;
  el<HTMLButtonElement>("logout").disabled = !user;
  el<HTMLButtonElement>("publish").disabled = user?.role !== "admin";
  el<HTMLTextAreaElement>("policy").readOnly = user?.role !== "admin";
  el<HTMLButtonElement>("acknowledge").disabled = !(
    user &&
    report &&
    canReview(user, report, true)
  );
  el<HTMLButtonElement>("reject").disabled = !(
    user &&
    report &&
    canReview(user, report, false)
  );
}
/** Refresh policy/history without conflating saved historical evidence and a new draft. */
async function refresh(preserveDraft = false): Promise<void> {
  workspace = (await api("/api/workspace")) as Workspace;
  el("policy-name").textContent = workspace.policy.name;
  el("version").textContent =
    `Version ${workspace.version} · data-only organizational policy`;
  if (!preserveDraft || user!.role !== "admin") {
    el<HTMLTextAreaElement>("policy").value = JSON.stringify(
      workspace.policy,
      null,
      2,
    );
    policyDraftVersion = workspace.version;
  }
  el("identity").textContent = `${user!.name} / ${user!.role}`;
  el("policy-role").textContent =
    user!.role === "admin"
      ? `ADMIN · DRAFT v${policyDraftVersion}`
      : "READ ONLY";
  el("history").replaceChildren();
  workspace.history.forEach((item) => {
    const node = text("li", "");
    const button = text(
      "button",
      `Report ${item.id} · policy v${item.version} · ${item.creator}`,
    );
    button.className = "history-link";
    button.addEventListener(
      "click",
      () =>
        void action(async () => {
          invalidate();
          if (await loadReport(item.id, revision))
            el("message").textContent =
              "Historical evidence loaded with original policy and input.";
        }),
    );
    node.append(button);
    el("history").append(node);
  });
  el("audit").replaceChildren(
    ...workspace.audit.map((item) =>
      text("li", `${item.event} · v${item.version} · ${item.actor}`),
    ),
  );
  if (!workspace.audit.length)
    el("audit").append(
      text(
        "li",
        "Audit is restricted to designated organizational reviewers and administrators.",
      ),
    );
}
/** Show current or explicitly selected historical report using its original source-linked policy. */
function renderReport(): void {
  if (!report) return;
  const result: Result = report.result;
  const summary = counts(result.checks);
  el("outcome").replaceChildren(
    text("h2", statusLabel(result.status)),
    text(
      "p",
      `${summary.satisfied} satisfied · ${summary.blocked} blocked · ${summary.requires_review} review`,
    ),
  );
  el("report-label").textContent =
    `Report ${report.id} · original policy v${report.version}`;
  el("report-state").textContent =
    `${report.stale ? "STALE POLICY — re-evaluation required. " : ""}${report.review ? `Review: ${report.review.decision} by ${report.review.actor}. ` : "Independent review not yet recorded. "}${result.notice}`;
  el("checks").replaceChildren();
  const policy = report.policy as Policy;
  result.checks.forEach((check) => {
    const rule = policy.rules.find((r) => r.id === check.id)!;
    const row = document.createElement("tr");
    row.append(
      text("td", rule.title),
      text("td", statusLabel(check.status)),
      text("td", reasonLabel(check.reason)),
    );
    const source = text("td", "");
    const link = text("a", rule.reference) as HTMLAnchorElement;
    link.href = rule.source_url;
    link.rel = "noreferrer";
    source.append(link);
    row.append(source);
    el("checks").append(row);
  });
  el<HTMLButtonElement>("export").disabled = false;
}
/** Check revision after the final asynchronous fetch as well, including historical/review refreshes. */
async function loadReport(
  identifier: number,
  requested: number,
): Promise<boolean> {
  const selected = (await api(`/api/evaluations/${identifier}`)) as Report;
  if (requested !== revision) {
    el("message").textContent =
      "Draft changed during report loading; obsolete evidence was not restored.";
    return false;
  }
  report = selected;
  renderReport();
  return true;
}
/** Initialize only after successful authenticated identity lookup/login; keep credentials out of storage. */
async function signedIn(): Promise<void> {
  templates = (await api("/api/examples")) as Record<string, unknown>;
  el<HTMLTextAreaElement>("operation").value = JSON.stringify(
    templates.inspection,
    null,
    2,
  );
  invalidate();
  await refresh();
  el("login-panel").hidden = true;
  el("workspace").hidden = false;
  el("message").textContent =
    "Signed in. Load a case and evaluate its evidence.";
  permissions();
}
el<HTMLFormElement>("login-form").addEventListener("submit", (event) => {
  event.preventDefault();
  void action(async () => {
    try {
      user = (await api("/api/login", {
        username: el<HTMLInputElement>("username").value,
        password: el<HTMLInputElement>("password").value,
      })) as User;
      await signedIn();
    } finally {
      el<HTMLInputElement>("password").value = "";
    }
  });
});
el("scenario").addEventListener("change", () => {
  invalidate();
  el<HTMLTextAreaElement>("operation").value = JSON.stringify(
    templates[el<HTMLSelectElement>("scenario").value],
    null,
    2,
  );
  el("message").textContent =
    "Example loaded. Evaluate to create a new immutable report.";
});
[el("operation"), el("policy")].forEach((node) =>
  node.addEventListener("input", () => {
    invalidate();
    el("message").textContent = "Draft changed. Previous evidence cleared.";
  }),
);
el("evaluate").addEventListener(
  "click",
  () =>
    void action(async () => {
      invalidate();
      const requested = revision;
      const operation = JSON.parse(el<HTMLTextAreaElement>("operation").value);
      const result = (await api("/api/evaluations", {
        version: workspace!.version,
        operation,
      })) as { id: number };
      await refresh(true);
      if (requested !== revision) {
        el("message").textContent =
          "Draft changed during evaluation; saved history retained but obsolete output not displayed.";
        return;
      }
      if (await loadReport(result.id, requested))
        el("message").textContent =
          "Evaluation saved. Review every hold and limitation.";
    }),
);
el("publish").addEventListener(
  "click",
  () =>
    void action(async () => {
      invalidate();
      const requested = revision;
      const published = (await api("/api/policies", {
        expected_version: policyDraftVersion,
        policy: JSON.parse(el<HTMLTextAreaElement>("policy").value),
      })) as { version: number };
      policyDraftVersion = published.version;
      await refresh(requested !== revision);
      el("message").textContent =
        requested === revision
          ? "New immutable policy version published. Earlier reviews are stale."
          : "Policy version published; your later draft edits were preserved.";
    }),
);
el("refresh").addEventListener(
  "click",
  () =>
    void action(async () => {
      invalidate();
      await refresh();
      el("message").textContent =
        "Workspace refreshed. Load or evaluate a report.";
    }),
);
for (const [id, decision] of [
  ["acknowledge", "acknowledge"],
  ["reject", "reject"],
])
  el(id).addEventListener(
    "click",
    () =>
      void action(async () => {
        const identifier = report!.id;
        const requested = revision;
        await api(`/api/evaluations/${identifier}/review`, {
          decision,
          note: el<HTMLInputElement>("review-note").value,
        });
        const loaded = await loadReport(identifier, requested);
        await refresh(true);
        if (loaded)
          el("message").textContent =
            "Independent review recorded. This is not flight authorization.";
      }),
  );
el("logout").addEventListener(
  "click",
  () =>
    void action(async () => {
      await api("/api/logout", {});
      user = null;
      workspace = null;
      templates = {};
      invalidate();
      el<HTMLTextAreaElement>("operation").value = "";
      el<HTMLTextAreaElement>("policy").value = "";
      el("history").replaceChildren();
      el("audit").replaceChildren();
      el("workspace").hidden = true;
      el("login-panel").hidden = false;
      el("message").textContent = "Signed out. Session revoked.";
    }),
);
el("export").addEventListener("click", () => {
  if (!report) return;
  const url = URL.createObjectURL(
    new Blob([JSON.stringify(report, null, 2)], { type: "application/json" }),
  );
  const link = document.createElement("a");
  link.href = url;
  link.download = `policy-evidence-${report.id}.json`;
  link.click();
  URL.revokeObjectURL(url);
});
// Resume an existing local session without saving passwords/tokens in browser localStorage.
void (async () => {
  try {
    user = (await api("/api/me")) as User;
    await signedIn();
  } catch {
    permissions();
  }
})();
