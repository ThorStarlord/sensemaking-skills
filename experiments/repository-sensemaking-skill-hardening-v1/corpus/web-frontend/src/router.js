const routes = {};
export const router = {
  register(path, handler) { routes[path] = handler; },
  start() { window.addEventListener('hashchange', () => this.dispatch()); this.dispatch(); },
  dispatch() { const h = routes[window.location.hash.slice(1)]; if (h) h(); },
};
