const state = {
  index: null,
  docsByPath: new Map(),
  selectedPath: null,
};

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];

async function fetchJson(url) {
  const response = await fetch(url);
  if (!response.ok) {
    let detail = `${response.status} ${response.statusText}`;
    try {
      const payload = await response.json();
      detail = `${payload.error_code}: ${payload.reason}`;
    } catch {
      // Keep the HTTP status text when the response is not JSON.
    }
    throw new Error(detail);
  }
  return response.json();
}

async function loadIndex() {
  try {
    setStatus("Indexing repository...");
    state.index = await fetchJson("/api/index");
    state.docsByPath = new Map(state.index.documents.map((doc) => [doc.path, doc]));
    renderAll();
    setStatus(`${state.index.summary.documents} documents indexed`);
  } catch (error) {
    showFatalError(error);
  }
}

function setStatus(text) {
  $("#statusStrip").textContent = text;
}

function renderAll() {
  renderTree();
  renderTasks();
  renderReports();
  renderEvents();
  renderPlatform();
  renderRepositories();
  renderProperty();
  renderValidation();
  renderCompiler();
  renderReview();
  renderDigitalTwin();
  renderGit();
  renderSettings();
  renderGraph();
}

function renderTree() {
  const filter = $("#treeFilter").value.trim().toLowerCase();
  $("#tree").replaceChildren(renderTreeNode(state.index.tree, filter, true));
}

function renderTreeNode(node, filter, isRoot = false) {
  const wrapper = document.createElement("div");
  wrapper.className = "tree-item";
  const children = node.children || [];
  const searchable = `${node.name || ""} ${node.path || ""} ${node.title || ""}`.toLowerCase();
  const childElements = children
    .map((child) => renderTreeNode(child, filter))
    .filter((child) => child.dataset.visible === "true");
  const visible = isRoot || !filter || searchable.includes(filter) || childElements.length > 0;
  wrapper.dataset.visible = String(visible);
  if (!visible) return wrapper;

  if (!isRoot) {
    const row = document.createElement("div");
    row.className = "tree-row";
    const indicator = document.createElement("span");
    indicator.textContent = children.length ? "▸" : "·";
    const name = document.createElement("div");
    name.innerHTML = `<div class="file-name">${escapeHtml(node.name)}</div><div class="file-meta">${escapeHtml(node.layer || node.path || "")}</div>`;
    row.append(indicator, name);
    row.addEventListener("click", (event) => {
      event.stopPropagation();
      if (node.path) openDocument(node.path);
      const childWrap = wrapper.querySelector(":scope > .tree-children");
      if (childWrap) {
        const hidden = childWrap.style.display === "none";
        childWrap.style.display = hidden ? "block" : "none";
        indicator.textContent = hidden ? "▾" : "▸";
      }
    });
    wrapper.append(row);
  }

  if (childElements.length) {
    const childWrap = document.createElement("div");
    childWrap.className = "tree-children";
    if (!isRoot) childWrap.style.display = filter ? "block" : "none";
    childElements.forEach((child) => childWrap.append(child));
    wrapper.append(childWrap);
  }
  return wrapper;
}

async function openDocument(path) {
  try {
    state.selectedPath = path;
    const payload = await fetchJson(`/api/document?path=${encodeURIComponent(path)}`);
    const doc = state.docsByPath.get(path);
    $("#currentPath").textContent = path;
    $("#currentLayer").textContent = doc ? doc.layer : "";
    $("#editorText").textContent = payload.text;
    renderInspector(doc);
    activateView("workspace");
  } catch (error) {
    setStatus(`Open failed: ${error.message}`);
  }
}

function renderInspector(doc) {
  const target = $("#inspectorContent");
  if (!doc) {
    target.textContent = "No document metadata available.";
    return;
  }
  target.innerHTML = `
    <dl>
      <dt>Title</dt><dd>${escapeHtml(doc.title)}</dd>
      <dt>Layer</dt><dd>${escapeHtml(doc.layer)}</dd>
      <dt>Path</dt><dd>${escapeHtml(doc.path)}</dd>
      <dt>Size</dt><dd>${doc.size} bytes</dd>
      <dt>Headings</dt><dd>${doc.headings.map(escapeHtml).join("<br>") || "None"}</dd>
      <dt>Links</dt><dd>${doc.links.length}</dd>
    </dl>
  `;
}

