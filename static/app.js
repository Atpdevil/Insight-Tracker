async function api(path, opts){
  const res = await fetch('/api/' + path, opts);
  return res.json();
}

async function loadTargets(){
  const data = await api('targets');
  const list = document.getElementById('targets');
  list.innerHTML = '';
  (data || []).forEach(t=>{
    const li = document.createElement('li');
    li.textContent = `${t.id} — ${t.url}`;
    list.appendChild(li);
  });
}

async function loadAlerts(){
  const r = await api('alerts?limit=50');
  const div = document.getElementById('alerts');
  div.textContent = (r.alerts && r.alerts.length) ? r.alerts.join('\n') : 'No alerts yet.';
}

document.getElementById('addBtn').addEventListener('click', async ()=>{
  const url = document.getElementById('url').value.trim();
  if(!url) return alert('Enter a URL');
  await api('targets', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({url})});
  document.getElementById('url').value = '';
  await loadTargets();
});

document.getElementById('runBtn').addEventListener('click', async ()=>{
  const res = await api('check', {method:'POST'});
  await loadAlerts();
  if(res.new_alerts && res.new_alerts.length>0){
    alert('New alerts: ' + res.new_alerts.length);
  } else {
    alert('No new alerts');
  }
});

document.getElementById('startBtn').addEventListener('click', async ()=>{
  await api('start', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({interval:30})});
  alert('Auto-monitor started (every 30s).');
});

document.getElementById('stopBtn').addEventListener('click', async ()=>{
  await api('stop', {method:'POST'});
  alert('Auto-monitor stopped.');
});

window.addEventListener('load', ()=>{
  loadTargets();
  loadAlerts();
  setInterval(loadAlerts, 5000);
});

document.getElementById('clearBtn').addEventListener('click', async ()=>{
  const res = await api('alerts/clear', {method:'POST'});
  if(res.ok){
    alert('Alerts cleared!');
    await loadAlerts();
  }
});