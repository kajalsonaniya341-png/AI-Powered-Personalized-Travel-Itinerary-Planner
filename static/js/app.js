/* AI-Powered Personalized Travel Itinerary Planner - frontend.
 * A small single-page app using hash routes (#/plan, #/results, ...).
 * All calls go to the FastAPI backend under /api. If you host the frontend separately,
 * set window.APP_API_BASE = "https://your-backend.example.com" before this script loads.
 */
const API_BASE = window.APP_API_BASE || "";
const app = document.getElementById("app");
const INTERESTS = [
  ["history", "History"], ["adventure", "Adventure"], ["nature", "Nature"], ["food", "Food"],
  ["culture", "Culture"], ["shopping", "Shopping"], ["religious", "Religious places"],
  ["museums", "Museums"], ["wildlife", "Wildlife"],
];
const ICONS = { history: "🏰", culture: "🎭", architecture: "🏛️", nature: "🌿", adventure: "🧗", food: "🍛",
  shopping: "🛍️", religious: "🛕", museums: "🖼️", wildlife: "🦌" };
let currentMap = null;

/* ---------- helpers ---------- */
const esc = (v) => String(v ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const inr = (n) => (n === null || n === undefined ? "N/A" : "₹" + Number(n).toLocaleString("en-IN"));
const cap = (s) => s.charAt(0).toUpperCase() + s.slice(1);
const spinner = (msg = "Loading…") => `<div class="spinner" role="status" aria-label="${esc(msg)}"></div>`;

function toast(msg) {
  const el = document.getElementById("toast");
  el.textContent = msg; el.hidden = false;
  clearTimeout(toast.t); toast.t = setTimeout(() => (el.hidden = true), 3500);
}
const getToken = () => localStorage.getItem("tp_token");
const getUser = () => { try { return JSON.parse(localStorage.getItem("tp_user")); } catch { return null; } };
function setSession(data) { localStorage.setItem("tp_token", data.access_token); localStorage.setItem("tp_user", JSON.stringify(data.user)); }
function clearSession() { localStorage.removeItem("tp_token"); localStorage.removeItem("tp_user"); }

async function api(path, { method = "GET", body, auth = false } = {}) {
  const headers = {};
  if (body) headers["Content-Type"] = "application/json";
  if (auth) {
    if (!getToken()) throw Object.assign(new Error("Please log in to continue."), { status: 401 });
    headers.Authorization = "Bearer " + getToken();
  }
  let res;
  try {
    res = await fetch(API_BASE + path, { method, headers, body: body ? JSON.stringify(body) : undefined });
  } catch {
    throw new Error("Cannot reach the server. Check your connection and try again.");
  }
  let data = null;
  try { data = await res.json(); } catch { /* non-JSON response */ }
  if (!res.ok) {
    let msg = "Request failed (" + res.status + ").";
    if (data && typeof data.detail === "string") msg = data.detail;
    else if (data && Array.isArray(data.detail)) msg = data.detail.map((d) => (d.msg || "").replace(/^Value error, /, "")).join(" ");
    throw Object.assign(new Error(msg), { status: res.status });
  }
  return data;
}
function alertBox(kind, msg) { return `<div class="alert ${kind}" role="alert">${esc(msg)}</div>`; }

/* ---------- navigation ---------- */
function renderNav() {
  const user = getUser();
  const here = location.hash || "#/";
  const link = (h, t) => `<a href="${h}" class="${here === h ? "active" : ""}">${t}</a>`;
  document.getElementById("navLinks").innerHTML =
    link("#/", "Home") + link("#/plan", "Plan a Trip") + link("#/trips", "My Trips") +
    (user ? link("#/profile", esc(user.username)) + `<button class="link" id="logoutBtn">Logout</button>`
          : link("#/login", "Login") + `<a class="btn small" href="#/signup">Sign Up</a>`);
  const out = document.getElementById("logoutBtn");
  if (out) out.onclick = () => { clearSession(); toast("You have been logged out."); location.hash = "#/"; renderNav(); };
  document.getElementById("navLinks").classList.remove("open");
  document.getElementById("navToggle").setAttribute("aria-expanded", "false");
}
document.getElementById("navToggle").onclick = () => {
  const open = document.getElementById("navLinks").classList.toggle("open");
  document.getElementById("navToggle").setAttribute("aria-expanded", String(open));
};

/* ---------- pages ---------- */
async function homePage() {
  app.innerHTML = `
    <section class="hero">
      <span class="eyebrow">Incredible India &middot; All 36 states and UTs</span>
      <h1>Plan Smarter. <em>Travel Better.</em></h1>
      <p>Tell us your destination, budget and interests. A transparent scoring engine ranks real attractions for your interests and budget, then an AI
         assistant explains your plan, suggests the best order and answers your questions.</p>
      <div class="hero-cta"><a class="btn" href="#/plan">Plan Your Trip</a><a class="btn light" href="#destinations" onclick="document.getElementById('destGrid').scrollIntoView({behavior:'smooth'});return false;">Explore Destinations</a></div>
      <div class="hero-stats"><div><strong>82</strong><span>Destinations</span></div><div><strong>349</strong><span>Attractions</span></div><div><strong>36</strong><span>States and UTs</span></div><div><strong>9</strong><span>Interests</span></div></div>
      <svg class="skyline" viewBox="0 0 1200 130" preserveAspectRatio="none" aria-hidden="true"><g fill="#fbf7f0">
        <path d="M0 130V104h28v-8h10v8h24v-14h10v14h24V96h10v8h30v26z"/>
        <path d="M150 130v-34c0-16 14-28 30-40 16 12 30 24 30 40v34z"/><rect x="176" y="40" width="8" height="16"/>
        <path d="M230 130v-60l12-16 12 16v60zM262 130V80h26v50zM296 130v-60l12-16 12 16v60z"/>
        <path d="M360 130v-44h120v44z"/><path d="M380 86c0-20 20-36 40-36s40 16 40 36z"/><rect x="418" y="34" width="4" height="18"/>
        <rect x="350" y="62" width="12" height="68"/><rect x="478" y="62" width="12" height="68"/><circle cx="356" cy="58" r="7"/><circle cx="484" cy="58" r="7"/>
        <path d="M540 130V96l14-8 14 8 14-8 14 8 14-8 14 8v34z"/><path d="M552 130V70h60v60z"/>
        <path d="M640 130v-24l20-34 20 34v24zM680 130V92l26-40 26 40v38zM732 130V78l22-34 22 34v52z"/>
        <path d="M800 130V90h40v40zM812 90c0-14 8-24 8-24s8 10 8 24z"/>
        <path d="M870 130v-50l10-14 10 14v50zM900 130V60l16-24 16 24v70zM940 130V84l10-14 10 14v46z"/>
        <path d="M1000 130v-40c0-18 16-30 34-42 18 12 34 24 34 42v40z"/><rect x="1030" y="30" width="8" height="18"/>
        <path d="M1090 130V100h30v30zM1126 130V88l16-20 16 20v42zM1164 130V102h36v28z"/>
      </g></svg>
    </section>
    <section class="section"><div class="container">
      <h2>Explore Destinations Across India</h2><p class="lead">All states and union territories, with selected destinations in each. Sample data, not exhaustive.</p>
      <div class="row" style="max-width:640px;margin:0 auto 24px">
        <div class="field" style="margin:0"><label for="destSearch" class="sr">Search destinations</label>
          <input id="destSearch" type="text" placeholder="Search city or state…" autocomplete="off"></div>
        <div class="field" style="margin:0"><label for="stateFilter" class="sr">Filter by state</label>
          <select id="stateFilter"><option value="">All states and UTs</option></select></div>
      </div>
      <p id="destCount" class="hint" style="text-align:center;color:var(--muted)"></p>
      <div class="grid" id="destGrid">${spinner()}</div>
    </div></section>
    <section class="section band"><div class="container">
      <h2>How It Works</h2><p class="lead">Three simple steps from idea to itinerary.</p>
      <div class="grid">
        <div class="feature"><span class="step-num">1</span><h3>Tell us about your trip</h3><p>Pick a destination, days, budget, travelers and interests.</p></div>
        <div class="feature"><span class="step-num">2</span><h3>We rank attractions</h3><p>Places are scored on interest match, affordability and travel style.</p></div>
        <div class="feature"><span class="step-num">3</span><h3>Get your day-wise plan</h3><p>See each day, estimated entry costs and everything on a map. Save it to revisit later.</p></div>
      </div></div></section>
    <section class="section"><div class="container">
      <h2>Main Features</h2><p class="lead">Built to be honest about what it knows.</p>
      <div class="grid">
        <div class="feature"><div class="ico">🎯</div><h3>Personalized scoring</h3><p>Transparent weighting: 50% interests, 20% budget, 20% rating (when available), 10% travel style.</p></div>
        <div class="feature"><div class="ico">💰</div><h3>Budget-aware</h3><p>See an estimated total for stay, food, local transport, entry fees and extras, compared with your budget. Every figure is labelled as an estimate.</p></div>
        <div class="feature"><div class="ico">✨</div><h3>AI travel assistant</h3><p>An AI model writes your trip overview, day themes and tips, and answers questions about your plan.</p></div>
        <div class="feature"><div class="ico">🗺️</div><h3>Interactive map</h3><p>Leaflet and OpenStreetMap show attractions that have stored coordinates.</p></div>
        <div class="feature"><div class="ico">💾</div><h3>Save your trips</h3><p>Create an account to save, reopen and delete your itineraries.</p></div>
      </div></div></section>`;
  try {
    const dests = await api("/api/destinations");
    const states = [...new Set(dests.map((d) => d.state).filter(Boolean))].sort();
    document.getElementById("stateFilter").innerHTML += states.map((s) => `<option value="${esc(s)}">${esc(s)}</option>`).join("");
    const draw = () => {
      const q = document.getElementById("destSearch").value.trim().toLowerCase();
      const st = document.getElementById("stateFilter").value;
      const shown = dests.filter((d) => (!st || d.state === st) &&
        (!q || d.city.toLowerCase().includes(q) || (d.state || "").toLowerCase().includes(q)));
      document.getElementById("destCount").textContent = `${shown.length} of ${dests.length} destinations`;
      document.getElementById("destGrid").innerHTML = shown.length ? shown.map((d, i) => `
        <article class="card"><div class="thumb c-${esc(d.categories[0])}" aria-hidden="true"><span>${ICONS[d.categories[0]] || "📍"}</span></div>
          <div class="card-body"><h3>${esc(d.city)}</h3><p class="hint" style="margin:0 0 6px;color:var(--muted)">${esc(d.state || "")}</p>
            <p>${d.place_count} attractions &middot; ${d.categories.slice(0, 4).map((c) => `<span class="tag">${esc(c)}</span>`).join("")}</p>
            <a class="btn small secondary" href="#/plan?city=${encodeURIComponent(d.city)}">Plan ${esc(d.city)}</a></div></article>`).join("")
        : `<div class="empty" style="grid-column:1/-1">No destinations match your search.</div>`;
    };
    document.getElementById("destSearch").oninput = draw;
    document.getElementById("stateFilter").onchange = draw;
    draw();
  } catch (e) { document.getElementById("destGrid").innerHTML = alertBox("error", e.message); }
}

async function plannerPage(query) {
  app.innerHTML = `<div class="container"><div class="panel"><h1>Plan Your Trip</h1>${spinner()}</div></div>`;
  let dests;
  try { dests = await api("/api/destinations"); }
  catch (e) { app.innerHTML = `<div class="container"><div class="panel"><h1>Plan Your Trip</h1>${alertBox("error", e.message)}</div></div>`; return; }
  const preset = new URLSearchParams(query).get("city");
  app.innerHTML = `<div class="container"><form class="panel" id="planForm" novalidate>
    <h1>Plan Your Trip</h1><p class="lead" style="text-align:left;margin-bottom:20px">All fields are required.</p>
    <div class="field"><label for="destination">Destination</label>
      <select id="destination" required><option value="">Select a destination…</option>
      ${[...new Set(dests.map((d) => d.state || "Other"))].sort().map((st) => `<optgroup label="${esc(st)}">${
        dests.filter((d) => (d.state || "Other") === st).map((d) => `<option value="${esc(d.city)}" ${d.city === preset ? "selected" : ""}>${esc(d.city)}</option>`).join("")}</optgroup>`).join("")}</select>
      <div class="hint">${dests.length} destinations across ${new Set(dests.map((d) => d.state)).size} states and union territories.</div></div>
    <div class="row">
      <div class="field"><label for="days">Number of days (1–7)</label><input id="days" type="number" min="1" max="7" value="3" required></div>
      <div class="field"><label for="travelers">Number of travelers</label><input id="travelers" type="number" min="1" max="20" value="2" required></div>
    </div>
    <div class="field"><label for="budget">Total travel budget (INR)</label><input id="budget" type="number" min="1" step="100" placeholder="e.g. 15000" required>
      <div class="hint">Total for the whole group, covering stay, food, local transport, entry fees and extras (all estimated).</div></div>
    <div class="row">
      <div class="field"><label for="nights">Nights of stay (optional)</label><input id="nights" type="number" min="0" max="14" placeholder="Default: days − 1"></div>
      <div class="field"><label for="travelCost">Travel cost to destination, round trip per person (₹, optional)</label><input id="travelCost" type="number" min="0" step="100" placeholder="e.g. 3000 (your ticket or fuel + toll)"></div>
    </div>
    <fieldset class="field"><legend>How are you travelling to the destination? (optional)</legend><div class="chips">
      ${[["none", "Not decided"], ["flight", "✈️ Flight"], ["train", "🚆 Train"], ["bus", "🚌 Bus"], ["car", "🚗 Own car"]].map(([v, l]) => `<label class="chip"><input type="radio" name="mode" value="${v}" ${v === "none" ? "checked" : ""}><span>${l}</span></label>`).join("")}</div>
      <div class="hint">We don't know your starting city, so please enter the ticket (or fuel and toll) cost above to include it in the total.</div></fieldset>
    <fieldset class="field"><legend>Travel interests (choose at least one)</legend><div class="chips" id="interestChips"></div>
      <div class="hint" id="interestHint"></div></fieldset>
    <fieldset class="field"><legend>Travel style</legend><div class="chips">
      ${["budget", "balanced", "luxury"].map((s) => `<label class="chip"><input type="radio" name="style" value="${s}" ${s === "balanced" ? "checked" : ""}><span>${cap(s)}</span></label>`).join("")}</div></fieldset>
    <div id="formMsg"></div>
    <button class="btn" id="genBtn" type="submit">Generate My Itinerary</button></form></div>`;

  // Interests depend on the destination: only show those that have matching attractions there.
  const counts = Object.fromEntries(dests.map((d) => [d.city, d.interest_counts || {}]));
  const hasCounts = dests.some((d) => d.interest_counts);
  const drawInterests = () => {
    const city = document.getElementById("destination").value;
    const box = document.getElementById("interestChips"), hint = document.getElementById("interestHint");
    const checked = new Set([...document.querySelectorAll("input[name=interest]:checked")].map((c) => c.value));
    if (!city) { box.innerHTML = ""; hint.textContent = "Choose a destination to see the interests available there."; return; }
    const avail = hasCounts ? INTERESTS.filter(([v]) => (counts[city] || {})[v]) : INTERESTS;
    box.innerHTML = avail.map(([v, l]) => `<label class="chip"><input type="checkbox" name="interest" value="${v}" ${checked.has(v) ? "checked" : ""}><span>${l}${hasCounts ? ` <small>${counts[city][v]}</small>` : ""}</span></label>`).join("");
    hint.textContent = hasCounts ? `Showing the interests available in ${city}. The small number is how many attractions match.` : "";
  };
  document.getElementById("destination").onchange = drawInterests;
  drawInterests();

  document.getElementById("planForm").onsubmit = async (ev) => {
    ev.preventDefault();
    const msg = document.getElementById("formMsg"); msg.innerHTML = "";
    const payload = {
      destination: document.getElementById("destination").value,
      days: parseInt(document.getElementById("days").value, 10),
      travelers: parseInt(document.getElementById("travelers").value, 10),
      budget: parseFloat(document.getElementById("budget").value),
      interests: [...document.querySelectorAll("input[name=interest]:checked")].map((c) => c.value),
      travel_style: document.querySelector("input[name=style]:checked").value,
      travel_cost_per_person: parseFloat(document.getElementById("travelCost").value) || 0,
      travel_mode: document.querySelector("input[name=mode]:checked").value,
    };
    const nightsVal = document.getElementById("nights").value.trim();
    if (nightsVal !== "") payload.nights = parseInt(nightsVal, 10);
    const errors = [];
    if (!payload.destination) errors.push("Please choose a destination.");
    if (!(payload.days >= 1 && payload.days <= 7)) errors.push("Days must be between 1 and 7.");
    if (!(payload.travelers >= 1 && payload.travelers <= 20)) errors.push("Travelers must be between 1 and 20.");
    if (!(payload.budget > 0)) errors.push("Enter a budget greater than 0.");
    if (payload.interests.length === 0) errors.push("Select at least one interest.");
    if (payload.travel_cost_per_person < 0) errors.push("Travel cost cannot be negative.");
    if (payload.nights !== undefined && !(payload.nights >= 0 && payload.nights <= 14)) errors.push("Nights must be between 0 and 14.");
    if (errors.length) { msg.innerHTML = alertBox("error", errors.join(" ")); return; }
    const btn = document.getElementById("genBtn"); btn.disabled = true; btn.textContent = "Generating…";
    try {
      const plan = await api("/api/plan", { method: "POST", body: payload });
      sessionStorage.setItem("tp_plan", JSON.stringify({ plan, saved: false }));
      location.hash = "#/results";
    } catch (e) { msg.innerHTML = alertBox("error", e.message); btn.disabled = false; btn.textContent = "Generate My Itinerary"; }
  };
}

function placeCard(p) {
  const cats = p.categories.map((c) => `<span class="tag ${p.matched_interests.includes(c) ? "match" : ""}">${esc(c)}</span>`).join("");
  const loc = p.latitude !== null
    ? `📍 ${p.latitude.toFixed(4)}, ${p.longitude.toFixed(4)}${p.coordinates_approximate ? '<span class="badge">approx.</span>' : ""}`
    : `📍 Coordinates not available`;
  const cost = p.cost_per_person === null ? "Entry cost unknown"
    : p.cost_per_person === 0 ? `Free entry<span class="badge">estimate</span>`
    : `${inr(p.cost_per_person)} per person (${inr(p.entry_cost_total)} total)<span class="badge">estimate</span>`;
  return `<article class="card"><div class="thumb c-${esc(p.categories[0])}" aria-hidden="true"><span>${ICONS[p.categories[0]] || "📍"}</span></div>
    <div class="card-body"><h3>${esc(p.name)}</h3><div>${cats}</div><p>${esc(p.description)}</p>
      <div class="place-meta">
        <span>⏱️ About ${esc(p.hours)} hours<span class="badge">estimate</span></span>
        <span>🎟️ ${cost}</span>
        ${p.rating !== null ? `<span>⭐ ${esc(p.rating)} / 5</span>` : ""}
        <span>${loc}</span></div>
      <a href="${esc(p.map_url)}" target="_blank" rel="noopener noreferrer">${p.latitude !== null ? "Open on OpenStreetMap" : "Search on OpenStreetMap"} ↗</a>
    </div></article>`;
}

function drawMap(plan) {
  if (currentMap) { currentMap.remove(); currentMap = null; }
  const el = document.getElementById("map");
  if (!el) return;
  const pts = plan.daily_plan.flatMap((d) => d.places.filter((p) => p.latitude !== null).map((p) => ({ ...p, day: d.day })));
  if (typeof L === "undefined") { el.outerHTML = alertBox("warn", "The map library could not be loaded (check your internet connection)."); return; }
  if (!pts.length) { el.outerHTML = alertBox("info", "None of the recommended attractions have stored coordinates, so there is nothing to show on the map."); return; }
  currentMap = L.map(el);
  L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", { maxZoom: 19, attribution: "&copy; OpenStreetMap contributors" }).addTo(currentMap);
  const group = [];
  pts.forEach((p) => {
    const node = document.createElement("div");   // DOM nodes (not HTML strings) keep popups XSS-safe
    const b = document.createElement("strong"); b.textContent = p.name; node.appendChild(b);
    node.appendChild(document.createElement("br"));
    node.appendChild(document.createTextNode(`Day ${p.day} · ${p.latitude.toFixed(4)}, ${p.longitude.toFixed(4)}` + (p.coordinates_approximate ? " (approx.)" : "")));
    L.marker([p.latitude, p.longitude]).addTo(currentMap).bindPopup(node);
    group.push([p.latitude, p.longitude]);
  });
  currentMap.fitBounds(group, { padding: [30, 30], maxZoom: 14 });
}

/* Tiny, safe formatter for AI answers: escapes HTML first, then supports **bold**, "- " bullets and line breaks. */
function renderMd(text) {
  const lines = String(text || "").replace(/\s+[-*•]\s+(?=\*\*)/g, "\n- ").split(/\n+/).map((l) => l.trim()).filter(Boolean);
  const inline = (t) => esc(t).replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
  let html = "", list = [];
  const flush = () => { if (list.length) { html += "<ul>" + list.map((i) => `<li>${i}</li>`).join("") + "</ul>"; list = []; } };
  lines.forEach((l) => {
    const m = l.match(/^[-*•]\s+(.*)$/);
    if (m) list.push(inline(m[1])); else { flush(); html += `<p>${inline(l)}</p>`; }
  });
  flush();
  return html || "<p>No answer.</p>";
}

/* ---------- AI assistant (LLM-backed; the server turns it off if no API key is set) ---------- */
function showInsights(ai) {
  const out = document.getElementById("aiOut"); if (!out) return;
  out.innerHTML = `<h4 class="ai-title">${esc(ai.title)}</h4><p>${esc(ai.overview)}</p>` +
    (ai.budget_note ? `<p class="hint"><strong>Budget:</strong> ${esc(ai.budget_note)}</p>` : "");
  (ai.days || []).forEach((d) => {
    const el = document.getElementById("aiDay" + d.day); if (!el) return;
    el.innerHTML = `<div class="ai-day-box"><span class="ai-spark">✨ AI</span> <strong>${esc(d.theme)}</strong>` +
      (d.suggested_order && d.suggested_order.length ? `<div class="hint">Suggested order: ${d.suggested_order.map(esc).join(" → ")}</div>` : "") +
      (d.tips && d.tips.length ? `<ul>${d.tips.map((t) => `<li>${esc(t)}</li>`).join("")}</ul>` : "") + `</div>`;
  });
}

async function initAI(plan) {
  const panel = document.getElementById("aiPanel"); if (!panel) return;
  let status = { enabled: false };
  try { status = await api("/api/ai/status"); } catch { /* treat as off */ }
  if (!status.enabled) {
    panel.innerHTML = `<div class="ai-panel off"><h3>✨ AI Travel Assistant</h3><p>AI insights are switched off on this server. The site owner can turn them on by setting an AI API key (see the README). The itinerary above is produced by the rule-based scoring engine and works without it.</p></div>`;
    return;
  }
  panel.innerHTML = `<div class="ai-panel"><div class="ai-head"><h3>✨ AI Travel Assistant</h3><span class="badge">${esc(status.provider)} · ${esc(status.model)}</span></div>
    <div id="aiOut">${plan.ai ? "" : `<p>Get a personalised overview, a theme and tips for each day, and a suggested visiting order, written by an AI model from your itinerary.</p><button class="btn secondary" id="aiGo">Generate AI insights</button>`}</div>
    <div class="ai-chat"><label for="aiQ">Ask the AI about this trip</label>
      <div class="ai-ask"><input id="aiQ" type="text" maxlength="300" placeholder="e.g. Which day is best for photography?"><button class="btn small" id="aiAsk">Ask</button></div>
      <div id="aiAnswers" aria-live="polite"></div></div>
    <p class="hint">AI text can be wrong. It only sees your itinerary data, so always verify prices, timings and access rules.</p></div>`;
  if (plan.ai) showInsights(plan.ai);
  const go = document.getElementById("aiGo");
  if (go) go.onclick = async () => {
    go.disabled = true; go.textContent = "Thinking…";
    try {
      const ai = await api("/api/ai/insights", { method: "POST", body: { itinerary: plan } });
      plan.ai = ai;
      try { const st = JSON.parse(sessionStorage.getItem("tp_plan")); if (st) { st.plan.ai = ai; sessionStorage.setItem("tp_plan", JSON.stringify(st)); } } catch { /* ignore */ }
      showInsights(ai);
    } catch (e) { go.disabled = false; go.textContent = "Generate AI insights"; document.getElementById("aiOut").insertAdjacentHTML("beforeend", alertBox("error", e.message)); }
  };
  const ask = async () => {
    const input = document.getElementById("aiQ"), q = input.value.trim();
    if (q.length < 3) { toast("Type a question first."); return; }
    const btn = document.getElementById("aiAsk"); btn.disabled = true; btn.textContent = "…";
    const box = document.createElement("div"); box.className = "ai-qa";
    const qWrap = document.createElement("div"); qWrap.className = "ai-q";
    const qLabel = document.createElement("span"); qLabel.className = "ai-q-label"; qLabel.textContent = "You";
    const qText = document.createElement("p"); qText.textContent = q;
    qWrap.append(qLabel, qText);
    const aWrap = document.createElement("div"); aWrap.className = "ai-a";
    const avatar = document.createElement("span"); avatar.className = "ai-avatar"; avatar.textContent = "✨"; avatar.setAttribute("aria-hidden", "true");
    const aEl = document.createElement("div"); aEl.className = "ai-a-body";
    aEl.innerHTML = '<span class="ai-dots" aria-label="AI is thinking"><i></i><i></i><i></i></span>';
    aWrap.append(avatar, aEl);
    box.append(qWrap, aWrap); document.getElementById("aiAnswers").prepend(box);
    try { aEl.innerHTML = renderMd((await api("/api/ai/ask", { method: "POST", body: { itinerary: plan, question: q } })).answer); input.value = ""; }
    catch (e) { aEl.textContent = e.message; aEl.className = "ai-a-body ai-err"; }
    btn.disabled = false; btn.textContent = "Ask";
  };
  document.getElementById("aiAsk").onclick = ask;
  document.getElementById("aiQ").onkeydown = (ev) => { if (ev.key === "Enter") ask(); };
}

function costPanel(plan) {
  const f = plan.full_trip_cost; if (!f) return "";
  const pct = plan.budget > 0 ? Math.round((f.total / plan.budget) * 100) : 0;
  const over = f.total > plan.budget;
  const status = over ? `Over budget by ${inr(f.difference)}` : `Within budget, ${inr(f.difference)} to spare`;
  const rows = f.breakdown.map((b) => `<tr><td><strong>${esc(b.label)}</strong><div class="hint">${esc(b.basis)}</div></td><td class="num">${inr(b.amount)}</td></tr>`).join("");
  const alt = Object.entries(f.alternatives || {}).map(([k, v]) =>
    `<span class="alt ${k === f.style ? "now" : ""} ${v <= plan.budget ? "fits" : ""}"><small>${esc(cap(k))}${k === f.style ? " (selected)" : ""}</small><strong>${inr(v)}</strong></span>`).join("");
  return `<section class="cost-panel" aria-label="Full trip cost estimate">
    <div class="cost-head"><h3>💰 Full Trip Cost Estimate</h3><span class="cost-status ${over ? "over" : "ok"}">${esc(status)}</span></div>
    <div class="cost-bar" role="img" aria-label="Estimated cost is ${pct}% of your budget"><div class="cost-fill ${over ? "over" : ""}" style="width:${Math.min(100, pct)}%"></div></div>
    <div class="cost-bar-label"><span>Estimated ${inr(f.total)}</span><span>${pct}% of your ${inr(plan.budget)} budget</span></div>
    <table class="cost-table"><tbody>${rows}
      <tr class="total"><td><strong>Total estimate</strong><div class="hint">About ${inr(f.per_person)} per person &middot; ${inr(f.per_day)} per day</div></td><td class="num">${inr(f.total)}</td></tr></tbody></table>
    <p class="hint" style="margin:14px 0 6px"><strong>Total by travel style</strong> (same attractions):</p><div class="alts">${alt}</div>
    <ul class="cost-notes">${f.assumptions.map((a) => `<li>${esc(a)}</li>`).join("")}</ul></section>`;
}

function renderPlan(plan, { saved, tripId } = {}) {
  const days = plan.daily_plan.map((d) => `
    <section class="day"><div class="day-head"><h2>Day ${d.day}</h2>
      <span class="meta">${d.places.length} places &middot; ~${d.total_hours} hours &middot; entry fees ${inr(d.estimated_cost)} (estimate)</span></div>
      <div class="ai-day" id="aiDay${d.day}"></div>
      <div class="grid">${d.places.map(placeCard).join("")}</div></section>`).join("");
  const notes = [...plan.warnings.map((w) => alertBox("warn", w)), ...plan.notes.map((n) => alertBox("info", n))].join("");
  app.innerHTML = `
    <section class="summary"><div class="container">
      <h1>${esc(plan.destination)} Itinerary</h1>
      ${plan.daily_plan[0] && plan.daily_plan[0].places[0] && plan.daily_plan[0].places[0].state ? `<p style="margin:-6px 0 12px;opacity:.9">${esc(plan.daily_plan[0].places[0].state)}, India</p>` : ""}
      <div class="stats">
        <div class="stat"><small>Duration</small><strong>${plan.days} day${plan.days > 1 ? "s" : ""}</strong></div>
        <div class="stat"><small>Travelers</small><strong>${plan.travelers}</strong></div>
        <div class="stat"><small>Total budget</small><strong>${inr(plan.budget)}</strong></div>
        ${plan.full_trip_cost ? `<div class="stat"><small>Est. total trip cost</small><strong>${inr(plan.full_trip_cost.total)}</strong></div>` : ""}
        <div class="stat"><small>Est. entry fees</small><strong>${inr(plan.estimated_total_cost)}</strong></div>
        <div class="stat"><small>Style</small><strong>${esc(cap(plan.travel_style || "balanced"))}</strong></div>
      </div>
      <p style="margin:14px 0 0">${plan.interests.map((i) => `<span class="tag">${esc(i)}</span>`).join("")}</p></div></section>
    <div class="container">
      ${costPanel(plan)}${notes}
      ${alertBox("info", plan.cost_disclaimer)}
      ${plan.algorithm && plan.algorithm.ml && plan.algorithm.ml.used ? alertBox("info", "How places were ranked: rule-based scoring (80%) plus a machine-learning text-similarity score (20%) learned from the place descriptions in our dataset.") : ""}
      <section id="aiPanel"></section>
      <div class="actions" id="actions"></div>
      <h2 style="text-align:left;margin-top:24px">Map</h2>
      <p class="hint" style="color:var(--muted);margin:0">Markers use the stored (approximate) coordinates. No road distances or routes are calculated.</p>
      <div id="map" role="application" aria-label="Map of recommended attractions"></div>
      ${days}
    </div>`;
  const actions = document.getElementById("actions");
  if (tripId) {
    actions.innerHTML = `<a class="btn ghost" href="#/trips">← Back to My Trips</a><button class="btn ghost" onclick="window.print()">Print</button>`;
  } else {
    actions.innerHTML = `<button class="btn" id="saveBtn" ${saved ? "disabled" : ""}>${saved ? "Saved ✓" : "Save This Trip"}</button>
      <a class="btn ghost" href="#/plan">Plan Another Trip</a>`;
    const btn = document.getElementById("saveBtn");
    if (!saved) btn.onclick = () => saveTrip(plan, btn);
  }
  drawMap(plan);
  initAI(plan);
  window.scrollTo(0, 0);
}

async function saveTrip(plan, btn) {
  if (!getToken()) { sessionStorage.setItem("tp_after_login", "#/results"); toast("Log in to save your trip."); location.hash = "#/login"; return; }
  btn.disabled = true; btn.textContent = "Saving…";
  try {
    await api("/api/trips/save", { method: "POST", auth: true, body: {
      destination: plan.destination, days: plan.days, budget: plan.budget, travelers: plan.travelers,
      interests: plan.interests, itinerary: plan, estimated_total_cost: plan.estimated_total_cost } });
    sessionStorage.setItem("tp_plan", JSON.stringify({ plan, saved: true }));
    btn.textContent = "Saved ✓"; toast("Trip saved to My Trips.");
  } catch (e) {
    btn.disabled = false; btn.textContent = "Save This Trip";
    if (e.status === 401) { clearSession(); renderNav(); sessionStorage.setItem("tp_after_login", "#/results"); toast("Session expired. Please log in again."); location.hash = "#/login"; }
    else toast(e.message);
  }
}

function resultsPage() {
  let stored = null;
  try { stored = JSON.parse(sessionStorage.getItem("tp_plan")); } catch { /* ignore */ }
  if (!stored) { app.innerHTML = `<div class="container"><div class="panel empty"><h2>No itinerary yet</h2><p>Generate one first.</p><a class="btn" href="#/plan">Plan Your Trip</a></div></div>`; return; }
  renderPlan(stored.plan, { saved: stored.saved });
}

function authPage(mode) {
  const signup = mode === "signup";
  app.innerHTML = `<div class="container"><form class="panel narrow" id="authForm" novalidate>
    <h1>${signup ? "Create Account" : "Welcome Back"}</h1>
    ${signup ? `<div class="field"><label for="username">Username</label><input id="username" type="text" minlength="3" maxlength="30" autocomplete="username" required></div>` : ""}
    <div class="field"><label for="email">Email</label><input id="email" type="email" autocomplete="email" required></div>
    <div class="field"><label for="password">Password</label><input id="password" type="password" minlength="8" maxlength="72" autocomplete="${signup ? "new-password" : "current-password"}" required>
      ${signup ? `<div class="hint">At least 8 characters.</div>` : ""}</div>
    <div id="authMsg"></div>
    <button class="btn" id="authBtn" type="submit" style="width:100%">${signup ? "Sign Up" : "Log In"}</button>
    <p style="text-align:center;margin-bottom:0">${signup ? 'Already registered? <a href="#/login">Log in</a>' : 'New here? <a href="#/signup">Create an account</a>'}</p></form></div>`;
  document.getElementById("authForm").onsubmit = async (ev) => {
    ev.preventDefault();
    const msg = document.getElementById("authMsg"); msg.innerHTML = "";
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const username = signup ? document.getElementById("username").value.trim() : null;
    if (signup && username.length < 3) { msg.innerHTML = alertBox("error", "Username must be at least 3 characters."); return; }
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) { msg.innerHTML = alertBox("error", "Enter a valid email address."); return; }
    if (password.length < (signup ? 8 : 1)) { msg.innerHTML = alertBox("error", signup ? "Password must be at least 8 characters." : "Enter your password."); return; }
    const btn = document.getElementById("authBtn"); btn.disabled = true;
    try {
      const data = await api(signup ? "/api/auth/register" : "/api/auth/login", { method: "POST", body: signup ? { username, email, password } : { email, password } });
      setSession(data); renderNav(); toast(signup ? "Account created. Welcome!" : "Logged in.");
      const next = sessionStorage.getItem("tp_after_login"); sessionStorage.removeItem("tp_after_login");
      location.hash = next || "#/trips";
    } catch (e) { msg.innerHTML = alertBox("error", e.message); btn.disabled = false; }
  };
}

