const fs = require('fs');
const path = require('path');

let content = fs.readFileSync('src/App.jsx', 'utf8');

// Let's check where the unclosed divs are
// In BloodBanksPage:
// Let's inspect VolunteerInfoPage, NotificationsPage, SettingsPage, ProfilePage, DonationPage, ReceivePage, OrganizationsPage
console.log("Checking page heading rows...");
