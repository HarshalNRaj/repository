import { useEffect, useMemo, useState } from "react";
import "./admin.css";

const API = import.meta.env.VITE_API_URL || "http://127.0.0.1:5000";

function apiRequest(endpoint, options = {}) {
  const token = localStorage.getItem("token");

  const headers = {
    ...(options.headers || {}),
  };

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  return fetch(`${API}${endpoint}`, {
    ...options,
    headers,
  }).then(async (response) => {
    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
      throw new Error(data.message || data.error || "Request failed");
    }

    return data;
  });
}

function StatusBadge({ status }) {
  const value = String(status || "Unknown").toLowerCase();

  let className = "admin-status neutral";

  if (
    ["approved", "verified", "active", "completed", "available"].includes(value)
  ) {
    className = "admin-status success";
  } else if (
    ["pending", "requested", "processing", "in_progress"].includes(value)
  ) {
    className = "admin-status warning";
  } else if (
    ["rejected", "blocked", "inactive", "failed", "cancelled"].includes(value)
  ) {
    className = "admin-status danger";
  }

  return <span className={className}>{status || "Unknown"}</span>;
}

function StatCard({ icon, label, value, description }) {
  return (
    <div className="admin-stat-card">
      <div className="admin-stat-icon">{icon}</div>

      <div className="admin-stat-content">
        <span className="admin-stat-label">{label}</span>
        <strong>{value}</strong>
        {description && <small>{description}</small>}
      </div>
    </div>
  );
}