async function profilePage() {
  if (!getToken()) { location.hash = "#/login"; return; }
  app.innerHTML = `<div class="container"><div class="panel narrow"><h1>My Profile</h1>${spinner()}</div></div>`;
  try {
    const u = await api("/api/auth/me", { auth: true });
    localStorage.setItem("tp_user", JSON.stringify(u));
    app.innerHTML = `<div class="container"><div class="panel narrow"><h1>My Profile</h1>
      <p><strong>Username:</strong> ${esc(u.username)}</p><p><strong>Email:</strong> ${esc(u.email)}</p>
      <p><strong>Member since:</strong> ${u.created_at ? new Date(u.created_at).toLocaleDateString() : "N/A"}</p>
      <div class="actions"><a class="btn secondary" href="#/trips">My Trips</a><button class="btn ghost" id="pLogout">Logout</button></div></div></div>`;
    document.getElementById("pLogout").onclick = () => { clearSession(); renderNav(); toast("You have been logged out."); location.hash = "#/"; };
  } catch (e) {
    if (e.status === 401) { clearSession(); renderNav(); location.hash = "#/login"; }
    else app.innerHTML = `<div class="container"><div class="panel narrow"><h1>My Profile</h1>${alertBox("error", e.message)}</div></div>`;
  }
}

