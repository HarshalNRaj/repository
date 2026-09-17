import { useEffect, useState } from "react";
import "./ngo.css";

const API = import.meta.env.VITE_API_URL || "http://127.0.0.1:5000";

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
  const value = String(status || "pending").toLowerCase();

  let className = "ngo-status ngo-status-pending";

  if (
    value.includes("complete") ||
    value.includes("approved") ||
    value.includes("accepted") ||
    value.includes("active")
  ) {
    className = "ngo-status ngo-status-success";
  } else if (
    value.includes("reject") ||
    value.includes("cancel") ||
    value.includes("closed")
  ) {
    className = "ngo-status ngo-status-danger";
  } else if (
    value.includes("urgent") ||
    value.includes("high")
  ) {
    className = "ngo-status ngo-status-urgent";
  } else if (
    value.includes("requested") ||
    value.includes("progress")
  ) {
    className = "ngo-status ngo-status-info";
  }

  return <span className={className}>{status || "Pending"}</span>;
}

function StatCard({ icon, label, value, note }) {
  return (
    <div className="ngo-stat-card">
      <div className="ngo-stat-top">
        <span className="ngo-stat-label">{label}</span>
        <div className="ngo-stat-icon">{icon}</div>
      </div>

      <div className="ngo-stat-value">{value}</div>

      {note && <div className="ngo-stat-note">{note}</div>}
    </div>
  );
}

