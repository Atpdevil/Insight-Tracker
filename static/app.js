// Toast notification system
function toast(msg) {
  const container = document.getElementById("toast-container");
  const t = document.createElement("div");
  t.className = "toast";
  t.textContent = msg;
  container.appendChild(t);

  setTimeout(() => t.remove(), 3500);
}

// Simple wrapper for API calls
async function api(path, opts = {}) {
  const res = await fetch('/api/' + path, opts);
  return res.json();
}

// ---------------------- LOAD TARGETS ----------------------
async function loadTargets() {
  const data = await api('targets');
  const list = document.getElementById('targets');

  list.innerHTML = '';

  (data || []).forEach(t => {
    const li = document.createElement('li');
    li.textContent = t.url;
    list.appendChild(li);
  });
}

// ---------------------- LOAD ALERTS ----------------------
async function loadAlerts() {
  const r = await api('alerts?limit=50');
  const div = document.getElementById('alerts');

  if (r.alerts && r.alerts.length) {
    div.textContent = r.alerts.join('\n');
  } else {
    div.textContent = 'No alerts yet.';
  }
}

// ---------------------- ADD TARGET ----------------------
document.getElementById('addBtn').addEventListener('click', async () => {
  const url = document.getElementById('url').value.trim();
  if (!url) return toast('Enter a URL');

  await api('targets', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url })
  });

  document.getElementById('url').value = '';
  await loadTargets();
  toast('Target added!');
});

// ---------------------- RUN CHECK ----------------------
document.getElementById('runBtn').addEventListener('click', async () => {
  const res = await api('check', { method: 'POST' });
  await loadAlerts();

  if (res.new_alerts && res.new_alerts.length > 0) {
    toast(`New alerts: ${res.new_alerts.length}`);
  } else {
    toast('No new alerts');
  }
});

// ---------------------- AUTO START ----------------------
document.getElementById('startBtn').addEventListener('click', async () => {
  await api('start', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ interval: 30 })
  });
  toast('Auto-monitor started');
});

// ---------------------- AUTO STOP ----------------------
document.getElementById('stopBtn').addEventListener('click', async () => {
  await api('stop', { method: 'POST' });
  toast('Auto-monitor stopped');
});

// ---------------------- CLEAR EVERYTHING ----------------------
document.getElementById('clearBtn').addEventListener('click', async () => {
  const res = await api('clear-all', { method: 'POST' });

  if (res.ok) {
    document.getElementById('alerts').textContent = 'No alerts yet.';
    document.getElementById('targets').innerHTML = '';
    toast('All alerts and targets cleared!');
  }
});

// ---------------------- AUTO REFRESH ALERTS ----------------------
window.addEventListener('load', () => {
  loadTargets();
  loadAlerts();
  setInterval(loadAlerts, 5000);
});

document.getElementById("clearBtn").addEventListener("click", async () => {
  const res = await fetch("/api/clear-all", { method: "POST" });
  const data = await res.json();

  if (data.ok) {
    // refresh UI
    await loadTargets();
    await loadAlerts();
    alert("All alerts and targets cleared!");
  } else {
    alert("Failed to clear data.");
  }
});