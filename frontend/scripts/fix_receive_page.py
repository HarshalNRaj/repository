import re

file_path = r"c:/Users/harsh/Downloads/resqlink_fixed/resqlink/frontend/src/App.jsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace ReceivePage component
old_receive_pattern = r"function ReceivePage\(\{[\s\S]*?\n\}\n\n/\* ==="

new_receive_code = '''function ReceivePage({
  requirements = [],
  availableDonations = [],
  token,
  showMessage,
  loadUserData,
  navigate,
}) {
  const [activeFilter, setActiveFilter] = useState("All");
  const [selectedResource, setSelectedResource] = useState(null);
  const [requestingId, setRequestingId] = useState(null);
  const filters = ["All", "Clothes", "Books", "Food", "Electronics", "Household"];

  const combinedItems = useMemo(() => {
    const donationItems = availableDonations.map((d) => ({
      ...d,
      isDonation: true,
      title: d.item_name,
      type: d.donation_type ? `Donation (${d.donation_type})` : "Community Donation",
      organization: d.location ? `Location: ${d.location}` : "Community Donor",
      need: `${d.quantity || 1} unit(s)`,
      statusText: d.status || "available",
      isAvailable: d.status === "available",
      icon: d.category === "Clothes" ? "👕" : d.category === "Books" ? "📚" : d.category === "Food" ? "🍱" : d.category === "Electronics" ? "💻" : "🎁",
    }));

    const reqItems = requirements.map((r) => ({
      ...r,
      isRequirement: true,
      title: r.item_name,
      type: "NGO Requirement",
      organization: r.organization_name || "NGO / Ashram",
      need: `${r.quantity_required || 1} unit(s)`,
      statusText: r.priority === "urgent" ? "Urgent" : "Open",
      isAvailable: true,
      icon: r.category === "Clothes" ? "👕" : r.category === "Books" ? "📚" : r.category === "Food" ? "🍱" : "📦",
    }));

    const all = [...donationItems, ...reqItems];
    return all.length > 0 ? all : SAMPLE_NEEDS;
  }, [availableDonations, requirements]);

  const items = activeFilter === "All"
    ? combinedItems
    : combinedItems.filter((item) => {
        const name = (item.item_name || item.title || "").toLowerCase();
        const cat = (item.category || "").toLowerCase();
        const filterLower = activeFilter.toLowerCase();
        return name.includes(filterLower) || cat.includes(filterLower);
      });

  async function handleRequestResource(item) {
    if (!token) {
      if (typeof showMessage === "function") {
        showMessage("Please login to request resources.", "error");
      } else {
        alert("Please login to request resources.");
      }
      return;
    }

    if (item.isDonation && item.id) {
      setRequestingId(item.id);
      try {
        const response = await fetch(`${API}/api/donations/${item.id}/request`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        });
        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.message || data.error || "Unable to request resource.");
        }

        if (typeof showMessage === "function") {
          showMessage(data.message || "Resource requested successfully! Check 'My Requests' to track status.");
        }
        if (typeof loadUserData === "function") {
          loadUserData();
        }
        setSelectedResource(null);
      } catch (error) {
        if (typeof showMessage === "function") {
          showMessage(error.message || "Unable to request resource.", "error");
        } else {
          alert(error.message || "Unable to request resource.");
        }
      } finally {
        setRequestingId(null);
      }
    } else {
      if (typeof showMessage === "function") {
        showMessage("Request submitted! ResQLink coordinator will contact you shortly.");
      }
      setSelectedResource(null);
    }
  }

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
              ResQLink <span>/</span> Receive
            </div>
            <h1>Receive & Request Resources</h1>
            <p>
              Browse available community donations and NGO needs. Request items directly.
            </p>
          </div>
        </div>

        <button
          type="button"
          className="primary-button"
          onClick={() => navigate("donate")}
        >
          🎁 Donate Resource
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
            <div className="empty-state-icon">🔍</div>
            <h2>No resources found for "{activeFilter}"</h2>
            <p>Try selecting a different category or check back later.</p>
          </div>
        ) : items.map((item, index) => {
          const fallback = SAMPLE_NEEDS[index % SAMPLE_NEEDS.length];
          const title = item.item_name || item.title || fallback.title;
          const org = item.organization_name || item.organization || fallback.organization || "Community Donor";
          const qty = item.need || item.quantity_required || `${item.quantity || 1} unit(s)`;
          const loc = item.location || fallback.location;
          const type = item.type || item.organization_type || fallback.type;
          const isUrgent = item.priority === "urgent" || item.statusText === "urgent";
          const isRequested = item.status === "requested";

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
                <span style={{ fontSize: "36px" }}>{item.icon || fallback.icon}</span>
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
                      background: isUrgent ? "#fef2f2" : isRequested ? "#fffbe6" : "#f0fdf4",
                      color: isUrgent ? "#dc2626" : isRequested ? "#d46b08" : "#16a34a",
                      border: `1px solid ${isUrgent ? "#fecaca" : isRequested ? "#ffe58f" : "#bbf7d0"}`,
                      whiteSpace: "nowrap",
                      textTransform: "capitalize"
                    }}
                  >
                    {isRequested ? "⏳ Requested" : isUrgent ? "⚡ Urgent" : "✓ Available"}
                  </span>
                </div>

                <p style={{ fontSize: "13px", color: "#4b5563", lineHeight: 1.5, margin: 0 }}>
                  {item.description || `Resource available: ${title}`}
                </p>

                <div className="organization-meta">
                  <span>🏢 {org}</span>
                  <span>📍 {loc}</span>
                </div>

                <div style={{ paddingTop: "4px" }}>
                  <span>📦 {qty}</span>
                </div>

                <div style={{ marginTop: "auto", display: "flex", gap: "8px", paddingTop: "10px" }}>
                  <button
                    type="button"
                    style={{
                      flex: 1,
                      padding: "8px 0",
                      borderRadius: "8px",
                      border: "1.5px solid #147d63",
                      background: "transparent",
                      color: "#147d63",
                      fontWeight: 600,
                      fontSize: "13px",
                      cursor: "pointer",
                    }}
                    onClick={() =>
                      setSelectedResource({
                        ...item,
                        title,
                        org,
                        qty,
                        loc,
                        type,
                        description: item.description || `Resource available: ${title}`
                      })
                    }
                  >
                    View Details
                  </button>

                  <button
                    type="button"
                    disabled={isRequested || requestingId === item.id}
                    style={{
                      flex: 1,
                      padding: "8px 0",
                      borderRadius: "8px",
                      border: "none",
                      background: isRequested ? "#e2e8f0" : "#147d63",
                      color: isRequested ? "#94a3b8" : "#fff",
                      fontWeight: 600,
                      fontSize: "13px",
                      cursor: isRequested ? "not-allowed" : "pointer",
                    }}
                    onClick={() => handleRequestResource(item)}
                  >
                    {requestingId === item.id ? "Requesting..." : isRequested ? "Requested" : "Request"}
                  </button>
                </div>
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
                <span style={{ fontSize: "32px" }}>{selectedResource.icon || "📦"}</span>
                <div>
                  <h3>{selectedResource.title}</h3>
                  <span className="verified-badge">
                    {selectedResource.type} • {selectedResource.status === "requested" ? "Requested" : "Available"}
                  </span>
                </div>
              </div>
              <button
                type="button"
                className="modal-close"
                onClick={() => setSelectedResource(null)}
              >
                ×
              </button>
            </div>

            <div className="modal-body" style={{ display: "flex", flexDirection: "column", gap: "16px", marginTop: "16px" }}>
              <div>
                <strong style={{ fontSize: "12px", color: "#8fa39e", textTransform: "uppercase" }}>Source / Organization</strong>
                <p style={{ marginTop: "4px", fontSize: "14px", color: "#173b35" }}>🏢 {selectedResource.org}</p>
              </div>
              <div>
                <strong style={{ fontSize: "12px", color: "#8fa39e", textTransform: "uppercase" }}>Description</strong>
                <p style={{ marginTop: "4px", fontSize: "14px", color: "#173b35" }}>{selectedResource.description}</p>
              </div>
              <div>
                <strong style={{ fontSize: "12px", color: "#8fa39e", textTransform: "uppercase" }}>Quantity</strong>
                <p style={{ marginTop: "4px", fontSize: "14px", color: "#173b35" }}>📦 {selectedResource.qty}</p>
              </div>
              <div>
                <strong style={{ fontSize: "12px", color: "#8fa39e", textTransform: "uppercase" }}>Location</strong>
                <p style={{ marginTop: "4px", fontSize: "14px", color: "#173b35" }}>📍 {selectedResource.loc}</p>
              </div>
              <div style={{ background: "#f4faf7", padding: "16px", borderRadius: "12px", border: "1px solid #bce3d6" }}>
                <strong style={{ color: "#147d63", fontSize: "14px" }}>Request Information</strong>
                <p style={{ fontSize: "13px", color: "#2c594e", marginTop: "4px" }}>
                  Click "Request This Resource" to claim or request this item. Your request will be recorded and processed through ResQLink.
                </p>
              </div>
            </div>

            <div style={{ marginTop: "24px", display: "flex", gap: "12px" }}>
              <button
                type="button"
                className="primary-button full"
                disabled={selectedResource.status === "requested" || requestingId === selectedResource.id}
                onClick={() => handleRequestResource(selectedResource)}
              >
                {requestingId === selectedResource.id
                  ? "Submitting Request..."
                  : selectedResource.status === "requested"
                  ? "Already Requested"
                  : "Request This Resource →"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

/* ==='''

