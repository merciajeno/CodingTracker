// main.js — reads data/*.json and populates the case file dashboard

const LC_FILE  = '../data/lc_history.json';
const GIT_FILE = '../data/git_history.json';
const ALERT_FILE = '../data/alerts.json';

// ── helpers ──────────────────────────────────────────────────────────────────
function today() {
  return new Date().toISOString().slice(0, 10);
}

function daysAgo(n) {
  const d = new Date();
  d.setDate(d.getDate() - n);
  return d.toISOString().slice(0, 10);
}

function within(entries, days) {
  const cutoff = daysAgo(days);
  return entries.filter(e => (e.date || '') >= cutoff);
}

function calcStreak(entries) {
  // entries sorted newest first, each has a .date field (YYYY-MM-DD)
  const days = [...new Set(entries.map(e => e.date))].sort().reverse();
  let streak = 0;
  let cursor = today();
  for (const d of days) {
    if (d === cursor) { streak++; cursor = daysAgo(1 + (streak - 1) + 1 - streak); }
    // simpler version:
    else break;
  }
  // proper streak: consecutive days ending today or yesterday
  let streak2 = 0;
  let ref = today();
  for (const d of days) {
    if (d === ref) { streak2++; const prev = new Date(ref); prev.setDate(prev.getDate()-1); ref = prev.toISOString().slice(0,10); }
    else if (d < ref) break;
  }
  return streak2;
}

async function load(url) {
  try {
    const r = await fetch(url);
    if (!r.ok) return [];
    return await r.json();
  } catch { return []; }
}

// ── render functions ──────────────────────────────────────────────────────────
function renderStats(lc, git, alerts) {
  const t = today();
  const lcToday  = lc.filter(s => s.date === t).length;
  const gitToday = git.filter(c => c.date === t).length;
  const lcWeek   = within(lc, 7).length;
  const gitWeek  = within(git, 7).length;
  const streak   = calcStreak(lc);
  const flagCount = alerts.length;

  document.getElementById('lc-today').textContent  = lcToday;
  document.getElementById('git-today').textContent = gitToday;
  document.getElementById('lc-streak').textContent = streak;
  document.getElementById('flag-count').textContent = flagCount;
  document.getElementById('lc-week').textContent   = `${lcWeek} this week`;
  document.getElementById('git-week').textContent  = `${gitWeek} this week`;

  if (flagCount === 0) document.getElementById('flag-count').classList.add('good');
  if (lcToday > 0)     document.getElementById('lc-today').classList.add('good');
  if (gitToday > 0)    document.getElementById('git-today').classList.add('good');

  // header status badge
  const badge = document.getElementById('status-badge');
  badge.textContent = flagCount > 0 ? `${flagCount} ALERT${flagCount > 1 ? 'S' : ''}` : 'NOMINAL';
  badge.className = 'badge ' + (flagCount > 0 ? 'alert' : 'ok');

  // report date
  document.getElementById('report-date').textContent =
    new Date().toUTCString().toUpperCase();
}

function renderAlerts(alertLog) {
  const list = document.getElementById('alerts-list');
  // alertLog is array of {date, alerts: [...strings]}
  const recent = alertLog.slice(0, 3); // last 3 runs
  const all = recent.flatMap(r => r.alerts || []);

  if (!all.length) {
    list.innerHTML = '<div class="no-alerts">NO ANOMALIES DETECTED. SUBJECT IS PERFORMING WITHIN EXPECTED PARAMETERS.</div>';
    return;
  }

  list.innerHTML = all.map(msg => {
    const [code, ...rest] = msg.split(':');
    return `<div class="alert-item">
      <span class="alert-code">[${code}]</span>
      <span>${rest.join(':').trim()}</span>
    </div>`;
  }).join('');
}

function renderDifficulty(lc) {
  const recent = lc.slice(0, 20);
  const easy   = recent.filter(s => s.difficulty === 'Easy').length;
  const medium = recent.filter(s => s.difficulty === 'Medium').length;
  const hard   = recent.filter(s => s.difficulty === 'Hard').length;
  const total  = recent.length || 1;

  // trigger width after paint so CSS transition fires
  requestAnimationFrame(() => {
    document.getElementById('bar-easy').style.width   = (easy/total*100)   + '%';
    document.getElementById('bar-medium').style.width = (medium/total*100) + '%';
    document.getElementById('bar-hard').style.width   = (hard/total*100)   + '%';
    document.getElementById('cnt-easy').textContent   = easy;
    document.getElementById('cnt-medium').textContent = medium;
    document.getElementById('cnt-hard').textContent   = hard;
  });
}

