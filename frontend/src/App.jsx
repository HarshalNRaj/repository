import { useEffect, useMemo, useState } from "react";
import "./index.css";
import "./App.css";

import Volunteer from "./Volunteer";
import NGO from "./NGO";
import BloodBank from "./BloodBank";
import Admin from "./Admin";

const API = "http://127.0.0.1:5000";

const ROLE_LABELS = {
  user: "Normal User",
  volunteer: "Volunteer",
  ngo: "NGO / Ashram",
  blood_bank: "Blood Bank",
  admin: "Administrator",
};

const CATEGORY_DATA = [
  { icon: "👕", name: "Clothes", tone: "purple" },
  { icon: "📚", name: "Books", tone: "orange" },
  { icon: "🍱", name: "Food", tone: "green" },
  { icon: "🛋️", name: "Furniture", tone: "blue" },
  { icon: "💻", name: "Electronics", tone: "violet" },
  { icon: "🎓", name: "Education", tone: "rose" },
  { icon: "🏠", name: "Household", tone: "teal" },
  { icon: "•••", name: "Others", tone: "gray" },
];

const SAMPLE_NEEDS = [
  {
    icon: "🧣",
    title: "Winter Blankets",
    type: "NGO",
    need: "50 blankets",
    location: "2.3 km away",
    organization: "Hope Foundation",
    status: "Urgent",
    statusClass: "urgent",
  },
  {
    icon: "📚",
    title: "School Books",
    type: "Ashram",
    need: "30 sets",
    location: "3.8 km away",
    organization: "Sri Sai Ashram",
    status: "Open",
    statusClass: "open",
  },
  {
    icon: "🍚",
    title: "Food Supplies",
    type: "NGO",
    need: "100 kg",
    location: "5.1 km away",
    organization: "Helping Hands",
    status: "Open",
    statusClass: "open",
  },
];

const SAMPLE_ORGANIZATIONS = [
  {
    icon: "🏢",
    name: "Helping Hands",
    type: "Community Support",
  },
  {
    icon: "🏠",
    name: "Care Foundation",
    type: "Child Welfare",
  },
  {
    icon: "🌱",
    name: "Hope Community",
    type: "Social Development",
  },
];

function getStoredUser() {
  try {
    const saved = localStorage.getItem("resqlink_user");
    return saved ? JSON.parse(saved) : null;
  } catch {
    return null;
  }
}

function getStoredToken() {
  return localStorage.getItem("resqlink_token") || "";
}

