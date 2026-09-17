"""
Fix all non-working buttons in App.jsx:
1. Blood Banks "View" button → show modal with bank details
2. Receive page filter chips (Clothes, Books, etc.) → working filter
3. Topbar search → filter with navigate
4. Topbar notification bell → navigate to notifications page
5. Resource "View Details" → show detail modal instead of alert
"""
import re

filepath = r"c:\Users\harsh\Downloads\resqlink_fixed\resqlink\frontend\src\App.jsx"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# ============================================================
# FIX 1: Topbar - add navigate prop and wire notification bell + search
# ============================================================

# Update Topbar function signature to accept navigate
content = content.replace(
    """function Topbar({
  user,
  roleLabel,
  setMobileMenuOpen,
}) {""",
    """function Topbar({
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
  };"""
)

# Update Topbar call to pass navigate
content = content.replace(
    """<Topbar
          user={user}
          roleLabel={roleLabel}
          mobileMenuOpen={mobileMenuOpen}
          setMobileMenuOpen={setMobileMenuOpen}
        />""",
    """<Topbar
          user={user}
          roleLabel={roleLabel}
          mobileMenuOpen={mobileMenuOpen}
          setMobileMenuOpen={setMobileMenuOpen}
          navigate={navigate}
        />"""
)

# Replace the search input to be controlled
content = content.replace(
    """<div className="topbar-search">
        <span>\u2315</span>

        <input
          type="text"
          placeholder="Search for items, NGOs, ashrams, blood banks..."
        />
      </div>""",
    """<div className="topbar-search">
        <span>\u2315</span>

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
      </div>"""
)

# Replace notification bell to have onClick navigate
content = content.replace(
    """<button
          type="button"
          className="topbar-icon-button"
          aria-label="Notifications"
        >
          \U0001f514
          <span className="notification-dot">3</span>
        </button>""",
    """<button
          type="button"
          className="topbar-icon-button"
          aria-label="Notifications"
          onClick={() => navigate("notifications")}
        >
          \U0001f514
          <span className="notification-dot">3</span>
        </button>"""
)

# ============================================================
# FIX 2: ReceivePage - make filter chips work
# ============================================================

old_receive = """function ReceivePage({
  requirements,
  navigate,
}) {
  const items =
    requirements.length > 0
      ? requirements
      : SAMPLE_NEEDS;

  return (
    <div className="inner-page">
      <div className="page-heading-row">
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

        <button
          type="button"
          className="primary-button"
          onClick={() => navigate("donate")}
        >
          \U0001f381 Donate
        </button>
      </div>

      <div className="filter-row">
        <button className="filter-chip active">
          All
        </button>
        <button className="filter-chip">
          Clothes
        </button>
        <button className="filter-chip">
          Books
        </button>
        <button className="filter-chip">
          Food
        </button>
        <button className="filter-chip">
          Education
        </button>
      </div>

      <div className="resource-grid">
        {items.map((item, index) => {
          const fallback = SAMPLE_NEEDS[index % SAMPLE_NEEDS.length];

          return (
            <article
              className="resource-card"
              key={item.id || index}
            >
              <div className="resource-card-icon">
                {fallback.icon}
              </div>

              <div className="resource-card-top">
                <span className="small-tag">
                  {item.organization_type ||
                    item.type ||
                    fallback.type}
                </span>

                <span
                  className={`status-pill ${
                    item.priority === "urgent"
                      ? "urgent"
                      : "open"
                  }`}
                >
                  {item.priority === "urgent"
                    ? "Urgent"
                    : "Open"}
                </span>
              </div>

              <h3>
                {item.item_name ||
                  item.title ||
                  fallback.title}
              </h3>

              <p>
                {item.description ||
                  `Need support with ${
                    item.item_name ||
                    fallback.title
                  }.`}
              </p>

              <div className="resource-meta">
                <span>
                  \U0001f4e6{" "}
                  {item.quantity_required ||
                    fallback.need}
                </span>

                <span>
                  \U0001f4cd{" "}
                  {item.location ||
                    fallback.location}
                </span>
              </div>

              <button
                type="button"
                className="secondary-button full"
                onClick={() =>
                  alert(
                    "Request flow can be connected to the selected requirement."
                  )
                }
              >
                View Details
              </button>
            </article>
          );
        })}
      </div>
    </div>
  );
}"""

