import { useEffect, useState } from "react";
import "./blood.css";

const API = "http://127.0.0.1:5000";

function getStoredUser() {
  try {
    return JSON.parse(localStorage.getItem("user") || "null");
  } catch {
    return null;
  }
}

function getToken() {
  return localStorage.getItem("token") || "";
}

async function apiRequest(url, options = {}) {
  const token = getToken();

  const headers = {
    ...(options.headers || {}),
  };

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`${API}${url}`, {
    ...options,
    headers,
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.message || data.error || "Request failed");
  }

  return data;
}

function StatusBadge({ status }) {
  const value = String(status || "active").toLowerCase();

  let className = "blood-status blood-status-info";

  if (
    value.includes("available") ||
    value.includes("active") ||
    value.includes("approved") ||
    value.includes("completed") ||
    value.includes("fulfilled")
  ) {
    className = "blood-status blood-status-success";
  } else if (
    value.includes("urgent") ||
    value.includes("critical")
  ) {
    className = "blood-status blood-status-danger";
  } else if (
    value.includes("pending") ||
    value.includes("requested")
  ) {
    className = "blood-status blood-status-warning";
  } else if (
    value.includes("closed") ||
    value.includes("rejected")
  ) {
    className = "blood-status blood-status-muted";
  }

  return (
    <span className={className}>
      {status || "Active"}
    </span>
  );
}

function StatCard({ icon, label, value, note }) {
  return (
    <div className="blood-stat-card">
      <div className="blood-stat-top">
        <span className="blood-stat-label">{label}</span>

        <div className="blood-stat-icon">
          {icon}
        </div>
      </div>

      <div className="blood-stat-value">
        {value}
      </div>

      {note && (
        <div className="blood-stat-note">
          {note}
        </div>
      )}
    </div>
  );
}

function DashboardPage({
  dashboard,
  inventory,
  requests,
  onNavigate,
}) {
  const stats = dashboard?.stats || dashboard || {};

  const inventoryCount =
    stats.inventory ??
    stats.total_inventory ??
    inventory.length;

  const requestCount =
    stats.requests ??
    stats.total_requests ??
    requests.length;

  const urgentCount =
    stats.urgent_requests ??
    stats.urgent ??
    requests.filter((item) => {
      const value = String(
        item.priority || item.urgency || ""
      ).toLowerCase();

      return value === "urgent" || value === "critical";
    }).length;

  const totalUnits =
    stats.total_units ??
    inventory.reduce(
      (sum, item) =>
        sum +
        Number(
          item.units ??
            item.quantity ??
            item.available_units ??
            0
        ),
      0
    );

  return (
    <div>
      <div className="blood-welcome">
        <div>
          <h1>Blood Bank Dashboard</h1>

          <p>
            Manage blood inventory, monitor requests, and
            coordinate eligible donor support through ResQLink.
          </p>
        </div>

        <button
          className="blood-btn blood-btn-primary"
          onClick={() => onNavigate("inventory")}
        >
          + Update Inventory
        </button>
      </div>

      <div className="blood-info-banner">
        <div className="blood-info-icon">✓</div>

        <div>
          <strong>Coordination platform</strong>

          <p>
            ResQLink helps connect blood banks, requests, and
            eligible donors. Medical eligibility and compatibility
            decisions remain with qualified healthcare professionals.
          </p>
        </div>
      </div>

      <div className="blood-stats-grid">
        <StatCard
          icon="🩸"
          label="Blood Groups"
          value={inventoryCount}
          note="Inventory entries"
        />

        <StatCard
          icon="📦"
          label="Total Units"
          value={totalUnits}
          note="Current recorded stock"
        />

        <StatCard
          icon="📋"
          label="Requests"
          value={requestCount}
          note="Blood requests"
        />

        <StatCard
          icon="🚨"
          label="Urgent"
          value={urgentCount}
          note="Priority requests"
        />
      </div>

      <div className="blood-dashboard-grid">
        <section className="blood-panel">
          <div className="blood-section-header">
            <div>
              <h2>Current Inventory</h2>
              <p>Latest blood stock information.</p>
            </div>

            <button
              className="blood-link-btn"
              onClick={() => onNavigate("inventory")}
            >
              View all
            </button>
          </div>

          {inventory.length === 0 ? (
            <div className="blood-empty-small">
              <div className="blood-empty-icon">
                🩸
              </div>

              <strong>No inventory recorded</strong>

              <span>
                Add blood group quantities to start tracking
                inventory.
              </span>
            </div>
          ) : (
            <div className="blood-inventory-mini-grid">
              {inventory.slice(0, 8).map((item) => (
                <div
                  className="blood-mini-card"
                  key={item.id}
                >
                  <div className="blood-mini-group">
                    {item.blood_group ||
                      item.group ||
                      "—"}
                  </div>

                  <div className="blood-mini-units">
                    {item.units ??
                      item.quantity ??
                      item.available_units ??
                      0}
                  </div>

                  <span>units</span>
                </div>
              ))}
            </div>
          )}
        </section>

        <section className="blood-panel">
          <div className="blood-section-header">
            <div>
              <h2>Recent Requests</h2>
              <p>Latest blood requirements.</p>
            </div>

            <button
              className="blood-link-btn"
              onClick={() => onNavigate("requests")}
            >
              View all
            </button>
          </div>

          {requests.length === 0 ? (
            <div className="blood-empty-small">
              <div className="blood-empty-icon">
                📋
              </div>

              <strong>No requests</strong>

              <span>
                New blood requests will appear here.
              </span>
            </div>
          ) : (
            <div className="blood-list">
              {requests.slice(0, 5).map((item) => (
                <div
                  className="blood-list-item"
                  key={item.id}
                >
                  <div className="blood-list-main">
                    <div className="blood-list-title">
                      {item.blood_group ||
                        item.group ||
                        "Blood request"}
                    </div>

                    <div className="blood-list-meta">
                      {item.units ??
                        item.quantity ??
                        0}{" "}
                      units
                      {item.location
                        ? ` · ${item.location}`
                        : ""}
                    </div>
                  </div>

                  <StatusBadge
                    status={
                      item.priority ||
                      item.urgency ||
                      item.status
                    }
                  />
                </div>
              ))}
            </div>
          )}
        </section>
      </div>
    </div>
  );
}