function App() {
  const [user, setUser] = useState(getStoredUser());
  const [token, setToken] = useState(getStoredToken());

  const [authMode, setAuthMode] = useState("login");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState("");

  const [activePage, setActivePage] = useState("home");
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const [donationCount, setDonationCount] = useState(0);
  const [requestCount, setRequestCount] = useState(0);
  const [completedCount, setCompletedCount] = useState(0);

  const [organizations, setOrganizations] = useState([]);
  const [requirements, setRequirements] = useState([]);

  const [loginForm, setLoginForm] = useState({
    email: "",
    password: "",
  });

  const [signupForm, setSignupForm] = useState({
    name: "",
    phone: "",
    email: "",
    password: "",
    location: "",
    role: "user",
    organization_name: "",
    organization_type: "NGO",
    organization_address: "",
  });

  const [donationForm, setDonationForm] = useState({
    category: "Clothes",
    item_name: "",
    quantity: "1",
    condition: "Good",
    description: "",
    location: "",
    donation_type: "item",
    target_type: "person",
  });

  const isLoggedIn = Boolean(user && token);

  const roleLabel = useMemo(() => {
    if (!user?.role) return "Community Member";
    return ROLE_LABELS[user.role] || user.role;
  }, [user]);

  useEffect(() => {
    if (!isLoggedIn) return;

    loadUserData();
  }, [isLoggedIn]);

  async function loadUserData() {
    try {
      const [donationsResponse, requirementsResponse, organizationsResponse] =
        await Promise.all([
          fetch(`${API}/api/donations/my`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }),
          fetch(`${API}/api/requirements`),
          fetch(`${API}/api/organizations`),
        ]);

      if (donationsResponse.ok) {
        const donations = await donationsResponse.json();

        const donationList = Array.isArray(donations)
          ? donations
          : donations.donations || [];

        setDonationCount(donationList.length);

        const completed = donationList.filter(
          (item) =>
            String(item.status || "").toLowerCase() === "completed"
        ).length;

        setCompletedCount(completed);
      }

      if (requirementsResponse.ok) {
        const data = await requirementsResponse.json();

        const list = Array.isArray(data)
          ? data
          : data.requirements || [];

        setRequirements(list);
      }

      if (organizationsResponse.ok) {
        const data = await organizationsResponse.json();

        const list = Array.isArray(data)
          ? data
          : data.organizations || [];

        setOrganizations(list);
      }
    } catch (error) {
      console.error("Unable to load dashboard data:", error);
    }
  }

  function showMessage(text, type = "success") {
    setMessage(text);
    setMessageType(type);

    window.setTimeout(() => {
      setMessage("");
      setMessageType("");
    }, 4000);
  }

  function handleLoginChange(event) {
    const { name, value } = event.target;

    setLoginForm((previous) => ({
      ...previous,
      [name]: value,
    }));
  }

  function handleSignupChange(event) {
    const { name, value } = event.target;

    setSignupForm((previous) => ({
      ...previous,
      [name]: value,
    }));
  }

  function handleDonationChange(event) {
    const { name, value } = event.target;

    setDonationForm((previous) => ({
      ...previous,
      [name]: value,
    }));
  }

  async function handleLogin(event) {
    event.preventDefault();

    if (!loginForm.email.trim() || !loginForm.password) {
      showMessage("Please enter your email and password.", "error");
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      const response = await fetch(`${API}/api/auth/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: loginForm.email.trim(),
          password: loginForm.password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.message || data.error || "Login failed. Please check your details."
        );
      }

      const loggedInUser = data.user;
      const receivedToken = data.access_token || data.token;

      if (!loggedInUser || !receivedToken) {
        throw new Error("Login response did not contain user or token.");
      }

      localStorage.setItem(
        "resqlink_user",
        JSON.stringify(loggedInUser)
      );

      localStorage.setItem("resqlink_token", receivedToken);

      setUser(loggedInUser);
      setToken(receivedToken);

      setLoginForm({
        email: "",
        password: "",
      });

      setActivePage("home");

      showMessage("Welcome back to ResQLink.");
    } catch (error) {
      showMessage(error.message || "Unable to login.", "error");
    } finally {
      setLoading(false);
    }
  }

  async function handleSignup(event) {
    event.preventDefault();

    if (
      !signupForm.name.trim() ||
      !signupForm.email.trim() ||
      !signupForm.password
    ) {
      showMessage(
        "Please complete your name, email and password.",
        "error"
      );
      return;
    }

    if (signupForm.password.length < 6) {
      showMessage(
        "Password must contain at least 6 characters.",
        "error"
      );
      return;
    }

    if (
      (signupForm.role === "ngo" ||
        signupForm.role === "blood_bank") &&
      !signupForm.organization_name.trim()
    ) {
      showMessage(
        "Organization name is required for this role.",
        "error"
      );
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      const response = await fetch(`${API}/api/auth/signup`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: signupForm.name.trim(),
          phone: signupForm.phone.trim(),
          email: signupForm.email.trim(),
          password: signupForm.password,
          location: signupForm.location.trim(),
          role: signupForm.role,
          organization_name:
            signupForm.organization_name.trim() || undefined,
          organization_type:
            signupForm.role === "blood_bank"
              ? "Blood Bank"
              : signupForm.organization_type,
          organization_address:
            signupForm.organization_address.trim() || undefined,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.message || data.error || "Unable to create account."
        );
      }

      showMessage(
        signupForm.role === "ngo" ||
          signupForm.role === "blood_bank"
          ? "Account created. Your organization will be reviewed by an administrator."
          : "Account created successfully. You can now login."
      );

      setAuthMode("login");

      setLoginForm({
        email: signupForm.email,
        password: "",
      });

      setSignupForm({
        name: "",
        phone: "",
        email: "",
        password: "",
        location: "",
        role: "user",
        organization_name: "",
        organization_type: "NGO",
        organization_address: "",
      });
    } catch (error) {
      showMessage(
        error.message || "Unable to create account.",
        "error"
      );
    } finally {
      setLoading(false);
    }
  }

  async function handleDonationSubmit(event) {
    event.preventDefault();

    if (!donationForm.item_name.trim()) {
      showMessage("Please enter the item name.", "error");
      return;
    }

    if (!donationForm.quantity || Number(donationForm.quantity) <= 0) {
      showMessage("Please enter a valid quantity.", "error");
      return;
    }

    setLoading(true);

    try {
      const formData = new FormData();

      Object.entries(donationForm).forEach(([key, value]) => {
        formData.append(key, value);
      });

      const response = await fetch(`${API}/api/donations`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.message || data.error || "Unable to create donation."
        );
      }

      setDonationForm({
        category: "Clothes",
        item_name: "",
        quantity: "1",
        condition: "Good",
        description: "",
        location: user?.location || "",
        donation_type: "item",
        target_type: "person",
      });

      setActivePage("home");
      setDonationCount((count) => count + 1);

      showMessage(
        "Donation created successfully. Thank you for making an impact."
      );
    } catch (error) {
      showMessage(
        error.message || "Unable to create donation.",
        "error"
      );
    } finally {
      setLoading(false);
    }
  }

  function logout() {
    localStorage.removeItem("resqlink_user");
    localStorage.removeItem("resqlink_token");

    setUser(null);
    setToken("");
    setActivePage("home");
    setMobileMenuOpen(false);

    showMessage("You have been logged out.");
  }

  function navigate(page) {
    setActivePage(page);
    setMobileMenuOpen(false);
  }

  function selectRole(role) {
    setSignupForm((previous) => ({
      ...previous,
      role,
      organization_name:
        role === "user" || role === "volunteer"
          ? ""
          : previous.organization_name,
    }));
  }

  if (!isLoggedIn) {
    return (
      <AuthScreen
        authMode={authMode}
        setAuthMode={setAuthMode}
        loginForm={loginForm}
        signupForm={signupForm}
        loading={loading}
        message={message}
        messageType={messageType}
        handleLoginChange={handleLoginChange}
        handleSignupChange={handleSignupChange}
        handleLogin={handleLogin}
        handleSignup={handleSignup}
        selectRole={selectRole}
      />
    );
  }

  if (user.role === "volunteer") {
    return (
      <Volunteer
        user={user}
        token={token}
        onLogout={logout}
      />
    );
  }

  if (user.role === "ngo") {
    return (
      <NGO
        user={user}
        token={token}
        onLogout={logout}
      />
    );
  }

  if (user.role === "blood_bank") {
    return (
      <BloodBank
        user={user}
        token={token}
        onLogout={logout}
      />
    );
  }

  if (user.role === "admin") {
    return (
      <Admin
        user={user}
        token={token}
        onLogout={logout}
      />
    );
  }

  return (
    <div className="resqlink-app">
      <Sidebar
        activePage={activePage}
        navigate={navigate}
        user={user}
        mobileMenuOpen={mobileMenuOpen}
        setMobileMenuOpen={setMobileMenuOpen}
        logout={logout}
      />

      <div className="dashboard-shell">
        <Topbar
          user={user}
          roleLabel={roleLabel}
          mobileMenuOpen={mobileMenuOpen}
          setMobileMenuOpen={setMobileMenuOpen}
          navigate={navigate}
          logout={logout}
        />

        <main className="dashboard-content">
          {message && (
            <Toast
              message={message}
              type={messageType}
            />
          )}

          {activePage === "home" && (
            <HomeDashboard
              user={user}
              donationCount={donationCount}
              requestCount={requestCount}
              completedCount={completedCount}
              requirements={requirements}
              organizations={organizations}
              navigate={navigate}
            />
          )}

          {activePage === "donate" && (
            <DonationPage
              user={user}
              donationForm={donationForm}
              handleDonationChange={handleDonationChange}
              handleDonationSubmit={handleDonationSubmit}
              loading={loading}
              navigate={navigate}
            />
          )}

          {activePage === "receive" && (
            <ReceivePage
              requirements={requirements}
              navigate={navigate}
            />
          )}

          {activePage === "organizations" && (
            <OrganizationsPage
              organizations={organizations}
              navigate={navigate}
            />
          )}

          {activePage === "blood-banks" && (
            <BloodBanksPage navigate={navigate} />
          )}

          {activePage === "donations" && (
            <SimpleListPage
              title="My Donations"
              subtitle="Track the resources you have shared with the community."
              icon="🎁"
              emptyText="Your donations will appear here."
            />
          )}

          {activePage === "requests" && (
            <SimpleListPage
              title="My Requests"
              subtitle="Keep track of resources you have requested."
              icon="📋"
              emptyText="Your requests will appear here."
            />
          )}

          {activePage === "volunteer" && (
            <VolunteerInfoPage navigate={navigate} />
          )}

          {activePage === "notifications" && (
            <NotificationsPage navigate={navigate} />
          )}

          {activePage === "settings" && (
            <SettingsPage user={user} navigate={navigate} />
          )}

          {activePage === "profile" && (
            <ProfilePage user={user} navigate={navigate} />
          )}
        </main>
      </div>
    </div>
  );
}

/* =========================================================
   AUTH SCREEN
========================================================= */

function AuthScreen({
  authMode,
  setAuthMode,
  loginForm,
  signupForm,
  loading,
  message,
  messageType,
  handleLoginChange,
  handleSignupChange,
  handleLogin,
  handleSignup,
  selectRole,
}) {
  return (
    <div className="auth-page">
      <div className="auth-card">
        <AuthBrandPanel />

        <section className="auth-form-panel">
          <div className="auth-top-link">
            {authMode === "login"
              ? "Don't have an account?"
              : "Already have an account?"}{" "}
            <button
              type="button"
              onClick={() =>
                setAuthMode(
                  authMode === "login" ? "signup" : "login"
                )
              }
              className="text-button"
            >
              {authMode === "login" ? "Sign Up" : "Login"}
            </button>
          </div>

          <div className="auth-heading">
            <div className="auth-heading-icon">
              {authMode === "login" ? "👤" : "👥"}
            </div>

            <div>
              <div className="auth-brand-small">ResQLink</div>

              <h1>
                {authMode === "login"
                  ? "Welcome Back"
                  : "Create Your Account"}
              </h1>

              <p>
                {authMode === "login"
                  ? "Login to continue making a difference."
                  : "Join our community and help resources reach the right hands."}
              </p>
            </div>
          </div>

          <div className="auth-tabs">
            <button
              type="button"
              className={authMode === "login" ? "active" : ""}
              onClick={() => setAuthMode("login")}
            >
              Login
            </button>

            <button
              type="button"
              className={authMode === "signup" ? "active" : ""}
              onClick={() => setAuthMode("signup")}
            >
              Sign Up
            </button>
          </div>

          {message && (
            <Toast
              message={message}
              type={messageType}
            />
          )}

          {authMode === "login" ? (
            <form
              className="auth-form"
              onSubmit={handleLogin}
            >
              <Field
                label="Email Address"
                name="email"
                type="email"
                placeholder="you@example.com"
                value={loginForm.email}
                onChange={handleLoginChange}
                icon="✉"
              />

              <Field
                label="Password"
                name="password"
                type="password"
                placeholder="Enter your password"
                value={loginForm.password}
                onChange={handleLoginChange}
                icon="🔒"
              />

              <div className="forgot-row">
                <span />
                <button
                  type="button"
                  className="text-button small"
                  onClick={() =>
                    alert(
                      "Password reset can be connected to email service later."
                    )
                  }
                >
                  Forgot password?
                </button>
              </div>

              <button
                className="primary-button full"
                disabled={loading}
                type="submit"
              >
                {loading ? "Logging in..." : "Login to ResQLink →"}
              </button>

              <div className="demo-login">
                <strong>Demo Admin</strong>
                <span>admin@resqlink.com</span>
                <span>Admin@123</span>
              </div>
            </form>
          ) : (
            <form
              className="auth-form"
              onSubmit={handleSignup}
            >
              <div className="form-grid two">
                <Field
                  label="Full Name"
                  name="name"
                  type="text"
                  placeholder="Your full name"
                  value={signupForm.name}
                  onChange={handleSignupChange}
                  icon="👤"
                />

                <Field
                  label="Mobile Number"
                  name="phone"
                  type="tel"
                  placeholder="Your mobile number"
                  value={signupForm.phone}
                  onChange={handleSignupChange}
                  icon="☎"
                />
              </div>

              <Field
                label="Email Address"
                name="email"
                type="email"
                placeholder="you@example.com"
                value={signupForm.email}
                onChange={handleSignupChange}
                icon="✉"
              />

              <Field
                label="Password"
                name="password"
                type="password"
                placeholder="Create a secure password"
                value={signupForm.password}
                onChange={handleSignupChange}
                icon="🔒"
              />

              <Field
                label="Current Location"
                name="location"
                type="text"
                placeholder="City, State"
                value={signupForm.location}
                onChange={handleSignupChange}
                icon="📍"
              />

              <RoleSelector
                role={signupForm.role}
                selectRole={selectRole}
              />

              {(signupForm.role === "ngo" ||
                signupForm.role === "blood_bank") && (
                <div className="organization-fields">
                  <div className="section-label">
                    Organization Information
                  </div>

                  <Field
                    label="Organization Name"
                    name="organization_name"
                    type="text"
                    placeholder={
                      signupForm.role === "blood_bank"
                        ? "Blood bank name"
                        : "NGO / Ashram name"
                    }
                    value={signupForm.organization_name}
                    onChange={handleSignupChange}
                    icon="🏢"
                  />

                  <div className="form-grid two">
                    <SelectField
                      label="Organization Type"
                      name="organization_type"
                      value={signupForm.organization_type}
                      onChange={handleSignupChange}
                      options={[
                        "NGO",
                        "Ashram",
                        "Community Organization",
                        "Trust",
                      ]}
                    />

                    <Field
                      label="Organization Address"
                      name="organization_address"
                      type="text"
                      placeholder="Address"
                      value={signupForm.organization_address}
                      onChange={handleSignupChange}
                      icon="📍"
                    />
                  </div>
                </div>
              )}

              <button
                className="primary-button full"
                disabled={loading}
                type="submit"
              >
                {loading ? "Creating account..." : "Create Account →"}
              </button>

              <div className="auth-note">
                <span>🔐</span>
                <p>
                  Your information is used only to create and manage
                  your ResQLink account.
                </p>
              </div>
            </form>
          )}
        </section>
      </div>
    </div>
  );
}

function AuthBrandPanel() {
  return (
    <section className="auth-brand-panel">
      <div className="brand-logo-row">
        <div className="brand-mark">♥</div>

        <div>
          <div className="brand-name">ResQLink</div>
          <div className="brand-tagline">
            Donate&nbsp; • &nbsp;Connect&nbsp; • &nbsp;Create Impact
          </div>
        </div>
      </div>

      <div className="brand-main-copy">
        <span className="brand-emoji">🤝</span>

        <h2>
          Give what you
          <br />
          don't need.
        </h2>

        <h3>Someone needs it.</h3>

        <p>
          A platform that connects donors with people in need,
          NGOs, ashrams and blood banks.
        </p>
      </div>

      <div className="impact-list">
        <div>
          <span>🎁</span>
          <strong>Donate</strong> items
        </div>

        <div>
          <span>👥</span>
          <strong>Help</strong> people
        </div>

        <div>
          <span>🏢</span>
          <strong>Support</strong> NGOs & Ashrams
        </div>

        <div>
          <span>🩸</span>
          <strong>Save</strong> lives
        </div>

        <div>
          <span>🌱</span>
          <strong>Build</strong> a better tomorrow
        </div>
      </div>

      <div className="brand-footer">
        Together we can make a difference <span>♡</span>
      </div>
    </section>
  );
}

function RoleSelector({ role, selectRole }) {
  const roles = [
    {
      value: "user",
      icon: "👤",
      title: "Normal User",
      description: "Donate & receive items",
    },
    {
      value: "volunteer",
      icon: "👥",
      title: "Volunteer",
      description: "Help with pickup & delivery",
    },
    {
      value: "ngo",
      icon: "🏢",
      title: "NGO / Ashram",
      description: "Manage donations & requirements",
    },
    {
      value: "blood_bank",
      icon: "🩸",
      title: "Blood Bank",
      description: "Manage blood requests & donors",
    },
  ];

  return (
    <div className="role-section">
      <div className="section-label">
        Select Your Role
        <span>Choose how you want to use the platform.</span>
      </div>

      <div className="role-grid">
        {roles.map((item) => (
          <button
            type="button"
            key={item.value}
            className={`role-card ${
              role === item.value ? "selected" : ""
            }`}
            onClick={() => selectRole(item.value)}
          >
            <span className="role-icon">{item.icon}</span>

            <span className="role-content">
              <strong>{item.title}</strong>
              <small>{item.description}</small>
            </span>

            {role === item.value && (
              <span className="role-check">✓</span>
            )}
          </button>
        ))}
      </div>

      <div className="admin-info">
        <span>🛡️</span>
        <span>
          Administrator access is securely provisioned and is not
          available through public signup.
        </span>
      </div>
    </div>
  );
}

/* =========================================================
   DASHBOARD LAYOUT
========================================================= */

function Sidebar({
  activePage,
  navigate,
  user,
  mobileMenuOpen,
  setMobileMenuOpen,
  logout,
}) {
  const menuGroups = [
    {
      title: "MAIN MENU",
      items: [
        { id: "home", icon: "⌂", label: "Home" },
        { id: "donate", icon: "🎁", label: "Donate" },
        { id: "receive", icon: "⌕", label: "Receive" },
        { id: "donations", icon: "📦", label: "My Donations" },
        { id: "requests", icon: "📋", label: "My Requests" },
      ],
    },
    {
      title: "COMMUNITY",
      items: [
        { id: "volunteer", icon: "🤝", label: "Volunteer" },
        {
          id: "organizations",
          icon: "🏢",
          label: "Organizations",
        },
        {
          id: "blood-banks",
          icon: "🩸",
          label: "Blood Banks",
        },
      ],
    },
    {
      title: "ACCOUNT",
      items: [
        {
          id: "notifications",
          icon: "🔔",
          label: "Notifications",
          badge: "3",
        },
        { id: "profile", icon: "♙", label: "Profile" },
        { id: "settings", icon: "⚙", label: "Settings" },
      ],
    },
  ];

  return (
    <>
      <button
        type="button"
        className="mobile-sidebar-backdrop"
        aria-label="Close menu"
        onClick={() => setMobileMenuOpen(false)}
      />

      <aside
        className={`sidebar ${
          mobileMenuOpen ? "mobile-open" : ""
        }`}
      >
        <div className="sidebar-brand">
          <div className="sidebar-logo">♥</div>

          <div>
            <div className="sidebar-brand-name">ResQLink</div>
            <div className="sidebar-brand-subtitle">
              Community Resource Network
            </div>
          </div>

          <button
            type="button"
            className="mobile-close-button"
            onClick={() => setMobileMenuOpen(false)}
          >
            ×
          </button>
        </div>

        <div className="sidebar-user">
          <div className="sidebar-avatar">
            {getInitials(user?.name)}
          </div>

          <div className="sidebar-user-info">
            <strong>{user?.name || "Community Member"}</strong>
            <span>{ROLE_LABELS[user?.role] || "Member"}</span>
          </div>

          <span className="verified-dot">✓</span>
        </div>

        <nav className="sidebar-navigation">
          {menuGroups.map((group) => (
            <div
              className="nav-group"
              key={group.title}
            >
              <div className="nav-group-title">
                {group.title}
              </div>

              {group.items.map((item) => (
                <button
                  type="button"
                  key={item.id}
                  className={`nav-item ${
                    activePage === item.id ? "active" : ""
                  }`}
                  onClick={() => navigate(item.id)}
                >
                  <span className="nav-icon">{item.icon}</span>

                  <span>{item.label}</span>

                  {item.badge && (
                    <span className="nav-badge">
                      {item.badge}
                    </span>
                  )}
                </button>
              ))}
            </div>
          ))}
        </nav>

        <div className="sidebar-impact">
          <div className="impact-decoration">🌿</div>
          <strong>Every action counts.</strong>
          <span>
            Be the reason someone gets what they need.
          </span>
        </div>

        <button
          type="button"
          className="sidebar-logout"
          onClick={logout}
        >
          <span>↪</span>
          Logout
        </button>
      </aside>
    </>
  );
}

function Topbar({
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
}

/* =========================================================
   HOME DASHBOARD
========================================================= */

function HomeDashboard({
  user,
  donationCount,
  requestCount,
  completedCount,
  requirements,
  organizations,
  navigate,
}) {
  const visibleRequirements =
    requirements.length > 0
      ? requirements.slice(0, 3)
      : SAMPLE_NEEDS;

  const visibleOrganizations =
    organizations.length > 0
      ? organizations.slice(0, 3)
      : SAMPLE_ORGANIZATIONS;

  return (
    <>
      <div className="page-heading-row">
        <div>
          <div className="breadcrumb">
            ResQLink <span>/</span> Home
          </div>

          <h1>Welcome back, {user?.name || "there"} 👋</h1>

          <p>
            Every donation can become someone's opportunity.
            Let's make resources reach the right hands.
          </p>
        </div>

        <div className="verified-profile-pill">
          <span>✓</span>
          Verified Member
        </div>
      </div>

      <section className="dashboard-hero">
        <div className="hero-copy">
          <span className="hero-eyebrow">
            MAKE AN IMPACT
          </span>

          <h2>
            Give what you
            <br />
            don't need.
          </h2>

          <p>
            Someone needs it. Your unused resources can become
            another person's opportunity.
          </p>

          <div className="hero-actions">
            <button
              type="button"
              className="primary-button"
              onClick={() => navigate("donate")}
            >
              🎁 Donate an Item
            </button>

            <button
              type="button"
              className="secondary-button"
              onClick={() => navigate("receive")}
            >
              ⌕ Find Resources
            </button>
          </div>
        </div>

        <div className="hero-visual">
          <div className="hero-box">
            <span>📦</span>
            <span>♥</span>
          </div>

          <div className="hero-hand hero-hand-one">🤲</div>
          <div className="hero-hand hero-hand-two">🤲</div>
        </div>
      </section>

      <section className="stats-grid">
        <StatCard
          icon="🎁"
          label="My Donations"
          value={donationCount}
          description="Items shared"
          tone="green"
        />

        <StatCard
          icon="⌕"
          label="My Requests"
          value={requestCount}
          description="Resources requested"
          tone="blue"
        />

        <StatCard
          icon="🤝"
          label="Completed"
          value={completedCount}
          description="Successful connections"
          tone="purple"
        />

        <StatCard
          icon="♥"
          label="People Helped"
          value={completedCount}
          description="Community impact"
          tone="rose"
        />
      </section>

      <section className="content-section">
        <SectionHeader
          title="Quick Actions"
          subtitle="What would you like to do today?"
        />

        <div className="quick-actions-grid">
          <QuickAction
            icon="🎁"
            title="Donate"
            description="Share items you no longer need."
            tone="green"
            onClick={() => navigate("donate")}
          />

          <QuickAction
            icon="⌕"
            title="Receive"
            description="Find resources available near you."
            tone="blue"
            onClick={() => navigate("receive")}
          />

          <QuickAction
            icon="🤝"
            title="Volunteer"
            description="Help with pickups and deliveries."
            tone="purple"
            onClick={() => navigate("volunteer")}
          />

          <QuickAction
            icon="🏢"
            title="Support Organizations"
            description="Discover verified NGOs and ashrams."
            tone="orange"
            onClick={() => navigate("organizations")}
          />
        </div>
      </section>

      <div className="dashboard-two-column">
        <section className="content-section">
          <SectionHeader
            title="Needs Near You"
            subtitle="People and organizations who need support"
            action="View all →"
            onAction={() => navigate("receive")}
          />

          <div className="needs-list">
            {visibleRequirements.map((item, index) => {
              const fallback = SAMPLE_NEEDS[index];

              return (
                <NeedCard
                  key={item.id || `${item.item_name}-${index}`}
                  item={{
                    ...fallback,
                    title:
                      item.item_name ||
                      fallback?.title ||
                      "Community Requirement",
                    need: item.quantity_required
                      ? `${item.quantity_required} units`
                      : fallback?.need,
                    organization:
                      item.organization_name ||
                      fallback?.organization,
                    status:
                      item.priority === "urgent"
                        ? "Urgent"
                        : fallback?.status || "Open",
                    statusClass:
                      item.priority === "urgent"
                        ? "urgent"
                        : "open",
                  }}
                  onDonate={() => navigate("donate")}
                />
              );
            })}
          </div>
        </section>

        <section className="content-section">
          <SectionHeader
            title="Verified Organizations"
            subtitle="Trusted organizations on ResQLink"
            action="View all →"
            onAction={() => navigate("organizations")}
          />

          <div className="organization-mini-list">
            {visibleOrganizations.map((organization, index) => {
              const fallback = SAMPLE_ORGANIZATIONS[index];

              return (
                <div
                  className="organization-mini-card"
                  key={
                    organization.id ||
                    organization.user_id ||
                    index
                  }
                >
                  <div className="organization-mini-icon">
                    {fallback?.icon || "🏢"}
                  </div>

                  <div className="organization-mini-content">
                    <strong>
                      {organization.organization_name ||
                        organization.name ||
                        fallback?.name ||
                        "Verified Organization"}
                    </strong>

                    <span>
                      {organization.organization_type ||
                        organization.type ||
                        fallback?.type ||
                        "Community Support"}
                    </span>
                  </div>

                  <span className="verified-check">✓</span>
                </div>
              );
            })}
          </div>

          <div className="impact-card">
            <span className="impact-card-icon">🌿</span>
            <div>
              <strong>Every donation counts.</strong>
              <p>
                Be the reason someone smiles today.
              </p>
            </div>
            <span className="impact-card-heart">♥</span>
          </div>
        </section>
      </div>

      <section className="content-section recent-section">
        <SectionHeader
          title="Recent Donations / Requests"
          subtitle="Your latest activity"
          action="View all →"
          onAction={() => navigate("donations")}
        />

        <div className="activity-table">
          <div className="activity-table-head">
            <span>Item</span>
            <span>Type</span>
            <span>Quantity</span>
            <span>Status</span>
            <span>Date</span>
            <span />
          </div>

          <ActivityRow
            icon="👕"
            item="Your donation activity"
            type="Donation"
            quantity={donationCount}
            status={donationCount > 0 ? "Available" : "No activity"}
            statusClass="available"
            date="Today"
          />

          <ActivityRow
            icon="📋"
            item="Community requests"
            type="Request"
            quantity={requestCount}
            status={requestCount > 0 ? "Pending" : "No activity"}
            statusClass="pending"
            date="—"
          />

          <ActivityRow
            icon="🤝"
            item="Completed connections"
            type="Impact"
            quantity={completedCount}
            status={completedCount > 0 ? "Completed" : "Getting started"}
            statusClass="completed"
            date="—"
          />
        </div>
      </section>
    </>
  );
}

/* =========================================================
   DONATION PAGE
========================================================= */

function DonationPage({
  user,
  donationForm,
  handleDonationChange,
  handleDonationSubmit,
  loading,
  navigate,
}) {
  return (
    <div className="inner-page">
      <div className="page-heading-row">
        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
          <button
            type="button"
            onClick={() => navigate("home")}
            style={{
              background: "none",
              border: "1.5px solid #cbd5e1",
              borderRadius: "8px",
              padding: "8px 12px",
              cursor: "pointer",
              fontSize: "18px",
              color: "#475569",
              display: "flex",
              alignItems: "center",
              gap: "6px",
              fontWeight: 600,
              transition: "all 0.2s"
            }}
            title="Go back"
          >
            ← Back
          </button>
          <div>
            <div className="breadcrumb">
              ResQLink <span>/</span> Donate
            </div>

            <h1>Donate an Item</h1>

            <p>
              Turn something you no longer need into something
              meaningful for someone else.
            </p>
          </div>
        </div>
      </div>

      <div className="donation-layout">
        <section className="form-card large">
          <div className="card-heading">
            <div className="card-heading-icon green">
              🎁
            </div>

            <div>
              <h2>Donation Details</h2>
              <p>
                Provide a few details so we can connect your
                donation with the right recipient.
              </p>
            </div>
          </div>

          <form
            className="dashboard-form"
            onSubmit={handleDonationSubmit}
          >
            <div className="form-grid two">
              <SelectField
                label="Category"
                name="category"
                value={donationForm.category}
                onChange={handleDonationChange}
                options={[
                  "Clothes",
                  "Books",
                  "Food",
                  "Furniture",
                  "Electronics",
                  "Education",
                  "Household",
                  "Others",
                ]}
              />

              <Field
                label="Item Name"
                name="item_name"
                type="text"
                placeholder="e.g. Winter jackets"
                value={donationForm.item_name}
                onChange={handleDonationChange}
              />
            </div>

            <div className="form-grid three">
              <Field
                label="Quantity"
                name="quantity"
                type="number"
                min="1"
                placeholder="1"
                value={donationForm.quantity}
                onChange={handleDonationChange}
              />

              <SelectField
                label="Condition"
                name="condition"
                value={donationForm.condition}
                onChange={handleDonationChange}
                options={[
                  "New",
                  "Like New",
                  "Good",
                  "Usable",
                ]}
              />

              <SelectField
                label="Donation Type"
                name="donation_type"
                value={donationForm.donation_type}
                onChange={handleDonationChange}
                options={["item", "bulk"]}
              />
            </div>

            <SelectField
              label="Who would you like to support?"
              name="target_type"
              value={donationForm.target_type}
              onChange={handleDonationChange}
              options={[
                "person",
                "ngo",
                "ashram",
              ]}
            />

            <Field
              label="Location"
              name="location"
              type="text"
              placeholder="City or pickup location"
              value={
                donationForm.location ||
                user?.location ||
                ""
              }
              onChange={handleDonationChange}
              icon="📍"
            />

            <TextAreaField
              label="Description"
              name="description"
              placeholder="Add useful details about the item..."
              value={donationForm.description}
              onChange={handleDonationChange}
            />

            <div className="form-field" style={{ marginTop: "8px" }}>
              <label style={{ fontWeight: 600, fontSize: "14px", color: "#374151", display: "block", marginBottom: "6px" }}>
                📷 Upload Photo <span style={{ fontWeight: 400, color: "#9ca3af" }}>(optional)</span>
              </label>
              <div
                style={{
                  border: "2px dashed #cbd5e1",
                  borderRadius: "12px",
                  padding: "24px",
                  textAlign: "center",
                  cursor: "pointer",
                  backgroundColor: "#f8fafc",
                  transition: "all 0.2s"
                }}
                onClick={() => document.getElementById("donation-photo-input").click()}
                onDragOver={(e) => { e.preventDefault(); e.currentTarget.style.borderColor = "#0d9488"; e.currentTarget.style.backgroundColor = "#f0fdfa"; }}
                onDragLeave={(e) => { e.currentTarget.style.borderColor = "#cbd5e1"; e.currentTarget.style.backgroundColor = "#f8fafc"; }}
              >
                <input
                  id="donation-photo-input"
                  type="file"
                  accept="image/*"
                  style={{ display: "none" }}
                  onChange={(e) => {
                    const file = e.target.files[0];
                    if (file) {
                      const reader = new FileReader();
                      reader.onload = (ev) => {
                        const preview = document.getElementById("donation-photo-preview");
                        if (preview) {
                          preview.src = ev.target.result;
                          preview.style.display = "block";
                          document.getElementById("donation-photo-placeholder").style.display = "none";
                        }
                      };
                      reader.readAsDataURL(file);
                    }
                  }}
                />
                <div id="donation-photo-placeholder">
                  <div style={{ fontSize: "32px", marginBottom: "8px" }}>📷</div>
                  <p style={{ color: "#64748b", fontSize: "14px", margin: 0 }}>
                    Click or drag &amp; drop to upload a photo
                  </p>
                  <p style={{ color: "#9ca3af", fontSize: "12px", margin: "4px 0 0" }}>
                    PNG, JPG, WEBP up to 5MB
                  </p>
                </div>
                <img
                  id="donation-photo-preview"
                  alt="preview"
                  style={{
                    display: "none",
                    maxWidth: "100%",
                    maxHeight: "200px",
                    borderRadius: "8px",
                    objectFit: "cover"
                  }}
                />
              </div>
            </div>

            <div className="form-actions">
              <button
                type="button"
                className="secondary-button"
                onClick={() => navigate("home")}
              >
                Cancel
              </button>

              <button
                type="submit"
                className="primary-button"
                disabled={loading}
              >
                {loading
                  ? "Creating donation..."
                  : "Create Donation →"}
              </button>
            </div>
          </form>
        </section>

        <aside className="donation-info-card">
          <div className="donation-illustration">
            📦
          </div>

          <h3>Small things can make a big difference.</h3>

          <p>
            Your usable items can support families, students,
            NGOs and communities.
          </p>

          <div className="donation-check-list">
            <div>
              <span>✓</span>
              Describe the item honestly
            </div>

            <div>
              <span>✓</span>
              Mention the quantity clearly
            </div>

            <div>
              <span>✓</span>
              Add an accurate location
            </div>

            <div>
              <span>✓</span>
              Keep donated items usable
            </div>
          </div>
        </aside>
      </div>
    </div>
  );
}

/* =========================================================
   RECEIVE
========================================================= */

function ReceivePage({
  requirements,
  navigate,
}) {
  const [activeFilter, setActiveFilter] = React.useState("All");
  const [selectedResource, setSelectedResource] = React.useState(null);
  const filters = ["All", "Clothes", "Books", "Food", "Education"];

  const allItems =
    requirements.length > 0
      ? requirements
      : SAMPLE_NEEDS;

  const items = activeFilter === "All"
    ? allItems
    : allItems.filter((item) => {
        const name = (item.item_name || item.title || "").toLowerCase();
        const cat = (item.category || "").toLowerCase();
        const filterLower = activeFilter.toLowerCase();
        return name.includes(filterLower) || cat.includes(filterLower);
      });

  return (
    <div className="inner-page">
      <div className="page-heading-row">
        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
          <button
            type="button"
            onClick={() => typeof navigate === "function" && navigate("home")}
            style={{
              background: "none",
              border: "1.5px solid #cbd5e1",
              borderRadius: "8px",
              padding: "8px 12px",
              cursor: "pointer",
              fontSize: "18px",
              color: "#475569",
              display: "flex",
              alignItems: "center",
              gap: "6px",
              fontWeight: 600,
              transition: "all 0.2s"
            }}
            title="Go back"
          >
            \u2190 Back
          </button>
          <div>
            <div className="breadcrumb">
              ResQLink <span>/</span> Receive
            </div>
            <h1>Find Resources</h1>
            <p>
              Explore community requirements and resources
              available through ResQLink.
            </p>
          </div>
        </div>

        <button
          type="button"
          className="primary-button"
          onClick={() => navigate("donate")}
        >
          \U0001f381 Donate
        </button>
      </div>

      <div className="filter-row">
        {filters.map((f) => (
          <button
            key={f}
            type="button"
            className={`filter-chip ${activeFilter === f ? "active" : ""}`}
            onClick={() => setActiveFilter(f)}
          >
            {f}
          </button>
        ))}
      </div>

      <div className="organization-grid">
        {items.length === 0 ? (
          <div className="empty-state-card" style={{ gridColumn: "1 / -1" }}>
            <div className="empty-state-icon">&#128269;</div>
            <h2>No resources found for "{activeFilter}"</h2>
            <p>Try selecting a different category or check back later.</p>
          </div>
        ) : items.map((item, index) => {
          const fallback = SAMPLE_NEEDS[index % SAMPLE_NEEDS.length];
          const title = item.item_name || item.title || fallback.title;
          const org = item.organization_name || item.organization || fallback.organization || "Community";
          const qty = item.quantity_required || fallback.need;
          const loc = item.location || fallback.location;
          const type = item.organization_type || item.type || fallback.type;
          const isUrgent = item.priority === "urgent";

          return (
            <article className="organization-card" key={item.id || index}>
              <div
                className="organization-cover"
                style={{
                  background: isUrgent
                    ? "linear-gradient(135deg, #b33a1a, #8b2d14)"
                    : "linear-gradient(135deg, #147d63, #0e5f4d)"
                }}
              >
                <span style={{ fontSize: "36px" }}>{fallback.icon}</span>
              </div>

              <div className="organization-card-body">
                <div className="organization-title-row">
                  <h3>{title}</h3>
                  <span
                    style={{
                      fontSize: "11px",
                      fontWeight: 700,
                      padding: "3px 10px",
                      borderRadius: "20px",
                      background: isUrgent ? "#fef2f2" : "#f0fdf4",
                      color: isUrgent ? "#dc2626" : "#16a34a",
                      border: `1px solid ${isUrgent ? "#fecaca" : "#bbf7d0"}`,
                      whiteSpace: "nowrap"
                    }}
                  >
                    {isUrgent ? "\u26a1 Urgent" : "\u2713 Open"}
                  </span>
                </div>

                <p style={{ fontSize: "13px", color: "#4b5563", lineHeight: 1.5, margin: 0 }}>
                  {item.description || `Need support with ${title}.`}
                </p>

                <div className="organization-meta">
                  <span>&#127970; {type}</span>
                  <span>&#128205; {loc}</span>
                </div>

                <div style={{ paddingTop: "4px" }}>
                  <span style={{ fontSize: "12px", color: "#6b7f7a" }}>&#128230; {qty}</span>
                </div>

                <button
                  type="button"
                  style={{
                    width: "100%",
                    marginTop: "auto",
                    padding: "10px 0",
                    borderRadius: "10px",
                    border: "1.5px solid #147d63",
                    background: "transparent",
                    color: "#147d63",
                    fontWeight: 600,
                    fontSize: "14px",
                    cursor: "pointer",
                    transition: "all 0.2s"
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.background = "#147d63";
                    e.currentTarget.style.color = "#fff";
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.background = "transparent";
                    e.currentTarget.style.color = "#147d63";
                  }}
                  onClick={() =>
                    setSelectedResource({
                      title, org, qty, loc,
                      icon: fallback.icon, type,
                      priority: item.priority,
                      description: item.description || `Need support with ${title}.`
                    })
                  }
                >
                  View Details
                </button>
              </div>
            </article>
          );
        })}
      </div>

      {selectedResource && (
        <div className="modal-backdrop" onClick={() => setSelectedResource(null)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <div className="brand-logo-row">
                <span style={{ fontSize: "32px" }}>{selectedResource.icon}</span>
                <div>
                  <h3>{selectedResource.title}</h3>
                  <span className="verified-badge">
                    {selectedResource.type} &bull;{" "}
                    {selectedResource.priority === "urgent" ? "\u26a1 Urgent" : "\u2713 Open"}
                  </span>
                </div>
              </div>
              <button
                type="button"
                className="modal-close"
                onClick={() => setSelectedResource(null)}
              >
                &times;
              </button>
            </div>

            <div className="modal-body" style={{ display: "flex", flexDirection: "column", gap: "16px", marginTop: "16px" }}>
              <div>
                <strong style={{ fontSize: "12px", color: "#8fa39e", textTransform: "uppercase" }}>Organization</strong>
                <p style={{ marginTop: "4px", fontSize: "14px", color: "#173b35" }}>&#127970; {selectedResource.org}</p>
              </div>
              <div>
                <strong style={{ fontSize: "12px", color: "#8fa39e", textTransform: "uppercase" }}>Description</strong>
                <p style={{ marginTop: "4px", fontSize: "14px", color: "#173b35" }}>{selectedResource.description}</p>
              </div>
              <div>
                <strong style={{ fontSize: "12px", color: "#8fa39e", textTransform: "uppercase" }}>Quantity Required</strong>
                <p style={{ marginTop: "4px", fontSize: "14px", color: "#173b35" }}>&#128230; {selectedResource.qty}</p>
              </div>
              <div>
                <strong style={{ fontSize: "12px", color: "#8fa39e", textTransform: "uppercase" }}>Location</strong>
                <p style={{ marginTop: "4px", fontSize: "14px", color: "#173b35" }}>&#128205; {selectedResource.loc}</p>
              </div>
              <div style={{ background: "#f4faf7", padding: "16px", borderRadius: "12px", border: "1px solid #bce3d6" }}>
                <strong style={{ color: "#147d63", fontSize: "14px" }}>How to Help</strong>
                <p style={{ fontSize: "13px", color: "#2c594e", marginTop: "4px" }}>
                  Click "Donate Now" to share this resource with the organization. Your donation will be coordinated through ResQLink.
                </p>
              </div>
            </div>

            <div style={{ marginTop: "24px", display: "flex", gap: "12px" }}>
              <button
                type="button"
                className="primary-button full"
                onClick={() => { setSelectedResource(null); navigate("donate"); }}
              >
                Donate Now \u2192
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

/* =========================================================
   ORGANIZATIONS
========================================================= */

function OrganizationsPage({
  organizations,
  navigate,
}) {
  const [selectedOrg, setSelectedOrg] = useState(null);
  const items =
    organizations.length > 0
      ? organizations
      : SAMPLE_ORGANIZATIONS;

  return (
    <div className="inner-page">
      <div className="page-heading-row">
        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
          <button
            type="button"
            onClick={() => typeof navigate === "function" && navigate("home")}
            style={{
              background: "none",
              border: "1.5px solid #cbd5e1",
              borderRadius: "8px",
              padding: "8px 12px",
              cursor: "pointer",
              fontSize: "18px",
              color: "#475569",
              display: "flex",
              alignItems: "center",
              gap: "6px",
              fontWeight: 600,
              transition: "all 0.2s"
            }}
            title="Go back"
          >
            ← Back
          </button>
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
}

/* =========================================================
   BLOOD BANKS
========================================================= */

function BloodBanksPage({ navigate }) {
  const [selectedBank, setSelectedBank] = useState(null);

  const banks = [
    {
      name: "City Blood Bank",
      location: "Community blood service",
      groups: "A+, A−, B+, B−, O+, O−",
      icon: "🩸",
      address: "MG Road, Mysore, Karnataka 570001",
      phone: "+91 821-2424242",
      hours: "24/7 Emergency Services",
      services: ["Whole Blood", "Platelets", "Plasma", "Red Blood Cells"],
    },
    {
      name: "Red Cross Blood Bank",
      location: "Regional blood service",
      groups: "A+, B+, O+, AB+",
      icon: "🏥",
      address: "Sayyaji Rao Road, Mysore, Karnataka 570005",
      phone: "+91 821-2525252",
      hours: "Mon-Sat: 8AM - 8PM",
      services: ["Whole Blood", "Platelets", "Blood Group Testing"],
    },
  ];

  return (
    <div className="inner-page">
      <div className="page-heading-row">
        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
          <button
            type="button"
            onClick={() => typeof navigate === "function" && navigate("home")}
            style={{
              background: "none",
              border: "1.5px solid #cbd5e1",
              borderRadius: "8px",
              padding: "8px 12px",
              cursor: "pointer",
              fontSize: "18px",
              color: "#475569",
              display: "flex",
              alignItems: "center",
              gap: "6px",
              fontWeight: 600,
              transition: "all 0.2s"
            }}
            title="Go back"
          >
            ← Back
          </button>
          <div>
            <div className="breadcrumb">
              ResQLink <span>/</span> Blood Banks
            </div>

            <h1>Blood Bank Network</h1>

            <p>
              Find verified blood banks and view available
              coordination information.
            </p>
          </div>
        </div>
      </div>

      <div className="blood-safety-banner">
        <span>🩸</span>

        <div>
          <strong>Important</strong>
          <p>
            ResQLink supports coordination. Blood eligibility,
            compatibility and medical decisions remain with
            qualified medical professionals.
          </p>
        </div>
      </div>

      <div className="blood-bank-grid">
        {banks.map((bank) => (
          <article
            className="blood-bank-card"
            key={bank.name}
          >
            <div className="blood-bank-icon">
              {bank.icon}
            </div>

            <div>
              <div className="blood-bank-name-row">
                <h3>{bank.name}</h3>
                <span>✓</span>
              </div>

              <p>{bank.location}</p>

              <div className="blood-groups">
                {bank.groups}
              </div>
            </div>

            <button
              type="button"
              className="secondary-button"
              onClick={() => setSelectedBank(bank)}
            >
              View
            </button>
          </article>
        ))}
      </div>

      {selectedBank && (
        <div className="modal-backdrop" onClick={() => setSelectedBank(null)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <div className="brand-logo-row">
                <span style={{ fontSize: '32px' }}>{selectedBank.icon}</span>
                <div>
                  <h3>{selectedBank.name}</h3>
                  <span className="verified-badge">✓ Verified Blood Bank</span>
                </div>
              </div>
              <button type="button" className="modal-close" onClick={() => setSelectedBank(null)}>×</button>
            </div>

            <div className="modal-body" style={{ display: 'flex', flexDirection: 'column', gap: '16px', marginTop: '16px' }}>
              <div>
                <strong style={{ fontSize: '12px', color: '#8fa39e', textTransform: 'uppercase' }}>Available Blood Groups</strong>
                <p style={{ marginTop: '4px', fontSize: '14px', color: '#173b35' }}>🩸 {selectedBank.groups}</p>
              </div>

              <div>
                <strong style={{ fontSize: '12px', color: '#8fa39e', textTransform: 'uppercase' }}>Address</strong>
                <p style={{ marginTop: '4px', fontSize: '14px', color: '#173b35' }}>📍 {selectedBank.address}</p>
              </div>

              <div>
                <strong style={{ fontSize: '12px', color: '#8fa39e', textTransform: 'uppercase' }}>Contact</strong>
                <p style={{ marginTop: '4px', fontSize: '14px', color: '#173b35' }}>☎ {selectedBank.phone}</p>
              </div>

              <div>
                <strong style={{ fontSize: '12px', color: '#8fa39e', textTransform: 'uppercase' }}>Hours</strong>
                <p style={{ marginTop: '4px', fontSize: '14px', color: '#173b35' }}>⏰ {selectedBank.hours}</p>
              </div>

              <div style={{ background: '#fef6f4', padding: '16px', borderRadius: '12px', border: '1px solid #f0c4bc' }}>
                <strong style={{ color: '#b33a1a', fontSize: '14px' }}>Services Offered</strong>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginTop: '8px' }}>
                  {selectedBank.services.map((s) => (
                    <span key={s} style={{ background: '#fff0ed', color: '#b33a1a', padding: '4px 12px', borderRadius: '20px', fontSize: '13px' }}>{s}</span>
                  ))}
                </div>
              </div>
            </div>

            <div style={{ marginTop: '24px', display: 'flex', gap: '12px' }}>
              <button type="button" className="primary-button full" onClick={() => setSelectedBank(null)}>
                Contact Blood Bank →
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

/* =========================================================
   VOLUNTEER INFO
========================================================= */

function VolunteerInfoPage({
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
        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
          <button
            type="button"
            onClick={() => typeof navigate === "function" && navigate("home")}
            style={{
              background: "none",
              border: "1.5px solid #cbd5e1",
              borderRadius: "8px",
              padding: "8px 12px",
              cursor: "pointer",
              fontSize: "18px",
              color: "#475569",
              display: "flex",
              alignItems: "center",
              gap: "6px",
              fontWeight: 600,
              transition: "all 0.2s"
            }}
            title="Go back"
          >
            ← Back
          </button>
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
}


/* =========================================================
   SETTINGS / PROFILE
========================================================= */

function NotificationsPage({ navigate }) {
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

function SettingsPage({ user, navigate }) {
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
        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
          {navigate && (
            <button
              type="button"
              onClick={() => navigate("home")}
              style={{
                background: "none",
                border: "1.5px solid #cbd5e1",
                borderRadius: "8px",
                padding: "8px 12px",
                cursor: "pointer",
                fontSize: "18px",
                color: "#475569",
                display: "flex",
                alignItems: "center",
                gap: "6px",
                fontWeight: 600,
                transition: "all 0.2s"
              }}
              title="Go back"
            >
              ← Back
            </button>
          )}
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
        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
          {navigate && (
            <button
              type="button"
              onClick={() => navigate("home")}
              style={{
                background: "none",
                border: "1.5px solid #cbd5e1",
                borderRadius: "8px",
                padding: "8px 12px",
                cursor: "pointer",
                fontSize: "18px",
                color: "#475569",
                display: "flex",
                alignItems: "center",
                gap: "6px",
                fontWeight: 600,
                transition: "all 0.2s"
              }}
              title="Go back"
            >
              ← Back
            </button>
          )}
          <div>
            <div className="breadcrumb">
              ResQLink <span>/</span> Profile
            </div>

            <h1>Your Profile</h1>

            <p>
              Your ResQLink community identity and account information.
            </p>
          </div>
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
}

/* =========================================================
   GENERIC COMPONENTS
========================================================= */

function SectionHeader({
  title,
  subtitle,
  action,
  onAction,
}) {
  return (
    <div className="section-header">
      <div>
        <h2>{title}</h2>
        {subtitle && <p>{subtitle}</p>}
      </div>

      {action && (
        <button
          type="button"
          className="section-action"
          onClick={onAction}
        >
          {action}
        </button>
      )}
    </div>
  );
}

function StatCard({
  icon,
  label,
  value,
  description,
  tone,
}) {
  return (
    <div className={`stat-card ${tone}`}>
      <div className="stat-icon">
        {icon}
      </div>

      <div className="stat-content">
        <span>{label}</span>
        <strong>{value}</strong>
        <small>{description}</small>
      </div>
    </div>
  );
}

function QuickAction({
  icon,
  title,
  description,
  tone,
  onClick,
}) {
  return (
    <button
      type="button"
      className={`quick-action ${tone}`}
      onClick={onClick}
    >
      <span className="quick-action-icon">
        {icon}
      </span>

      <span className="quick-action-text">
        <strong>{title}</strong>
        <small>{description}</small>
      </span>

      <span className="quick-action-arrow">
        →
      </span>
    </button>
  );
}

function NeedCard({
  item,
  onDonate,
}) {
  return (
    <article className="need-card">
      <div className="need-image">
        {item.icon || "📦"}
      </div>

      <div className="need-main">
        <div className="need-topline">
          <span className="small-tag">
            {item.type || "Community"}
          </span>

          <span
            className={`status-pill ${item.statusClass}`}
          >
            {item.status}
          </span>
        </div>

        <h3>{item.organization}</h3>

        <p>
          Needs: <strong>{item.title}</strong>
        </p>

        <div className="need-meta">
          <span>📍 {item.location}</span>
          <span>✓ Verified</span>
        </div>
      </div>

      <div className="need-quantity">
        <span>They Need</span>
        <strong>{item.need}</strong>
      </div>

      <button
        type="button"
        className="small-primary-button"
        onClick={onDonate}
      >
        Donate
      </button>
    </article>
  );
}

function ActivityRow({
  icon,
  item,
  type,
  quantity,
  status,
  statusClass,
  date,
}) {
  return (
    <div className="activity-row">
      <div className="activity-item">
        <span>{icon}</span>
        <strong>{item}</strong>
      </div>

      <span className="activity-type">{type}</span>

      <span>{quantity}</span>

      <span
        className={`status-pill ${statusClass}`}
      >
        {status}
      </span>

      <span>{date}</span>

      <button
        type="button"
        className="table-view-button"
      >
        View
      </button>
    </div>
  );
}

function SimpleListPage({
  title,
  subtitle,
  icon,
  emptyText,
}) {
  return (
    <div className="inner-page">
      <div className="page-heading-row">
        <div>
          <div className="breadcrumb">
            ResQLink <span>/</span> {title}
          </div>

          <h1>{title}</h1>

          <p>{subtitle}</p>
        </div>
      </div>

      <div className="empty-state-card">
        <div className="empty-state-icon">
          {icon}
        </div>

        <h2>{emptyText}</h2>

        <p>
          Your activity will appear here as you use
          ResQLink.
        </p>
      </div>
    </div>
  );
}

function Field({
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
}


function SelectField({
  label,
  name,
  value,
  onChange,
  options,
}) {
  return (
    <label className="field">
      <span className="field-label">{label}</span>

      <span className="field-control select-control">
        <select
          name={name}
          value={value}
          onChange={onChange}
        >
          {options.map((option) => (
            <option
              value={option}
              key={option}
            >
              {option}
            </option>
          ))}
        </select>

        <span className="select-arrow">⌄</span>
      </span>
    </label>
  );
}

function TextAreaField({
  label,
  name,
  placeholder,
  value,
  onChange,
}) {
  return (
    <label className="field">
      <span className="field-label">{label}</span>

      <textarea
        name={name}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        rows="5"
      />
    </label>
  );
}

function Toast({
  message,
  type,
}) {
  return (
    <div className={`toast ${type || "success"}`}>
      <span>
        {type === "error" ? "!" : "✓"}
      </span>
      <p>{message}</p>
    </div>
  );
}

function getInitials(name) {
  if (!name) return "RL";

  const parts = name
    .trim()
    .split(/\s+/)
    .filter(Boolean);

  if (parts.length === 1) {
    return parts[0].slice(0, 2).toUpperCase();
  }

  return `${parts[0][0]}${parts[parts.length - 1][0]}`.toUpperCase();
}

export default App;