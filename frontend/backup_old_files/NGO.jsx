import { useEffect, useState } from "react";
import "./ngo.css";

const API = "http://127.0.0.1:5000";

function NGO({ user, onLogout }) {
  const [active, setActive] = useState("dashboard");
  const [profile, setProfile] = useState(null);
  const [dashboard, setDashboard] = useState({});
  const [requirements, setRequirements] = useState([]);
  const [donations, setDonations] = useState([]);
  const [requests, setRequests] = useState([]);

  const [form, setForm] = useState({
    category: "Clothes",
    item_name: "",
    quantity_required: "",
    priority: "normal",
    description: "",
    location: ""
  });

  const token = localStorage.getItem("token");

  const headers = {
    Authorization: `Bearer ${token}`,
    "Content-Type": "application/json"
  };

  async function loadData() {
    try {
      const [p, d, r, a, q] = await Promise.all([
        fetch(`${API}/api/ngo/profile`, {
          headers: { Authorization: `Bearer ${token}` }
        }),
        fetch(`${API}/api/ngo/dashboard`, {
          headers: { Authorization: `Bearer ${token}` }
        }),
        fetch(`${API}/api/ngo/requirements`, {
          headers: { Authorization: `Bearer ${token}` }
        }),
        fetch(`${API}/api/ngo/donations`, {
          headers: { Authorization: `Bearer ${token}` }
        }),
        fetch(`${API}/api/ngo/requests`, {
          headers: { Authorization: `Bearer ${token}` }
        })
      ]);

      if (p.ok) setProfile(await p.json());
      if (d.ok) setDashboard(await d.json());
      if (r.ok) setRequirements(await r.json());
      if (a.ok) setDonations(await a.json());
      if (q.ok) setRequests(await q.json());
    } catch (error) {
      console.error(error);
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  async function createRequirement(e) {
    e.preventDefault();

    if (!form.item_name || !form.quantity_required) {
      alert("Enter item name and quantity");
      return;
    }

    const response = await fetch(`${API}/api/ngo/requirements`, {
      method: "POST",
      headers,
      body: JSON.stringify(form)
    });

    const data = await response.json();

    if (!response.ok) {
      alert(data.message || "Could not create requirement");
      return;
    }

    alert("Requirement posted successfully!");

    setForm({
      category: "Clothes",
      item_name: "",
      quantity_required: "",
      priority: "normal",
      description: "",
      location: ""
    });

    loadData();
    setActive("requirements");
  }

  async function requestDonation(id) {
    const response = await fetch(
      `${API}/api/ngo/donations/${id}/request`,
      {
        method: "POST",
        headers
      }
    );

    const data = await response.json();

    if (!response.ok) {
      alert(data.message || "Request failed");
      return;
    }

    alert("Donation requested successfully!");
    loadData();
  }

  const organization = profile?.organization;

  return (
    <div className="ngo-app">

      <aside className="ngo-sidebar">

        <div className="ngo-logo">
          <div className="ngo-logo-icon">R</div>
          <div>
            <strong>ResQLink</strong>
            <span>NGO / Ashram</span>
          </div>
        </div>

        <nav>
          <button
            className={active === "dashboard" ? "active" : ""}
            onClick={() => setActive("dashboard")}
          >
            🏠 Dashboard
          </button>

          <button
            className={active === "requirements" ? "active" : ""}
            onClick={() => setActive("requirements")}
          >
            📋 Requirements
          </button>

          <button
            className={active === "donations" ? "active" : ""}
            onClick={() => setActive("donations")}
          >
            🎁 Donations
          </button>

          <button
            className={active === "requests" ? "active" : ""}
            onClick={() => setActive("requests")}
          >
            📦 My Requests
          </button>

          <button
            className={active === "post" ? "active" : ""}
            onClick={() => setActive("post")}
          >
            ➕ Post Requirement
          </button>
        </nav>

        <button className="ngo-logout" onClick={onLogout}>
          ↪ Logout
        </button>

      </aside>

      <main className="ngo-main">

        <header className="ngo-header">
          <div>
            <p className="eyebrow">ORGANIZATION DASHBOARD</p>
            <h1>
              Welcome, {organization?.organization_name || user?.name}
            </h1>
            <p>Manage needs, donations and community support.</p>
          </div>

          <div className="ngo-verification">
            {user?.is_verified ? "✓ Verified Organization" : "Pending Verification"}
          </div>
        </header>

        {active === "dashboard" && (
          <>
            <section className="ngo-stats">

              <div className="ngo-stat">
                <span>📋</span>
                <div>
                  <small>Total Requirements</small>
                  <strong>{dashboard.requirements || 0}</strong>
                </div>
              </div>

              <div className="ngo-stat">
                <span>🔴</span>
                <div>
                  <small>Open Requirements</small>
                  <strong>{dashboard.open_requirements || 0}</strong>
                </div>
              </div>

              <div className="ngo-stat">
                <span>📦</span>
                <div>
                  <small>Donation Requests</small>
                  <strong>{dashboard.requests || 0}</strong>
                </div>
              </div>

              <div className="ngo-stat">
                <span>✓</span>
                <div>
                  <small>Completed</small>
                  <strong>{dashboard.completed || 0}</strong>
                </div>
              </div>

            </section>

            <section className="ngo-grid">

              <div className="ngo-card">
                <div className="card-title">
                  <div>
                    <h2>Organization</h2>
                    <p>Your verified organization information</p>
                  </div>
                </div>

                <div className="org-info">
                  <strong>{organization?.organization_name}</strong>
                  <span>{organization?.organization_type}</span>
                  <span>📍 {organization?.address || "Address not added"}</span>
                  <span>✓ Verification: {organization?.verification_status}</span>
                </div>
              </div>

              <div className="ngo-card">
                <div className="card-title">
                  <div>
                    <h2>Quick Actions</h2>
                    <p>Manage your organization</p>
                  </div>
                </div>

                <div className="quick-actions">
                  <button onClick={() => setActive("post")}>
                    ➕ Post Requirement
                  </button>

                  <button onClick={() => setActive("donations")}>
                    🎁 Find Donations
                  </button>

                  <button onClick={() => setActive("requests")}>
                    📦 Track Requests
                  </button>
                </div>
              </div>

            </section>

            <section className="ngo-card">
              <div className="card-title">
                <div>
                  <h2>How ResQLink Helps</h2>
                  <p>Connect your needs with available community donations.</p>
                </div>
              </div>

              <div className="flow">
                <div>📋<span>Post Need</span></div>
                <b>→</b>
                <div>🎁<span>Match Donation</span></div>
                <b>→</b>
                <div>🚚<span>Volunteer</span></div>
                <b>→</b>
                <div>✓<span>Receive</span></div>
              </div>
            </section>
          </>
        )}

        {active === "post" && (
          <section className="ngo-card large-card">
            <div className="card-title">
              <div>
                <h2>Post a Requirement</h2>
                <p>Tell donors what your organization currently needs.</p>
              </div>
            </div>

            <form className="ngo-form" onSubmit={createRequirement}>

              <label>
                Category
                <select
                  value={form.category}
                  onChange={(e) =>
                    setForm({ ...form, category: e.target.value })
                  }
                >
                  <option>Clothes</option>
                  <option>Books</option>
                  <option>Food</option>
                  <option>Furniture</option>
                  <option>Electronics</option>
                  <option>School Supplies</option>
                  <option>Blankets</option>
                  <option>Other</option>
                </select>
              </label>

              <label>
                Item Name
                <input
                  placeholder="Example: Blankets"
                  value={form.item_name}
                  onChange={(e) =>
                    setForm({ ...form, item_name: e.target.value })
                  }
                />
              </label>

              <label>
                Quantity Required
                <input
                  type="number"
                  min="1"
                  placeholder="100"
                  value={form.quantity_required}
                  onChange={(e) =>
                    setForm({
                      ...form,
                      quantity_required: e.target.value
                    })
                  }
                />
              </label>

              <label>
                Priority
                <select
                  value={form.priority}
                  onChange={(e) =>
                    setForm({ ...form, priority: e.target.value })
                  }
                >
                  <option value="normal">Normal</option>
                  <option value="high">High</option>
                  <option value="urgent">Urgent</option>
                </select>
              </label>

              <label>
                Location
                <input
                  placeholder="Delivery location"
                  value={form.location}
                  onChange={(e) =>
                    setForm({ ...form, location: e.target.value })
                  }
                />
              </label>

              <label className="full">
                Description
                <textarea
                  placeholder="Explain the requirement..."
                  value={form.description}
                  onChange={(e) =>
                    setForm({
                      ...form,
                      description: e.target.value
                    })
                  }
                />
              </label>

              <button className="primary-btn" type="submit">
                Post Requirement
              </button>

            </form>
          </section>
        )}

        {active === "requirements" && (
          <section className="ngo-card large-card">
            <div className="card-title">
              <div>
                <h2>Current Requirements</h2>
                <p>Needs posted by your organization.</p>
              </div>
            </div>

            {requirements.length === 0 ? (
              <div className="empty">No requirements posted yet.</div>
            ) : (
              <div className="ngo-list">
                {requirements.map((r) => (
                  <div className="ngo-list-item" key={r.id}>
                    <div>
                      <strong>{r.item_name}</strong>
                      <span>{r.category} · {r.quantity_required} units</span>
                      <p>{r.description || "No description"}</p>
                    </div>

                    <div className={`priority ${r.priority}`}>
                      {r.priority}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </section>
        )}

        {active === "donations" && (
          <section className="ngo-card large-card">
            <div className="card-title">
              <div>
                <h2>Available Donations</h2>
                <p>Community donations currently available.</p>
              </div>
            </div>

            {donations.length === 0 ? (
              <div className="empty">
                No available donations right now.
              </div>
            ) : (
              <div className="ngo-list">

                {donations.map((d) => (
                  <div className="donation-card" key={d.id}>

                    <div className="donation-icon">🎁</div>

                    <div className="donation-content">
                      <h3>{d.item_name}</h3>

                      <p>
                        {d.category} · Quantity: {d.quantity}
                      </p>

                      <span>
                        Condition: {d.condition || "Not specified"}
                      </span>

                      <span>
                        📍 {d.location || "Location not specified"}
                      </span>

                      <span>
                        Donor: {d.donor?.name || "Anonymous"}
                      </span>
                    </div>

                    <button
                      className="primary-btn small"
                      onClick={() => requestDonation(d.id)}
                    >
                      Request
                    </button>

                  </div>
                ))}

              </div>
            )}
          </section>
        )}

        {active === "requests" && (
          <section className="ngo-card large-card">
            <div className="card-title">
              <div>
                <h2>My Donation Requests</h2>
                <p>Track donations requested by your organization.</p>
              </div>
            </div>

            {requests.length === 0 ? (
              <div className="empty">No requests yet.</div>
            ) : (
              <div className="ngo-list">
                {requests.map((r) => (
                  <div className="ngo-list-item" key={r.id}>
                    <div>
                      <strong>
                        {r.donation?.item_name || "Donation"}
                      </strong>

                      <span>
                        Quantity: {r.donation?.quantity || "-"}
                      </span>

                      <span>
                        📍 {r.donation?.location || "-"}
                      </span>
                    </div>

                    <div className={`status ${r.status}`}>
                      {r.status}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </section>
        )}

      </main>
    </div>
  );
}

export default NGO;