function InventoryPage({
  inventory,
  form,
  setForm,
  onSubmit,
  onRefresh,
}) {
  return (
    <div>
      <div className="blood-page-heading">
        <div>
          <h1>Blood Inventory</h1>

          <p>
            Maintain an up-to-date record of available blood
            units.
          </p>
        </div>

        <button
          className="blood-btn blood-btn-outline"
          onClick={onRefresh}
        >
          ↻ Refresh
        </button>
      </div>

      <div className="blood-content-grid">
        <section className="blood-form-card">
          <div className="blood-card-heading">
            <h2>Update Inventory</h2>

            <p>
              Add or update the recorded quantity for a blood
              group.
            </p>
          </div>

          <form onSubmit={onSubmit}>
            <div className="blood-form-grid">
              <div className="blood-form-group">
                <label>Blood Group</label>

                <select
                  value={form.blood_group}
                  onChange={(e) =>
                    setForm({
                      ...form,
                      blood_group: e.target.value,
                    })
                  }
                  required
                >
                  <option value="">
                    Select blood group
                  </option>

                  <option value="A+">A+</option>
                  <option value="A-">A-</option>
                  <option value="B+">B+</option>
                  <option value="B-">B-</option>
                  <option value="AB+">AB+</option>
                  <option value="AB-">AB-</option>
                  <option value="O+">O+</option>
                  <option value="O-">O-</option>
                </select>
              </div>

              <div className="blood-form-group">
                <label>Units</label>

                <input
                  type="number"
                  min="0"
                  placeholder="e.g. 25"
                  value={form.units}
                  onChange={(e) =>
                    setForm({
                      ...form,
                      units: e.target.value,
                    })
                  }
                  required
                />
              </div>

              <div className="blood-form-group blood-full">
                <label>Status</label>

                <select
                  value={form.status}
                  onChange={(e) =>
                    setForm({
                      ...form,
                      status: e.target.value,
                    })
                  }
                >
                  <option value="available">
                    Available
                  </option>

                  <option value="low">
                    Low Stock
                  </option>

                  <option value="unavailable">
                    Unavailable
                  </option>
                </select>
              </div>
            </div>

            <div className="blood-form-actions">
              <button
                type="submit"
                className="blood-btn blood-btn-primary"
              >
                Save Inventory
              </button>
            </div>
          </form>
        </section>

        <section className="blood-panel">
          <div className="blood-section-header">
            <div>
              <h2>Current Stock</h2>
              <p>Recorded units by blood group.</p>
            </div>
          </div>

          {inventory.length === 0 ? (
            <div className="blood-empty-small">
              <div className="blood-empty-icon">
                🩸
              </div>

              <strong>No inventory yet</strong>

              <span>
                Add your first blood group using the form.
              </span>
            </div>
          ) : (
            <div className="blood-stock-list">
              {inventory.map((item) => (
                <div
                  className="blood-stock-row"
                  key={item.id}
                >
                  <div className="blood-group-badge">
                    {item.blood_group ||
                      item.group ||
                      "—"}
                  </div>

                  <div className="blood-stock-info">
                    <strong>
                      {item.units ??
                        item.quantity ??
                        item.available_units ??
                        0}{" "}
                      units
                    </strong>

                    <span>
                      {item.updated_at
                        ? `Updated ${new Date(
                            item.updated_at
                          ).toLocaleDateString()}`
                        : "Current inventory"}
                    </span>
                  </div>

                  <StatusBadge
                    status={item.status || "available"}
                  />
                </div>
              ))}
            </div>
          )}
        </section>
      </div>
    </div>
  );
}

