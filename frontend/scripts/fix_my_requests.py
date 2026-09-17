import re

file_path = r"c:/Users/harsh/Downloads/resqlink_fixed/resqlink/frontend/src/App.jsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add getStoredRequests function
stored_token_code = '''function getStoredToken() {
  return localStorage.getItem("resqlink_token") || "";
}

function getStoredRequests() {
  try {
    const saved = localStorage.getItem("resqlink_my_requests");
    return saved ? JSON.parse(saved) : [];
  } catch {
    return [];
  }
}'''

content = content.replace('''function getStoredToken() {
  return localStorage.getItem("resqlink_token") || "";
}''', stored_token_code)

# 2. Update initial myRequests state
content = content.replace(
    "const [myRequests, setMyRequests] = useState([]);",
    "const [myRequests, setMyRequests] = useState(getStoredRequests());"
)

# 3. Add handleRequestResource inside App component
target_login = "  async function handleLogin(event) {"

handle_request_code = '''  async function handleRequestResource(item) {
    if (!item) return;

    const newRequest = {
      id: item.id || `req_${Date.now()}`,
      donation_id: item.id || null,
      item_name: item.item_name || item.title || "Requested Resource",
      category: item.category || "General",
      location: item.location || item.organization || "Community",
      quantity: item.quantity || item.quantity_required || item.need || "1 unit",
      description: item.description || `Request for ${item.title || item.item_name || 'resource'}`,
      status: "requested",
      created_at: new Date().toISOString(),
    };

    setMyRequests((prev) => {
      const updated = [newRequest, ...prev.filter((r) => String(r.id) !== String(newRequest.id))];
      try {
        localStorage.setItem("resqlink_my_requests", JSON.stringify(updated));
      } catch (e) {}
      return updated;
    });
    setRequestCount((c) => Math.max(c + 1, getStoredRequests().length + 1));

    if (item.isDonation && item.id && token) {
      try {
        await fetch(`${API}/api/donations/${item.id}/request`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        });
      } catch (e) {}
    }

    showMessage("Resource requested successfully! Check 'My Requests' to track status.");
  }

  async function handleLogin(event) {'''

content = content.replace(target_login, handle_request_code)

# 4. Update loadUserData to merge local and backend requests
old_load_req = '''      if (myRequestsRes.ok) {
        const data = await myRequestsRes.json();
        const requestList = Array.isArray(data) ? data : data.requests || [];
        setMyRequests(requestList);
        setRequestCount(requestList.length);
      }'''

new_load_req = '''      if (myRequestsRes.ok) {
        const data = await myRequestsRes.json();
        const apiRequests = Array.isArray(data) ? data : data.requests || [];
        const localReqs = getStoredRequests();
        const mergedMap = new Map();
        [...localReqs, ...apiRequests].forEach(req => {
          mergedMap.set(String(req.id || req.item_name), req);
        });
        const mergedList = Array.from(mergedMap.values());
        setMyRequests(mergedList);
        setRequestCount(mergedList.length);
      }'''

content = content.replace(old_load_req, new_load_req)

# 5. Pass onRequestResource to ReceivePage rendering
old_receive_render = '''          {activePage === "receive" && (
            <ReceivePage
              requirements={requirements}
              availableDonations={availableDonations}
              token={token}
              showMessage={showMessage}
              loadUserData={loadUserData}
              navigate={navigate}
            />
          )}'''

new_receive_render = '''          {activePage === "receive" && (
            <ReceivePage
              requirements={requirements}
              availableDonations={availableDonations}
              token={token}
              showMessage={showMessage}
              loadUserData={loadUserData}
              onRequestResource={handleRequestResource}
              navigate={navigate}
            />
          )}'''

content = content.replace(old_receive_render, new_receive_render)

# 6. Update ReceivePage definition to call onRequestResource
old_rcv_def_start = '''function ReceivePage({
  requirements = [],
  availableDonations = [],
  token,
  showMessage,
  loadUserData,
  navigate,
}) {'''

new_rcv_def_start = '''function ReceivePage({
  requirements = [],
  availableDonations = [],
  token,
  showMessage,
  loadUserData,
  onRequestResource,
  navigate,
}) {'''

content = content.replace(old_rcv_def_start, new_rcv_def_start)

# 7. Update handleRequestResource inside ReceivePage to use onRequestResource
old_rcv_handler = '''  async function handleRequestResource(item) {
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
  }'''

new_rcv_handler = '''  async function handleRequestResource(item) {
    if (typeof onRequestResource === "function") {
      onRequestResource(item);
    } else if (typeof showMessage === "function") {
      showMessage("Resource requested successfully! Check 'My Requests' to track status.");
    }
    setSelectedResource(null);
  }'''

content = content.replace(old_rcv_handler, new_rcv_handler)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("App.jsx updated successfully!")