async function runSearch(query) {
  try {
    const payload = await fetchJson(`/api/search?q=${encodeURIComponent(query)}`);
    const container = $("#searchResults");
    container.replaceChildren();
    payload.results.forEach((result) => {
      const row = document.createElement("div");
      row.className = "result-row";
      row.innerHTML = `
        <div class="result-title">${escapeHtml(result.title)}</div>
        <div class="result-path">${escapeHtml(result.path)} · score ${result.score || 0}</div>
        <div class="mini">${escapeHtml(result.excerpt || "")}</div>
      `;
      row.addEventListener("click", () => openDocument(result.path));
      container.append(row);
    });
  } catch (error) {
    setStatus(`Search failed: ${error.message}`);
  }
}

function renderGraph() {
  const svg = $("#graphCanvas");
  svg.replaceChildren();
  const graph = state.index.graph;
  const width = svg.clientWidth || 900;
  const height = svg.clientHeight || 600;
  svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
  const nodes = graph.nodes.slice(0, 80).map((node, index) => {
    const angle = (index / Math.max(1, graph.nodes.length)) * Math.PI * 2;
    const radius = Math.min(width, height) * 0.38;
    return {
      ...node,
      x: width / 2 + Math.cos(angle) * radius,
      y: height / 2 + Math.sin(angle) * radius,
    };
  });
  const byId = new Map(nodes.map((node) => [node.id, node]));
  graph.edges.forEach((edge) => {
    const a = byId.get(edge.source);
    const b = byId.get(edge.target);
    if (!a || !b) return;
    const line = svgEl("line", { x1: a.x, y1: a.y, x2: b.x, y2: b.y, stroke: relationshipColor(edge.type), "stroke-width": 1, opacity: 0.45 });
    svg.append(line);
  });
  nodes.forEach((node) => {
    const group = svgEl("g", { class: "graph-node" });
    group.append(svgEl("circle", { cx: node.x, cy: node.y, r: 6, fill: layerColor(node.layer), stroke: "#101214", "stroke-width": 1 }));
    const text = svgEl("text", { x: node.x + 9, y: node.y + 4, fill: "#dfe7eb", "font-size": 10 });
    text.textContent = node.title.slice(0, 34);
    group.append(text);
    group.addEventListener("click", () => openDocument(node.path));
    svg.append(group);
  });
  $("#graphLegend").textContent = `${graph.nodes.length} nodes, ${graph.edges.length} relationships. Click a node to open its source.`;
}

function svgEl(name, attrs) {
  const element = document.createElementNS("http://www.w3.org/2000/svg", name);
  Object.entries(attrs).forEach(([key, value]) => element.setAttribute(key, value));
  return element;
}

function layerColor(layer) {
  const colors = {
    doctrine: "#7cc7a2",
    contracts: "#8fb7ff",
    schemas: "#e7b95b",
    governance: "#d99bf5",
    domains: "#80d5ff",
    lifecycle: "#eeaa7b",
    registries: "#aacb72",
    operations: "#d0d6dd",
  };
  return colors[layer] || "#9aa8b2";
}

function relationshipColor(type) {
  const colors = {
    implements: "#7cc7a2",
    depends_on: "#e7b95b",
    composes: "#8fb7ff",
    extends: "#d99bf5",
    generated_from: "#ee7b75",
    verified_by: "#78d19a",
  };
  return colors[type] || "#64707a";
}

