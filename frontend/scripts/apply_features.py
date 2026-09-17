import os
import re

app_jsx_path = r"C:\Users\harsh\Downloads\resqlink_fixed\resqlink\frontend\src\App.jsx"
app_css_path = r"C:\Users\harsh\Downloads\resqlink_fixed\resqlink\frontend\src\App.css"

with open(app_jsx_path, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update Field component for Password Eye Toggle
new_field_code = """function Field({
  label,
  name,
  type = "text",
  placeholder,
  value,
  onChange,
  icon,
  min,
}) {
  const [showPassword, setShowPassword] = useState(false);
  const isPassword = type === "password";
  const actualType = isPassword ? (showPassword ? "text" : "password") : type;

  return (
    <label className="field">
      <span className="field-label">{label}</span>

      <span className="field-control">
        {icon && (
          <span className="field-icon">
            {icon}
          </span>
        )}

        <input
          name={name}
          type={actualType}
          placeholder={placeholder}
          value={value}
          onChange={onChange}
          min={min}
          autoComplete={isPassword ? "current-password" : undefined}
        />

        {isPassword && (
          <button
            type="button"
            className="password-toggle-btn"
            onClick={(e) => {
              e.preventDefault();
              setShowPassword(!showPassword);
            }}
            title={showPassword ? "Hide Password" : "Show Password"}
          >
            {showPassword ? "🙈" : "👁️"}
          </button>
        )}
      </span>
    </label>
  );
}"""

code = re.sub(r'function Field\(.*?^\}', new_field_code, code, flags=re.DOTALL | re.MULTILINE)

# 2. Update OrganizationsPage component for Modal View
new_org_page = """function OrganizationsPage({
  organizations,
}) {
  const [selectedOrg, setSelectedOrg] = useState(null);
  const items =
    organizations.length > 0
      ? organizations
      : SAMPLE_ORGANIZATIONS;

  return (
    <div className="inner-page">
      <div className="page-heading-row">
        <div>
          <div className="breadcrumb">
            ResQLink <span>/</span> Organizations
          </div>

          <h1>Verified Organizations</h1>

          <p>
            Discover verified NGOs, ashrams and community
            organizations.
          </p>
        </div>
      </div>

      <div className="organization-grid">
        {items.map((organization, index) => {
          const fallback =
            SAMPLE_ORGANIZATIONS[
              index % SAMPLE_ORGANIZATIONS.length
            ];
          const name = organization.organization_name || organization.name || fallback.name;
          const type = organization.organization_type || organization.type || fallback.type;
          const icon = fallback.icon || "🏢";

          return (
            <article
              className="organization-card"
              key={
                organization.id ||
                organization.user_id ||
                index
              }
            >
              <div className="organization-cover">
                <span>{icon}</span>
              </div>

              <div className="organization-card-body">
                <div className="organization-title-row">
                  <div>
                    <h3>{name}</h3>
                    <span>{type}</span>
                  </div>

                  <div className="verified-badge">
                    ✓ Verified
                  </div>
                </div>

                <p>
                  Supporting communities by connecting people
                  with useful resources and assistance.
                </p>

                <div className="organization-meta">
                  <span>📍 Community network</span>
                  <span>🤝 Active</span>
                </div>

                <button
                  type="button"
                  className="secondary-button full"
                  onClick={() => setSelectedOrg({ name, type, icon, address: organization.address || "Mysore, Karnataka", phone: organization.phone || "+91 98765 43210" })}
                >
                  View Organization
                </button>
              </div>
            </article>
          );
        })}
      </div>

      {selectedOrg && (
        <div className="modal-backdrop" onClick={() => setSelectedOrg(null)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <div className="brand-logo-row">
                <span style={{ fontSize: '32px' }}>{selectedOrg.icon}</span>
                <div>
                  <h3>{selectedOrg.name}</h3>
                  <span className="verified-badge">✓ Verified {selectedOrg.type}</span>
                </div>
              </div>
              <button type="button" className="modal-close" onClick={() => setSelectedOrg(null)}>×</button>
            </div>

            <div className="modal-body" style={{ display: 'flex', flexDirection: 'column', gap: '16px', marginTop: '16px' }}>
              <div>
                <strong style={{ fontSize: '12px', color: '#8fa39e', textTransform: 'uppercase' }}>About Organization</strong>
                <p style={{ marginTop: '4px', fontSize: '14px', color: '#173b35' }}>
                  Registered community organization providing shelter, food, clothing, and educational supplies to underprivileged individuals.
                </p>
              </div>

              <div>
                <strong style={{ fontSize: '12px', color: '#8fa39e', textTransform: 'uppercase' }}>Address & Location</strong>
                <p style={{ marginTop: '4px', fontSize: '14px', color: '#173b35' }}>📍 {selectedOrg.address}</p>
              </div>

              <div>
                <strong style={{ fontSize: '12px', color: '#8fa39e', textTransform: 'uppercase' }}>Contact Information</strong>
                <p style={{ marginTop: '4px', fontSize: '14px', color: '#173b35' }}>☎ {selectedOrg.phone}</p>
              </div>

              <div style={{ background: '#f4faf7', padding: '16px', borderRadius: '12px', border: '1px solid #bce3d6' }}>
                <strong style={{ color: '#147d63', fontSize: '14px' }}>Active Requirements</strong>
                <p style={{ fontSize: '13px', color: '#2c594e', marginTop: '4px' }}>
                  This organization currently accepts Clothes, Food Supplies, and Educational Books.
                </p>
              </div>
            </div>

            <div style={{ marginTop: '24px', display: 'flex', gap: '12px' }}>
              <button type="button" className="primary-button full" onClick={() => setSelectedOrg(null)}>
                Connect & Donate →
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}"""

code = re.sub(r'function OrganizationsPage\(.*?^\}', new_org_page, code, flags=re.DOTALL | re.MULTILINE)

# 3. Update VolunteerInfoPage component for Onboarding Modal
new_vol_page = """function VolunteerInfoPage({
  navigate,
}) {
  const [showModal, setShowModal] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [form, setForm] = useState({
    area: "Mysore Central",
    vehicle: "Two Wheeler",
    availability: "Weekends & Evenings",
    phone: "9876543210"
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmitted(true);
  };

  return (
    <div className="inner-page">
      <div className="page-heading-row">
        <div>
          <div className="breadcrumb">
            ResQLink <span>/</span> Volunteer
          </div>

          <h1>Make an Impact as a Volunteer</h1>

          <p>
            Help connect donations with people and organizations
            who need them.
          </p>
        </div>
      </div>

      <div className="volunteer-promo">
        <div className="volunteer-promo-icon">
          🤝
        </div>

        <div>
          <span className="hero-eyebrow">
            COMMUNITY SUPPORT
          </span>

          <h2>
            Your time can move resources where they're needed.
          </h2>

          <p>
            Volunteers can help with pickup, delivery and
            community coordination.
          </p>

          <button
            type="button"
            className="primary-button"
            onClick={() => setShowModal(true)}
          >
            Become a Volunteer →
          </button>
        </div>
      </div>

      {showModal && (
        <div className="modal-backdrop" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>🤝 Volunteer Verification & Onboarding</h3>
              <button type="button" className="modal-close" onClick={() => setShowModal(false)}>×</button>
            </div>

            {submitted ? (
              <div style={{ textAlign: 'center', padding: '24px 0' }}>
                <div style={{ fontSize: '48px', marginBottom: '16px' }}>🎉</div>
                <h3 style={{ fontSize: '20px', color: '#147d63', marginBottom: '8px' }}>Application Submitted!</h3>
                <p style={{ color: '#6b7f7a', marginBottom: '24px' }}>
                  Thank you for joining ResQLink! Your volunteer profile is active for <strong>{form.area}</strong>.
                </p>
                <button type="button" className="primary-button full" onClick={() => { setShowModal(false); setSubmitted(false); }}>
                  Go to Dashboard
                </button>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="auth-form">
                <Field
                  label="Preferred Service Area"
                  value={form.area}
                  onChange={(e) => setForm({ ...form, area: e.target.value })}
                  placeholder="e.g. Mysore Central / North"
                  icon="📍"
                />

                <Field
                  label="Vehicle / Transport Mode"
                  value={form.vehicle}
                  onChange={(e) => setForm({ ...form, vehicle: e.target.value })}
                  placeholder="e.g. Two Wheeler / Four Wheeler"
                  icon="🚲"
                />

                <Field
                  label="Availability"
                  value={form.availability}
                  onChange={(e) => setForm({ ...form, availability: e.target.value })}
                  placeholder="e.g. Weekends / Evenings"
                  icon="⏰"
                />

                <Field
                  label="Contact Mobile Number"
                  value={form.phone}
                  onChange={(e) => setForm({ ...form, phone: e.target.value })}
                  placeholder="Your mobile number"
                  icon="☎"
                />

                <button type="submit" className="primary-button full" style={{ marginTop: '12px' }}>
                  Complete Registration & Become Volunteer →
                </button>
              </form>
            )}
          </div>
        </div>
      )}
    </div>
  );
}"""

code = re.sub(r'function VolunteerInfoPage\(.*?^\}', new_vol_page, code, flags=re.DOTALL | re.MULTILINE)

# 4. Add NotificationsPage component and replace SimpleListPage render for notifications
notifications_page_code = """function NotificationsPage() {
  const [notifications, setNotifications] = useState([
    {
      id: 1,
      icon: "🎁",
      title: "Donation Verified",
      message: "Your donation of 50 Winter Blankets to Hope Foundation has been verified.",
      time: "10m ago",
      read: false
    },
    {
      id: 2,
      icon: "📋",
      title: "New Requirement Posted",
      message: "Sri Sai Ashram posted a requirement for School Books near Mysore.",
      time: "1h ago",
      read: false
    },
    {
      id: 3,
      icon: "🤝",
      title: "Volunteer Coordination",
      message: "Pickup scheduled for tomorrow at 10:00 AM in Mysore Central.",
      time: "3h ago",
      read: false
    }
  ]);

  const markAllRead = () => {
    setNotifications(notifications.map(n => ({ ...n, read: true })));
  };

  return (
    <div className="inner-page">
      <div className="page-heading-row">
        <div>
          <div className="breadcrumb">
            ResQLink <span>/</span> Notifications
          </div>

          <h1>Notifications</h1>

          <p>Stay updated on your activity, requirements, and community impacts.</p>
        </div>

        <button type="button" className="secondary-button" onClick={markAllRead}>
          ✓ Mark all as read
        </button>
      </div>

      <div className="notifications-list">
        {notifications.map((item) => (
          <div key={item.id} className={`notification-card ${item.read ? 'read' : 'unread'}`}>
            <div className="notification-icon">{item.icon}</div>

            <div className="notification-content">
              <div className="notification-header">
                <strong>{item.title}</strong>
                <span className="notification-time">{item.time}</span>
              </div>
              <p>{item.message}</p>
            </div>

            {!item.read && <span className="unread-dot">●</span>}
          </div>
        ))}
      </div>
    </div>
  );
}
"""

if "function NotificationsPage" not in code:
    code = code.replace("function SettingsPage", notifications_page_code + "\nfunction SettingsPage")

code = code.replace(
    '''{activePage === "notifications" && (
            <SimpleListPage
              title="Notifications"
              subtitle="Stay updated about your donations and requests."
              icon="🔔"
              emptyText="You're all caught up."
            />
          )}''',
    '''{activePage === "notifications" && (
            <NotificationsPage />
          )}'''
)

with open(app_jsx_path, "w", encoding="utf-8") as f:
    f.write(code)

print("App.jsx patched successfully!")

# Also append CSS rules to App.css
css_append = """
/* PASSWORD TOGGLE BUTTON */
.password-toggle-btn {
  position: absolute;
  right: 14px;
  background: none;
  border: none;
  font-size: 16px;
  cursor: pointer;
  z-index: 2;
}

/* NOTIFICATIONS LIST */
.notifications-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
  margin-top: 16px;
}

.notification-card {
  background: #ffffff;
  border: 1px solid #e0eae6;
  border-radius: 16px;
  padding: 18px 20px;
  display: flex;
  align-items: flex-start;
  gap: 16px;
  transition: all 0.2s ease;
  position: relative;
}

.notification-card.unread {
  border-left: 4px solid #147d63;
  background: #fbfdfc;
}

.notification-card.read {
  opacity: 0.8;
}

.notification-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: #f0f7f4;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  flex-shrink: 0;
}

.notification-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.notification-header strong {
  font-size: 15px;
  font-weight: 700;
  color: #173b35;
}

.notification-time {
  font-size: 12px;
  color: #8fa39e;
}

.notification-content p {
  font-size: 14px;
  color: #6b7f7a;
  margin: 0;
}

.unread-dot {
  color: #147d63;
  font-size: 10px;
}

/* VOLUNTEER PROMO */
.volunteer-promo {
  background: linear-gradient(135deg, #ffffff 0%, #f4faf7 100%);
  border: 1px solid #e0eae6;
  border-radius: 20px;
  padding: 40px;
  display: flex;
  align-items: center;
  gap: 32px;
  box-shadow: 0 4px 20px rgba(24, 61, 53, 0.04);
}

.volunteer-promo-icon {
  width: 80px;
  height: 80px;
  border-radius: 24px;
  background: #e8f7f1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  flex-shrink: 0;
}

.volunteer-promo h2 {
  font-size: 24px;
  font-weight: 800;
  color: #173b35;
  margin: 6px 0 10px;
}

.volunteer-promo p {
  font-size: 15px;
  color: #6b7f7a;
  margin-bottom: 24px;
}

/* ORGANIZATIONS GRID */
.organization-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-top: 16px;
}

.organization-card {
  background: #ffffff;
  border: 1px solid #e0eae6;
  border-radius: 18px;
  overflow: hidden;
  transition: all 0.2s ease;
  display: flex;
  flex-direction: column;
}

.organization-card:hover {
  transform: translateY(-2px);
  border-color: #147d63;
  box-shadow: 0 8px 24px rgba(24, 61, 53, 0.08);
}

.organization-cover {
  height: 90px;
  background: linear-gradient(135deg, #147d63, #0e5f4d);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 36px;
  color: #ffffff;
}

.organization-card-body {
  padding: 20px;
  display: flex;
  flex-direction: column;
  flex: 1;
  gap: 12px;
}

.organization-title-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.organization-title-row h3 {
  font-size: 16px;
  font-weight: 700;
  color: #173b35;
}

.organization-title-row span {
  font-size: 12px;
  color: #6b7f7a;
}

.organization-meta {
  display: flex;
  gap: 14px;
  font-size: 12px;
  color: #6b7f7a;
  margin-top: auto;
  padding-top: 12px;
  border-top: 1px solid #f0f5f3;
}
"""

with open(app_css_path, "a", encoding="utf-8") as f:
    f.write(css_append)

print("App.css appended successfully!")
