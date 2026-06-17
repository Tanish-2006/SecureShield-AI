import { NavLink } from "react-router-dom";
import { Gauge, FolderKanban, KeyRound, ScanLine, ShieldAlert } from "lucide-react";

const navItems = [
  { to: "/dashboard", label: "Dashboard", icon: Gauge },
  { to: "/projects", label: "Projects", icon: FolderKanban },
  { to: "/api-keys", label: "API Keys", icon: KeyRound },
  { to: "/prompt-scanner", label: "Scanner", icon: ScanLine },
  { to: "/threat-logs", label: "Logs", icon: ShieldAlert },
];

function BottomNav() {
  return (
    <nav className="bottom-nav" aria-label="Mobile navigation">
      {navItems.map((item) => {
        const Icon = item.icon;
        return (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) => `bottom-nav-item ${isActive ? "active" : ""}`}
          >
            <Icon size={20} />
            <span>{item.label}</span>
          </NavLink>
        );
      })}
    </nav>
  );
}

export default BottomNav;
