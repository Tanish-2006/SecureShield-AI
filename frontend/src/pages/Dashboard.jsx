import { useEffect, useState, useCallback } from "react";
import {
  Shield, ShieldAlert, TrendingUp, Activity, FolderOpen,
  CheckCircle2, AlertTriangle
} from "lucide-react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import { getDashboard } from "../services/dashboardService";
import { useProject } from "../context/ProjectContext";

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.08 },
  },
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { duration: 0.4 } },
};

const statConfig = [
  { key: "total_threats", label: "Total Threats", color: "critical", icon: ShieldAlert },
  { key: "critical", label: "Critical", color: "critical", icon: ShieldAlert },
  { key: "high", label: "High", color: "high", icon: TrendingUp },
  { key: "medium", label: "Medium", color: "medium", icon: Activity },
  { key: "low", label: "Low", color: "low", icon: Shield },
  { key: "blocked", label: "Blocked", color: "critical", icon: ShieldAlert },
];

function SecurityScoreCard({ score }) {
  const color = score >= 80 ? "var(--status-low)"
    : score >= 50 ? "var(--status-high)"
    : "var(--status-critical)";

  const label = score >= 80 ? "Good"
    : score >= 50 ? "Needs attention"
    : "Critical";

  const circumference = 2 * Math.PI * 54;
  const offset = circumference - (score / 100) * circumference;

  return (
    <div className="glass-card stat-card" style={{ gridColumn: "span 1" }}>
      <div className="glass-card-header">
        <h3>Security Score</h3>
        {score >= 80 ? <CheckCircle2 size={18} color="var(--status-low)" />
          : <AlertTriangle size={18} color={color} />}
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: 16, marginTop: 8 }}>
        <div style={{ position: "relative", width: 120, height: 120, flexShrink: 0 }}>
          <svg width="120" height="120" style={{ transform: "rotate(-90deg)" }}>
            <circle
              cx="60" cy="60" r="54"
              fill="none"
              stroke="var(--bg-hover)"
              strokeWidth="8"
            />
            <circle
              cx="60" cy="60" r="54"
              fill="none"
              stroke={color}
              strokeWidth="8"
              strokeDasharray={circumference}
              strokeDashoffset={offset}
              strokeLinecap="round"
              style={{ transition: "stroke-dashoffset 1s ease" }}
            />
          </svg>
          <div style={{
            position: "absolute", inset: 0,
            display: "flex", alignItems: "center", justifyContent: "center",
            flexDirection: "column",
          }}>
            <span style={{ fontSize: 28, fontWeight: 800, color: "var(--text-primary)", lineHeight: 1 }}>
              {score}
            </span>
            <span style={{ fontSize: 11, color: "var(--text-muted)" }}>/100</span>
          </div>
        </div>
        <div>
          <div style={{ fontSize: 14, fontWeight: 600, color, marginBottom: 4 }}>{label}</div>
          <div style={{ fontSize: 12, color: "var(--text-muted)", lineHeight: 1.5 }}>
            Based on threat severity distribution across your project
          </div>
        </div>
      </div>
    </div>
  );
}

function Dashboard() {
  const navigate = useNavigate();
  const { projectId, selectedProject, hasProjects, loading: projectLoading } = useProject();
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [dataLoading, setDataLoading] = useState(false);

  const loadDashboard = useCallback(async () => {
    if (!projectId) return;
    setDataLoading(true);
    setError(null);
    try {
      const response = await getDashboard(projectId);
      setData(response);
    } catch (err) {
      console.error(err);
      setError("Failed to load dashboard data");
    } finally {
      setDataLoading(false);
    }
  }, [projectId]);

  useEffect(() => {
    if (projectId) loadDashboard();
  }, [projectId, loadDashboard]);

  if (projectLoading || dataLoading) {
    return (
      <div className="loading-state">
        <div className="spinner" />
        <p>Loading your security overview...</p>
      </div>
    );
  }

  if (!hasProjects) {
    return (
      <div className="empty-state">
        <div className="empty-state-icon"><FolderOpen size={28} /></div>
        <h3>No projects yet</h3>
        <p>Create your first project to start monitoring prompt security threats.</p>
        <button className="btn btn-primary" onClick={() => navigate("/projects")}>
          Create Project
        </button>
      </div>
    );
  }

  if (error) {
    return (
      <div className="empty-state">
        <div className="empty-state-icon"><ShieldAlert size={28} /></div>
        <h3>Error loading dashboard</h3>
        <p>{error}</p>
        <button className="btn btn-primary" onClick={loadDashboard}>Retry</button>
      </div>
    );
  }

  if (!data) return null;

  return (
    <div>
      <div className="page-header" style={{ marginBottom: 24 }}>
        <h1>Security Overview</h1>
        <p>
          {selectedProject
            ? `Monitoring threats for "${selectedProject.name}"`
            : "Real-time threat intelligence and prompt security monitoring"}
        </p>
      </div>

      <motion.div
        className="stats-grid"
        variants={container}
        initial="hidden"
        animate="show"
      >
        {statConfig.map((stat) => {
          const Icon = stat.icon;
          const value = data[stat.key];
          return (
            <motion.div key={stat.key} variants={item}>
              <div className={`glass-card stat-card ${stat.color}`}>
                <div className="glass-card-header">
                  <h3>{stat.label}</h3>
                  <Icon size={18} color={`var(--status-${stat.color})`} />
                </div>
                <div className="card-value">{value ?? "-"}</div>
                <div className="card-subtitle">
                  {stat.key === "total_threats"
                    ? "All detected threats"
                    : stat.key === "blocked"
                    ? "Successfully blocked"
                    : `${stat.label.toLowerCase()} severity alerts`}
                </div>
              </div>
            </motion.div>
          );
        })}

        <motion.div variants={item}>
          <SecurityScoreCard score={data.security_score ?? 100} />
        </motion.div>
      </motion.div>
    </div>
  );
}

export default Dashboard;