function renderValidation() {
  const validation = state.index.validation;
  const counts = validation.counts || {};
  $("#validationSummary").innerHTML = `
    ${metric("Status", validation.status)}
    ${metric("Errors", counts.error || 0)}
    ${metric("Warnings", counts.warning || 0)}
    ${metric("Diagnostics", validation.diagnostics.length)}
  `;
  const list = $("#diagnostics");
  list.replaceChildren();
  if (!validation.diagnostics.length) {
    const row = document.createElement("div");
    row.className = "diag-row severity-info";
    row.textContent = "No validation diagnostics.";
    list.append(row);
    return;
  }
  validation.diagnostics.forEach((diag) => {
    const row = document.createElement("div");
    row.className = `diag-row severity-${diag.severity}`;
    row.innerHTML = `<strong>${escapeHtml(diag.rule)} · ${escapeHtml(diag.severity)}</strong><span>${escapeHtml(diag.path)}</span><span class="mini">${escapeHtml(diag.message)}</span>`;
    list.append(row);
  });
}

function metric(label, value) {
  return `<div class="metric"><span>${escapeHtml(label)}</span><strong>${escapeHtml(String(value))}</strong></div>`;
}

function renderCompiler() {
  $("#compilerTargets").replaceChildren(...state.index.compiler.targets.map((target) => card(target.name, target.state, "Compiler pipeline stage")));
}

function renderReview() {
  const reports = state.index.reports;
  const cards = [
    card("Repository Health", reports.repositoryHealth, `${reports.documentCount} indexed documents`),
    card("Validation Diagnostics", String(reports.validationDiagnostics), "Actionable repository diagnostics"),
    card("Doctrine Coverage", String(reports.coverage.doctrine), "Doctrine documents"),
    card("Pattern Coverage", String(reports.coverage.patterns), "Pattern-bearing documents"),
  ];
  $("#reviewContent").replaceChildren(...cards);
}

function renderDigitalTwin() {
  const docs = state.index.documents;
  const readinessDocs = docs.filter((doc) => /digital-twin|readiness|spatial|reality-state/i.test(doc.path));
  const cards = [
    card("Readiness Sources", String(readinessDocs.length), "Documents that define twin readiness"),
    card("Scope Identity", "modeled", "Universal Scope and physical scope contracts"),
    card("Generated Twins", "extension-slot", "Backend extension target"),
    card("Reality Sync", "source-backed", "Observation and service records remain canonical"),
  ];
  $("#digitalTwinContent").replaceChildren(...cards);
}

function renderPlatform() {
  const platform = state.index.platform;
  const active = platform.services.filter((service) => service.state === "active").length;
  const cards = [
    card("Service Architecture", `${active}/${platform.services.length} active`, "UI-independent services with stable API surfaces"),
    card("Workspace", platform.workspace.name, `${platform.workspace.repositories.length} repositories in local workspace`),
    card("Event Bus", `${platform.events.length} events`, "Recent internal platform events"),
    card("Local First", "enabled", "No cloud dependency, no hidden canonical state"),
  ];
  $("#platformContent").replaceChildren(...cards, ...platform.services.map((service) => card(service.name, service.state, "Service API surface")));
}

function renderRepositories() {
  const repos = state.index.platform.repositories;
  const cards = repos.map((repo) => card(repo.name, repo.health, `${repo.kind} · ${repo.path} · deps: ${repo.dependencies.join(", ") || "none"}`));
  $("#repositoriesContent").replaceChildren(...cards);
}

function renderProperty() {
  const property = state.index.platform.property;
  const instantiation = state.index.platform.workspace;
  const cards = [
    card("Property Support", property.status, property.repositorySupport),
    card("Object Types", String(property.objectTypes.length), property.objectTypes.join(", ")),
    card("Workspace Link", instantiation.name, "Property repositories can open alongside Build Bible and Operations"),
    card("Instantiation", "preview-only", "Pattern-to-specification workflow is designed but does not write canonical files yet"),
  ];
  $("#propertyContent").replaceChildren(...cards);
}

function renderGit() {
  const list = $("#gitContent");
  list.replaceChildren();
  const git = state.index.git;
  if (!git.available) {
    list.textContent = git.error || "Git unavailable.";
    return;
  }
  if (!git.entries.length) {
    list.textContent = "No changes.";
    return;
  }
  git.entries.forEach((entry) => {
    const row = document.createElement("div");
    row.className = "git-row";
    row.textContent = entry;
    list.append(row);
  });
}

