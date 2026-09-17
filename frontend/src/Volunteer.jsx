import { useEffect, useMemo, useState } from "react";
import "./volunteer.css";

const API = "http://127.0.0.1:5000";

function Volunteer() {
  const [activePage, setActivePage] = useState("dashboard");
  const [user, setUser] = useState(null);

  const [dashboard, setDashboard] = useState({
    available_tasks: 0,
    my_tasks: 0,
    completed_tasks: 0,
    active_tasks: 0,
  });

  const [availableTasks, setAvailableTasks] = useState([]);
  const [myTasks, setMyTasks] = useState([]);
  const [profile, setProfile] = useState(null);

  const [showVerify, setShowVerify] = useState(false);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  const [verifyForm, setVerifyForm] = useState({
    service_area: "",
    skills: "",
    availability: "",
    phone: "",
    document: null,
  });

  const token = localStorage.getItem("token");

  useEffect(() => {
    const storedUser = localStorage.getItem("user");

    if (storedUser) {
      try {
        setUser(JSON.parse(storedUser));
      } catch {
        setUser(null);
      }
    }

    loadData();
  }, []);

  const authHeaders = useMemo(
    () => ({
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    }),
    [token]
  );

  async function loadData() {
    setLoading(true);

    try {
      const headers = {
        Authorization: `Bearer ${token}`,
      };

      const [dashboardRes, availableRes, myTasksRes, profileRes] =
        await Promise.all([
          fetch(`${API}/api/volunteer/dashboard`, { headers }),
          fetch(`${API}/api/volunteer/tasks/available`, { headers }),
          fetch(`${API}/api/volunteer/tasks/my`, { headers }),
          fetch(`${API}/api/volunteer/profile`, { headers }),
        ]);

      if (dashboardRes.ok) {
        const data = await dashboardRes.json();
        setDashboard(data);
      }

      if (availableRes.ok) {
        const data = await availableRes.json();
        setAvailableTasks(data.tasks || data || []);
      }

      if (myTasksRes.ok) {
        const data = await myTasksRes.json();
        setMyTasks(data.tasks || data || []);
      }

      if (profileRes.ok) {
        const data = await profileRes.json();
        setProfile(data);
      }
    } catch (error) {
      console.error("Volunteer dashboard error:", error);
    } finally {
      setLoading(false);
    }
  }

  function showMessage(text) {
    setMessage(text);

    setTimeout(() => {
      setMessage("");
    }, 3500);
  }

  async function taskAction(taskId, action) {
    try {
      const response = await fetch(
        `${API}/api/volunteer/tasks/${taskId}/${action}`,
        {
          method: "POST",
          headers: authHeaders,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        showMessage(data.message || "Action could not be completed.");
        return;
      }

      showMessage(data.message || `Task ${action} completed.`);
      await loadData();
    } catch (error) {
      console.error(error);
      showMessage("Unable to connect to the server.");
    }
  }

  async function submitVerification(event) {
    event.preventDefault();

    try {
      const formData = new FormData();

      formData.append("service_area", verifyForm.service_area);
      formData.append("skills", verifyForm.skills);
      formData.append("availability", verifyForm.availability);
      formData.append("phone", verifyForm.phone);

      if (verifyForm.document) {
        formData.append("document", verifyForm.document);
      }

      const response = await fetch(`${API}/api/volunteer/verify`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        showMessage(data.message || "Verification failed.");
        return;
      }

      showMessage(data.message || "Volunteer profile verified.");
      setShowVerify(false);
      await loadData();
    } catch (error) {
      console.error(error);
      showMessage("Unable to connect to the server.");
    }
  }

  function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    window.location.reload();
  }

  function initials() {
    const name = user?.name || "Volunteer";

    return name
      .split(" ")
      .map((word) => word[0])
      .join("")
      .slice(0, 2)
      .toUpperCase();
  }

  function statusClass(status) {
    const value = String(status || "").toLowerCase();

    if (value.includes("complete")) return "success";
    if (value.includes("deliver")) return "info";
    if (value.includes("pickup")) return "warning";
    if (value.includes("accept")) return "info";
    if (value.includes("request")) return "warning";

    return "neutral";
  }

  function formatStatus(status) {
    if (!status) return "Available";

    return String(status)
      .replaceAll("_", " ")
      .replace(/\b\w/g, (letter) => letter.toUpperCase());
  }

  function renderTaskAction(task) {
    const status = String(task.status || "").toLowerCase();
    const id = task.id;

    if (status === "available" || status === "requested") {
      return (
        <button
          className="vol-primary-btn"
          onClick={() => taskAction(id, "accept")}
        >
          Accept Task
        </button>
      );
    }

    if (status.includes("accept")) {
      return (
        <button
          className="vol-primary-btn"
          onClick={() => taskAction(id, "pickup")}
        >
          Mark Pickup
        </button>
      );
    }

    if (status.includes("pickup")) {
      return (
        <button
          className="vol-primary-btn"
          onClick={() => taskAction(id, "deliver")}
        >
          Mark Delivered
        </button>
      );
    }

    if (status.includes("deliver")) {
      return (
        <button
          className="vol-primary-btn"
          onClick={() => taskAction(id, "complete")}
        >
          Complete Task
        </button>
      );
    }

    if (status.includes("complete")) {
      return (
        <span className="vol-completed-label">
          ✓ Completed
        </span>
      );
    }

    return null;
  }

  function TaskCard({ task, available = false }) {
    return (
      <div className="vol-task-card">
        <div className="vol-task-top">
          <div className="vol-task-icon">📦</div>

          <div className="vol-task-heading">
            <h3>
              {task.item_name ||
                task.donation_item ||
                task.title ||
                "Resource Delivery"}
            </h3>

            <span className={`vol-status ${statusClass(task.status)}`}>
              {formatStatus(task.status)}
            </span>
          </div>
        </div>

        <div className="vol-task-details">
          <div>
            <span>📍 Pickup</span>
            <strong>
              {task.pickup_location || task.donation_location || "Location not specified"}
            </strong>
          </div>

          <div>
            <span>🏠 Delivery</span>
            <strong>
              {task.delivery_location ||
                task.receiver_location ||
                "Destination not specified"}
            </strong>
          </div>

          <div>
            <span>📦 Quantity</span>
            <strong>{task.quantity || "1 item"}</strong>
          </div>
        </div>

        {task.description && (
          <p className="vol-task-description">{task.description}</p>
        )}

        <div className="vol-task-footer">
          <small>
            {available ? "Community task" : "Your assigned task"}
          </small>

          {renderTaskAction(task)}
        </div>
      </div>
    );
  }

  function DashboardPage() {
    return (
      <>
        <section className="vol-welcome">
          <div>
            <span className="vol-eyebrow">MAKE A DIFFERENCE</span>

            <h1>
              Welcome back,{" "}
              {user?.name?.split(" ")[0] || "Volunteer"} 👋
            </h1>

            <p>
              Your time can help move essential resources from people who
              have them to people who need them.
            </p>

            <div className="vol-welcome-actions">
              <button
                className="vol-primary-btn"
                onClick={() => setActivePage("available")}
              >
                🤝 Find Tasks
              </button>

              <button
                className="vol-secondary-btn"
                onClick={() => setActivePage("mytasks")}
              >
                📦 My Tasks
              </button>
            </div>
          </div>

          <div className="vol-welcome-art">🤝</div>
        </section>

        <section className="vol-stats">
          <div className="vol-stat-card">
            <div className="vol-stat-icon green">📋</div>
            <div>
              <span>Available Tasks</span>
              <strong>{dashboard.available_tasks || 0}</strong>
              <small>Ready to accept</small>
            </div>
          </div>

          <div className="vol-stat-card">
            <div className="vol-stat-icon blue">🚚</div>
            <div>
              <span>My Tasks</span>
              <strong>{dashboard.my_tasks || 0}</strong>
              <small>Assigned to you</small>
            </div>
          </div>

          <div className="vol-stat-card">
            <div className="vol-stat-icon orange">⏳</div>
            <div>
              <span>Active Tasks</span>
              <strong>{dashboard.active_tasks || 0}</strong>
              <small>In progress</small>
            </div>
          </div>

          <div className="vol-stat-card">
            <div className="vol-stat-icon purple">✓</div>
            <div>
              <span>Completed</span>
              <strong>{dashboard.completed_tasks || 0}</strong>
              <small>Successful deliveries</small>
            </div>
          </div>
        </section>

        <div className="vol-two-column">
          <section className="vol-panel">
            <div className="vol-panel-heading">
              <div>
                <h2>Available Opportunities</h2>
                <p>Help the community with an active task.</p>
              </div>

              <button onClick={() => setActivePage("available")}>
                View all →
              </button>
            </div>

            {availableTasks.length === 0 ? (
              <div className="vol-empty-small">
                <span>🤝</span>
                <p>No tasks are available right now.</p>
                <small>Check again later for new community requests.</small>
              </div>
            ) : (
              <div className="vol-mini-list">
                {availableTasks.slice(0, 3).map((task) => (
                  <div className="vol-mini-task" key={task.id}>
                    <div className="vol-mini-icon">📦</div>

                    <div>
                      <strong>
                        {task.item_name ||
                          task.donation_item ||
                          "Resource Delivery"}
                      </strong>

                      <small>
                        📍{" "}
                        {task.pickup_location ||
                          task.donation_location ||
                          "Pickup location"}
                      </small>
                    </div>

                    <button onClick={() => taskAction(task.id, "accept")}>
                      Accept
                    </button>
                  </div>
                ))}
              </div>
            )}
          </section>

          <section className="vol-panel">
            <div className="vol-panel-heading">
              <div>
                <h2>My Progress</h2>
                <p>Track the tasks you are helping with.</p>
              </div>

              <button onClick={() => setActivePage("mytasks")}>
                View all →
              </button>
            </div>

            {myTasks.length === 0 ? (
              <div className="vol-empty-small">
                <span>📦</span>
                <p>No assigned tasks yet.</p>
                <small>Accept an available task to get started.</small>
              </div>
            ) : (
              <div className="vol-mini-list">
                {myTasks.slice(0, 3).map((task) => (
                  <div className="vol-mini-task" key={task.id}>
                    <div className="vol-mini-icon">🚚</div>

                    <div>
                      <strong>
                        {task.item_name ||
                          task.donation_item ||
                          "Delivery Task"}
                      </strong>

                      <small>{formatStatus(task.status)}</small>
                    </div>

                    <span className={`vol-status ${statusClass(task.status)}`}>
                      {formatStatus(task.status)}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </section>
        </div>
      </>
    );
  }

  function AvailablePage() {
    return (
      <section className="vol-page-section">
        <div className="vol-page-header">
          <div>
            <span className="vol-eyebrow">COMMUNITY OPPORTUNITIES</span>
            <h1>Available Tasks</h1>
            <p>
              Choose a delivery or pickup task that you can help complete.
            </p>
          </div>
        </div>

        {availableTasks.length === 0 ? (
          <div className="vol-large-empty">
            <div>🤝</div>
            <h2>No tasks available</h2>
            <p>
              New volunteer opportunities will appear here when community
              requests need assistance.
            </p>
          </div>
        ) : (
          <div className="vol-task-grid">
            {availableTasks.map((task) => (
              <TaskCard key={task.id} task={task} available />
            ))}
          </div>
        )}
      </section>
    );
  }

  function MyTasksPage() {
    return (
      <section className="vol-page-section">
        <div className="vol-page-header">
          <div>
            <span className="vol-eyebrow">YOUR CONTRIBUTION</span>
            <h1>My Tasks</h1>
            <p>Manage your accepted pickups and deliveries.</p>
          </div>
        </div>

        {myTasks.length === 0 ? (
          <div className="vol-large-empty">
            <div>📦</div>
            <h2>No tasks yet</h2>
            <p>
              Accept an available community task to start helping.
            </p>

            <button
              className="vol-primary-btn"
              onClick={() => setActivePage("available")}
            >
              Find Available Tasks
            </button>
          </div>
        ) : (
          <div className="vol-task-grid">
            {myTasks.map((task) => (
              <TaskCard key={task.id} task={task} />
            ))}
          </div>
        )}
      </section>
    );
  }

  function ProfilePage() {
    const verified =
      profile?.is_verified ||
      profile?.verified ||
      user?.is_verified;

    return (
      <section className="vol-page-section">
        <div className="vol-page-header">
          <div>
            <span className="vol-eyebrow">VOLUNTEER PROFILE</span>
            <h1>My Profile</h1>
            <p>Manage your volunteer information and availability.</p>
          </div>
        </div>

        <div className="vol-profile-card">
          <div className="vol-profile-top">
            <div className="vol-profile-avatar">{initials()}</div>

            <div>
              <h2>{user?.name || "Volunteer"}</h2>
              <p>{user?.email || "Volunteer account"}</p>

              <span className="vol-verified-badge">
                {verified ? "✓ Verified Volunteer" : "Verification Pending"}
              </span>
            </div>
          </div>

          <div className="vol-profile-grid">
            <div>
              <span>Email</span>
              <strong>{user?.email || "—"}</strong>
            </div>

            <div>
              <span>Phone</span>
              <strong>{profile?.phone || user?.phone || "Not added"}</strong>
            </div>

            <div>
              <span>Service Area</span>
              <strong>{profile?.service_area || "Not specified"}</strong>
            </div>

            <div>
              <span>Availability</span>
              <strong>{profile?.availability || "Not specified"}</strong>
            </div>

            <div>
              <span>Skills</span>
              <strong>{profile?.skills || "Not specified"}</strong>
            </div>

            <div>
              <span>Volunteer Status</span>
              <strong>{verified ? "Active" : "Pending"}</strong>
            </div>
          </div>

          <button
            className="vol-primary-btn"
            onClick={() => setShowVerify(true)}
          >
            ✎ Update Volunteer Profile
          </button>
        </div>
      </section>
    );
  }

  function renderPage() {
    if (activePage === "available") {
      return <AvailablePage />;
    }

    if (activePage === "mytasks") {
      return <MyTasksPage />;
    }

    if (activePage === "profile") {
      return <ProfilePage />;
    }

    return <DashboardPage />;
  }

  if (loading) {
    return (
      <div className="vol-loading">
        <div className="vol-loading-spinner">♻</div>
        <h2>Loading Volunteer Dashboard</h2>
        <p>Connecting you with community opportunities...</p>
      </div>
    );
  }

  return (
    <div className="volunteer-app">
      {/* SIDEBAR */}

      <aside className="vol-sidebar">
        <div className="vol-brand">
          <div className="vol-brand-icon">♻</div>

          <div>
            <strong>ResQLink</strong>
            <small>Community Resource Network</small>
          </div>
        </div>

        <div className="vol-profile-mini">
          <div className="vol-mini-avatar">{initials()}</div>

          <div>
            <strong>{user?.name || "Volunteer"}</strong>
            <small>Volunteer</small>
          </div>
        </div>

        <p className="vol-nav-title">MAIN MENU</p>

        <nav className="vol-nav">
          <button
            className={activePage === "dashboard" ? "active" : ""}
            onClick={() => setActivePage("dashboard")}
          >
            <span>⌂</span>
            Home
          </button>

          <button
            className={activePage === "available" ? "active" : ""}
            onClick={() => setActivePage("available")}
          >
            <span>🤝</span>
            Find Tasks
          </button>

          <button
            className={activePage === "mytasks" ? "active" : ""}
            onClick={() => setActivePage("mytasks")}
          >
            <span>📦</span>
            My Tasks
          </button>

          <button
            className={activePage === "profile" ? "active" : ""}
            onClick={() => setActivePage("profile")}
          >
            <span>👤</span>
            My Profile
          </button>
        </nav>

        <div className="vol-sidebar-bottom">
          <button onClick={() => showMessage("Notifications coming soon.")}>
            <span>🔔</span>
            Notifications
          </button>

          <button onClick={() => showMessage("Settings coming soon.")}>
            <span>⚙️</span>
            Settings
          </button>

          <button className="vol-logout" onClick={logout}>
            <span>↪</span>
            Logout
          </button>
        </div>
      </aside>

      {/* MAIN */}

      <main className="vol-main">
        <header className="vol-topbar">
          <div>
            <p>ResQLink / Volunteer</p>
            <h2>
              {activePage === "dashboard"
                ? "Volunteer Dashboard"
                : activePage === "available"
                ? "Available Tasks"
                : activePage === "mytasks"
                ? "My Tasks"
                : "My Profile"}
            </h2>
          </div>

          <div className="vol-top-actions">
            <button
              className="vol-icon-button"
              onClick={() => showMessage("You're all caught up.")}
            >
              🔔
            </button>

            <div className="vol-top-user">
              <div className="vol-mini-avatar">{initials()}</div>

              <div>
                <strong>{user?.name || "Volunteer"}</strong>
                <small>
                  {user?.is_verified ? "✓ Verified" : "Volunteer"}
                </small>
              </div>
            </div>
          </div>
        </header>

        {message && <div className="vol-toast">✓ {message}</div>}

        {renderPage()}
      </main>

      {/* VERIFICATION / PROFILE MODAL */}

      {showVerify && (
        <div
          className="vol-modal-overlay"
          onClick={() => setShowVerify(false)}
        >
          <div
            className="vol-modal"
            onClick={(event) => event.stopPropagation()}
          >
            <div className="vol-modal-header">
              <div>
                <span className="vol-eyebrow">VOLUNTEER DETAILS</span>
                <h2>Update Your Profile</h2>
              </div>

              <button onClick={() => setShowVerify(false)}>×</button>
            </div>

            <form onSubmit={submitVerification}>
              <div className="vol-form-grid">
                <div>
                  <label>Service Area</label>
                  <input
                    value={verifyForm.service_area}
                    onChange={(event) =>
                      setVerifyForm({
                        ...verifyForm,
                        service_area: event.target.value,
                      })
                    }
                    placeholder="e.g. Your city / area"
                  />
                </div>

                <div>
                  <label>Availability</label>
                  <input
                    value={verifyForm.availability}
                    onChange={(event) =>
                      setVerifyForm({
                        ...verifyForm,
                        availability: event.target.value,
                      })
                    }
                    placeholder="e.g. Weekends"
                  />
                </div>

                <div className="vol-full">
                  <label>Skills</label>
                  <input
                    value={verifyForm.skills}
                    onChange={(event) =>
                      setVerifyForm({
                        ...verifyForm,
                        skills: event.target.value,
                      })
                    }
                    placeholder="e.g. Pickup, driving, coordination"
                  />
                </div>

                <div className="vol-full">
                  <label>Phone</label>
                  <input
                    value={verifyForm.phone}
                    onChange={(event) =>
                      setVerifyForm({
                        ...verifyForm,
                        phone: event.target.value,
                      })
                    }
                    placeholder="Enter phone number"
                  />
                </div>

                <div className="vol-full">
                  <label>Verification Document</label>
                  <input
                    type="file"
                    onChange={(event) =>
                      setVerifyForm({
                        ...verifyForm,
                        document: event.target.files?.[0] || null,
                      })
                    }
                  />

                  <small className="vol-form-help">
                    Upload an optional supporting document.
                  </small>
                </div>
              </div>

              <div className="vol-modal-actions">
                <button
                  type="button"
                  className="vol-secondary-btn"
                  onClick={() => setShowVerify(false)}
                >
                  Cancel
                </button>

                <button type="submit" className="vol-primary-btn">
                  Save Profile
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default Volunteer;