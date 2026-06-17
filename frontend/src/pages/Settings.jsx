import { useState } from "react";
import { Shield, Bell, Moon, Globe, Key } from "lucide-react";
import { motion } from "framer-motion";
import { useToast } from "../context/ToastContext";

function Settings() {
  const toast = useToast();
  const [notifications, setNotifications] = useState(true);
  const [autoScan, setAutoScan] = useState(true);
  const [defaultThreshold, setDefaultThreshold] = useState("70");

  const handleSave = () => {
    toast("Settings saved successfully", "success");
  };

  return (
    <div>
      <div className="page-header">
        <h1>Settings</h1>
        <p>Configure your SecureShield AI preferences</p>
      </div>

      <div className="settings-section">
        <h2>Security</h2>
        <p>Configure security scanning and protection settings</p>
        <div className="settings-card">
          <div className="settings-row">
            <div>
              <div className="settings-row-label">
                <div className="flex items-center gap-2">
                  <Shield size={16} color="var(--brand-blue)" />
                  Default Risk Threshold
                </div>
              </div>
              <div className="settings-row-desc">Prompts exceeding this score will be blocked</div>
            </div>
            <select
              className="form-select"
              style={{ width: 120 }}
              value={defaultThreshold}
              onChange={(e) => setDefaultThreshold(e.target.value)}
            >
              <option value="50">50 (Strict)</option>
              <option value="70">70 (Moderate)</option>
              <option value="90">90 (Relaxed)</option>
            </select>
          </div>

          <div className="settings-row">
            <div>
              <div className="settings-row-label">
                <div className="flex items-center gap-2">
                  <Shield size={16} color="var(--brand-blue)" />
                  Auto-scan all prompts
                </div>
              </div>
              <div className="settings-row-desc">Automatically scan every prompt for threats</div>
            </div>
            <label className="toggle">
              <input
                type="checkbox"
                checked={autoScan}
                onChange={(e) => setAutoScan(e.target.checked)}
              />
              <span className="toggle-slider" />
            </label>
          </div>
        </div>
      </div>

      <div className="settings-section">
        <h2>Notifications</h2>
        <p>Manage alert and notification preferences</p>
        <div className="settings-card">
          <div className="settings-row">
            <div>
              <div className="settings-row-label">
                <div className="flex items-center gap-2">
                  <Bell size={16} color="var(--brand-blue)" />
                  Security alerts
                </div>
              </div>
              <div className="settings-row-desc">Receive alerts for critical threats</div>
            </div>
            <label className="toggle">
              <input
                type="checkbox"
                checked={notifications}
                onChange={(e) => setNotifications(e.target.checked)}
              />
              <span className="toggle-slider" />
            </label>
          </div>
        </div>
      </div>

      <div className="settings-section">
        <h2>Account</h2>
        <p>Manage your account settings</p>
        <div className="settings-card">
          <div className="settings-row">
            <div>
              <div className="settings-row-label">
                <div className="flex items-center gap-2">
                  <Key size={16} color="var(--brand-blue)" />
                  Session
                </div>
              </div>
              <div className="settings-row-desc">JWT secured session — 30 min expiry</div>
            </div>
            <button className="btn btn-secondary btn-sm">Refresh</button>
          </div>
        </div>
      </div>

      <motion.div
        style={{ marginTop: 32 }}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3 }}
      >
        <button className="btn btn-primary" onClick={handleSave}>
          Save Settings
        </button>
      </motion.div>
    </div>
  );
}

export default Settings;
