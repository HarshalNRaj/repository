import os

css_content = """/* =========================================================
   RESQLINK — COMPLETE APPLICATION STYLES (ALL JSX CLASSES MATCHED)
   ========================================================= */

:root {
  --primary: #147d63;
  --primary-dark: #0e5f4d;
  --primary-light: #e8f7f1;

  --text: #173b35;
  --text-dark: #12342e;
  --text-muted: #6b7f7a;

  --border: #dfeae6;
  --border-light: #edf3f0;

  --surface: #ffffff;
  --surface-soft: #f7faf9;
  --background: #f4f8f6;

  --success: #21885f;
  --warning: #d68a24;
  --danger: #c94b55;
  --info: #3478b9;

  --shadow-sm: 0 2px 10px rgba(24, 61, 53, 0.05);
  --shadow: 0 8px 28px rgba(24, 61, 53, 0.08);
  --shadow-lg: 0 20px 55px rgba(24, 61, 53, 0.12);

  --radius-sm: 10px;
  --radius: 16px;
  --radius-lg: 22px;

  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html, body, #root {
  min-height: 100%;
  width: 100%;
  margin: 0;
  background: var(--background);
  color: var(--text);
}

button, input, select, textarea {
  font: inherit;
}

button {
  cursor: pointer;
}

/* =========================================================
   AUTHENTICATION PAGE STYLES (.auth-page, .auth-card)
   ========================================================= */

.auth-page {
  min-height: 100vh;
  width: 100vw;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 32px 20px;
  background: radial-gradient(circle at 10% 20%, #eef7f4 0%, #f4f8f6 100%);
}

.auth-card {
  width: 100%;
  max-width: 1100px;
  min-height: 680px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  background: #ffffff;
  border-radius: 24px;
  box-shadow: 0 20px 60px rgba(18, 52, 46, 0.12);
  overflow: hidden;
  border: 1px solid #e0eae6;
}

.auth-brand-panel {
  background: linear-gradient(145deg, #147d63 0%, #0e5f4d 100%);
  color: #ffffff;
  padding: 48px 40px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
}

.auth-brand-panel::before {
  content: "";
  position: absolute;
  top: -100px;
  right: -100px;
  width: 300px;
  height: 300px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.08);
  pointer-events: none;
}

.brand-logo-row {
  display: flex;
  align-items: center;
  gap: 16px;
}

.brand-mark {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
}

.brand-name {
  font-size: 24px;
  font-weight: 800;
  letter-spacing: -0.5px;
}

.brand-tagline {
  font-size: 13px;
  opacity: 0.85;
  margin-top: 2px;
}

.brand-main-copy {
  margin: 32px 0;
}

.brand-emoji {
  font-size: 40px;
  display: block;
  margin-bottom: 16px;
}

.brand-main-copy h2 {
  font-size: 32px;
  font-weight: 700;
  color: #ffffff;
  line-height: 1.25;
  margin-bottom: 8px;
}

.brand-main-copy h3 {
  font-size: 20px;
  font-weight: 600;
  color: #a3e4d7;
  margin-bottom: 16px;
}

.brand-main-copy p {
  font-size: 15px;
  line-height: 1.6;
  opacity: 0.9;
  max-width: 400px;
}

.impact-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin: 24px 0;
}

.impact-list div {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  background: rgba(255, 255, 255, 0.1);
  padding: 10px 16px;
  border-radius: 12px;
  backdrop-filter: blur(4px);
}

.impact-list span {
  font-size: 18px;
}

.brand-footer {
  font-size: 13px;
  opacity: 0.8;
  display: flex;
  align-items: center;
  gap: 6px;
}

.auth-form-panel {
  padding: 48px 44px;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  background: #ffffff;
}

.auth-top-link {
  text-align: right;
  font-size: 14px;
  color: #5d6d69;
  margin-bottom: 24px;
}

.auth-top-link .text-button {
  color: #147d63;
  font-weight: 600;
  margin-left: 6px;
  background: none;
  border: none;
  cursor: pointer;
  text-decoration: underline;
}

.auth-heading {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 24px;
}

.auth-heading-icon {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  background: #e8f7f1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  flex-shrink: 0;
}

.auth-brand-small {
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #147d63;
  margin-bottom: 4px;
}

.auth-heading h1 {
  font-size: 26px;
  font-weight: 700;
  color: #173b35;
  margin: 0 0 6px 0;
}

.auth-heading p {
  font-size: 14px;
  color: #6b7f7a;
  margin: 0;
}

.auth-tabs {
  display: flex;
  background: #f0f5f3;
  padding: 4px;
  border-radius: 12px;
  margin-bottom: 28px;
}

.auth-tabs button {
  flex: 1;
  padding: 10px;
  border: none;
  background: transparent;
  font-size: 14px;
  font-weight: 600;
  color: #6b7f7a;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.auth-tabs button.active {
  background: #ffffff;
  color: #147d63;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
  width: 100%;
}

.field-label {
  font-size: 13px;
  font-weight: 600;
  color: #2c443e;
}

.field-control {
  position: relative;
  display: flex;
  align-items: center;
  width: 100%;
}

.field-icon {
  position: absolute;
  left: 14px;
  font-size: 16px;
  color: #8fa39e;
  pointer-events: none;
  z-index: 1;
}

.field-control input,
.field-control select,
.field-control textarea {
  width: 100%;
  padding: 12px 14px 12px 42px;
  font-size: 14px;
  border: 1px solid #d3e0dc;
  border-radius: 10px;
  background: #fcfdfe;
  color: #173b35;
  transition: border-color 0.2s, box-shadow 0.2s;
  box-sizing: border-box;
}

.field-control input:focus,
.field-control select:focus,
.field-control textarea:focus {
  outline: none;
  border-color: #147d63;
  box-shadow: 0 0 0 3px rgba(20, 125, 99, 0.12);
  background: #ffffff;
}

.forgot-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: -4px;
}

.text-button {
  background: none;
  border: none;
  color: #147d63;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  padding: 0;
}

.text-button.small {
  font-size: 12px;
}

.primary-button,
.primary-btn {
  background: #147d63;
  color: #ffffff;
  border: none;
  padding: 14px 24px;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s, transform 0.1s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: auto;
}

.primary-button:hover,
.primary-btn:hover {
  background: #0e5f4d;
}

.primary-button.full,
.primary-btn.full {
  width: 100%;
}

.secondary-button,
.secondary-btn {
  background: #ffffff;
  color: #147d63;
  border: 1px solid #d3e0dc;
  padding: 12px 20px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.secondary-button:hover,
.secondary-btn:hover {
  background: #f4f8f6;
  border-color: #147d63;
}

.demo-login {
  background: #f4faf7;
  border: 1px dashed #bce3d6;
  padding: 12px 16px;
  border-radius: 10px;
  font-size: 12px;
  color: #2c594e;
  display: flex;
  gap: 12px;
  align-items: center;
  margin-top: 8px;
}

.demo-login strong {
  color: #147d63;
}

.form-grid.two {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.role-section {
  margin-bottom: 20px;
}

.section-label {
  font-size: 14px;
  font-weight: 700;
  color: #173b35;
  margin-bottom: 12px;
  display: flex;
  flex-direction: column;
}

.section-label span {
  font-size: 12px;
  font-weight: 400;
  color: #6b7f7a;
}

.role-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.role-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  border: 1px solid #d3e0dc;
  border-radius: 12px;
  background: #ffffff;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
}

.role-card:hover {
  border-color: #147d63;
  background: #f7faf9;
}

.role-card.selected {
  border-color: #147d63;
  background: #e8f7f1;
  box-shadow: 0 0 0 1px #147d63;
}

.role-icon {
  font-size: 22px;
  flex-shrink: 0;
}

.role-content {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.role-content strong {
  font-size: 13px;
  color: #173b35;
}

.role-content small {
  font-size: 11px;
  color: #6b7f7a;
}

.role-check {
  color: #147d63;
  font-weight: bold;
  font-size: 14px;
}

.admin-info {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #6b7f7a;
  background: #f7f9f8;
  padding: 10px 14px;
  border-radius: 8px;
  margin-top: 12px;
}

/* =========================================================
   MAIN APPLICATION LAYOUT (.resqlink-app)
   ========================================================= */

.resqlink-app {
  min-height: 100vh;
  width: 100vw;
  display: flex;
  background: #f4f8f6;
  color: #173b35;
  overflow-x: hidden;
}

/* =========================================================
   SIDEBAR STYLES
   ========================================================= */

.mobile-sidebar-backdrop {
  display: none;
}

.sidebar {
  width: 275px;
  min-width: 275px;
  height: 100vh;
  position: sticky;
  top: 0;
  background: #ffffff;
  border-right: 1px solid #e0eae6;
  display: flex;
  flex-direction: column;
  z-index: 100;
  overflow-y: auto;
}

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 24px 20px 20px;
  border-bottom: 1px solid #f0f5f3;
}

.sidebar-logo {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  background: linear-gradient(135deg, #147d63, #0e5f4d);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: bold;
  box-shadow: 0 4px 10px rgba(20, 125, 99, 0.2);
}

.sidebar-brand-name {
  font-size: 19px;
  font-weight: 800;
  color: #173b35;
  letter-spacing: -0.4px;
}

.sidebar-brand-subtitle {
  font-size: 11px;
  color: #6b7f7a;
  margin-top: 1px;
}

.mobile-close-button {
  display: none;
}

.sidebar-user {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  background: #f7faf9;
  margin: 16px;
  border-radius: 14px;
  border: 1px solid #e5eeeb;
}

.sidebar-avatar {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  background: #147d63;
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
  flex-shrink: 0;
}

.sidebar-user-info {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
}

.sidebar-user-info strong {
  font-size: 13px;
  font-weight: 700;
  color: #173b35;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sidebar-user-info span {
  font-size: 11px;
  color: #6b7f7a;
  margin-top: 1px;
}

.verified-dot {
  color: #147d63;
  font-weight: bold;
  font-size: 14px;
}

.sidebar-navigation {
  flex: 1;
  padding: 8px 16px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.nav-group {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.nav-group-title {
  font-size: 11px;
  font-weight: 700;
  color: #94a5a0;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  padding: 0 12px 6px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  border-radius: 12px;
  border: none;
  background: transparent;
  color: #4a5d58;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  text-align: left;
  width: 100%;
  transition: all 0.2s ease;
}

.nav-item:hover {
  background: #f0f5f3;
  color: #147d63;
}

.nav-item.active {
  background: #e8f7f1;
  color: #147d63;
  font-weight: 700;
}

.nav-icon {
  font-size: 18px;
  width: 22px;
  display: inline-flex;
  justify-content: center;
}

.nav-badge {
  margin-left: auto;
  background: #147d63;
  color: #ffffff;
  font-size: 11px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 99px;
}

.sidebar-impact {
  margin: 16px;
  padding: 14px;
  background: linear-gradient(135deg, #e8f7f1, #d6f0e6);
  border-radius: 14px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 12px;
  color: #173b35;
}

.impact-decoration {
  font-size: 20px;
}

.sidebar-logout {
  margin: 0 16px 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 14px;
  border: 1px solid #fee2e2;
  background: #fff5f5;
  color: #dc2626;
  font-size: 14px;
  font-weight: 600;
  border-radius: 12px;
  cursor: pointer;
  width: calc(100% - 32px);
  transition: all 0.2s ease;
}

.sidebar-logout:hover {
  background: #fdeeee;
}

/* =========================================================
   DASHBOARD SHELL & TOPBAR
   ========================================================= */

.dashboard-shell {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.topbar {
  height: 72px;
  min-height: 72px;
  background: #ffffff;
  border-bottom: 1px solid #e0eae6;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
  position: sticky;
  top: 0;
  z-index: 90;
}

.mobile-menu-button {
  display: none;
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  margin-right: 12px;
  color: #173b35;
}

.topbar-search {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #f4f8f6;
  border: 1px solid #e0eae6;
  border-radius: 12px;
  padding: 8px 16px;
  width: 380px;
  max-width: 100%;
  transition: all 0.2s;
}

.topbar-search:focus-within {
  border-color: #147d63;
  background: #ffffff;
  box-shadow: 0 0 0 3px rgba(20, 125, 99, 0.1);
}

.topbar-search span {
  color: #8fa39e;
  font-size: 16px;
}

.topbar-search input {
  border: none;
  background: transparent;
  outline: none;
  font-size: 14px;
  width: 100%;
  color: #173b35;
}

.topbar-actions {
  display: flex;
  align-items: center;
  gap: 18px;
}

.topbar-location {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #4a5d58;
  background: #f4f8f6;
  padding: 8px 14px;
  border-radius: 10px;
  border: 1px solid #e0eae6;
}

.topbar-icon-button {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  border: 1px solid #e0eae6;
  background: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  cursor: pointer;
  position: relative;
  transition: all 0.2s;
}

.topbar-icon-button:hover {
  background: #f4f8f6;
  border-color: #147d63;
}

.notification-dot {
  position: absolute;
  top: -4px;
  right: -4px;
  background: #dc2626;
  color: #ffffff;
  font-size: 10px;
  font-weight: bold;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #ffffff;
}

.topbar-profile {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 12px;
  transition: background 0.2s;
}

.topbar-profile:hover {
  background: #f4f8f6;
}

.topbar-avatar {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: #147d63;
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
}

.topbar-profile-text {
  display: flex;
  flex-direction: column;
  text-align: left;
}

.topbar-profile-text strong {
  font-size: 13px;
  font-weight: 700;
  color: #173b35;
}

.topbar-profile-text span {
  font-size: 11px;
  color: #6b7f7a;
}

.topbar-chevron {
  font-size: 12px;
  color: #6b7f7a;
}

/* =========================================================
   DASHBOARD CONTENT & WIDGETS
   ========================================================= */

.dashboard-content {
  flex: 1;
  padding: 32px;
  background: #f4f8f6;
  overflow-y: auto;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

.page-heading-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 28px;
}

.breadcrumb {
  font-size: 12px;
  color: #6b7f7a;
  margin-bottom: 6px;
  font-weight: 500;
}

.breadcrumb span {
  margin: 0 4px;
  color: #b0c0bc;
}

.page-heading-row h1 {
  font-size: 28px;
  font-weight: 800;
  color: #173b35;
  margin-bottom: 6px;
}

.page-heading-row p {
  font-size: 14px;
  color: #6b7f7a;
  margin: 0;
}

.verified-profile-pill {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #e8f7f1;
  color: #147d63;
  padding: 8px 16px;
  border-radius: 99px;
  font-size: 13px;
  font-weight: 600;
  border: 1px solid #bce3d6;
}

.dashboard-hero {
  background: linear-gradient(135deg, #147d63 0%, #0e5f4d 100%);
  border-radius: 20px;
  padding: 36px 40px;
  color: #ffffff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  box-shadow: 0 10px 30px rgba(20, 125, 99, 0.2);
  position: relative;
  overflow: hidden;
}

.hero-copy {
  max-width: 520px;
  z-index: 2;
}

.hero-eyebrow {
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 1.5px;
  opacity: 0.85;
  display: block;
  margin-bottom: 8px;
}

.hero-copy h2 {
  font-size: 28px;
  font-weight: 800;
  margin-bottom: 10px;
  line-height: 1.25;
  color: #ffffff;
}

.hero-copy p {
  font-size: 14px;
  opacity: 0.9;
  margin-bottom: 24px;
  line-height: 1.6;
}

.hero-buttons {
  display: flex;
  gap: 12px;
}

.hero-buttons .primary-button {
  background: #ffffff;
  color: #147d63;
}

.hero-buttons .primary-button:hover {
  background: #f0f5f3;
}

.hero-buttons .secondary-button {
  background: rgba(255, 255, 255, 0.15);
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.hero-buttons .secondary-button:hover {
  background: rgba(255, 255, 255, 0.25);
}

/* STATS GRID */

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 32px;
}

.stat-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 20px 24px;
  border: 1px solid #e0eae6;
  box-shadow: 0 4px 16px rgba(24, 61, 53, 0.04);
  display: flex;
  align-items: center;
  gap: 16px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(24, 61, 53, 0.08);
}

.stat-icon-wrapper {
  width: 52px;
  height: 52px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  flex-shrink: 0;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 24px;
  font-weight: 800;
  color: #173b35;
  margin-bottom: 2px;
}

.stat-label {
  font-size: 13px;
  color: #6b7f7a;
  font-weight: 500;
}

/* CATEGORIES */

.categories-section {
  margin-bottom: 32px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-header h3 {
  font-size: 18px;
  font-weight: 700;
  color: #173b35;
}

.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 14px;
}

.category-chip {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 18px 12px;
  background: #ffffff;
  border: 1px solid #e0eae6;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 13px;
  font-weight: 600;
  color: #173b35;
}

.category-chip:hover {
  border-color: #147d63;
  background: #f7faf9;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(20, 125, 99, 0.08);
}

.category-icon {
  font-size: 26px;
}

/* CONTENT GRID */

.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-bottom: 32px;
}

.card {
  background: #ffffff;
  border-radius: 18px;
  border: 1px solid #e0eae6;
  padding: 24px;
  box-shadow: 0 4px 16px rgba(24, 61, 53, 0.04);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.card-header h3 {
  font-size: 18px;
  font-weight: 700;
  color: #173b35;
}

.need-item,
.org-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 16px;
  border-radius: 12px;
  border: 1px solid #eef4f2;
  background: #fafcfb;
  margin-bottom: 12px;
  transition: all 0.2s;
}

.need-item:hover,
.org-item:hover {
  border-color: #147d63;
  background: #ffffff;
  box-shadow: 0 4px 12px rgba(24, 61, 53, 0.06);
}

.need-info,
.org-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.need-info strong,
.org-info strong {
  font-size: 14px;
  font-weight: 700;
  color: #173b35;
}

.need-info span,
.org-info span {
  font-size: 12px;
  color: #6b7f7a;
}

/* MODALS */

.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(15, 35, 30, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
  padding: 20px;
}

.modal {
  background: #ffffff;
  border-radius: 20px;
  padding: 32px;
  width: 100%;
  max-width: 560px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
  border: 1px solid #e0eae6;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.modal-header h3 {
  font-size: 20px;
  font-weight: 700;
  color: #173b35;
}

.modal-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #6b7f7a;
}

/* RESPONSIVE DESIGN */

@media (max-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .content-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 900px) {
  .sidebar {
    position: fixed;
    left: -280px;
    transition: left 0.3s ease;
  }
  .sidebar.mobile-open {
    left: 0;
  }
  .mobile-sidebar-backdrop {
    display: block;
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.5);
    z-index: 99;
  }
  .mobile-menu-button {
    display: block;
  }
  .mobile-close-button {
    display: block;
  }
  .topbar {
    padding: 0 16px;
  }
  .dashboard-content {
    padding: 20px 16px;
  }
  .dashboard-hero {
    flex-direction: column;
    align-items: flex-start;
    gap: 20px;
    padding: 24px;
  }
}

@media (max-width: 640px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  .topbar-search {
    display: none;
  }
  .topbar-location {
    display: none;
  }
}
"""

with open(r"C:\Users\harsh\Downloads\resqlink_fixed\resqlink\frontend\src\App.css", "w", encoding="utf-8") as f:
    f.write(css_content)

print("App.css completely updated!")
