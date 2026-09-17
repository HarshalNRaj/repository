"""
Fix ReceivePage to use organization-grid card style.
Also handle GitHub push + gh-pages deployment.
"""
import re

# Read file
with open(r'c:\Users\harsh\Downloads\resqlink_fixed\resqlink\frontend\src\App.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

# The range to replace is from "   RECEIVE" section (line 2038) through closing "}" (line 2221)
# We'll use a regex to capture the whole ReceivePage function and replace it

old_pattern = r'   RECEIVE\r\n={57} \*\/\r\n\r\nfunction ReceivePage\(\{[\s\S]*?\r\n\}'

new_receive_page = r'''   RECEIVE
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
}'''

# Find start/end of the ReceivePage function precisely
start_marker = "   RECEIVE\r\n========================================================= */\r\n\r\nfunction ReceivePage({"
end_section_after = "function OrganizationsPage("

start_idx = text.find(start_marker)
end_idx = text.find(end_section_after)

if start_idx == -1:
    # try LF only
    start_marker_lf = start_marker.replace("\r\n", "\n")
    start_idx = text.find(start_marker_lf)
    print(f"LF start idx: {start_idx}")
else:
    print(f"Found start at idx: {start_idx}")

if end_idx == -1:
    end_section_after_lf = end_section_after
    end_idx = text.find(end_section_after_lf)
    
print(f"end_idx: {end_idx}")

if start_idx != -1 and end_idx != -1:
    # Find the closing "}" of ReceivePage - it's just before "/* ====\n   ORGANIZATIONS"
    # The section just before OrganizationsPage is "\r\n/* =========\n   ORGANIZATIONS"
    section_divider = "/* =========================================================\r\n   ORGANIZATIONS"
    div_idx = text.find(section_divider, start_idx)
    if div_idx == -1:
        section_divider = "/* =========================================================\n   ORGANIZATIONS"
        div_idx = text.find(section_divider, start_idx)
    
    print(f"div_idx: {div_idx}")
    
    if div_idx != -1:
        # Replace everything from start_marker to just before section_divider
        # (the "\r\n\r\n" before section_divider belongs to what we're replacing)
        receive_section = text[start_idx:div_idx]
        print(f"Receive section length: {len(receive_section)}")
        print(f"First 200 chars: {receive_section[:200]}")
        print(f"Last 100 chars: {receive_section[-100:]}")
        
        # Build replacement with consistent \r\n endings
        new_text = (
            text[:start_idx] +
            new_receive_page.replace("\n", "\r\n") +
            "\r\n\r\n" +
            text[div_idx:]
        )
        
        with open(r'c:\Users\harsh\Downloads\resqlink_fixed\resqlink\frontend\src\App.jsx', 'w', encoding='utf-8') as f:
            f.write(new_text)
        
        print("ReceivePage successfully replaced with org-grid style!")
    else:
        print("ERROR: Could not find section divider")
else:
    print(f"ERROR: start_idx={start_idx}, end_idx={end_idx}")
