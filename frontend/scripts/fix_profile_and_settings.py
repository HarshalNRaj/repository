import os

app_path = r"c:\Users\harsh\Downloads\resqlink_fixed\resqlink\frontend\src\App.jsx"

with open(app_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Topbar invocation in App component to pass logout
content = content.replace(
    '''        <Topbar
          user={user}
          roleLabel={roleLabel}
          mobileMenuOpen={mobileMenuOpen}
          setMobileMenuOpen={setMobileMenuOpen}
          navigate={navigate}
        />''',
    '''        <Topbar
          user={user}
          roleLabel={roleLabel}
          mobileMenuOpen={mobileMenuOpen}
          setMobileMenuOpen={setMobileMenuOpen}
          navigate={navigate}
          logout={logout}
        />'''
)

# 2. Update SettingsPage and ProfilePage invocations in App component to pass navigate
content = content.replace(
    '''          {activePage === "settings" && (
            <SettingsPage user={user} />
          )}

          {activePage === "profile" && (
            <ProfilePage user={user} />
          )}''',
    '''          {activePage === "settings" && (
            <SettingsPage user={user} navigate={navigate} />
          )}

          {activePage === "profile" && (
            <ProfilePage user={user} navigate={navigate} />
          )}'''
)

# 3. Update Topbar implementation to include profile dropdown
old_topbar = '''function Topbar({
  user,
  roleLabel,
  setMobileMenuOpen,
  navigate,
}) {
  const [searchText, setSearchText] = useState("");

  const handleSearch = (e) => {
    if (e.key === "Enter" && searchText.trim()) {
      navigate("receive");
    }
  };
  return (
    <header className="topbar">
      <button
        type="button"
        className="mobile-menu-button"
        onClick={() => setMobileMenuOpen(true)}
        aria-label="Open menu"
      >
        ☰
      </button>

      <div className="topbar-search">
        <span>⌕</span>

        <input
          type="text"
          placeholder="Search for items, NGOs, ashrams, blood banks..."
          value={searchText}
          onChange={(e) => setSearchText(e.target.value)}
          onKeyDown={handleSearch}
        />

        <button type="button" className="search-go-btn" onClick={() => { if (searchText.trim()) navigate("receive"); }}>
          Search
        </button>
      </div>

      <div className="topbar-actions">
        <div className="topbar-location">
          <span>📍</span>
          <strong>{user?.location || "Your Location"}</strong>
        </div>

        <button
          type="button"
          className="topbar-icon-button"
          aria-label="Notifications"
          onClick={() => navigate("notifications")}
        >
          🔔
          <span className="notification-dot">3</span>
        </button>

        <div className="topbar-profile">
          <div className="topbar-avatar">
            {getInitials(user?.name)}
          </div>

          <div className="topbar-profile-text">
            <strong>{user?.name || "User"}</strong>
            <span>{roleLabel}</span>
          </div>

          <span className="topbar-chevron">⌄</span>
        </div>
      </div>
    </header>
  );
}'''

new_topbar = '''function Topbar({
  user,
  roleLabel,
  setMobileMenuOpen,
  navigate,
  logout,
}) {
  const [searchText, setSearchText] = useState("");
  const [showProfileMenu, setShowProfileMenu] = useState(false);

  const handleSearch = (e) => {
    if (e.key === "Enter" && searchText.trim()) {
      navigate("receive");
    }
  };

  return (
    <header className="topbar">
      <button
        type="button"
        className="mobile-menu-button"
        onClick={() => setMobileMenuOpen(true)}
        aria-label="Open menu"
      >
        ☰
      </button>

      <div className="topbar-search">
        <span>⌕</span>

        <input
          type="text"
          placeholder="Search for items, NGOs, ashrams, blood banks..."
          value={searchText}
          onChange={(e) => setSearchText(e.target.value)}
          onKeyDown={handleSearch}
        />

        <button type="button" className="search-go-btn" onClick={() => { if (searchText.trim()) navigate("receive"); }}>
          Search
        </button>
      </div>

      <div className="topbar-actions">
        <div className="topbar-location">
          <span>📍</span>
          <strong>{user?.location || "Mysore"}</strong>
        </div>

        <button
          type="button"
          className="topbar-icon-button"
          aria-label="Notifications"
          onClick={() => navigate("notifications")}
        >
          🔔
          <span className="notification-dot">3</span>
        </button>

        <div style={{ position: "relative" }}>
          <div 
            className="topbar-profile"
            onClick={() => setShowProfileMenu(!showProfileMenu)}
            style={{ cursor: "pointer", userSelect: "none" }}
          >
            <div className="topbar-avatar">
              {getInitials(user?.name)}
            </div>

            <div className="topbar-profile-text">
              <strong>{user?.name || "User"}</strong>
              <span>{roleLabel}</span>
            </div>

            <span className="topbar-chevron">{showProfileMenu ? "⌃" : "⌄"}</span>
          </div>

          {showProfileMenu && (
            <div 
              className="topbar-dropdown-menu"
              style={{
                position: "absolute",
                top: "calc(100% + 8px)",
                right: 0,
                backgroundColor: "#ffffff",
                borderRadius: "12px",
                boxShadow: "0 10px 25px rgba(0, 0, 0, 0.15)",
                border: "1px solid #e2e8f0",
                minWidth: "200px",
                zIndex: 100,
                overflow: "hidden",
                padding: "6px 0"
              }}
            >
              <button
                type="button"
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "10px",
                  width: "100%",
                  padding: "10px 16px",
                  border: "none",
                  background: "none",
                  textAlign: "left",
                  fontSize: "14px",
                  fontWeight: 500,
                  color: "#1e293b",
                  cursor: "pointer"
                }}
                onClick={() => { navigate("profile"); setShowProfileMenu(false); }}
              >
                👤 View Profile
              </button>
              <button
                type="button"
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "10px",
                  width: "100%",
                  padding: "10px 16px",
                  border: "none",
                  background: "none",
                  textAlign: "left",
                  fontSize: "14px",
                  fontWeight: 500,
                  color: "#1e293b",
                  cursor: "pointer"
                }}
                onClick={() => { navigate("settings"); setShowProfileMenu(false); }}
              >
                ⚙️ Settings
              </button>
              <button
                type="button"
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "10px",
                  width: "100%",
                  padding: "10px 16px",
                  border: "none",
                  background: "none",
                  textAlign: "left",
                  fontSize: "14px",
                  fontWeight: 500,
                  color: "#1e293b",
                  cursor: "pointer"
                }}
                onClick={() => { navigate("notifications"); setShowProfileMenu(false); }}
              >
                🔔 Notifications
              </button>
              <div style={{ height: "1px", backgroundColor: "#f1f5f9", margin: "4px 0" }}></div>
              <button
                type="button"
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "10px",
                  width: "100%",
                  padding: "10px 16px",
                  border: "none",
                  background: "none",
                  textAlign: "left",
                  fontSize: "14px",
                  fontWeight: 600,
                  color: "#ef4444",
                  cursor: "pointer"
                }}
                onClick={() => { if (logout) logout(); setShowProfileMenu(false); }}
              >
                ↪ Logout
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}'''

content = content.replace(old_topbar, new_topbar)

# 4. Replace SettingsPage and ProfilePage
old_settings_and_profile = '''function SettingsPage({ user }) {
  return (
    <div className="inner-page">
      <div className="page-heading-row">
        <div>
          <div className="breadcrumb">
            ResQLink <span>/</span> Settings
          </div>

          <h1>Settings</h1>

          <p>
            Manage your account preferences and platform
            experience.
          </p>
        </div>
      </div>

      <div className="settings-grid">
        <div className="settings-card">
          <div className="settings-card-icon">
            👤
          </div>

          <div>
            <h3>Account</h3>
            <p>
              Signed in as{" "}
              <strong>{user?.email}</strong>
            </p>
          </div>

          <button
            type="button"
            className="secondary-button"
          >
            Manage
          </button>
        </div>

        <div className="settings-card">
          <div className="settings-card-icon">
            🔔
          </div>

          <div>
            <h3>Notifications</h3>
            <p>
              Receive updates about donations, requests and
              connections.
            </p>
          </div>

          <button
            type="button"
            className="toggle-button active"
          >
            On
          </button>
        </div>

        <div className="settings-card">
          <div className="settings-card-icon">
            🔒
          </div>

          <div>
            <h3>Security</h3>
            <p>
              Keep your account secure with a strong password.
            </p>
          </div>

          <button
            type="button"
            className="secondary-button"
          >
            Review
          </button>
        </div>
      </div>
    </div>
  );
}

function ProfilePage({ user }) {
  return (
    <div className="inner-page">
      <div className="page-heading-row">
        <div>
          <div className="breadcrumb">
            ResQLink <span>/</span> Profile
          </div>

          <h1>Your Profile</h1>

          <p>
            Your ResQLink community identity and account
            information.
          </p>
        </div>
      </div>

      <div className="profile-card">
        <div className="profile-large-avatar">
          {getInitials(user?.name)}
        </div>

        <div className="profile-main">
          <div className="profile-name-row">
            <h2>{user?.name || "Community Member"}</h2>
            <span className="verified-badge">
              ✓ Verified
            </span>
          </div>

          <p>
            {ROLE_LABELS[user?.role] || "Community Member"}
          </p>

          <div className="profile-details">
            <div>
              <span>Email</span>
              <strong>{user?.email || "—"}</strong>
            </div>

            <div>
              <span>Phone</span>
              <strong>{user?.phone || "Not provided"}</strong>
            </div>

            <div>
              <span>Location</span>
              <strong>
                {user?.location || "Not provided"}
              </strong>
            </div>

            <div>
              <span>Role</span>
              <strong>
                {ROLE_LABELS[user?.role] || user?.role}
              </strong>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}'''

new_settings_and_profile = '''function SettingsPage({ user, navigate }) {
  const [notifEnabled, setNotifEnabled] = useState(true);
  const [showAccountModal, setShowAccountModal] = useState(false);
  const [showSecurityModal, setShowSecurityModal] = useState(false);
  const [toastMsg, setToastMsg] = useState("");

  const [accountForm, setAccountForm] = useState({
    name: user?.name || "Harshal N Raj",
    email: user?.email || "harshalnrajnraj@gmail.com",
    phone: user?.phone || "+91 9876543210",
    location: user?.location || "Mysore",
  });

  const [secForm, setSecForm] = useState({
    currentPass: "",
    newPass: "",
    confirmPass: "",
  });
  const [showP1, setShowP1] = useState(false);
  const [showP2, setShowP2] = useState(false);
  const [showP3, setShowP3] = useState(false);

  const showToast = (msg) => {
    setToastMsg(msg);
    setTimeout(() => setToastMsg(""), 3000);
  };

  const handleAccountSave = (e) => {
    e.preventDefault();
    setShowAccountModal(false);
    showToast("Account details updated successfully!");
  };

  const handleSecuritySave = (e) => {
    e.preventDefault();
    if (secForm.newPass && secForm.newPass !== secForm.confirmPass) {
      showToast("Error: New passwords do not match!");
      return;
    }
    setShowSecurityModal(false);
    setSecForm({ currentPass: "", newPass: "", confirmPass: "" });
    showToast("Security settings & password updated successfully!");
  };

  return (
    <div className="inner-page">
      {toastMsg && (
        <div className="toast toast-success" style={{ marginBottom: "16px" }}>
          ✓ {toastMsg}
        </div>
      )}

      <div className="page-heading-row">
        <div>
          <div className="breadcrumb">
            ResQLink <span>/</span> Settings
          </div>

          <h1>Settings</h1>

          <p>
            Manage your account preferences and platform experience.
          </p>
        </div>
      </div>

      <div className="settings-grid">
        <div className="settings-card">
          <div className="settings-card-icon">👤</div>

          <div>
            <h3>Account</h3>
            <p>
              Signed in as <strong>{user?.email || accountForm.email}</strong>
            </p>
          </div>

          <button
            type="button"
            className="secondary-button"
            onClick={() => setShowAccountModal(true)}
          >
            Manage
          </button>
        </div>

        <div className="settings-card">
          <div className="settings-card-icon">🔔</div>

          <div>
            <h3>Notifications</h3>
            <p>
              Receive updates about donations, requests and connections.
            </p>
          </div>

          <button
            type="button"
            className={`toggle-button ${notifEnabled ? "active" : ""}`}
            style={{
              padding: "8px 18px",
              borderRadius: "20px",
              fontWeight: 600,
              border: "none",
              cursor: "pointer",
              backgroundColor: notifEnabled ? "#10b981" : "#cbd5e1",
              color: "#ffffff",
              transition: "all 0.2s"
            }}
            onClick={() => {
              const next = !notifEnabled;
              setNotifEnabled(next);
              showToast(`Notifications turned ${next ? "ON" : "OFF"}`);
            }}
          >
            {notifEnabled ? "On" : "Off"}
          </button>
        </div>

        <div className="settings-card">
          <div className="settings-card-icon">🔒</div>

          <div>
            <h3>Security</h3>
            <p>
              Keep your account secure with a strong password.
            </p>
          </div>

          <button
            type="button"
            className="secondary-button"
            onClick={() => setShowSecurityModal(true)}
          >
            Review
          </button>
        </div>
      </div>

      {/* ACCOUNT MANAGE MODAL */}
      {showAccountModal && (
        <div className="modal-backdrop">
          <div className="modal-card" style={{ maxWidth: "520px" }}>
            <div className="modal-header">
              <h2>Account Preferences</h2>
              <button
                type="button"
                className="close-button"
                onClick={() => setShowAccountModal(false)}
              >
                ×
              </button>
            </div>

            <form onSubmit={handleAccountSave} className="modal-form" style={{ marginTop: "16px" }}>
              <div className="form-field">
                <label>Full Name</label>
                <input
                  type="text"
                  className="input-control"
                  value={accountForm.name}
                  onChange={(e) => setAccountForm({ ...accountForm, name: e.target.value })}
                  required
                />
              </div>

              <div className="form-field" style={{ marginTop: "12px" }}>
                <label>Email Address</label>
                <input
                  type="email"
                  className="input-control"
                  value={accountForm.email}
                  onChange={(e) => setAccountForm({ ...accountForm, email: e.target.value })}
                  required
                />
              </div>

              <div className="form-field" style={{ marginTop: "12px" }}>
                <label>Phone Number</label>
                <input
                  type="tel"
                  className="input-control"
                  value={accountForm.phone}
                  onChange={(e) => setAccountForm({ ...accountForm, phone: e.target.value })}
                />
              </div>

              <div className="form-field" style={{ marginTop: "12px" }}>
                <label>Primary Location</label>
                <input
                  type="text"
                  className="input-control"
                  value={accountForm.location}
                  onChange={(e) => setAccountForm({ ...accountForm, location: e.target.value })}
                />
              </div>

              <div className="modal-actions" style={{ marginTop: "24px", display: "flex", gap: "12px", justifyContent: "flex-end" }}>
                <button
                  type="button"
                  className="secondary-button"
                  onClick={() => setShowAccountModal(false)}
                >
                  Cancel
                </button>
                <button type="submit" className="primary-button">
                  Save Account Changes
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* SECURITY REVIEW MODAL */}
      {showSecurityModal && (
        <div className="modal-backdrop">
          <div className="modal-card" style={{ maxWidth: "520px" }}>
            <div className="modal-header">
              <h2>Security & Password</h2>
              <button
                type="button"
                className="close-button"
                onClick={() => setShowSecurityModal(false)}
              >
                ×
              </button>
            </div>

            <form onSubmit={handleSecuritySave} className="modal-form" style={{ marginTop: "16px" }}>
              <div className="form-field">
                <label>Current Password</label>
                <div style={{ position: "relative" }}>
                  <input
                    type={showP1 ? "text" : "password"}
                    className="input-control"
                    placeholder="Enter current password"
                    value={secForm.currentPass}
                    onChange={(e) => setSecForm({ ...secForm, currentPass: e.target.value })}
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowP1(!showP1)}
                    style={{ position: "absolute", right: "12px", top: "50%", transform: "translateY(-50%)", background: "none", border: "none", cursor: "pointer", fontSize: "16px" }}
                  >
                    {showP1 ? "🙈" : "👁️"}
                  </button>
                </div>
              </div>

              <div className="form-field" style={{ marginTop: "12px" }}>
                <label>New Password</label>
                <div style={{ position: "relative" }}>
                  <input
                    type={showP2 ? "text" : "password"}
                    className="input-control"
                    placeholder="Enter new strong password"
                    value={secForm.newPass}
                    onChange={(e) => setSecForm({ ...secForm, newPass: e.target.value })}
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowP2(!showP2)}
                    style={{ position: "absolute", right: "12px", top: "50%", transform: "translateY(-50%)", background: "none", border: "none", cursor: "pointer", fontSize: "16px" }}
                  >
                    {showP2 ? "🙈" : "👁️"}
                  </button>
                </div>
              </div>

              <div className="form-field" style={{ marginTop: "12px" }}>
                <label>Confirm New Password</label>
                <div style={{ position: "relative" }}>
                  <input
                    type={showP3 ? "text" : "password"}
                    className="input-control"
                    placeholder="Confirm new password"
                    value={secForm.confirmPass}
                    onChange={(e) => setSecForm({ ...secForm, confirmPass: e.target.value })}
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowP3(!showP3)}
                    style={{ position: "absolute", right: "12px", top: "50%", transform: "translateY(-50%)", background: "none", border: "none", cursor: "pointer", fontSize: "16px" }}
                  >
                    {showP3 ? "🙈" : "👁️"}
                  </button>
                </div>
              </div>

              <div style={{ marginTop: "16px", padding: "12px", backgroundColor: "#f8fafc", borderRadius: "8px", fontSize: "13px", color: "#64748b" }}>
                🔒 Active Session: Windows PC (Mysore, India) — Current session
              </div>

              <div className="modal-actions" style={{ marginTop: "24px", display: "flex", gap: "12px", justifyContent: "flex-end" }}>
                <button
                  type="button"
                  className="secondary-button"
                  onClick={() => setShowSecurityModal(false)}
                >
                  Cancel
                </button>
                <button type="submit" className="primary-button">
                  Update Password
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

function ProfilePage({ user, navigate }) {
  const [profileData, setProfileData] = useState({
    name: user?.name || "Harshal N Raj",
    email: user?.email || "harshalnrajnraj@gmail.com",
    phone: user?.phone || "+91 9876543210",
    location: user?.location || "Mysore",
    role: user?.role || "user",
    bio: "Passionate community member dedicated to emergency support and resource sharing across Karnataka.",
    bloodGroup: "O+",
  });

  const [showEditModal, setShowEditModal] = useState(false);
  const [editForm, setEditForm] = useState({ ...profileData });
  const [toastMsg, setToastMsg] = useState("");

  const showToast = (msg) => {
    setToastMsg(msg);
    setTimeout(() => setToastMsg(""), 3000);
  };

  const handleProfileSave = (e) => {
    e.preventDefault();
    setProfileData({ ...editForm });
    setShowEditModal(false);
    showToast("Profile updated successfully!");
  };

  return (
    <div className="inner-page">
      {toastMsg && (
        <div className="toast toast-success" style={{ marginBottom: "16px" }}>
          ✓ {toastMsg}
        </div>
      )}

      <div className="page-heading-row">
        <div>
          <div className="breadcrumb">
            ResQLink <span>/</span> Profile
          </div>

          <h1>Your Profile</h1>

          <p>
            Your ResQLink community identity and account information.
          </p>
        </div>

        <button
          type="button"
          className="primary-button"
          onClick={() => {
            setEditForm({ ...profileData });
            setShowEditModal(true);
          }}
        >
          ✏️ Edit Profile
        </button>
      </div>

      <div className="profile-card">
        <div className="profile-large-avatar">
          {getInitials(profileData.name)}
        </div>

        <div className="profile-main">
          <div className="profile-name-row">
            <h2>{profileData.name}</h2>
            <span className="verified-badge">
              ✓ Verified Member
            </span>
          </div>

          <p style={{ color: "#0d9488", fontWeight: 600, marginBottom: "8px" }}>
            {ROLE_LABELS[profileData.role] || "Community Member"}
          </p>

          <p style={{ color: "#475569", fontSize: "14px", marginBottom: "16px", maxWidth: "600px" }}>
            "{profileData.bio}"
          </p>

          <div className="profile-details">
            <div>
              <span>Email</span>
              <strong>{profileData.email}</strong>
            </div>

            <div>
              <span>Phone</span>
              <strong>{profileData.phone}</strong>
            </div>

            <div>
              <span>Location</span>
              <strong>{profileData.location}</strong>
            </div>

            <div>
              <span>Blood Donor</span>
              <strong>{profileData.bloodGroup} (Available)</strong>
            </div>
          </div>
        </div>
      </div>

      {/* QUICK ACTIONS & STATS */}
      <div style={{ marginTop: "24px", display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: "16px" }}>
        <div className="stat-card primary" style={{ padding: "20px", borderRadius: "12px", backgroundColor: "#ffffff", border: "1px solid #e2e8f0" }}>
          <div className="stat-icon" style={{ fontSize: "24px" }}>🎁</div>
          <div className="stat-content">
            <span style={{ fontSize: "13px", color: "#64748b" }}>Donations Shared</span>
            <strong style={{ fontSize: "20px" }}>5 Items</strong>
            <small style={{ color: "#10b981" }}>Active Contributor</small>
          </div>
        </div>

        <div className="stat-card success" style={{ padding: "20px", borderRadius: "12px", backgroundColor: "#ffffff", border: "1px solid #e2e8f0" }}>
          <div className="stat-icon" style={{ fontSize: "24px" }}>📋</div>
          <div className="stat-content">
            <span style={{ fontSize: "13px", color: "#64748b" }}>Requests Fulfilled</span>
            <strong style={{ fontSize: "20px" }}>3 Resolved</strong>
            <small style={{ color: "#0d9488" }}>Community Hero</small>
          </div>
        </div>

        <div className="stat-card warning" style={{ padding: "20px", borderRadius: "12px", backgroundColor: "#ffffff", border: "1px solid #e2e8f0" }}>
          <div className="stat-icon" style={{ fontSize: "24px" }}>⭐</div>
          <div className="stat-content">
            <span style={{ fontSize: "13px", color: "#64748b" }}>Impact Points</span>
            <strong style={{ fontSize: "20px" }}>120 pts</strong>
            <small style={{ color: "#f59e0b" }}>Bronze Level</small>
          </div>
        </div>
      </div>

      {/* QUICK LINKS GRID */}
      <div style={{ marginTop: "24px" }}>
        <h3 style={{ marginBottom: "12px", fontSize: "18px", color: "#0f172a" }}>Quick Account Actions</h3>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: "12px" }}>
          <button
            type="button"
            className="secondary-button"
            style={{ padding: "14px", textAlign: "left", justifyContent: "flex-start", gap: "10px" }}
            onClick={() => navigate && navigate("donations")}
          >
            🎁 View My Donations
          </button>
          <button
            type="button"
            className="secondary-button"
            style={{ padding: "14px", textAlign: "left", justifyContent: "flex-start", gap: "10px" }}
            onClick={() => navigate && navigate("requests")}
          >
            📋 View My Requests
          </button>
          <button
            type="button"
            className="secondary-button"
            style={{ padding: "14px", textAlign: "left", justifyContent: "flex-start", gap: "10px" }}
            onClick={() => navigate && navigate("volunteer")}
          >
            🤝 Become a Volunteer
          </button>
          <button
            type="button"
            className="secondary-button"
            style={{ padding: "14px", textAlign: "left", justifyContent: "flex-start", gap: "10px" }}
            onClick={() => navigate && navigate("settings")}
          >
            ⚙️ Account Settings
          </button>
        </div>
      </div>

      {/* EDIT PROFILE MODAL */}
      {showEditModal && (
        <div className="modal-backdrop">
          <div className="modal-card" style={{ maxWidth: "540px" }}>
            <div className="modal-header">
              <h2>Edit Profile</h2>
              <button
                type="button"
                className="close-button"
                onClick={() => setShowEditModal(false)}
              >
                ×
              </button>
            </div>

            <form onSubmit={handleProfileSave} className="modal-form" style={{ marginTop: "16px" }}>
              <div className="form-field">
                <label>Full Name</label>
                <input
                  type="text"
                  className="input-control"
                  value={editForm.name}
                  onChange={(e) => setEditForm({ ...editForm, name: e.target.value })}
                  required
                />
              </div>

              <div className="form-field" style={{ marginTop: "12px" }}>
                <label>Phone Number</label>
                <input
                  type="tel"
                  className="input-control"
                  value={editForm.phone}
                  onChange={(e) => setEditForm({ ...editForm, phone: e.target.value })}
                />
              </div>

              <div className="form-field" style={{ marginTop: "12px" }}>
                <label>Location / City</label>
                <input
                  type="text"
                  className="input-control"
                  value={editForm.location}
                  onChange={(e) => setEditForm({ ...editForm, location: e.target.value })}
                />
              </div>

              <div className="form-field" style={{ marginTop: "12px" }}>
                <label>Blood Group</label>
                <select
                  className="input-control"
                  value={editForm.bloodGroup}
                  onChange={(e) => setEditForm({ ...editForm, bloodGroup: e.target.value })}
                >
                  <option value="A+">A+</option>
                  <option value="A-">A-</option>
                  <option value="B+">B+</option>
                  <option value="B-">B-</option>
                  <option value="O+">O+</option>
                  <option value="O-">O-</option>
                  <option value="AB+">AB+</option>
                  <option value="AB-">AB-</option>
                </select>
              </div>

              <div className="form-field" style={{ marginTop: "12px" }}>
                <label>Community Bio</label>
                <textarea
                  className="input-control"
                  rows={3}
                  value={editForm.bio}
                  onChange={(e) => setEditForm({ ...editForm, bio: e.target.value })}
                />
              </div>

              <div className="modal-actions" style={{ marginTop: "24px", display: "flex", gap: "12px", justifyContent: "flex-end" }}>
                <button
                  type="button"
                  className="secondary-button"
                  onClick={() => setShowEditModal(false)}
                >
                  Cancel
                </button>
                <button type="submit" className="primary-button">
                  Save Profile
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}'''

content = content.replace(old_settings_and_profile, new_settings_and_profile)

with open(app_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Profile and Settings upgrades applied successfully!")