function DashboardPage({
  dashboard,
  requirements,
  matches,
  requests,
  onNavigate,
}) {
  const stats = dashboard?.stats || dashboard || {};

  const requirementCount =
    stats.requirements ??
    stats.total_requirements ??
    requirements.length;

  const requestCount =
    stats.requests ??
    stats.total_requests ??
    requests.length;

  const matchCount =
    stats.matches ??
    stats.total_matches ??
    matches.length;

  const completedCount =
    stats.completed ??
    stats.completed_requests ??
    requests.filter((item) =>
      String(item.status || "").toLowerCase().includes("complete")
    ).length;

  return (
    <div>
      <div className="ngo-welcome">
        <div>
          <h1>Good to see you again.</h1>
          <p>
            Manage your organization, post requirements, discover matching
            donations, and coordinate support from one place.
          </p>
        </div>

        <button
          className="ngo-btn ngo-btn-primary"
          onClick={() => onNavigate("requirements")}
        >
          + Post Requirement
        </button>
      </div>

      <div className="ngo-stats-grid">
        <StatCard
          icon="📋"
          label="Requirements"
          value={requirementCount}
          note="Active requirements"
        />

        <StatCard
          icon="🎁"
          label="Matched Donations"
          value={matchCount}
          note="Potential matches"
        />

        <StatCard
          icon="🤝"
          label="Requests"
          value={requestCount}
          note="Donation requests"
        />

        <StatCard
          icon="✓"
          label="Completed"
          value={completedCount}
          note="Successfully received"
        />
      </div>

      <div className="ngo-dashboard-grid">
        <section className="ngo-panel">
          <div className="ngo-section-header">
            <div>
              <h2>Recent Requirements</h2>
              <p>Latest needs posted by your organization.</p>
            </div>

            <button
              className="ngo-link-btn"
              onClick={() => onNavigate("requirements")}
            >
              View all
            </button>
          </div>

          {requirements.length === 0 ? (
            <div className="ngo-empty-small">
              <div className="ngo-empty-icon">📋</div>
              <strong>No requirements yet</strong>
              <span>
                Post a requirement when your organization needs support.
              </span>
            </div>
          ) : (
            <div className="ngo-list">
              {requirements.slice(0, 4).map((item) => (
                <div className="ngo-list-item" key={item.id}>
                  <div className="ngo-list-main">
                    <div className="ngo-list-title">
                      {item.item_name || item.name || "Requirement"}
                    </div>

                    <div className="ngo-list-meta">
                      {item.category || "General"} · Quantity:{" "}
                      {item.quantity_required ?? item.quantity ?? 0}
                    </div>
                  </div>

                  <StatusBadge status={item.priority || item.status} />
                </div>
              ))}
            </div>
          )}
        </section>

        <section className="ngo-panel">
          <div className="ngo-section-header">
            <div>
              <h2>Donation Matches</h2>
              <p>Donations that may fulfill your requirements.</p>
            </div>

            <button
              className="ngo-link-btn"
              onClick={() => onNavigate("matches")}
            >
              Explore
            </button>
          </div>

          {matches.length === 0 ? (
            <div className="ngo-empty-small">
              <div className="ngo-empty-icon">🎁</div>
              <strong>No matches found</strong>
              <span>
                Matching donations will appear here when available.
              </span>
            </div>
          ) : (
            <div className="ngo-list">
              {matches.slice(0, 4).map((item) => (
                <div className="ngo-list-item" key={item.id}>
                  <div className="ngo-list-main">
                    <div className="ngo-list-title">
                      {item.item_name || item.name || "Donation"}
                    </div>

                    <div className="ngo-list-meta">
                      {item.category || "General"} · Qty:{" "}
                      {item.quantity ?? item.quantity_available ?? 0}
                    </div>
                  </div>

                  <button
                    className="ngo-small-btn"
                    onClick={() => onNavigate("matches")}
                  >
                    View
                  </button>
                </div>
              ))}
            </div>
          )}
        </section>
      </div>

      <section className="ngo-panel ngo-panel-spaced">
        <div className="ngo-section-header">
          <div>
            <h2>Recent Requests</h2>
            <p>Track donation requests made by your organization.</p>
          </div>

          <button
            className="ngo-link-btn"
            onClick={() => onNavigate("requests")}
          >
            View all
          </button>
        </div>

        {requests.length === 0 ? (
          <div className="ngo-empty-small">
            <div className="ngo-empty-icon">🤝</div>
            <strong>No requests yet</strong>
            <span>
              Requests created from matching donations will appear here.
            </span>
          </div>
        ) : (
          <div className="ngo-table-wrapper">
            <table className="ngo-table">
              <thead>
                <tr>
                  <th>Donation</th>
                  <th>Category</th>
                  <th>Quantity</th>
                  <th>Status</th>
                </tr>
              </thead>

              <tbody>
                {requests.slice(0, 5).map((item) => (
                  <tr key={item.id}>
                    <td>
                      {item.item_name ||
                        item.donation_name ||
                        item.donation?.item_name ||
                        "Donation"}
                    </td>

                    <td>
                      {item.category ||
                        item.donation?.category ||
                        "General"}
                    </td>

                    <td>
                      {item.quantity ??
                        item.donation?.quantity ??
                        "—"}
                    </td>

                    <td>
                      <StatusBadge status={item.status} />
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

function RequirementsPage({
  requirements,
  form,
  setForm,
  onCreate,
  onRefresh,
}) {
  return (
    <div>
      <div className="ngo-page-heading">
        <div>
          <h1>Requirements</h1>
          <p>
            Tell donors what your organization currently needs.
          </p>
        </div>

        <button className="ngo-btn ngo-btn-outline" onClick={onRefresh}>
          ↻ Refresh
        </button>
      </div>

      <div className="ngo-content-grid">
        <section className="ngo-form-card">
          <div className="ngo-card-heading">
            <h2>Post a Requirement</h2>
            <p>
              Create a clear request so matching donations can be discovered.
            </p>
          </div>

          <form onSubmit={onCreate}>
            <div className="ngo-form-grid">
              <div className="ngo-form-group">
                <label>Category</label>

                <select
                  value={form.category}
                  onChange={(e) =>
                    setForm({
                      ...form,
                      category: e.target.value,
                    })
                  }
                  required
                >
                  <option value="">Select category</option>
                  <option value="Clothes">Clothes</option>
                  <option value="Books">Books</option>
                  <option value="Furniture">Furniture</option>
                  <option value="Food">Food</option>
                  <option value="Electronics">Electronics</option>
                  <option value="School Supplies">
                    School Supplies
                  </option>
                  <option value="Blankets">Blankets</option>
                  <option value="Other">Other</option>
                </select>
              </div>

              <div className="ngo-form-group">
                <label>Item Name</label>

                <input
                  type="text"
                  placeholder="e.g. Blankets"
                  value={form.item_name}
                  onChange={(e) =>
                    setForm({
                      ...form,
                      item_name: e.target.value,
                    })
                  }
                  required
                />
              </div>

              <div className="ngo-form-group">
                <label>Quantity Required</label>

                <input
                  type="number"
                  min="1"
                  placeholder="e.g. 100"
                  value={form.quantity_required}
                  onChange={(e) =>
                    setForm({
                      ...form,
                      quantity_required: e.target.value,
                    })
                  }
                  required
                />
              </div>

              <div className="ngo-form-group">
                <label>Priority</label>

                <select
                  value={form.priority}
                  onChange={(e) =>
                    setForm({
                      ...form,
                      priority: e.target.value,
                    })
                  }
                >
                  <option value="normal">Normal</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                  <option value="urgent">Urgent</option>
                </select>
              </div>

              <div className="ngo-form-group ngo-full">
                <label>Location</label>

                <input
                  type="text"
                  placeholder="Where is the support required?"
                  value={form.location}
                  onChange={(e) =>
                    setForm({
                      ...form,
                      location: e.target.value,
                    })
                  }
                />
              </div>

              <div className="ngo-form-group ngo-full">
                <label>Description</label>

                <textarea
                  placeholder="Explain why this item is needed..."
                  value={form.description}
                  onChange={(e) =>
                    setForm({
                      ...form,
                      description: e.target.value,
                    })
                  }
                />
              </div>
            </div>

            <div className="ngo-form-actions">
              <button
                type="submit"
                className="ngo-btn ngo-btn-primary"
              >
                Post Requirement
              </button>
            </div>
          </form>
        </section>

        <section className="ngo-panel">
          <div className="ngo-section-header">
            <div>
              <h2>Your Requirements</h2>
              <p>Requirements currently registered.</p>
            </div>
          </div>

          {requirements.length === 0 ? (
            <div className="ngo-empty-small">
              <div className="ngo-empty-icon">📋</div>
              <strong>No requirements</strong>
              <span>Create your first requirement using the form.</span>
            </div>
          ) : (
            <div className="ngo-requirement-list">
              {requirements.map((item) => (
                <div className="ngo-requirement-card" key={item.id}>
                  <div className="ngo-requirement-top">
                    <div>
                      <span className="ngo-category">
                        {item.category || "General"}
                      </span>

                      <h3>
                        {item.item_name || "Requirement"}
                      </h3>
                    </div>

                    <StatusBadge
                      status={item.priority || item.status}
                    />
                  </div>

                  <div className="ngo-requirement-info">
                    <span>
                      <b>Quantity:</b>{" "}
                      {item.quantity_required ?? item.quantity ?? 0}
                    </span>

                    {item.location && (
                      <span>
                        <b>Location:</b> {item.location}
                      </span>
                    )}
                  </div>

                  {item.description && (
                    <p className="ngo-requirement-description">
                      {item.description}
                    </p>
                  )}
                </div>
              ))}
            </div>
          )}
        </section>
      </div>
    </div>
  );
}

function MatchesPage({ matches, onRequest, loading }) {
  return (
    <div>
      <div className="ngo-page-heading">
        <div>
          <h1>Donation Matches</h1>
          <p>
            Discover available donations that match your organization's
            requirements.
          </p>
        </div>
      </div>

      {loading ? (
        <div className="ngo-loading">
          <div className="ngo-spinner"></div>
          Loading matches...
        </div>
      ) : matches.length === 0 ? (
        <div className="ngo-empty">
          <div className="ngo-empty-icon">🎁</div>
          <h3>No matching donations yet</h3>
          <p>
            New donations will appear here when they match your
            requirements.
          </p>
        </div>
      ) : (
        <div className="ngo-match-grid">
          {matches.map((item) => (
            <div className="ngo-match-card" key={item.id}>
              <div className="ngo-match-header">
                <div>
                  <span className="ngo-category">
                    {item.category || "General"}
                  </span>

                  <h3>
                    {item.item_name ||
                      item.name ||
                      "Available Donation"}
                  </h3>
                </div>

                <span className="ngo-match-icon">🎁</span>
              </div>

              <div className="ngo-match-details">
                <div>
                  <span>Quantity</span>
                  <strong>
                    {item.quantity ??
                      item.quantity_available ??
                      "—"}
                  </strong>
                </div>

                <div>
                  <span>Condition</span>
                  <strong>{item.condition || "—"}</strong>
                </div>

                <div>
                  <span>Location</span>
                  <strong>{item.location || "—"}</strong>
                </div>

                <div>
                  <span>Status</span>
                  <strong>{item.status || "Available"}</strong>
                </div>
              </div>

              {item.description && (
                <p className="ngo-match-description">
                  {item.description}
                </p>
              )}

              <div className="ngo-match-footer">
                <span className="ngo-match-note">
                  Potential requirement match
                </span>

                <button
                  className="ngo-btn ngo-btn-primary"
                  onClick={() => onRequest(item.id)}
                >
                  Request Donation
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function RequestsPage({ requests, loading }) {
  return (
    <div>
      <div className="ngo-page-heading">
        <div>
          <h1>Donation Requests</h1>
          <p>
            Track requests sent to donors and their current status.
          </p>
        </div>
      </div>

      <div className="ngo-panel">
        {loading ? (
          <div className="ngo-loading">
            <div className="ngo-spinner"></div>
            Loading requests...
          </div>
        ) : requests.length === 0 ? (
          <div className="ngo-empty">
            <div className="ngo-empty-icon">🤝</div>
            <h3>No requests yet</h3>
            <p>
              Requests you create for available donations will appear here.
            </p>
          </div>
        ) : (
          <div className="ngo-table-wrapper">
            <table className="ngo-table">
              <thead>
                <tr>
                  <th>Donation</th>
                  <th>Category</th>
                  <th>Quantity</th>
                  <th>Created</th>
                  <th>Status</th>
                </tr>
              </thead>

              <tbody>
                {requests.map((item) => (
                  <tr key={item.id}>
                    <td>
                      {item.item_name ||
                        item.donation_name ||
                        item.donation?.item_name ||
                        "Donation"}
                    </td>

                    <td>
                      {item.category ||
                        item.donation?.category ||
                        "General"}
                    </td>

                    <td>
                      {item.quantity ??
                        item.donation?.quantity ??
                        "—"}
                    </td>

                    <td>
                      {item.created_at
                        ? new Date(
                            item.created_at
                          ).toLocaleDateString()
                        : "—"}
                    </td>

                    <td>
                      <StatusBadge status={item.status} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
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
    "Organization";

  return (
    <div>
      <div className="ngo-page-heading">
        <div>
          <h1>Organization Profile</h1>
          <p>
            Organization information and verification status.
          </p>
        </div>
      </div>

      <div className="ngo-profile-grid">
        <section className="ngo-profile-card">
          <div className="ngo-profile-heading">
            <div className="ngo-profile-avatar">
              {organizationName.charAt(0).toUpperCase()}
            </div>

            <div>
              <h2>{organizationName}</h2>
              <span>NGO / Ashram</span>
            </div>
          </div>

          <div className="ngo-verification-box">
            <div className="ngo-verification-icon">✓</div>

            <div>
              <strong>
                {organization.verification_status === "approved"
                  ? "Verified Organization"
                  : "Verification Pending"}
              </strong>

              <p>
                {organization.verification_status === "approved"
                  ? "Your organization has been approved by the administrator."
                  : "Your organization will receive full access after admin verification."}
              </p>
            </div>
          </div>
        </section>

        <section className="ngo-profile-card">
          <h2 className="ngo-card-title">Organization Details</h2>

          <div className="ngo-profile-details">
            <div className="ngo-profile-row">
              <span>Organization name</span>
              <strong>{organizationName}</strong>
            </div>

            <div className="ngo-profile-row">
              <span>Organization type</span>
              <strong>
                {organization.organization_type || "NGO"}
              </strong>
            </div>

            <div className="ngo-profile-row">
              <span>Email</span>
              <strong>
                {organization.email ||
                  user?.email ||
                  "Not provided"}
              </strong>
            </div>

            <div className="ngo-profile-row">
              <span>Phone</span>
              <strong>
                {organization.phone ||
                  user?.phone ||
                  "Not provided"}
              </strong>
            </div>

            <div className="ngo-profile-row">
              <span>Address</span>
              <strong>
                {organization.address ||
                  user?.location ||
                  "Not provided"}
              </strong>
            </div>

            <div className="ngo-profile-row">
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

export default function NGO() {
  const [user, setUser] = useState(getStoredUser());

  const [activePage, setActivePage] = useState("dashboard");

  const [dashboard, setDashboard] = useState(null);
  const [requirements, setRequirements] = useState([]);
  const [matches, setMatches] = useState([]);
  const [requests, setRequests] = useState([]);
  const [profile, setProfile] = useState(null);

  const [loading, setLoading] = useState(true);
  const [pageLoading, setPageLoading] = useState(false);

  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState("success");

  const [form, setForm] = useState({
    category: "",
    item_name: "",
    quantity_required: "",
    priority: "normal",
    description: "",
    location: "",
  });

  const showMessage = (text, type = "success") => {
    setMessage(text);
    setMessageType(type);

    window.setTimeout(() => {
      setMessage("");
    }, 3500);
  };

  const loadDashboard = async () => {
    try {
      const data = await apiRequest("/api/ngo/dashboard");
      setDashboard(data);
    } catch (error) {
      console.error("Dashboard error:", error);
    }
  };

  const loadRequirements = async () => {
    try {
      const data = await apiRequest("/api/ngo/requirements");

      const list =
        data.requirements ||
        data.data ||
        (Array.isArray(data) ? data : []);

      setRequirements(list);
    } catch (error) {
      console.error("Requirements error:", error);
    }
  };

  const loadMatches = async () => {
    try {
      setPageLoading(true);

      const data = await apiRequest("/api/ngo/matches");

      const list =
        data.matches ||
        data.data ||
        (Array.isArray(data) ? data : []);

      setMatches(list);
    } catch (error) {
      console.error("Matches error:", error);
      showMessage(
        error.message || "Unable to load donation matches.",
        "error"
      );
    } finally {
      setPageLoading(false);
    }
  };

  const loadRequests = async () => {
    try {
      setPageLoading(true);

      const data = await apiRequest("/api/ngo/requests");

      const list =
        data.requests ||
        data.data ||
        (Array.isArray(data) ? data : []);

      setRequests(list);
    } catch (error) {
      console.error("Requests error:", error);
      showMessage(
        error.message || "Unable to load requests.",
        "error"
      );
    } finally {
      setPageLoading(false);
    }
  };

  const loadProfile = async () => {
    try {
      const data = await apiRequest("/api/ngo/profile");
      setProfile(data);
    } catch (error) {
      console.error("Profile error:", error);
    }
  };

  const loadAll = async () => {
    setLoading(true);

    await Promise.all([
      loadDashboard(),
      loadRequirements(),
      loadMatches(),
      loadRequests(),
      loadProfile(),
    ]);

    setLoading(false);
  };

  useEffect(() => {
    loadAll();
  }, []);

  const createRequirement = async (event) => {
    event.preventDefault();

    try {
      const payload = {
        category: form.category,
        item_name: form.item_name,
        quantity_required: Number(form.quantity_required),
        priority: form.priority,
        description: form.description,
        location: form.location,
      };

      await apiRequest("/api/ngo/requirements", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      showMessage("Requirement posted successfully.");

      setForm({
        category: "",
        item_name: "",
        quantity_required: "",
        priority: "normal",
        description: "",
        location: "",
      });

      await Promise.all([
        loadRequirements(),
        loadDashboard(),
        loadMatches(),
      ]);
    } catch (error) {
      showMessage(
        error.message || "Unable to create requirement.",
        "error"
      );
    }
  };

  const requestDonation = async (donationId) => {
    try {
      await apiRequest(`/api/ngo/donations/${donationId}/request`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });

      showMessage("Donation request sent successfully.");

      await Promise.all([
        loadRequests(),
        loadDashboard(),
        loadMatches(),
      ]);
    } catch (error) {
      showMessage(
        error.message || "Unable to request this donation.",
        "error"
      );
    }
  };

  const acceptRequest = async (requestId) => {
    try {
      await apiRequest(`/api/ngo/requests/${requestId}/accept`, {
        method: "POST",
      });

      showMessage("Request accepted.");

      await Promise.all([
        loadRequests(),
        loadDashboard(),
      ]);
    } catch (error) {
      showMessage(
        error.message || "Unable to accept request.",
        "error"
      );
    }
  };

  const rejectRequest = async (requestId) => {
    try {
      await apiRequest(`/api/ngo/requests/${requestId}/reject`, {
        method: "POST",
      });

      showMessage("Request rejected.");

      await Promise.all([
        loadRequests(),
        loadDashboard(),
      ]);
    } catch (error) {
      showMessage(
        error.message || "Unable to reject request.",
        "error"
      );
    }
  };

  const navigate = async (page) => {
    setActivePage(page);

    if (page === "matches") {
      await loadMatches();
    }

    if (page === "requests") {
      await loadRequests();
    }

    if (page === "requirements") {
      await loadRequirements();
    }

    if (page === "profile") {
      await loadProfile();
    }

    if (page === "dashboard") {
      await loadDashboard();
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
      .toUpperCase() || "NG";

  if (loading) {
    return (
      <div className="ngo-loading-screen">
        <div className="ngo-loading-logo">R</div>
        <div className="ngo-spinner"></div>
        <p>Loading your organization dashboard...</p>
      </div>
    );
  }

  return (
    <div className="ngo-app">
      <aside className="ngo-sidebar">
        <div className="ngo-brand">
          <div className="ngo-brand-mark">R</div>

          <div className="ngo-brand-text">
            <div className="ngo-brand-title">ResQLink</div>
            <div className="ngo-brand-subtitle">
              Organization Portal
            </div>
          </div>
        </div>

        <nav className="ngo-nav">
          <div className="ngo-nav-label">Workspace</div>

          <button
            className={`ngo-nav-item ${
              activePage === "dashboard" ? "active" : ""
            }`}
            onClick={() => navigate("dashboard")}
          >
            <span className="ngo-nav-icon">⌂</span>
            Dashboard
          </button>

          <button
            className={`ngo-nav-item ${
              activePage === "requirements" ? "active" : ""
            }`}
            onClick={() => navigate("requirements")}
          >
            <span className="ngo-nav-icon">▣</span>
            Requirements
          </button>

          <button
            className={`ngo-nav-item ${
              activePage === "matches" ? "active" : ""
            }`}
            onClick={() => navigate("matches")}
          >
            <span className="ngo-nav-icon">◇</span>
            Donation Matches
          </button>

          <button
            className={`ngo-nav-item ${
              activePage === "requests" ? "active" : ""
            }`}
            onClick={() => navigate("requests")}
          >
            <span className="ngo-nav-icon">↗</span>
            Requests
          </button>

          <div className="ngo-nav-label ngo-nav-label-space">
            Organization
          </div>

          <button
            className={`ngo-nav-item ${
              activePage === "profile" ? "active" : ""
            }`}
            onClick={() => navigate("profile")}
          >
            <span className="ngo-nav-icon">○</span>
            Organization Profile
          </button>
        </nav>

        <div className="ngo-sidebar-bottom">
          <div className="ngo-sidebar-user">
            <div className="ngo-sidebar-avatar">{initials}</div>

            <div className="ngo-sidebar-user-info">
              <strong>{user?.name || "Organization"}</strong>
              <span>NGO / Ashram</span>
            </div>
          </div>

          <button className="ngo-logout" onClick={logout}>
            <span>↪</span>
            Logout
          </button>
        </div>
      </aside>

      <main className="ngo-main">
        <header className="ngo-topbar">
          <div>
            <div className="ngo-topbar-title">
              {activePage === "dashboard" && "Organization Dashboard"}
              {activePage === "requirements" && "Requirements"}
              {activePage === "matches" && "Donation Matches"}
              {activePage === "requests" && "Donation Requests"}
              {activePage === "profile" && "Organization Profile"}
            </div>

            <div className="ngo-topbar-subtitle">
              ResQLink support coordination
            </div>
          </div>

          <div className="ngo-topbar-right">
            <button
              className="ngo-refresh"
              onClick={loadAll}
              title="Refresh dashboard"
            >
              ↻
            </button>

            <div className="ngo-user">
              <div className="ngo-user-avatar">{initials}</div>

              <div className="ngo-user-info">
                <strong>{user?.name || "Organization"}</strong>
                <span>Verified organization</span>
              </div>
            </div>
          </div>
        </header>

        <div className="ngo-content">
          {message && (
            <div className={`ngo-alert ${messageType}`}>
              <span>
                {messageType === "error" ? "!" : "✓"}
              </span>

              <div>{message}</div>

              <button onClick={() => setMessage("")}>×</button>
            </div>
          )}

          {activePage === "dashboard" && (
            <DashboardPage
              dashboard={dashboard}
              requirements={requirements}
              matches={matches}
              requests={requests}
              onNavigate={navigate}
            />
          )}

          {activePage === "requirements" && (
            <RequirementsPage
              requirements={requirements}
              form={form}
              setForm={setForm}
              onCreate={createRequirement}
              onRefresh={loadRequirements}
            />
          )}

          {activePage === "matches" && (
            <MatchesPage
              matches={matches}
              onRequest={requestDonation}
              loading={pageLoading}
            />
          )}

          {activePage === "requests" && (
            <RequestsPage
              requests={requests}
              loading={pageLoading}
              onAccept={acceptRequest}
              onReject={rejectRequest}
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