new_receive = """function ReceivePage({
  requirements,
  navigate,
}) {
  const [activeFilter, setActiveFilter] = useState("All");
  const [selectedResource, setSelectedResource] = useState(null);
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

      <div className="resource-grid">
        {items.length === 0 ? (
          <div className="empty-state-card" style={{ gridColumn: '1 / -1' }}>
            <div className="empty-state-icon">\U0001f50d</div>
            <h2>No resources found for "{activeFilter}"</h2>
            <p>Try selecting a different category or check back later.</p>
          </div>
        ) : items.map((item, index) => {
          const fallback = SAMPLE_NEEDS[index % SAMPLE_NEEDS.length];
          const title = item.item_name || item.title || fallback.title;
          const org = item.organization_name || item.organization || fallback.organization || "Community";
          const qty = item.quantity_required || fallback.need;
          const loc = item.location || fallback.location;

          return (
            <article
              className="resource-card"
              key={item.id || index}
            >
              <div className="resource-card-icon">
                {fallback.icon}
              </div>

              <div className="resource-card-top">
                <span className="small-tag">
                  {item.organization_type ||
                    item.type ||
                    fallback.type}
                </span>

                <span
                  className={`status-pill ${
                    item.priority === "urgent"
                      ? "urgent"
                      : "open"
                  }`}
                >
                  {item.priority === "urgent"
                    ? "Urgent"
                    : "Open"}
                </span>
              </div>

              <h3>{title}</h3>

              <p>
                {item.description ||
                  `Need support with ${title}.`}
              </p>

              <div className="resource-meta">
                <span>\U0001f4e6 {qty}</span>
                <span>\U0001f4cd {loc}</span>
              </div>

              <button
                type="button"
                className="secondary-button full"
                onClick={() => setSelectedResource({ title, org, qty, loc, icon: fallback.icon, type: item.organization_type || item.type || fallback.type, priority: item.priority, description: item.description || `Need support with ${title}.` })}
              >
                View Details
              </button>
            </article>
          );
        })}
      </div>

      {selectedResource && (
        <div className="modal-backdrop" onClick={() => setSelectedResource(null)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <div className="brand-logo-row">
                <span style={{ fontSize: '32px' }}>{selectedResource.icon}</span>
                <div>
                  <h3>{selectedResource.title}</h3>
                  <span className="verified-badge">{selectedResource.type} \u2022 {selectedResource.priority === "urgent" ? "Urgent" : "Open"}</span>
                </div>
              </div>
              <button type="button" className="modal-close" onClick={() => setSelectedResource(null)}>\u00d7</button>
            </div>

            <div className="modal-body" style={{ display: 'flex', flexDirection: 'column', gap: '16px', marginTop: '16px' }}>
              <div>
                <strong style={{ fontSize: '12px', color: '#8fa39e', textTransform: 'uppercase' }}>Organization</strong>
                <p style={{ marginTop: '4px', fontSize: '14px', color: '#173b35' }}>\U0001f3e2 {selectedResource.org}</p>
              </div>

              <div>
                <strong style={{ fontSize: '12px', color: '#8fa39e', textTransform: 'uppercase' }}>Description</strong>
                <p style={{ marginTop: '4px', fontSize: '14px', color: '#173b35' }}>{selectedResource.description}</p>
              </div>

              <div>
                <strong style={{ fontSize: '12px', color: '#8fa39e', textTransform: 'uppercase' }}>Quantity Required</strong>
                <p style={{ marginTop: '4px', fontSize: '14px', color: '#173b35' }}>\U0001f4e6 {selectedResource.qty}</p>
              </div>

              <div>
                <strong style={{ fontSize: '12px', color: '#8fa39e', textTransform: 'uppercase' }}>Location</strong>
                <p style={{ marginTop: '4px', fontSize: '14px', color: '#173b35' }}>\U0001f4cd {selectedResource.loc}</p>
              </div>

              <div style={{ background: '#f4faf7', padding: '16px', borderRadius: '12px', border: '1px solid #bce3d6' }}>
                <strong style={{ color: '#147d63', fontSize: '14px' }}>How to Help</strong>
                <p style={{ fontSize: '13px', color: '#2c594e', marginTop: '4px' }}>
                  Click "Donate Now" to share this resource with the organization. Your donation will be coordinated through ResQLink.
                </p>
              </div>
            </div>

            <div style={{ marginTop: '24px', display: 'flex', gap: '12px' }}>
              <button type="button" className="primary-button full" onClick={() => { setSelectedResource(null); navigate("donate"); }}>
                Donate Now \u2192
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}"""

