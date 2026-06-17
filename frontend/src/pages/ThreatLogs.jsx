import { useEffect, useState, useCallback } from "react";
import { ShieldAlert, AlertTriangle, FolderOpen } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { getThreatLogs } from "../services/threatService";
import { useProject } from "../context/ProjectContext";

const severityBadge = {
  CRITICAL: "badge-critical",
  HIGH: "badge-high",
  MEDIUM: "badge-medium",
  LOW: "badge-low",
};

function ThreatLogs() {
  const navigate = useNavigate();
  const { projectId, hasProjects, loading: projectLoading } = useProject();

  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadLogs = useCallback(async () => {
    if (!projectId) return;
    try {
      const response = await getThreatLogs(projectId);
      setLogs(response);
    } catch (err) {
      console.error(err);
      setError("Failed to load threat logs");
    } finally {
      setLoading(false);
    }
  }, [projectId]);

  useEffect(() => {
    setLoading(true);
    setError(null);
    if (projectId) loadLogs();
  }, [projectId, loadLogs]);

  if (projectLoading || loading) {
    return (
      <div className="loading-state">
        <div className="spinner" />
        <p>Loading threat logs...</p>
      </div>
    );
  }

  if (!hasProjects) {
    return (
      <div className="empty-state">
        <div className="empty-state-icon"><FolderOpen size={28} /></div>
        <h3>No projects yet</h3>
        <p>Create a project first to view threat logs.</p>
        <button className="btn btn-primary" onClick={() => navigate("/projects")}>
          Create Project
        </button>
      </div>
    );
  }

  if (error) {
    return (
      <div className="empty-state">
        <div className="empty-state-icon"><AlertTriangle size={28} /></div>
        <h3>Error</h3>
        <p>{error}</p>
        <button className="btn btn-primary" onClick={loadLogs}>Retry</button>
      </div>
    );
  }

  return (
    <div>
      <div className="page-header">
        <h1>Threat Logs</h1>
        <p>Detailed audit trail of all scanned prompts and security events</p>
      </div>

      {logs.length === 0 ? (
        <div className="empty-state">
          <div className="empty-state-icon"><ShieldAlert size={28} /></div>
          <h3>No threats detected</h3>
          <p>Your prompts are clean. Threat logs will appear here when security events are detected.</p>
        </div>
      ) : (
        <div className="table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Severity</th>
                <th>Risk Score</th>
                <th>Action</th>
                <th>Prompt</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {logs.map((log, index) => (
                <motion.tr
                  key={log.id}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.03 }}
                >
                  <td style={{ color: "var(--text-muted)", fontFamily: "var(--font-mono)", fontSize: 13 }}>
                    #{log.id}
                  </td>
                  <td>
                    <span className={`badge ${severityBadge[log.severity] || ""}`}>
                      {log.severity}
                    </span>
                  </td>
                  <td>
                    <span style={{
                      fontFamily: "var(--font-mono)",
                      fontWeight: 600,
                      color: log.risk_score >= 70 ? "var(--status-critical)"
                        : log.risk_score >= 40 ? "var(--status-high)"
                        : "var(--status-low)"
                    }}>
                      {log.risk_score}
                    </span>
                  </td>
                  <td>
                    <span className={`badge ${log.action === "BLOCK" ? "badge-critical" : "badge-low"}`}>
                      {log.action}
                    </span>
                  </td>
                  <td style={{ maxWidth: 250 }} className="truncate">
                    {log.prompt}
                  </td>
                  <td style={{ color: "var(--text-muted)", fontSize: 13, whiteSpace: "nowrap" }}>
                    {new Date(log.created_at).toLocaleString()}
                  </td>
                </motion.tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default ThreatLogs;