function diffTag(d) {
  const cls = d === 'Easy' ? 'easy' : d === 'Hard' ? 'hard' : 'medium';
  return `<span class="tag ${cls}">${d.toUpperCase()}</span>`;
}

function renderLCList(lc) {
  const ul = document.getElementById('lc-list');
  const recent = lc.slice(0, 8);
  if (!recent.length) { ul.innerHTML = '<li class="entry-item" style="color:var(--text-dim)">NO SUBMISSIONS ON RECORD</li>'; return; }
  ul.innerHTML = recent.map((s, i) => `
    <li class="entry-item" style="animation-delay:${i*0.05}s">
      <div class="entry-title">${s.title}</div>
      <div class="entry-meta">
        <span>${s.date}</span>
        ${s.difficulty ? diffTag(s.difficulty) : ''}
        ${(s.tags || []).slice(0, 2).map(t => `<span class="tag">${t}</span>`).join('')}
      </div>
    </li>`).join('');
}

function renderGitList(git) {
  const ul = document.getElementById('git-list');
  const recent = git.slice(0, 8);
  if (!recent.length) { ul.innerHTML = '<li class="entry-item" style="color:var(--text-dim)">NO COMMITS ON RECORD</li>'; return; }
  ul.innerHTML = recent.map((c, i) => `
    <li class="entry-item" style="animation-delay:${i*0.05}s">
      <div class="entry-title">${c.message || '(no message)'}</div>
      <div class="entry-meta">
        <span>${c.date}</span>
        <span>${c.repo ? c.repo.split('/')[1] : ''}</span>
        <span>+${c.additions || 0}/-${c.deletions || 0}</span>
        ${(c.flags || []).map(f => `<span class="tag flag">${f}</span>`).join('')}
      </div>
    </li>`).join('');
}

function renderTagCloud(lc) {
  const cloud = document.getElementById('tag-cloud');
  const all = lc.flatMap(s => s.tags || []);
  if (!all.length) { cloud.innerHTML = '<span class="loading-line">NO TAG DATA</span>'; return; }

  const counts = {};
  for (const t of all) counts[t] = (counts[t] || 0) + 1;
  const sorted = Object.entries(counts).sort((a,b) => b[1]-a[1]).slice(0, 18);
  const max = sorted[0][1];

  cloud.innerHTML = sorted.map(([tag, count]) => {
    const rank = count >= max * 0.7 ? 'rank-1' : count >= max * 0.4 ? 'rank-2' : 'rank-3';
    return `<span class="topic-tag ${rank}" title="${count} times">${tag}</span>`;
  }).join('');
}

function updateTicker(lc, git) {
  const t = today();
  const items = [
    `LC SOLVED TODAY: ${lc.filter(s=>s.date===t).length}`,
    `GIT COMMITS TODAY: ${git.filter(c=>c.date===t).length}`,
    `TOTAL LC ON RECORD: ${lc.length}`,
    `TOTAL COMMITS ON RECORD: ${git.length}`,
    `LAST SOLVE: ${lc[0]?.title || 'N/A'}`,
    `LAST COMMIT: ${git[0]?.message || 'N/A'}`,
  ];
  document.getElementById('ticker').textContent =
    items.join('  ///  ') + '  ///  ' + items.join('  ///  ');
}

// ── main ──────────────────────────────────────────────────────────────────────
async function main() {
  const [lc, git, alertLog] = await Promise.all([
    load(LC_FILE), load(GIT_FILE), load(ALERT_FILE)
  ]);

  const latestAlerts = alertLog[0]?.alerts || [];

  renderStats(lc, git, latestAlerts);
  renderAlerts(alertLog);
  renderDifficulty(lc);
  renderLCList(lc);
  renderGitList(git);
  renderTagCloud(lc);
  updateTicker(lc, git);
}

main();