function DashboardPage({ users, pending, loginHistory, refreshData }) {
  const stats = useMemo(() => {
    const totalUsers = users.length;

    const verifiedUsers = users.filter(
      (user) => user.is_verified === true
    ).length;

    const volunteers = users.filter(
      (user) => user.role === "volunteer"
    ).length;

    const organizations = users.filter(
      (user) =>
        user.role === "ngo" ||
        user.role === "blood_bank" ||
        user.role === "organization"
    ).length;

    return {
      totalUsers,
      verifiedUsers,
      volunteers,
      organizations,
      pending: pending.length,
      logins: loginHistory.length,
    };
  }, [users, pending, loginHistory]);

  return (
    <div className="admin-page">
      <div className="admin-page-heading">
        <div>
          <span className="admin-eyebrow">ADMIN CONTROL CENTER</span>
          <h1>Platform Overview</h1>
          <p>
            Monitor users, organization verification and platform activity.
          </p>
        </div>

        <button className="admin-refresh-btn" onClick={refreshData}>
          ↻ Refresh
        </button>
      </div>

      <div className="admin-stats-grid">
        <StatCard
          icon="👥"
          label="Total Users"
          value={stats.totalUsers}
          description="Registered accounts"
        />

        <StatCard
          icon="✓"
          label="Verified Users"
          value={stats.verifiedUsers}
          description="Trusted accounts"
        />

        <StatCard
          icon="🤝"
          label="Volunteers"
          value={stats.volunteers}
          description="Active volunteers"
        />

        <StatCard
          icon="🏢"
          label="Organizations"
          value={stats.organizations}
          description="NGOs and blood banks"
        />

        <StatCard
          icon="⏳"
          label="Pending Reviews"
          value={stats.pending}
          description="Need admin action"
        />

        <StatCard
          icon="🔐"
          label="Login Records"
          value={stats.logins}
          description="Recent activity"
        />
      </div>

      <div className="admin-dashboard-grid">
        <section className="admin-panel">
          <div className="admin-panel-header">
            <div>
              <h2>Pending Verifications</h2>
              <p>Organizations waiting for approval.</p>
            </div>

            <span className="admin-count-badge">{pending.length}</span>
          </div>

          {pending.length === 0 ? (
            <div className="admin-empty">
              <div className="admin-empty-icon">✓</div>
              <h3>All caught up</h3>
              <p>No organizations are waiting for verification.</p>
            </div>
          ) : (
            <div className="admin-pending-list">
              {pending.slice(0, 5).map((item) => (
                <div
                  className="admin-pending-item"
                  key={item.id || item.user_id}
                >
                  <div className="admin-org-avatar">
                    {(item.organization_name ||
                      item.name ||
                      item.email ||
                      "O")
                      .charAt(0)
                      .toUpperCase()}
                  </div>

                  <div className="admin-pending-info">
                    <strong>
                      {item.organization_name ||
                        item.name ||
                        "Organization"}
                    </strong>

                    <span>
                      {item.email || "No email available"}
                    </span>
                  </div>

                  <StatusBadge status="Pending" />
                </div>
              ))}
            </div>
          )}
        </section>

        <section className="admin-panel">
          <div className="admin-panel-header">
            <div>
              <h2>Admin Responsibilities</h2>
              <p>Trust and safety controls.</p>
            </div>
          </div>

          <div className="admin-responsibility-list">
            <div className="admin-responsibility">
              <span>✓</span>
              <div>
                <strong>Verify organizations</strong>
                <p>Review NGO and blood bank registrations.</p>
              </div>
            </div>

            <div className="admin-responsibility">
              <span>🛡</span>
              <div>
                <strong>Maintain trust</strong>
                <p>Keep the platform limited to verified entities.</p>
              </div>
            </div>

            <div className="admin-responsibility">
              <span>🔎</span>
              <div>
                <strong>Monitor activity</strong>
                <p>Review account and login activity.</p>
              </div>
            </div>

            <div className="admin-responsibility">
              <span>🚫</span>
              <div>
                <strong>Moderate access</strong>
                <p>Handle inappropriate or suspicious accounts.</p>
              </div>
            </div>
          </div>
        </section>
      </div>

      <section className="admin-panel admin-activity-panel">
        <div className="admin-panel-header">
          <div>
            <h2>Recent Login Activity</h2>
            <p>Latest authentication records.</p>
          </div>
        </div>

        {loginHistory.length === 0 ? (
          <div className="admin-empty compact">
            <p>No login activity available.</p>
          </div>
        ) : (
          <div className="admin-table-wrapper">
            <table className="admin-table">
              <thead>
                <tr>
                  <th>User</th>
                  <th>Email</th>
                  <th>Role</th>
                  <th>Time</th>
                  <th>Status</th>
                </tr>
              </thead>

              <tbody>
                {loginHistory.slice(0, 8).map((entry, index) => (
                  <tr key={entry.id || index}>
                    <td>
                      <strong>
                        {entry.name || entry.username || "User"}
                      </strong>
                    </td>

                    <td>{entry.email || "—"}</td>

                    <td>
                      <span className="admin-role-text">
                        {entry.role || "user"}
                      </span>
                    </td>

                    <td>
                      {entry.created_at
                        ? new Date(entry.created_at).toLocaleString()
                        : "—"}
                    </td>

                    <td>
                      <StatusBadge
                        status={
                          entry.status ||
                          (entry.success === false ? "Failed" : "Success")
                        }
                      />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </div>
  );
}

function UsersPage({ users, refreshData }) {
  const [search, setSearch] = useState("");
  const [roleFilter, setRoleFilter] = useState("all");

  const filteredUsers = useMemo(() => {
    return users.filter((user) => {
      const searchText = search.toLowerCase().trim();

      const matchesSearch =
        !searchText ||
        String(user.name || "")
          .toLowerCase()
          .includes(searchText) ||
        String(user.email || "")
          .toLowerCase()
          .includes(searchText) ||
        String(user.phone || "")
          .toLowerCase()
          .includes(searchText);

      const matchesRole =
        roleFilter === "all" || user.role === roleFilter;

      return matchesSearch && matchesRole;
    });
  }, [users, search, roleFilter]);

  return (
    <div className="admin-page">
      <div className="admin-page-heading">
        <div>
          <span className="admin-eyebrow">USER MANAGEMENT</span>
          <h1>Users</h1>
          <p>View and monitor registered ResQLink accounts.</p>
        </div>

        <button className="admin-refresh-btn" onClick={refreshData}>
          ↻ Refresh
        </button>
      </div>

      <section className="admin-panel">
        <div className="admin-filter-bar">
          <div className="admin-search-box">
            <span>⌕</span>
            <input
              type="text"
              placeholder="Search by name, email or phone..."
              value={search}
              onChange={(event) => setSearch(event.target.value)}
            />
          </div>

          <select
            value={roleFilter}
            onChange={(event) => setRoleFilter(event.target.value)}
          >
            <option value="all">All Roles</option>
            <option value="user">Users</option>
            <option value="volunteer">Volunteers</option>
            <option value="ngo">NGOs</option>
            <option value="blood_bank">Blood Banks</option>
            <option value="admin">Admins</option>
          </select>
        </div>

        {filteredUsers.length === 0 ? (
          <div className="admin-empty">
            <div className="admin-empty-icon">⌕</div>
            <h3>No users found</h3>
            <p>Try changing the search or role filter.</p>
          </div>
        ) : (
          <div className="admin-table-wrapper">
            <table className="admin-table">
              <thead>
                <tr>
                  <th>User</th>
                  <th>Email</th>
                  <th>Phone</th>
                  <th>Role</th>
                  <th>Verification</th>
                  <th>Joined</th>
                </tr>
              </thead>

              <tbody>
                {filteredUsers.map((user) => (
                  <tr key={user.id}>
                    <td>
                      <div className="admin-user-cell">
                        <div className="admin-user-avatar">
                          {(user.name || user.email || "U")
                            .charAt(0)
                            .toUpperCase()}
                        </div>

                        <div>
                          <strong>{user.name || "Unnamed User"}</strong>
                          <small>ID #{user.id}</small>
                        </div>
                      </div>
                    </td>

                    <td>{user.email || "—"}</td>

                    <td>{user.phone || "—"}</td>

                    <td>
                      <span className="admin-role-pill">
                        {String(user.role || "user").replace("_", " ")}
                      </span>
                    </td>

                    <td>
                      <StatusBadge
                        status={user.is_verified ? "Verified" : "Pending"}
                      />
                    </td>

                    <td>
                      {user.created_at
                        ? new Date(user.created_at).toLocaleDateString()
                        : "—"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </div>
  );
}

function VerificationPage({ pending, refreshData }) {
  const [processingId, setProcessingId] = useState(null);
  const [message, setMessage] = useState("");

  const handleDecision = async (id, action) => {
    if (!id) return;

    const organization =
      pending.find((item) => item.id === id) ||
      pending.find((item) => item.user_id === id);

    const name =
      organization?.organization_name ||
      organization?.name ||
      organization?.email ||
      "this organization";

    const actionText = action === "approve" ? "approve" : "reject";

    if (!window.confirm(`Are you sure you want to ${actionText} ${name}?`)) {
      return;
    }

    setProcessingId(id);
    setMessage("");

    try {
      await apiRequest(
        `/api/accounts/pending-verifications/${id}/${action}`,
        {
          method: "POST",
        }
      );

      setMessage(
        action === "approve"
          ? "Organization approved successfully."
          : "Organization rejected successfully."
      );

      await refreshData();
    } catch (error) {
      setMessage(error.message);
    } finally {
      setProcessingId(null);
    }
  };

  return (
    <div className="admin-page">
      <div className="admin-page-heading">
        <div>
          <span className="admin-eyebrow">TRUST & VERIFICATION</span>
          <h1>Pending Verifications</h1>
          <p>
            Review NGO and blood bank registrations before granting access.
          </p>
        </div>

        <button className="admin-refresh-btn" onClick={refreshData}>
          ↻ Refresh
        </button>
      </div>

      {message && <div className="admin-message">{message}</div>}

      <section className="admin-panel">
        {pending.length === 0 ? (
          <div className="admin-empty large">
            <div className="admin-empty-icon">✓</div>
            <h3>No pending organizations</h3>
            <p>
              New NGO and blood bank registrations will appear here for review.
            </p>
          </div>
        ) : (
          <div className="admin-verification-list">
            {pending.map((item) => {
              const id = item.id || item.user_id;

              return (
                <div className="admin-verification-card" key={id}>
                  <div className="admin-verification-main">
                    <div className="admin-org-avatar large">
                      {(
                        item.organization_name ||
                        item.name ||
                        item.email ||
                        "O"
                      )
                        .charAt(0)
                        .toUpperCase()}
                    </div>

                    <div className="admin-verification-info">
                      <div className="admin-verification-title">
                        <h3>
                          {item.organization_name ||
                            item.name ||
                            "Organization"}
                        </h3>

                        <StatusBadge status="Pending" />
                      </div>

                      <p>{item.email || "No email provided"}</p>

                      <div className="admin-detail-grid">
                        <div>
                          <span>Role</span>
                          <strong>
                            {String(item.role || "organization").replace(
                              "_",
                              " "
                            )}
                          </strong>
                        </div>

                        <div>
                          <span>Phone</span>
                          <strong>{item.phone || "Not provided"}</strong>
                        </div>

                        <div>
                          <span>Location</span>
                          <strong>
                            {item.location ||
                              item.address ||
                              "Not provided"}
                          </strong>
                        </div>

                        <div>
                          <span>Organization ID</span>
                          <strong>#{id}</strong>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="admin-verification-actions">
                    <button
                      className="admin-action-btn approve"
                      disabled={processingId === id}
                      onClick={() => handleDecision(id, "approve")}
                    >
                      {processingId === id ? "Processing..." : "✓ Approve"}
                    </button>

                    <button
                      className="admin-action-btn reject"
                      disabled={processingId === id}
                      onClick={() => handleDecision(id, "reject")}
                    >
                      ✕ Reject
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </section>
    </div>
  );
}

function LoginHistoryPage({ loginHistory, refreshData }) {
  const [search, setSearch] = useState("");

  const filteredHistory = useMemo(() => {
    const searchText = search.toLowerCase().trim();

    if (!searchText) return loginHistory;

    return loginHistory.filter((entry) => {
      return (
        String(entry.name || "")
          .toLowerCase()
          .includes(searchText) ||
        String(entry.email || "")
          .toLowerCase()
          .includes(searchText) ||
        String(entry.role || "")
          .toLowerCase()
          .includes(searchText)
      );
    });
  }, [loginHistory, search]);

  return (
    <div className="admin-page">
      <div className="admin-page-heading">
        <div>
          <span className="admin-eyebrow">SECURITY MONITORING</span>
          <h1>Login History</h1>
          <p>Review authentication activity across the platform.</p>
        </div>

        <button className="admin-refresh-btn" onClick={refreshData}>
          ↻ Refresh
        </button>
      </div>

      <section className="admin-panel">
        <div className="admin-filter-bar">
          <div className="admin-search-box">
            <span>⌕</span>

            <input
              type="text"
              placeholder="Search login records..."
              value={search}
              onChange={(event) => setSearch(event.target.value)}
            />
          </div>
        </div>

        {filteredHistory.length === 0 ? (
          <div className="admin-empty">
            <div className="admin-empty-icon">🔐</div>
            <h3>No login records</h3>
            <p>There are no matching authentication records.</p>
          </div>
        ) : (
          <div className="admin-table-wrapper">
            <table className="admin-table">
              <thead>
                <tr>
                  <th>User</th>
                  <th>Email</th>
                  <th>Role</th>
                  <th>IP Address</th>
                  <th>Time</th>
                  <th>Status</th>
                </tr>
              </thead>

              <tbody>
                {filteredHistory.map((entry, index) => (
                  <tr key={entry.id || index}>
                    <td>
                      <strong>{entry.name || "User"}</strong>
                    </td>

                    <td>{entry.email || "—"}</td>

                    <td>
                      <span className="admin-role-pill">
                        {entry.role || "user"}
                      </span>
                    </td>

                    <td>{entry.ip_address || entry.ip || "—"}</td>

                    <td>
                      {entry.created_at
                        ? new Date(entry.created_at).toLocaleString()
                        : "—"}
                    </td>

                    <td>
                      <StatusBadge
                        status={
                          entry.status ||
                          (entry.success === false ? "Failed" : "Success")
                        }
                      />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </div>
  );
}

function ProfilePage({ adminUser }) {
  return (
    <div className="admin-page">
      <div className="admin-page-heading">
        <div>
          <span className="admin-eyebrow">ACCOUNT</span>
          <h1>Admin Profile</h1>
          <p>Administrator account information.</p>
        </div>
      </div>

      <section className="admin-profile-card">
        <div className="admin-profile-header">
          <div className="admin-profile-avatar">
            {(adminUser?.name || adminUser?.email || "A")
              .charAt(0)
              .toUpperCase()}
          </div>

          <div>
            <span className="admin-profile-label">Administrator</span>

            <h2>{adminUser?.name || "ResQLink Administrator"}</h2>

            <p>{adminUser?.email || "admin@resqlink.com"}</p>
          </div>

          <StatusBadge status="Verified" />
        </div>

        <div className="admin-profile-grid">
          <div className="admin-profile-field">
            <span>Full Name</span>
            <strong>
              {adminUser?.name || "ResQLink Administrator"}
            </strong>
          </div>

          <div className="admin-profile-field">
            <span>Email Address</span>
            <strong>
              {adminUser?.email || "admin@resqlink.com"}
            </strong>
          </div>

          <div className="admin-profile-field">
            <span>Role</span>
            <strong>Administrator</strong>
          </div>

          <div className="admin-profile-field">
            <span>Account Status</span>
            <strong>Active</strong>
          </div>
        </div>
      </section>

      <section className="admin-panel admin-security-note">
        <div className="admin-security-icon">🛡</div>

        <div>
          <h3>Administrator access</h3>
          <p>
            Admin access is reserved for platform management. Public users
            cannot register directly as administrators.
          </p>
        </div>
      </section>
    </div>
  );
}

export default function Admin() {
  const [activePage, setActivePage] = useState("dashboard");

  const [users, setUsers] = useState([]);
  const [pending, setPending] = useState([]);
  const [loginHistory, setLoginHistory] = useState([]);

  const [adminUser, setAdminUser] = useState(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const user = JSON.parse(localStorage.getItem("user") || "null");

  const loadData = async () => {
    setLoading(true);
    setError("");

    try {
      const [usersResponse, pendingResponse, historyResponse] =
        await Promise.all([
          apiRequest("/api/admin/users"),
          apiRequest("/api/accounts/pending-verifications"),
          apiRequest("/api/admin/login-history"),
        ]);

      setUsers(
        Array.isArray(usersResponse)
          ? usersResponse
          : usersResponse.users || []
      );

      setPending(
        Array.isArray(pendingResponse)
          ? pendingResponse
          : pendingResponse.pending || pendingResponse.verifications || []
      );

      setLoginHistory(
        Array.isArray(historyResponse)
          ? historyResponse
          : historyResponse.login_history ||
              historyResponse.history ||
              []
      );
    } catch (err) {
      console.error("Admin data loading error:", err);
      setError(err.message || "Unable to load admin data.");
    } finally {
      setLoading(false);
    }
  };

  const loadAdminProfile = async () => {
    try {
      const response = await apiRequest("/api/auth/me");
      setAdminUser(response.user || response);
    } catch {
      setAdminUser(user);
    }
  };

  useEffect(() => {
    loadData();
    loadAdminProfile();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    window.location.href = "/";
  };

  const pageTitle = {
    dashboard: "Dashboard",
    users: "Users",
    verification: "Verification",
    history: "Login History",
    profile: "Profile",
  };

  return (
    <div className="admin-shell">
      <aside className="admin-sidebar">
        <div className="admin-brand">
          <div className="admin-brand-mark">R</div>

          <div>
            <strong>ResQLink</strong>
            <span>Admin Portal</span>
          </div>
        </div>

        <div className="admin-nav-section">
          <span className="admin-nav-label">OVERVIEW</span>

          <button
            className={`admin-nav-item ${
              activePage === "dashboard" ? "active" : ""
            }`}
            onClick={() => setActivePage("dashboard")}
          >
            <span>⌂</span>
            Dashboard
          </button>
        </div>

        <div className="admin-nav-section">
          <span className="admin-nav-label">MANAGEMENT</span>

          <button
            className={`admin-nav-item ${
              activePage === "users" ? "active" : ""
            }`}
            onClick={() => setActivePage("users")}
          >
            <span>👥</span>
            Users
          </button>

          <button
            className={`admin-nav-item ${
              activePage === "verification" ? "active" : ""
            }`}
            onClick={() => setActivePage("verification")}
          >
            <span>✓</span>
            Verification

            {pending.length > 0 && (
              <span className="admin-nav-count">{pending.length}</span>
            )}
          </button>
        </div>

        <div className="admin-nav-section">
          <span className="admin-nav-label">SECURITY</span>

          <button
            className={`admin-nav-item ${
              activePage === "history" ? "active" : ""
            }`}
            onClick={() => setActivePage("history")}
          >
            <span>🔐</span>
            Login History
          </button>
        </div>

        <div className="admin-sidebar-bottom">
          <button
            className={`admin-nav-item ${
              activePage === "profile" ? "active" : ""
            }`}
            onClick={() => setActivePage("profile")}
          >
            <span>⚙</span>
            Profile
          </button>

          <button className="admin-logout-btn" onClick={handleLogout}>
            <span>↪</span>
            Logout
          </button>

          <div className="admin-sidebar-user">
            <div className="admin-mini-avatar">
              {(user?.name || user?.email || "A")
                .charAt(0)
                .toUpperCase()}
            </div>

            <div>
              <strong>{user?.name || "Administrator"}</strong>
              <span>{user?.email || "Admin account"}</span>
            </div>
          </div>
        </div>
      </aside>

      <main className="admin-main">
        <header className="admin-topbar">
          <div className="admin-breadcrumb">
            <span>ResQLink</span>
            <b>/</b>
            <strong>{pageTitle[activePage]}</strong>
          </div>

          <div className="admin-topbar-actions">
            <div className="admin-live-indicator">
              <span></span>
              System Online
            </div>

            <div className="admin-top-avatar">
              {(user?.name || user?.email || "A")
                .charAt(0)
                .toUpperCase()}
            </div>
          </div>
        </header>

        {loading && activePage !== "profile" ? (
          <div className="admin-loading">
            <div className="admin-loader"></div>
            <h3>Loading admin dashboard...</h3>
            <p>Fetching the latest platform information.</p>
          </div>
        ) : error && activePage !== "profile" ? (
          <div className="admin-error-page">
            <div className="admin-error-icon">!</div>
            <h2>Unable to load admin data</h2>
            <p>{error}</p>

            <button className="admin-primary-btn" onClick={loadData}>
              Try Again
            </button>
          </div>
        ) : (
          <>
            {activePage === "dashboard" && (
              <DashboardPage
                users={users}
                pending={pending}
                loginHistory={loginHistory}
                refreshData={loadData}
              />
            )}

            {activePage === "users" && (
              <UsersPage users={users} refreshData={loadData} />
            )}

            {activePage === "verification" && (
              <VerificationPage
                pending={pending}
                refreshData={loadData}
              />
            )}

            {activePage === "history" && (
              <LoginHistoryPage
                loginHistory={loginHistory}
                refreshData={loadData}
              />
            )}

            {activePage === "profile" && (
              <ProfilePage adminUser={adminUser || user} />
            )}
          </>
        )}
      </main>
    </div>
  );
}