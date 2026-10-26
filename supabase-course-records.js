/* VisaWatch Supabase shared course records integration.
   Uses only the public publishable key in the browser. Database access is enforced by Supabase Auth + RLS. */
(function () {
  const CONFIG_KEY = "visawatch_supabase_public_config_v1";
  let client = null;
  let currentUser = null;
  const $ = (id) => document.getElementById(id);
  const status = (message, isError = false) => {
    const el = $("vwSharedStatus");
    if (el) { el.textContent = message; el.style.color = isError ? "#b42318" : "#16734f"; }
  };
  const escapeHtml = (value) => String(value ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  const fields = {
    institution: "crInstitution", course: "crCourse", destination: "crCountry",
    campus: "crCampus", intake: "crIntake", duration: "crDuration",
    tuition: "crTuition", entry_requirements: "crEntry", official_course_url: "crCourseUrl",
    official_register_url: "crRegisterUrl", verification_status: "crStatus",
    checked_by: "crCheckedBy", checked_date: "crCheckedDate", notes: "crNotes"
  };
  function config() {
    try { return JSON.parse(localStorage.getItem(CONFIG_KEY) || "{}"); } catch (_) { return {}; }
  }
  function getFormRecord() {
    const row = {};
    Object.entries(fields).forEach(([column, id]) => { row[column] = ($(id)?.value || "").trim() || null; });
    if (currentUser) row.created_by = currentUser.id;
    return row;
  }
  function loadRecord(row) {
    Object.entries(fields).forEach(([column, id]) => { if ($(id)) $(id).value = row[column] || ""; });
    status("Shared record loaded into the form. Review the official sources before advising.");
    window.scrollTo({top: $("crInstitution").getBoundingClientRect().top + window.scrollY - 80, behavior:"smooth"});
  }
  function ensurePanel() {
    if ($("vwSharedPanel")) return;
    const savedPanel = $("crSavedPanel");
    if (!savedPanel) return;
    const panel = document.createElement("div");
    panel.id = "vwSharedPanel";
    panel.className = "panel";
    panel.style.cssText = "padding:18px;margin:18px 0";
    panel.innerHTML = `
      <h3 style="margin-top:0">Shared course records · Supabase</h3>
      <p style="font-size:12px;color:var(--muted)">Sign in with your team account to save and view records shared through the secured database. The publishable key is public; never enter a secret/service_role key here.</p>
      <div class="filterbar"><input id="vwProjectUrl" type="url" placeholder="Supabase Project URL (https://....supabase.co)" autocomplete="url"><input id="vwPublishableKey" type="password" placeholder="Supabase publishable key (sb_publishable_…)" autocomplete="off"></div>
      <div class="filterbar"><input id="vwEmail" type="email" placeholder="Work email" autocomplete="username"><input id="vwPassword" type="password" placeholder="Password" autocomplete="current-password"></div>
      <div style="display:flex;gap:8px;flex-wrap:wrap"><button class="smallbtn" id="vwConnect" type="button">Connect project</button><button class="smallbtn" id="vwSignIn" type="button">Sign in</button><button class="smallbtn" id="vwSignUp" type="button">Create account</button><button class="smallbtn" id="vwSignOut" type="button">Sign out</button><button class="smallbtn" id="vwSaveShared" type="button">Save current record to shared database</button><button class="smallbtn" id="vwLoadShared" type="button">Refresh shared records</button></div>
      <p id="vwSharedStatus" role="status" aria-live="polite" style="font-size:12px;margin:12px 0 6px">Not connected. Enter your project URL and publishable key.</p>
      <div id="vwSharedList"></div>
    `;
    savedPanel.parentNode.insertBefore(panel, savedPanel);
    const cfg = config();
    $("vwProjectUrl").value = cfg.url || "";
    $("vwPublishableKey").value = cfg.key || "";
    $("vwConnect").onclick = connect;
    $("vwSignIn").onclick = () => authenticate(false);
    $("vwSignUp").onclick = () => authenticate(true);
    $("vwSignOut").onclick = signOut;
    $("vwSaveShared").onclick = saveShared;
    $("vwLoadShared").onclick = loadShared;
    if (cfg.url && cfg.key) connect();
  }
  function connect() {
    const url = $("vwProjectUrl").value.trim().replace(/\/$/, "");
    const key = $("vwPublishableKey").value.trim();
    if (!/^https:\/\/[a-z0-9-]+\.supabase\.co$/i.test(url) || !key.startsWith("sb_publishable_")) {
      status("Check the Project URL and publishable key. Do not use a secret/service_role key.", true); return;
    }
    if (!window.supabase || typeof window.supabase.createClient !== "function") {
      status("Supabase library did not load. Refresh the page and try again.", true); return;
    }
    try {
      localStorage.setItem(CONFIG_KEY, JSON.stringify({url, key}));
      client = window.supabase.createClient(url, key, {auth:{persistSession:true, autoRefreshToken:true, detectSessionInUrl:true}});
      status("Project connected. Sign in with your team account.");
      client.auth.getSession().then(({data, error}) => {
        if (error) throw error;
        currentUser = data.session?.user || null;
        status(currentUser ? "Signed in as " + currentUser.email : "Project connected. Sign in with your team account.");
        if (currentUser) loadShared();
      }).catch(e => status("Could not check session: " + e.message, true));
    } catch (e) { status("Could not connect: " + e.message, true); }
  }
  async function authenticate(signUp) {
    if (!client) { status("First click Connect project.", true); return; }
    const email = $("vwEmail").value.trim(), password = $("vwPassword").value;
    if (!email || password.length < 8) { status("Enter your work email and a password with at least 8 characters.", true); return; }
    try {
      const result = signUp
        ? await client.auth.signUp({email, password})
        : await client.auth.signInWithPassword({email, password});
      if (result.error) throw result.error;
      currentUser = result.data.user || result.data.session?.user || null;
      if (signUp && !result.data.session) {
        status("Account request created. Check your email for the Supabase confirmation link, then sign in.");
      } else {
        status("Signed in as " + (currentUser?.email || email));
        await loadShared();
      }
    } catch (e) { status("Login error: " + e.message, true); }
  }
  async function signOut() {
    if (!client) { status("Connect the project first.", true); return; }
    const {error} = await client.auth.signOut();
    if (error) { status("Sign-out failed: " + error.message, true); return; }
    currentUser = null; $("vwSharedList").textContent = ""; status("Signed out.");
  }
  async function saveShared() {
    if (!client || !currentUser) { status("Connect and sign in before saving shared records.", true); return; }
    const row = getFormRecord();
    if (!row.institution || !row.course || !row.destination) {
      status("Fill in Institution, Exact course and Destination first.", true); return;
    }
    try {
      const {data, error} = await client.from("course_verification_records").insert(row).select("id").single();
      if (error) throw error;
      status("Saved to shared database. Record ID: " + data.id);
      await loadShared();
    } catch (e) { status("Shared save failed: " + e.message + ". Check the table name, RLS policies and signed-in account.", true); }
  }
  async function loadShared() {
    if (!client || !currentUser) { status("Connect and sign in before viewing shared records.", true); return; }
    try {
      const {data, error} = await client.from("course_verification_records")
        .select("id,institution,course,destination,campus,intake,verification_status,checked_by,checked_date,updated_at")
        .order("updated_at", {ascending:false}).limit(100);
      if (error) throw error;
      const host = $("vwSharedList"); host.textContent = "";
      if (!data?.length) { host.textContent = "No shared course records visible yet."; status("Loaded shared records: 0"); return; }
      data.forEach(row => {
        const card = document.createElement("div"); card.className = "panel"; card.style.cssText = "padding:12px;margin:10px 0";
        const title = document.createElement("b"); title.textContent = row.institution || "Unnamed institution";
        const details = document.createElement("p"); details.style.cssText = "font-size:12px;margin:6px 0;color:var(--muted)";
        details.textContent = [row.course || "Course not entered", row.destination || "Destination not selected", row.campus, row.verification_status, row.checked_date ? "Checked " + row.checked_date : ""].filter(Boolean).join(" · ");
        const btn = document.createElement("button"); btn.className = "smallbtn"; btn.type = "button"; btn.textContent = "Load into form"; btn.onclick = () => loadRecord(row);
        card.append(title, details, btn); host.appendChild(card);
      });
      status("Loaded " + data.length + " shared record(s).");
    } catch (e) { status("Could not load shared records: " + e.message + ". Confirm the SQL schema has been run.", true); }
  }
  function start() {
    if (!document.getElementById("crSavedPanel")) { setTimeout(start, 150); return; }
    ensurePanel();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start); else start();
})();