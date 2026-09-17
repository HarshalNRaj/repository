import re

app_path = r"c:\Users\harsh\Downloads\resqlink_fixed\resqlink\frontend\src\App.jsx"

with open(app_path, "r", encoding="utf-8") as f:
    content = f.read()

# =====================================================================
# 1. DonationPage - add navigate to props + back arrow + photo upload
# =====================================================================

old_donation_heading = '''      <div className="page-heading-row">
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
      </div>'''

new_donation_heading = '''      <div className="page-heading-row">
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
      </div>'''

content = content.replace(old_donation_heading, new_donation_heading)

# Add photo upload field after TextAreaField for description in DonationPage
old_textarea_donation = '''            <TextAreaField
              label="Description"
              name="description"
              placeholder="Add useful details about the item..."
              value={donationForm.description}
              onChange={handleDonationChange}
            />

            <div className="form-actions">'''

new_textarea_donation = '''            <TextAreaField
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

            <div className="form-actions">'''

content = content.replace(old_textarea_donation, new_textarea_donation)

# =====================================================================
# 2. ReceivePage - add back arrow to heading
# =====================================================================

old_receive_heading = '''    <div className="inner-page">
      <div className="page-heading-row">
        <div>
          <div className="breadcrumb">
            ResQLink <span>/</span> Find Resources
          </div>'''

new_receive_heading = '''    <div className="inner-page">
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
              ResQLink <span>/</span> Find Resources
            </div>'''

content = content.replace(old_receive_heading, new_receive_heading, 1)

# Close the inner div for ReceivePage heading - find the pattern after "Find Resources" heading close
old_receive_heading_end = '''            ResQLink <span>/</span> Find Resources
            </div>

          <h1>Find Resources Near You</h1>

          <p>
            Browse available resources and connect with NGOs,
            ashrams, and community donors.
          </p>
        </div>
      </div>'''

new_receive_heading_end = '''            ResQLink <span>/</span> Find Resources
            </div>

          <h1>Find Resources Near You</h1>

          <p>
            Browse available resources and connect with NGOs,
            ashrams, and community donors.
          </p>
          </div>
        </div>
      </div>'''

content = content.replace(old_receive_heading_end, new_receive_heading_end, 1)

# =====================================================================
# 3. OrganizationsPage - add back arrow
# =====================================================================

old_org_heading = '''    <div className="inner-page">
      <div className="page-heading-row">
        <div>
          <div className="breadcrumb">
            ResQLink <span>/</span> Organizations
          </div>'''

new_org_heading = '''    <div className="inner-page">
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
            </div>'''

content = content.replace(old_org_heading, new_org_heading, 1)

# OrganizationsPage - close the extra inner div
old_org_heading_end = '''            ResQLink <span>/</span> Organizations
          </div>

          <h1>NGOs &amp; Ashrams Near You</h1>

          <p>
            Connect with verified organizations doing meaningful
            work in your community.
          </p>
        </div>
      </div>'''

new_org_heading_end = '''            ResQLink <span>/</span> Organizations
            </div>

          <h1>NGOs &amp; Ashrams Near You</h1>

          <p>
            Connect with verified organizations doing meaningful
            work in your community.
          </p>
          </div>
        </div>
      </div>'''

content = content.replace(old_org_heading_end, new_org_heading_end, 1)

# =====================================================================
# 4. BloodBanksPage - add back arrow
# =====================================================================

old_blood_heading = '''    <div className="inner-page">
      <div className="page-heading-row">
        <div>
          <div className="breadcrumb">
            ResQLink <span>/</span> Blood Banks
          </div>'''

new_blood_heading = '''    <div className="inner-page">
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
            </div>'''

content = content.replace(old_blood_heading, new_blood_heading, 1)

# BloodBanksPage - close the extra inner div
old_blood_heading_end = '''            ResQLink <span>/</span> Blood Banks
          </div>

          <h1>Blood Banks</h1>

          <p>
            Find nearby blood banks for emergency needs. Search
            by location or blood group.
          </p>
        </div>
      </div>'''

new_blood_heading_end = '''            ResQLink <span>/</span> Blood Banks
            </div>

          <h1>Blood Banks</h1>

          <p>
            Find nearby blood banks for emergency needs. Search
            by location or blood group.
          </p>
          </div>
        </div>
      </div>'''

content = content.replace(old_blood_heading_end, new_blood_heading_end, 1)

# =====================================================================
# 5. NotificationsPage - add back arrow and navigate prop
# =====================================================================

old_notif_func = 'function NotificationsPage() {'
new_notif_func = 'function NotificationsPage({ navigate }) {'
content = content.replace(old_notif_func, new_notif_func, 1)

