with open(r'c:\Users\harsh\Downloads\resqlink_fixed\resqlink\frontend\src\App.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect each occurrence of "inner-page"
import re

# Let's look at all page-heading-row blocks
pages = ['DonationPage', 'ReceivePage', 'OrganizationsPage', 'BloodBanksPage', 'VolunteerInfoPage', 'NotificationsPage', 'SettingsPage', 'ProfilePage']

# Let's write a python replacer that ensures standard clean heading for each inner page:
# Pattern:
# <div className="inner-page">
#   <div className="page-heading-row">
#     <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
#       <button ...>← Back</button>
#       <div>
#         <div className="breadcrumb">...</div>
#         <h1>...</h1>
#         <p>...</p>
#       </div>
#     </div>
#   </div>
#
# Notice the 3 closing </div> tags! (1 for breadcrumb parent div, 1 for flex wrapper, 1 for page-heading-row).

print("Fixing page heading rows in App.jsx...")

# 1. BloodBanksPage
blood_banks_orig = """    <div className="inner-page">
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
      </div>"""

blood_banks_fixed = """    <div className="inner-page">
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
      </div>"""

# 2. VolunteerInfoPage
volunteer_orig = """    <div className="inner-page">
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
            ResQLink <span>/</span> Volunteer
          </div>

          <h1>Make an Impact as a Volunteer</h1>

          <p>
            Help connect donations with people and organizations
            who need them.
          </p>
        </div>
      </div>"""

volunteer_fixed = """    <div className="inner-page">
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
      </div>"""

# 3. NotificationsPage
notif_orig = """    <div className="inner-page">
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
              ResQLink <span>/</span> Notifications
            </div>

          <h1>Notification Center</h1>

          <p>
            Stay updated with real-time alerts, matches, and requests.
          </p>
        </div>
      </div>"""

notif_fixed = """    <div className="inner-page">
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
              ResQLink <span>/</span> Notifications
            </div>

            <h1>Notification Center</h1>

            <p>
              Stay updated with real-time alerts, matches, and requests.
            </p>
          </div>
        </div>
      </div>"""

# 4. SettingsPage
settings_orig = """    <div className="inner-page">
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
              ResQLink <span>/</span> Settings
            </div>

          <h1>Account & Security Settings</h1>

          <p>
            Manage your account preferences, security settings, and notification preferences.
          </p>
        </div>
      </div>"""

settings_fixed = """    <div className="inner-page">
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
              ResQLink <span>/</span> Settings
            </div>

            <h1>Account & Security Settings</h1>

            <p>
              Manage your account preferences, security settings, and notification preferences.
            </p>
          </div>
        </div>
      </div>"""

# 5. ProfilePage
profile_orig = """    <div className="inner-page">
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
              ResQLink <span>/</span> Profile
            </div>

          <h1>User Profile</h1>

          <p>
            Manage your personal information, activity history, and community stats.
          </p>
        </div>
      </div>"""

profile_fixed = """    <div className="inner-page">
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
              ResQLink <span>/</span> Profile
            </div>

            <h1>User Profile</h1>

            <p>
              Manage your personal information, activity history, and community stats.
            </p>
          </div>
        </div>
      </div>"""

# 6. DonationPage
donation_orig = """    <div className="inner-page">
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
            ResQLink <span>/</span> Donate
          </div>

          <h1>Donate an Item</h1>

          <p>
            Share unused medicine, surplus food, usable clothes,
            books or essential supplies.
          </p>
        </div>
      </div>"""

donation_fixed = """    <div className="inner-page">
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
              ResQLink <span>/</span> Donate
            </div>

            <h1>Donate an Item</h1>

            <p>
              Share unused medicine, surplus food, usable clothes,
              books or essential supplies.
            </p>
          </div>
        </div>
      </div>"""

# 7. ReceivePage
receive_orig = """    <div className="inner-page">
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
            ResQLink <span>/</span> Receive
          </div>

          <h1>Available Community Resources</h1>

          <p>
            Browse verified listings created by donors across the
            network.
          </p>
        </div>
      </div>"""

receive_fixed = """    <div className="inner-page">
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

            <h1>Available Community Resources</h1>

            <p>
              Browse verified listings created by donors across the
              network.
            </p>
          </div>
        </div>
      </div>"""

replacements = [
    (blood_banks_orig, blood_banks_fixed, "BloodBanksPage"),
    (volunteer_orig, volunteer_fixed, "VolunteerInfoPage"),
    (notif_orig, notif_fixed, "NotificationsPage"),
    (settings_orig, settings_fixed, "SettingsPage"),
    (profile_orig, profile_fixed, "ProfilePage"),
    (donation_orig, donation_fixed, "DonationPage"),
    (receive_orig, receive_fixed, "ReceivePage"),
]

for orig, fixed, name in replacements:
    if orig in text:
        text = text.replace(orig, fixed, 1)
        print(f"Fixed {name}")
    else:
        print(f"Pattern NOT found for {name} (checking alternative...)")

with open(r'c:\Users\harsh\Downloads\resqlink_fixed\resqlink\frontend\src\App.jsx', 'w', encoding='utf-8') as f:
    f.write(text)

print("Saved App.jsx with all fixed page headings!")
