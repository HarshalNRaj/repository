import { useEffect, useState } from "react";
import "./blood.css";

const API = "http://127.0.0.1:5000";

function BloodBank({ user, onLogout }) {
  const [active, setActive] = useState("dashboard");

  const [profile, setProfile] = useState(null);
  const [dashboard, setDashboard] = useState({});
  const [inventory, setInventory] = useState([]);
  const [requests, setRequests] = useState([]);

  const [inventoryForm, setInventoryForm] = useState({
    blood_group: "O+",
    units_available: ""
  });

  const [requestForm, setRequestForm] = useState({
    patient_name: "",
    blood_group: "O+",
    units_required: "",
    urgency: "normal",
    hospital: "",
    contact: ""
  });

  const token = localStorage.getItem("token");

  async function loadData() {
    const auth = {
      Authorization: `Bearer ${token}`
    };

    try {
      const [p, d, i, r] = await Promise.all([
        fetch(`${API}/api/blood/profile`, { headers: auth }),
        fetch(`${API}/api/blood/dashboard`, { headers: auth }),
        fetch(`${API}/api/blood/inventory`, { headers: auth }),
        fetch(`${API}/api/blood/requests`, { headers: auth })
      ]);

      if (p.ok) setProfile(await p.json());
      if (d.ok) setDashboard(await d.json());
      if (i.ok) setInventory(await i.json());
      if (r.ok) setRequests(await r.json());
    } catch (error) {
      console.error(error);
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  async function updateInventory(e) {
    e.preventDefault();

    const response = await fetch(`${API}/api/blood/inventory`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify(inventoryForm)
    });

    const data = await response.json();

    if (!response.ok) {
      alert(data.message || "Could not update inventory");
      return;
    }

    alert("Inventory updated successfully!");

    setInventoryForm({
      blood_group: "O+",
      units_available: ""
    });

    loadData();
  }

  async function createBloodRequest(e) {
    e.preventDefault();

    const response = await fetch(`${API}/api/blood/requests`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify(requestForm)
    });

    const data = await response.json();

    if (!response.ok) {
      alert(data.message || "Could not create request");
      return;
    }

    alert("Blood request created successfully!");

    setRequestForm({
      patient_name: "",
      blood_group: "O+",
      units_required: "",
      urgency: "normal",
      hospital: "",
      contact: ""
    });

    loadData();
    setActive("requests");
  }

  async function updateStatus(id, status) {
    const response = await fetch(
      `${API}/api/blood/requests/${id}/status`,
      {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ status })
      }
    );

    const data = await response.json();

    if (!response.ok) {
      alert(data.message || "Update failed");
      return;
    }

    loadData();
  }

  return (
    <div className="blood-app">

      <aside className="blood-sidebar">

        <div className="blood-logo">
          <div className="blood-logo-icon">+</div>
          <div>
            <strong>ResQLink</strong>
            <span>Blood Bank</span>
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
            className={active === "inventory" ? "active" : ""}
            onClick={() => setActive("inventory")}
          >
            🩸 Blood Inventory
          </button>

          <button
            className={active === "requests" ? "active" : ""}
            onClick={() => setActive("requests")}
          >
            🚨 Blood Requests
          </button>

          <button
            className={active === "update" ? "active" : ""}
            onClick={() => setActive("update")}
          >
            ➕ Update Inventory
          </button>

          <button
            className={active === "new-request" ? "active" : ""}
            onClick={() => setActive("new-request")}
          >
            🚨 New Request
          </button>

        </nav>

        <button className="blood-logout" onClick={onLogout}>
          ↪ Logout
        </button>

      </aside>

      <main className="blood-main">

        <header className="blood-header">

          <div>
            <p className="blood-eyebrow">BLOOD COORDINATION CENTER</p>

            <h1>
              Welcome, {profile?.name || user?.name}
            </h1>

            <p>
              Coordinate blood inventory and urgent requirements.
            </p>
          </div>

          <div className="blood-verified">
            ✓ Verified Blood Bank
          </div>

        </header>

        {active === "dashboard" && (
          <>

            <section className="blood-stats">

              <div className="blood-stat">
                <span>🩸</span>
                <div>
                  <small>Blood Groups</small>
                  <strong>{dashboard.blood_groups || 0}</strong>
                </div>
              </div>

              <div className="blood-stat">
                <span>📦</span>
                <div>
                  <small>Total Units</small>
                  <strong>{dashboard.total_units || 0}</strong>
                </div>
              </div>

              <div className="blood-stat">
                <span>📋</span>
                <div>
                  <small>Total Requests</small>
                  <strong>{dashboard.total_requests || 0}</strong>
                </div>
              </div>

              <div className="blood-stat urgent-stat">
                <span>🚨</span>
                <div>
                  <small>Urgent</small>
                  <strong>{dashboard.urgent_requests || 0}</strong>
                </div>
              </div>

            </section>

            <section className="blood-grid">

              <div className="blood-card">

                <div className="blood-card-title">
                  <h2>Blood Inventory</h2>

                  <button onClick={() => setActive("inventory")}>
                    View All
                  </button>
                </div>

                <div className="blood-mini-list">

                  {inventory.length === 0 ? (
                    <p className="empty-blood">
                      No inventory added yet.
                    </p>
                  ) : (
                    inventory.map((item) => (
                      <div
                        className="blood-row"
                        key={item.id}
                      >
                        <strong>{item.blood_group}</strong>
                        <span>{item.units_available} units</span>
                      </div>
                    ))
                  )}

                </div>

              </div>

              <div className="blood-card">

                <div className="blood-card-title">
                  <h2>Quick Actions</h2>
                </div>

                <div className="blood-actions">

                  <button onClick={() => setActive("update")}>
                    🩸 Update Blood Stock
                  </button>

                  <button onClick={() => setActive("new-request")}>
                    🚨 Create Blood Request
                  </button>

                  <button onClick={() => setActive("requests")}>
                    📋 View Requests
                  </button>

                </div>

              </div>

            </section>

            <section className="blood-card">

              <div className="blood-card-title">
                <div>
                  <h2>ResQLink Blood Coordination</h2>
                  <p>
                    Keep inventory information updated so blood requirements
                    can be coordinated quickly.
                  </p>
                </div>
              </div>

              <div className="blood-flow">

                <div>
                  🩸
                  <span>Blood Stock</span>
                </div>

                <b>→</b>

                <div>
                  🚨
                  <span>Requirement</span>
                </div>

                <b>→</b>

                <div>
                  📞
                  <span>Coordination</span>
                </div>

                <b>→</b>

                <div>
                  ✓
                  <span>Fulfilled</span>
                </div>

              </div>

            </section>

          </>
        )}

        {active === "inventory" && (
          <section className="blood-card">

            <div className="blood-card-title">
              <div>
                <h2>Blood Inventory</h2>
                <p>Current available units.</p>
              </div>
            </div>

            <div className="inventory-grid">

              {inventory.map((item) => (
                <div
                  className="inventory-card"
                  key={item.id}
                >
                  <div className="blood-type">
                    {item.blood_group}
                  </div>

                  <strong>
                    {item.units_available}
                  </strong>

                  <span>Units Available</span>
                </div>
              ))}

            </div>

          </section>
        )}

        {active === "update" && (
          <section className="blood-card">

            <div className="blood-card-title">
              <div>
                <h2>Update Blood Inventory</h2>
                <p>Update current stock for a blood group.</p>
              </div>
            </div>

            <form
              className="blood-form"
              onSubmit={updateInventory}
            >

              <label>
                Blood Group

                <select
                  value={inventoryForm.blood_group}
                  onChange={(e) =>
                    setInventoryForm({
                      ...inventoryForm,
                      blood_group: e.target.value
                    })
                  }
                >
                  <option>O+</option>
                  <option>O-</option>
                  <option>A+</option>
                  <option>A-</option>
                  <option>B+</option>
                  <option>B-</option>
                  <option>AB+</option>
                  <option>AB-</option>
                </select>
              </label>

              <label>
                Units Available

                <input
                  type="number"
                  min="0"
                  placeholder="25"
                  value={inventoryForm.units_available}
                  onChange={(e) =>
                    setInventoryForm({
                      ...inventoryForm,
                      units_available: e.target.value
                    })
                  }
                />
              </label>

              <button className="blood-primary">
                Update Inventory
              </button>

            </form>

          </section>
        )}

        {active === "new-request" && (
          <section className="blood-card">

            <div className="blood-card-title">
              <div>
                <h2>Create Blood Requirement</h2>
                <p>
                  Record a blood requirement for coordination.
                </p>
              </div>
            </div>

            <form
              className="blood-form"
              onSubmit={createBloodRequest}
            >

              <label>
                Patient Name

                <input
                  value={requestForm.patient_name}
                  onChange={(e) =>
                    setRequestForm({
                      ...requestForm,
                      patient_name: e.target.value
                    })
                  }
                />
              </label>

              <label>
                Blood Group

                <select
                  value={requestForm.blood_group}
                  onChange={(e) =>
                    setRequestForm({
                      ...requestForm,
                      blood_group: e.target.value
                    })
                  }
                >
                  <option>O+</option>
                  <option>O-</option>
                  <option>A+</option>
                  <option>A-</option>
                  <option>B+</option>
                  <option>B-</option>
                  <option>AB+</option>
                  <option>AB-</option>
                </select>
              </label>

              <label>
                Units Required

                <input
                  type="number"
                  min="1"
                  value={requestForm.units_required}
                  onChange={(e) =>
                    setRequestForm({
                      ...requestForm,
                      units_required: e.target.value
                    })
                  }
                />
              </label>

              <label>
                Urgency

                <select
                  value={requestForm.urgency}
                  onChange={(e) =>
                    setRequestForm({
                      ...requestForm,
                      urgency: e.target.value
                    })
                  }
                >
                  <option value="normal">Normal</option>
                  <option value="urgent">Urgent</option>
                </select>
              </label>

              <label>
                Hospital

                <input
                  value={requestForm.hospital}
                  onChange={(e) =>
                    setRequestForm({
                      ...requestForm,
                      hospital: e.target.value
                    })
                  }
                />
              </label>

              <label>
                Contact

                <input
                  value={requestForm.contact}
                  onChange={(e) =>
                    setRequestForm({
                      ...requestForm,
                      contact: e.target.value
                    })
                  }
                />
              </label>

              <button className="blood-primary">
                Create Request
              </button>

            </form>

          </section>
        )}

        {active === "requests" && (
          <section className="blood-card">

            <div className="blood-card-title">
              <div>
                <h2>Blood Requests</h2>
                <p>Track and process blood requirements.</p>
              </div>
            </div>

            {requests.length === 0 ? (
              <div className="empty-blood">
                No blood requests yet.
              </div>
            ) : (

              <div className="blood-request-list">

                {requests.map((r) => (
                  <div
                    className={`blood-request ${
                      r.urgency === "urgent"
                        ? "urgent-request"
                        : ""
                    }`}
                    key={r.id}
                  >

                    <div className="request-type">
                      🩸
                    </div>

                    <div className="request-info">

                      <h3>
                        {r.patient_name}
                      </h3>

                      <span>
                        {r.blood_group} · {r.units_required} units
                      </span>

                      <span>
                        🏥 {r.hospital || "Hospital not specified"}
                      </span>

                      <span>
                        📞 {r.contact || "Contact not specified"}
                      </span>

                    </div>

                    <div className="request-right">

                      <strong className={`request-status ${r.status}`}>
                        {r.status}
                      </strong>

                      <select
                        value={r.status}
                        onChange={(e) =>
                          updateStatus(
                            r.id,
                            e.target.value
                          )
                        }
                      >
                        <option value="pending">
                          Pending
                        </option>

                        <option value="processing">
                          Processing
                        </option>

                        <option value="fulfilled">
                          Fulfilled
                        </option>

                        <option value="cancelled">
                          Cancelled
                        </option>
                      </select>

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

export default BloodBank;