function renderSettings() {
  const extensions = state.index.extensions;
  const cards = [
    card("Plugin Manager", "declared", extensions.pluginManager.join(", ")),
    card("AI Gateway", "abstract", extensions.aiGateway.join(", ")),
    card("Jarvis Interface", "future-ready", extensions.jarvisInterface.join(", ")),
    card("Hidden State", "none", "Index state is in memory; source remains in Git"),
  ];
  $("#settingsContent").replaceChildren(...cards);
}

function renderTasks() {
  const tasks = [
    ["Validate repository", "Run schema, reference, README, and layer checks"],
    ["Review EDRs", "Open engineering decision records and pending reviews"],
    ["Compile plans", "Inspect future backend target slots"],
    ["Inspect Git changes", "Review canonical source changes before commit"],
  ];
  $("#tasksList").replaceChildren(...tasks.map(([name, detail]) => taskRow(name, detail)));
}

function renderReports() {
  const reports = [
    ["Architecture Health", "Repository review and freeze status"],
    ["Traceability", "Relationship density and broken references"],
    ["Digital Twin Readiness", "Source readiness for generated twins"],
    ["Validation Health", "Diagnostics from repository validation"],
  ];
  $("#reportsList").replaceChildren(...reports.map(([name, detail]) => reportRow(name, detail)));
}

function renderEvents() {
  const events = state.index.platform.events || [];
  const rows = events.slice().reverse().map((event) => reportRow(event.type, `${event.source} · ${new Date(event.timestamp * 1000).toLocaleTimeString()}`));
  $("#eventsList").replaceChildren(...rows);
}

function card(title, value, detail) {
  const element = document.createElement("div");
  element.className = "card";
  element.innerHTML = `<h3>${escapeHtml(title)}</h3><p><span class="badge">${escapeHtml(value)}</span></p><p>${escapeHtml(detail)}</p>`;
  return element;
}

function taskRow(name, detail) {
  const row = document.createElement("div");
  row.className = "task-row";
  row.innerHTML = `<strong>${escapeHtml(name)}</strong><span class="mini">${escapeHtml(detail)}</span>`;
  return row;
}

function reportRow(name, detail) {
  const row = document.createElement("div");
  row.className = "report-row";
  row.innerHTML = `<strong>${escapeHtml(name)}</strong><span class="mini">${escapeHtml(detail)}</span>`;
  return row;
}

function activateView(viewName) {
  $$(".toolbar button").forEach((button) => button.classList.toggle("active", button.dataset.view === viewName));
  $$(".view").forEach((view) => view.classList.remove("active"));
  $(`#${viewName}View`).classList.add("active");
  if (viewName === "graph") requestAnimationFrame(renderGraph);
}

function activatePanel(panelName) {
  $$(".activity-bar button").forEach((button) => button.classList.toggle("active", button.dataset.panel === panelName));
  $$(".sidebar .panel").forEach((panel) => panel.classList.add("hidden"));
  $(`#${panelName}Panel`).classList.remove("hidden");
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function showFatalError(error) {
  console.error(error);
  setStatus(`Error: ${error.message}`);
  $("#editorText").textContent = `Build Bible Studio could not load the repository.\n\n${error.message}`;
  $("#currentPath").textContent = "Startup error";
}

function bindEvents() {
  $("#refreshButton").addEventListener("click", loadIndex);
  $("#treeFilter").addEventListener("input", renderTree);
  $("#searchInput").addEventListener("input", (event) => runSearch(event.target.value));
  $$(".quick-queries button").forEach((button) => {
    button.addEventListener("click", () => {
      $("#searchInput").value = button.dataset.query;
      runSearch(button.dataset.query);
    });
  });
  $$(".toolbar button").forEach((button) => button.addEventListener("click", () => activateView(button.dataset.view)));
  $$(".activity-bar button").forEach((button) => button.addEventListener("click", () => activatePanel(button.dataset.panel)));
}

bindEvents();
loadIndex();
