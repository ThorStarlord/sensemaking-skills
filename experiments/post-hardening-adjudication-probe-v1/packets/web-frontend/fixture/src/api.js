export async function loadData() {
  return fetch('/api/data').then(r => r.json());
}