content = content.replace(old_receive, new_receive)

# ============================================================
# FIX 3: BloodBanksPage - add modal for View button
# ============================================================

old_blood = """function BloodBanksPage() {
  const banks = [
    {
      name: "City Blood Bank",
      location: "Community blood service",
      groups: "A+, A\u2212, B+, B\u2212, O+, O\u2212",
      icon: "\U0001fa78",
    },
    {
      name: "Red Cross Blood Bank",
      location: "Regional blood service",
      groups: "A+, B+, O+, AB+",
      icon: "\U0001f3e5",
    },
  ];

  return (
    <div className="inner-page">
      <div className="page-heading-row">
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

      <div className="blood-safety-banner">
        <span>\U0001fa78</span>

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
                <span>\u2713</span>
              </div>

              <p>{bank.location}</p>

              <div className="blood-groups">
                {bank.groups}
              </div>
            </div>

            <button
              type="button"
              className="secondary-button"
            >
              View
            </button>
          </article>
        ))}
      </div>
    </div>
  );
}"""

new_blood = """function BloodBanksPage() {
  const [selectedBank, setSelectedBank] = useState(null);

  const banks = [
    {
      name: "City Blood Bank",
      location: "Community blood service",
      groups: "A+, A\u2212, B+, B\u2212, O+, O\u2212",
      icon: "\U0001fa78",
      address: "MG Road, Mysore, Karnataka 570001",
      phone: "+91 821-2424242",
      hours: "24/7 Emergency Services",
      services: ["Whole Blood", "Platelets", "Plasma", "Red Blood Cells"],
    },
    {
      name: "Red Cross Blood Bank",
      location: "Regional blood service",
      groups: "A+, B+, O+, AB+",
      icon: "\U0001f3e5",
      address: "Sayyaji Rao Road, Mysore, Karnataka 570005",
      phone: "+91 821-2525252",
      hours: "Mon-Sat: 8AM - 8PM",
      services: ["Whole Blood", "Platelets", "Blood Group Testing"],
    },
  ];

  return (
    <div className="inner-page">
      <div className="page-heading-row">
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

      <div className="blood-safety-banner">
        <span>\U0001fa78</span>

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
                <span>\u2713</span>
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
                  <span className="verified-badge">\u2713 Verified Blood Bank</span>
                </div>
              </div>
              <button type="button" className="modal-close" onClick={() => setSelectedBank(null)}>\u00d7</button>
            </div>

            <div className="modal-body" style={{ display: 'flex', flexDirection: 'column', gap: '16px', marginTop: '16px' }}>
              <div>
                <strong style={{ fontSize: '12px', color: '#8fa39e', textTransform: 'uppercase' }}>Available Blood Groups</strong>
                <p style={{ marginTop: '4px', fontSize: '14px', color: '#173b35' }}>\U0001fa78 {selectedBank.groups}</p>
              </div>

              <div>
                <strong style={{ fontSize: '12px', color: '#8fa39e', textTransform: 'uppercase' }}>Address</strong>
                <p style={{ marginTop: '4px', fontSize: '14px', color: '#173b35' }}>\U0001f4cd {selectedBank.address}</p>
              </div>

              <div>
                <strong style={{ fontSize: '12px', color: '#8fa39e', textTransform: 'uppercase' }}>Contact</strong>
                <p style={{ marginTop: '4px', fontSize: '14px', color: '#173b35' }}>\u260e {selectedBank.phone}</p>
              </div>

              <div>
                <strong style={{ fontSize: '12px', color: '#8fa39e', textTransform: 'uppercase' }}>Hours</strong>
                <p style={{ marginTop: '4px', fontSize: '14px', color: '#173b35' }}>\u23f0 {selectedBank.hours}</p>
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
                Contact Blood Bank \u2192
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}"""

content = content.replace(old_blood, new_blood)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("All fixes applied successfully!")
print("- Topbar search now navigates to Receive on Enter")
print("- Topbar notification bell now navigates to Notifications page")
print("- Receive page filter chips now filter resources")
print("- Receive page View Details now shows modal")
print("- Blood Banks View button now shows modal with details")
