const routes = {};
let current = null;
const guards = [];
export const router = {
  add(path, handler, guard) { routes[path] = { handler, guard }; },
  start() { this.dispatch(); },
  dispatch() {
    const path = window.location.hash.slice(1);
    const r = routes[path];
    if (!r) return;
    if (r.guard && !r.guard()) { current = 'blocked'; return; }
    current = path;
    r.handler();
  },
  get current() { return current; },
};