async function tripsPage() {
  if (!getToken()) {
    app.innerHTML = `<div class="container"><div class="panel empty"><h2>Log in to see your trips</h2><p>Saved itineraries are tied to your account.</p>
      <a class="btn" href="#/login">Log In</a> <a class="btn ghost" href="#/signup">Sign Up</a></div></div>`;
    sessionStorage.setItem("tp_after_login", "#/trips"); return;
  }
  app.innerHTML = `<div class="container section"><h1>My Trips</h1>${spinner()}</div>`;
  try {
    const trips = await api("/api/trips", { auth: true });
    const body = trips.length ? trips.map((t) => `
      <div class="trip-card" data-id="${esc(t.id)}"><div><h3>${esc(t.destination)} &middot; ${t.days} day${t.days > 1 ? "s" : ""}</h3>
        <div class="meta">${t.travelers} traveler${t.travelers > 1 ? "s" : ""} &middot; budget ${inr(t.budget)} &middot; ${t.estimated_full_cost ? `est. total ~${inr(t.estimated_full_cost)}` : `entry fees ~${inr(t.estimated_total_cost)} (est.)`}
        <br>${t.interests.map((i) => `<span class="tag">${esc(i)}</span>`).join("")} Saved ${new Date(t.created_at).toLocaleDateString()}</div></div>
        <div><a class="btn small secondary" href="#/trip/${esc(t.id)}">Open</a> <button class="btn small danger" data-del="${esc(t.id)}">Delete</button></div></div>`).join("")
      : `<div class="empty"><h2>No saved trips yet</h2><p>Generate an itinerary and press “Save This Trip”.</p><a class="btn" href="#/plan">Plan Your Trip</a></div>`;
    app.innerHTML = `<div class="container section"><h1>My Trips</h1><div id="tripMsg"></div>${body}</div>`;
    app.querySelectorAll("[data-del]").forEach((b) => (b.onclick = async () => {
      if (!confirm("Delete this saved trip? This cannot be undone.")) return;
      b.disabled = true;
      try { await api("/api/trips/" + b.dataset.del, { method: "DELETE", auth: true }); toast("Trip deleted."); tripsPage(); }
      catch (e) { document.getElementById("tripMsg").innerHTML = alertBox("error", e.message); b.disabled = false; }
    }));
  } catch (e) {
    if (e.status === 401) { clearSession(); renderNav(); location.hash = "#/login"; }
    else app.innerHTML = `<div class="container section"><h1>My Trips</h1>${alertBox("error", e.message)}</div>`;
  }
}