content, count = re.subn(old_receive_pattern, new_receive_code, content)
print(f"ReceivePage replaced: {count} times")

# Replace SimpleListPage component to accept items
old_simple_pattern = r"function SimpleListPage\(\{[\s\S]*?\n\}\n\nfunction Field"

new_simple_code = '''function SimpleListPage({
  title,
  subtitle,
  icon,
  emptyText,
  items = [],
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

      {items.length === 0 ? (
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
      ) : (
        <div className="organization-grid">
          {items.map((item, idx) => (
            <article className="organization-card" key={item.id || idx}>
              <div
                className="organization-cover"
                style={{
                  background: "linear-gradient(135deg, #147d63, #0e5f4d)"
                }}
              >
                <span style={{ fontSize: "36px" }}>{icon}</span>
              </div>

              <div className="organization-card-body">
                <div className="organization-title-row">
                  <h3>{item.item_name || item.title || "Resource"}</h3>
                  <span
                    style={{
                      fontSize: "11px",
                      fontWeight: 700,
                      padding: "3px 10px",
                      borderRadius: "20px",
                      background: "#f0fdf4",
                      color: "#16a34a",
                      border: "1px solid #bbf7d0",
                      whiteSpace: "nowrap",
                      textTransform: "capitalize"
                    }}
                  >
                    {item.status || "Active"}
                  </span>
                </div>

                <p style={{ fontSize: "13px", color: "#4b5563", lineHeight: 1.5, margin: 0 }}>
                  {item.description || `Category: ${item.category || "General"}`}
                </p>

                <div className="organization-meta" style={{ marginTop: "12px" }}>
                  <span>📦 Qty: {item.quantity || item.quantity_required || 1}</span>
                  <span>📍 {item.location || "Community"}</span>
                </div>

                {item.created_at && (
                  <div style={{ fontSize: "11px", color: "#6b7f7a", marginTop: "6px" }}>
                    Date: {new Date(item.created_at).toLocaleDateString()}
                  </div>
                )}
              </div>
            </article>
          ))}
        </div>
      )}
    </div>
  );
}

function Field'''

content, count2 = re.subn(old_simple_pattern, new_simple_code, content)
print(f"SimpleListPage replaced: {count2} times")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Done updating App.jsx!")