old_notif_heading = '''      <div className="page-heading-row">
        <div>
          <div className="breadcrumb">
            ResQLink <span>/</span> Notifications
          </div>

          <h1>Notifications</h1>

          <p>
            Stay updated on donations, requests and activity
            around you.
          </p>
        </div>
      </div>'''

new_notif_heading = '''      <div className="page-heading-row">
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
              ResQLink <span>/</span> Notifications
            </div>

            <h1>Notifications</h1>

            <p>
              Stay updated on donations, requests and activity
              around you.
            </p>
          </div>
        </div>
      </div>'''

content = content.replace(old_notif_heading, new_notif_heading, 1)

# Update NotificationsPage call to pass navigate
old_notif_call = '<NotificationsPage />'
new_notif_call = '<NotificationsPage navigate={navigate} />'
content = content.replace(old_notif_call, new_notif_call, 1)

# =====================================================================
# 6. SettingsPage - add back arrow
# =====================================================================

old_settings_heading = '''      <div className="page-heading-row">
        <div>
          <div className="breadcrumb">
            ResQLink <span>/</span> Settings
          </div>

          <h1>Settings</h1>

          <p>
            Manage your account preferences and platform experience.
          </p>
        </div>
      </div>'''

new_settings_heading = '''      <div className="page-heading-row">
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
      </div>'''

content = content.replace(old_settings_heading, new_settings_heading, 1)

# =====================================================================
# 7. ProfilePage - add back arrow
# =====================================================================

old_profile_heading_row = '''      <div className="page-heading-row">
        <div>
          <div className="breadcrumb">
            ResQLink <span>/</span> Profile
          </div>

          <h1>Your Profile</h1>

          <p>
            Your ResQLink community identity and account information.
          </p>
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
      </div>'''

new_profile_heading_row = '''      <div className="page-heading-row">
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
      </div>'''

content = content.replace(old_profile_heading_row, new_profile_heading_row, 1)

# =====================================================================
# 8. VolunteerInfoPage - add back arrow
# =====================================================================

old_vol_heading = '''      <div className="page-heading-row">
        <div>
          <div className="breadcrumb">
            ResQLink <span>/</span> Volunteer
          </div>'''

new_vol_heading = '''      <div className="page-heading-row">
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
          </div>'''

content = content.replace(old_vol_heading, new_vol_heading, 1)

# Fix the close div for volunteer heading
old_vol_heading_end = '''            ResQLink <span>/</span> Volunteer
          </div>

          <h1>Become a Volunteer</h1>

          <p>
            Join our network of volunteers and make a real
            difference in your community.
          </p>
        </div>
      </div>'''

new_vol_heading_end = '''            ResQLink <span>/</span> Volunteer
          </div>

          <h1>Become a Volunteer</h1>

          <p>
            Join our network of volunteers and make a real
            difference in your community.
          </p>
          </div>
        </div>
      </div>'''

content = content.replace(old_vol_heading_end, new_vol_heading_end, 1)

# =====================================================================
# 9. OrganizationsPage - add navigate prop
# =====================================================================

old_org_func = 'function OrganizationsPage({'
if 'function OrganizationsPage({\n  organizations,\n}) {' in content:
    old_org_func_sig = 'function OrganizationsPage({\n  organizations,\n}) {'
    new_org_func_sig = 'function OrganizationsPage({\n  organizations,\n  navigate,\n}) {'
    content = content.replace(old_org_func_sig, new_org_func_sig, 1)

# Also update OrganizationsPage call site to pass navigate
old_org_call = '''          {activePage === "organizations" && (
            <OrganizationsPage
              organizations={organizations}
            />
          )}'''
new_org_call = '''          {activePage === "organizations" && (
            <OrganizationsPage
              organizations={organizations}
              navigate={navigate}
            />
          )}'''
content = content.replace(old_org_call, new_org_call, 1)

# Also update BloodBanksPage call site to pass navigate
old_blood_call = '''          {activePage === "blood-banks" && (
            <BloodBanksPage />
          )}'''
new_blood_call = '''          {activePage === "blood-banks" && (
            <BloodBanksPage navigate={navigate} />
          )}'''
content = content.replace(old_blood_call, new_blood_call, 1)

# Update BloodBanksPage function to accept navigate
if 'function BloodBanksPage() {' in content:
    content = content.replace('function BloodBanksPage() {', 'function BloodBanksPage({ navigate }) {', 1)

with open(app_path, "w", encoding="utf-8") as f:
    f.write(content)

print("All back arrows and photo upload added successfully!")
print("- DonationPage: back arrow + optional photo upload")
print("- ReceivePage: back arrow")
print("- OrganizationsPage: back arrow + navigate prop")
print("- BloodBanksPage: back arrow + navigate prop")
print("- VolunteerInfoPage: back arrow")
print("- NotificationsPage: back arrow + navigate prop")
print("- SettingsPage: back arrow")
print("- ProfilePage: back arrow")