async function tripDetailPage(id) {
  if (!getToken()) { location.hash = "#/login"; return; }
  app.innerHTML = `<div class="container section">${spinner()}</div>`;
  try {
    const t = await api("/api/trips/" + encodeURIComponent(id), { auth: true });
    renderPlan(t.itinerary, { tripId: t.id });
  } catch (e) {
    if (e.status === 401) { clearSession(); renderNav(); location.hash = "#/login"; return; }
    app.innerHTML = `<div class="container section">${alertBox("error", e.message)}<a class="btn ghost" href="#/trips">← Back to My Trips</a></div>`;
  }
}

/* ---------- router ---------- */
function route() {
  const [path, query = ""] = (location.hash || "#/").slice(1).split("?");
  renderNav();
  if (currentMap) { currentMap.remove(); currentMap = null; }
  if (path === "/" || path === "") homePage();
  else if (path === "/plan") plannerPage(query);
  else if (path === "/results") resultsPage();
  else if (path === "/login") authPage("login");
  else if (path === "/signup") authPage("signup");
  else if (path === "/profile") profilePage();
  else if (path === "/trips") tripsPage();
  else if (path.startsWith("/trip/")) tripDetailPage(path.slice(6));
  else app.innerHTML = `<div class="container"><div class="panel empty"><h2>Page not found</h2><a class="btn" href="#/">Go Home</a></div></div>`;
  window.scrollTo(0, 0);
}
window.addEventListener("hashchange", route);
route();
