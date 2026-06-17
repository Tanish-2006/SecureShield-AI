import { useEffect, useState } from "react";
import { Bell, Menu, Search, ShieldCheck } from "lucide-react";
import { getCurrentUser } from "../services/authService";

function Navbar({ title, onMenu }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    let mounted = true;

    getCurrentUser()
      .then((data) => {
        if (mounted) setUser(data);
      })
      .catch(() => {
        if (mounted) setUser({ name: "Security Admin", email: "admin@secureshield.ai" });
      });

    return () => { mounted = false; };
  }, []);

  const initials = (user?.name || "SA")
    .split(" ")
    .map((part) => part[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();

  return (
    <header className="navbar">
      <div className="navbar-left">
        <button className="icon-btn mobile-only" onClick={onMenu} aria-label="Open menu">
          <Menu size={20} />
        </button>
        <div>
          <p className="eyebrow">
            <ShieldCheck size={14} />
            Secure workspace
          </p>
          <h1>{title}</h1>
        </div>
      </div>

      <div className="navbar-actions">
        <div className="search-bar desktop-only">
          <Search size={16} color="var(--text-muted)" />
          <input placeholder="Search security data..." />
        </div>
        <button className="icon-btn" aria-label="Notifications">
          <Bell size={18} />
          <span className="notification-dot" />
        </button>
        <div className="user-chip" aria-label="Current user">
          <span className="avatar">{initials}</span>
          <span className="desktop-only" style={{ fontSize: 13, fontWeight: 500, color: "var(--text-secondary)" }}>
            {user?.name || "Security Admin"}
          </span>
        </div>
      </div>
    </header>
  );
}

export default Navbar;
