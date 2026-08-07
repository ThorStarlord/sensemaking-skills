import { renderDashboard } from './components/dashboard.js';
import { router } from './router.js';
router.register('/dashboard', renderDashboard);
router.start();
