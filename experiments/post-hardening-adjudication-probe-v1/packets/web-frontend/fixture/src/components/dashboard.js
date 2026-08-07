import { loadData } from '../api.js';
export function renderDashboard() {
  loadData().then(data => { document.getElementById('app').innerHTML = '<pre>' + JSON.stringify(data) + '</pre>'; });
}