function RequestsPage({
  requests,
  loading,
  onClose,
}) {
  return (
    <div>
      <div className="blood-page-heading">
        <div>
          <h1>Blood Requests</h1>

          <p>
            Monitor requests and coordinate appropriate
            support.
          </p>
        </div>
      </div>

      <div className="blood-panel">
        {loading ? (
          <div className="blood-loading">
            <div className="blood-spinner"></div>
            Loading requests...
          </div>
        ) : requests.length === 0 ? (
          <div className="blood-empty">
            <div className="blood-empty-icon">
              📋
            </div>

            <h3>No blood requests</h3>

            <p>
              Requests received by the blood bank will appear
              here.
            </p>
          </div>
        ) : (
          <div className="blood-table-wrapper">
            <table className="blood-table">
              <thead>
                <tr>
                  <th>Blood Group</th>
                  <th>Units</th>
                  <th>Location</th>
                  <th>Priority</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>

              <tbody>
                {requests.map((item) => (
                  <tr key={item.id}>
                    <td>
                      <strong>
                        {item.blood_group ||
                          item.group ||
                          "—"}
                      </strong>
                    </td>

                    <td>
                      {item.units ??
                        item.quantity ??
                        "—"}
                    </td>

                    <td>
                      {item.location || "—"}
                    </td>

                    <td>
                      <StatusBadge
                        status={
                          item.priority ||
                          item.urgency ||
                          "Normal"
                        }
                      />
                    </td>

                    <td>
                      <StatusBadge
                        status={item.status || "Active"}
                      />
                    </td>

                    <td>
                      {!String(
                        item.status || ""
                      )
                        .toLowerCase()
                        .includes("closed") && (
                        <button
                          className="blood-small-btn"
                          onClick={() =>
                            onClose(item.id)
                          }
                        >
                          Close
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <div className="blood-safety-note">
        <strong>Important:</strong> Blood group compatibility,
        donor eligibility, clinical suitability, and transfusion
        decisions must be confirmed by qualified medical
        professionals.
      </div>
    </div>
  );
}

function ProfilePage({ profile, user }) {
  const organization =
    profile?.organization ||
    profile?.profile ||
    profile ||
    {};

  const organizationName =
    organization.organization_name ||
    user?.organization_name ||
    user?.name ||
    "Blood Bank";

  return (
    <div>
      <div className="blood-page-heading">
        <div>
          <h1>Blood Bank Profile</h1>

          <p>
            Manage your organization information and
            verification details.
          </p>
        </div>
      </div>

      <div className="blood-profile-grid">
        <section className="blood-profile-card">
          <div className="blood-profile-heading">
            <div className="blood-profile-avatar">
              🩸
            </div>

            <div>
              <h2>{organizationName}</h2>

              <span>Blood Bank</span>
            </div>
          </div>

          <div className="blood-verification-box">
            <div className="blood-verification-icon">
              ✓
            </div>

            <div>
              <strong>
                {organization.verification_status ===
                "approved"
                  ? "Verified Blood Bank"
                  : "Verification Pending"}
              </strong>

              <p>
                {organization.verification_status ===
                "approved"
                  ? "Your organization has been approved by the administrator."
                  : "Your organization is awaiting administrator verification."}
              </p>
            </div>
          </div>
        </section>

        <section className="blood-profile-card">
          <h2 className="blood-card-title">
            Organization Details
          </h2>

          <div className="blood-profile-details">
            <div className="blood-profile-row">
              <span>Organization name</span>

              <strong>{organizationName}</strong>
            </div>

            <div className="blood-profile-row">
              <span>Organization type</span>

              <strong>
                {organization.organization_type ||
                  "Blood Bank"}
              </strong>
            </div>

            <div className="blood-profile-row">
              <span>Email</span>

              <strong>
                {organization.email ||
                  user?.email ||
                  "Not provided"}
              </strong>
            </div>

            <div className="blood-profile-row">
              <span>Phone</span>

              <strong>
                {organization.phone ||
                  user?.phone ||
                  "Not provided"}
              </strong>
            </div>

            <div className="blood-profile-row">
              <span>Address</span>

              <strong>
                {organization.address ||
                  user?.location ||
                  "Not provided"}
              </strong>
            </div>

            <div className="blood-profile-row">
              <span>Verification</span>

              <StatusBadge
                status={
                  organization.verification_status ||
                  "pending"
                }
              />
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}

export default function BloodBank() {
  const [user] = useState(getStoredUser());

  const [activePage, setActivePage] =
    useState("dashboard");

  const [dashboard, setDashboard] = useState(null);
  const [inventory, setInventory] = useState([]);
  const [requests, setRequests] = useState([]);
  const [profile, setProfile] = useState(null);

  const [loading, setLoading] = useState(true);
  const [pageLoading, setPageLoading] =
    useState(false);

  const [message, setMessage] = useState("");
  const [messageType, setMessageType] =
    useState("success");

  const [form, setForm] = useState({
    blood_group: "",
    units: "",
    status: "available",
  });

  const showMessage = (
    text,
    type = "success"
  ) => {
    setMessage(text);
    setMessageType(type);

    window.setTimeout(() => {
      setMessage("");
    }, 3500);
  };

  const loadDashboard = async () => {
    try {
      const data = await apiRequest(
        "/api/blood/dashboard"
      );

      setDashboard(data);
    } catch (error) {
      console.error(
        "Blood dashboard error:",
        error
      );
    }
  };

  const loadInventory = async () => {
    try {
      const data = await apiRequest(
        "/api/blood/inventory"
      );

      const list =
        data.inventory ||
        data.data ||
        (Array.isArray(data) ? data : []);

      setInventory(list);
    } catch (error) {
      console.error(
        "Blood inventory error:",
        error
      );
    }
  };

  const loadRequests = async () => {
    try {
      setPageLoading(true);

      const data = await apiRequest(
        "/api/blood/requests"
      );

      const list =
        data.requests ||
        data.data ||
        (Array.isArray(data) ? data : []);

      setRequests(list);
    } catch (error) {
      console.error(
        "Blood requests error:",
        error
      );

      showMessage(
        error.message ||
          "Unable to load blood requests.",
        "error"
      );
    } finally {
      setPageLoading(false);
    }
  };

  const loadProfile = async () => {
    try {
      const data = await apiRequest(
        "/api/blood/profile"
      );

      setProfile(data);
    } catch (error) {
      console.error(
        "Blood profile error:",
        error
      );
    }
  };

  const loadAll = async () => {
    setLoading(true);

    await Promise.all([
      loadDashboard(),
      loadInventory(),
      loadRequests(),
      loadProfile(),
    ]);

    setLoading(false);
  };

  useEffect(() => {
    loadAll();
  }, []);

  const updateInventory = async (event) => {
    event.preventDefault();

    try {
      const payload = {
        blood_group: form.blood_group,
        units: Number(form.units),
        quantity: Number(form.units),
        status: form.status,
      };

      await apiRequest("/api/blood/inventory", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      showMessage(
        "Blood inventory updated successfully."
      );

      setForm({
        blood_group: "",
        units: "",
        status: "available",
      });

      await Promise.all([
        loadInventory(),
        loadDashboard(),
      ]);
    } catch (error) {
      showMessage(
        error.message ||
          "Unable to update inventory.",
        "error"
      );
    }
  };

  const closeRequest = async (requestId) => {
    try {
      await apiRequest(
        `/api/blood/requests/${requestId}/close`,
        {
          method: "POST",
        }
      );

      showMessage("Blood request closed.");

      await Promise.all([
        loadRequests(),
        loadDashboard(),
      ]);
    } catch (error) {
      showMessage(
        error.message ||
          "Unable to close request.",
        "error"
      );
    }
  };

  const navigate = async (page) => {
    setActivePage(page);

    if (page === "dashboard") {
      await loadDashboard();
    }

    if (page === "inventory") {
      await loadInventory();
    }

    if (page === "requests") {
      await loadRequests();
    }

    if (page === "profile") {
      await loadProfile();
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");

    window.location.href = "/";
  };

  const initials =
    user?.name
      ?.split(" ")
      .map((part) => part[0])
      .join("")
      .slice(0, 2)
      .toUpperCase() || "BB";

  if (loading) {
    return (
      <div className="blood-loading-screen">
        <div className="blood-loading-logo">
          🩸
        </div>

        <div className="blood-spinner"></div>

        <p>
          Loading blood bank dashboard...
        </p>
      </div>
    );
  }

  return (
    <div className="blood-app">
      <aside className="blood-sidebar">
        <div className="blood-brand">
          <div className="blood-brand-mark">
            R
          </div>

          <div className="blood-brand-text">
            <div className="blood-brand-title">
              ResQLink
            </div>

            <div className="blood-brand-subtitle">
              Blood Bank Portal
            </div>
          </div>
        </div>

        <nav className="blood-nav">
          <div className="blood-nav-label">
            Workspace
          </div>

          <button
            className={`blood-nav-item ${
              activePage === "dashboard"
                ? "active"
                : ""
            }`}
            onClick={() =>
              navigate("dashboard")
            }
          >
            <span className="blood-nav-icon">
              ⌂
            </span>
            Dashboard
          </button>

          <button
            className={`blood-nav-item ${
              activePage === "inventory"
                ? "active"
                : ""
            }`}
            onClick={() =>
              navigate("inventory")
            }
          >
            <span className="blood-nav-icon">
              🩸
            </span>
            Blood Inventory
          </button>

          <button
            className={`blood-nav-item ${
              activePage === "requests"
                ? "active"
                : ""
            }`}
            onClick={() =>
              navigate("requests")
            }
          >
            <span className="blood-nav-icon">
              ▣
            </span>
            Blood Requests
          </button>

          <div className="blood-nav-label blood-nav-space">
            Organization
          </div>

          <button
            className={`blood-nav-item ${
              activePage === "profile"
                ? "active"
                : ""
            }`}
            onClick={() =>
              navigate("profile")
            }
          >
            <span className="blood-nav-icon">
              ○
            </span>
            Blood Bank Profile
          </button>
        </nav>

        <div className="blood-sidebar-bottom">
          <div className="blood-sidebar-user">
            <div className="blood-sidebar-avatar">
              {initials}
            </div>

            <div className="blood-sidebar-user-info">
              <strong>
                {user?.name || "Blood Bank"}
              </strong>

              <span>Blood Bank</span>
            </div>
          </div>

          <button
            className="blood-logout"
            onClick={logout}
          >
            <span>↪</span>
            Logout
          </button>
        </div>
      </aside>

      <main className="blood-main">
        <header className="blood-topbar">
          <div>
            <div className="blood-topbar-title">
              {activePage === "dashboard" &&
                "Blood Bank Dashboard"}

              {activePage === "inventory" &&
                "Blood Inventory"}

              {activePage === "requests" &&
                "Blood Requests"}

              {activePage === "profile" &&
                "Blood Bank Profile"}
            </div>

            <div className="blood-topbar-subtitle">
              ResQLink emergency coordination
            </div>
          </div>

          <div className="blood-topbar-right">
            <button
              className="blood-refresh"
              onClick={loadAll}
              title="Refresh dashboard"
            >
              ↻
            </button>

            <div className="blood-user">
              <div className="blood-user-avatar">
                {initials}
              </div>

              <div className="blood-user-info">
                <strong>
                  {user?.name || "Blood Bank"}
                </strong>

                <span>
                  Organization account
                </span>
              </div>
            </div>
          </div>
        </header>

        <div className="blood-content">
          {message && (
            <div
              className={`blood-alert ${
                messageType === "error"
                  ? "error"
                  : ""
              }`}
            >
              <span>
                {messageType === "error"
                  ? "!"
                  : "✓"}
              </span>

              <div>{message}</div>

              <button
                onClick={() => setMessage("")}
              >
                ×
              </button>
            </div>
          )}

          {activePage === "dashboard" && (
            <DashboardPage
              dashboard={dashboard}
              inventory={inventory}
              requests={requests}
              onNavigate={navigate}
            />
          )}

          {activePage === "inventory" && (
            <InventoryPage
              inventory={inventory}
              form={form}
              setForm={setForm}
              onSubmit={updateInventory}
              onRefresh={loadInventory}
            />
          )}

          {activePage === "requests" && (
            <RequestsPage
              requests={requests}
              loading={pageLoading}
              onClose={closeRequest}
            />
          )}

          {activePage === "profile" && (
            <ProfilePage
              profile={profile}
              user={user}
            />
          )}
        </div>
      </main>
    </div>
  );
}