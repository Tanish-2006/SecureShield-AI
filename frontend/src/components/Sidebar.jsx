import { useState, useRef, useEffect } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import {
  Gauge,
  FolderKanban,
  KeyRound,
  ScanLine,
  ShieldAlert,
  Settings,
  LogOut,
  X,
  ShieldCheck,
  ChevronDown,
  Plus,
  Check,
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useProject } from "../context/ProjectContext";

const navItems = [
  { to: "/dashboard", label: "Dashboard", icon: Gauge },
  { to: "/projects", label: "Projects", icon: FolderKanban },
  { to: "/api-keys", label: "API Keys", icon: KeyRound },
  { to: "/prompt-scanner", label: "Prompt Scanner", icon: ScanLine },
  { to: "/threat-logs", label: "Threat Logs", icon: ShieldAlert },
  { to: "/settings", label: "Settings", icon: Settings },
];

const PROJECT_COLORS = [
  "#3b82f6", "#8b5cf6", "#06b6d4", "#10b981",
  "#f59e0b", "#ef4444", "#ec4899", "#6366f1",
];

function getProjectColor(id) {
  return PROJECT_COLORS[(id || 0) % PROJECT_COLORS.length];
}

function ProjectSwitcher({ onClose }) {
  const navigate = useNavigate();
  const { projects, projectId, selectedProject, selectProject, hasProjects } = useProject();
  const [open, setOpen] = useState(false);
  const ref = useRef(null);

  useEffect(() => {
    function handleClick(e) {
      if (ref.current && !ref.current.contains(e.target)) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, []);

  if (!hasProjects) {
    return (
      <div className="sidebar-project-section">
        <button
          className="sidebar-no-project"
          onClick={() => { navigate("/projects"); onClose?.(); }}
        >
          <Plus size={16} />
          <span>Create a project</span>
        </button>
      </div>
    );
  }

  return (
    <div className="sidebar-project-section" ref={ref}>
      <button
        className="sidebar-project-btn"
        onClick={() => setOpen(!open)}
      >
        <div
          className="sidebar-project-avatar"
          style={{ background: getProjectColor(projectId) }}
        >
          {selectedProject?.name?.charAt(0)?.toUpperCase() || "P"}
        </div>
        <div className="sidebar-project-info">
          <span className="sidebar-project-name">
            {selectedProject?.name || "Select project"}
          </span>
          <span className="sidebar-project-count">
            {projects.length} {projects.length === 1 ? "project" : "projects"}
          </span>
        </div>
        <ChevronDown size={16} className={`sidebar-chevron ${open ? "open" : ""}`} />
      </button>

      <AnimatePresence>
        {open && (
          <motion.div
            className="sidebar-project-dropdown"
            initial={{ opacity: 0, y: -8, scale: 0.96 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -8, scale: 0.96 }}
            transition={{ duration: 0.15 }}
          >
            {projects.map((p) => (
              <button
                key={p.id}
                className={`sidebar-project-item ${p.id === projectId ? "active" : ""}`}
                onClick={() => {
                  selectProject(p.id);
                  setOpen(false);
                }}
              >
                <div
                  className="sidebar-project-item-avatar"
                  style={{ background: getProjectColor(p.id) }}
                >
                  {p.name.charAt(0).toUpperCase()}
                </div>
                <span className="sidebar-project-item-name">{p.name}</span>
                {p.id === projectId && <Check size={14} className="sidebar-project-check" />}
              </button>
            ))}
            <div className="sidebar-project-dropdown-divider" />
            <button
              className="sidebar-project-item create"
              onClick={() => { navigate("/projects"); setOpen(false); onClose?.(); }}
            >
              <Plus size={16} />
              <span>Create Project</span>
            </button>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

function Sidebar({ isOpen, onClose }) {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <>
      <aside className={`sidebar ${isOpen ? "is-open" : ""}`} aria-label="Primary">
        <div className="sidebar-header">
          <div className="brand-mark" aria-hidden="true">
            <ShieldCheck size={20} />
          </div>
          <div>
            <p className="brand-name">SecureShield AI</p>
            <span className="brand-subtitle">Prompt security cloud</span>
          </div>
          <button className="icon-btn mobile-only" onClick={onClose} aria-label="Close menu">
            <X size={18} />
          </button>
        </div>

        <ProjectSwitcher onClose={onClose} />

        <nav className="sidebar-nav">
          <p className="nav-section-label">Main Menu</p>
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) => `nav-item ${isActive ? "active" : ""}`}
                onClick={onClose}
              >
                <Icon size={18} />
                <span>{item.label}</span>
              </NavLink>
            );
          })}
        </nav>

        <div className="sidebar-footer">
          <div className="status-card">
            <span className="status-dot" />
            <div>
              <strong>Live protection</strong>
              <small>JWT secured session</small>
            </div>
          </div>
          <button className="nav-item logout-button" onClick={handleLogout}>
            <LogOut size={18} />
            <span>Logout</span>
          </button>
        </div>
      </aside>

      {isOpen && <button className="sidebar-backdrop" onClick={onClose} aria-label="Close menu" />}
    </>
  );
}

export default Sidebar;
