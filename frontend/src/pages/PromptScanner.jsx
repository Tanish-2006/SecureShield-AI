import { useState } from "react";
import { ScanLine, Shield, AlertTriangle, Ban, CheckCircle, Loader2, FolderOpen } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { scanPrompt } from "../services/promptService";
import { useProject } from "../context/ProjectContext";
import { useToast } from "../context/ToastContext";

const severityConfig = {
  CRITICAL: { icon: Ban, color: "var(--status-critical)", badge: "badge-critical" },
  HIGH: { icon: AlertTriangle, color: "var(--status-high)", badge: "badge-high" },
  MEDIUM: { icon: Shield, color: "var(--status-medium)", badge: "badge-medium" },
  LOW: { icon: CheckCircle, color: "var(--status-low)", badge: "badge-low" },
};

function PromptScanner() {
  const navigate = useNavigate();
  const { projectId, hasProjects, loading: projectLoading } = useProject();
  const toast = useToast();

  const [prompt, setPrompt] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleScan = async () => {
    if (!prompt.trim() || !projectId) return;
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await scanPrompt(prompt, projectId);
      setResult(response);
    } catch (err) {
      const msg = err.message || "";
      if (msg.includes("Access denied") || msg.includes("403")) {
        setError("You don't have access to this project. Please select a valid project.");
      } else {
        setError(msg || "Scan failed. Please try again.");
      }
      toast("Prompt scan failed", "error");
    } finally {
      setLoading(false);
    }
  };

  if (projectLoading) {
    return (
      <div className="loading-state">
        <div className="spinner" />
        <p>Loading...</p>
      </div>
    );
  }

  if (!hasProjects) {
    return (
      <div className="empty-state">
        <div className="empty-state-icon"><FolderOpen size={28} /></div>
        <h3>No projects yet</h3>
        <p>Create a project first to start scanning prompts.</p>
        <button className="btn btn-primary" onClick={() => navigate("/projects")}>
          Create Project
        </button>
      </div>
    );
  }

  return (
    <div>
      <div className="page-header">
        <h1>Prompt Scanner</h1>
        <p>Analyze prompts for security threats, injections, and data exposure</p>
      </div>

      <div className="glass-card">
        <div className="form-group">
          <label className="form-label">Enter prompt to scan</label>
          <textarea
            className="form-textarea"
            rows={6}
            placeholder="Paste or type a prompt to analyze for potential security threats..."
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
          />
        </div>

        <div className="flex items-center gap-3">
          <button
            className="btn btn-primary"
            onClick={handleScan}
            disabled={loading || !prompt.trim()}
          >
            {loading ? (
              <>
                <Loader2 size={16} style={{ animation: "spin 0.8s linear infinite" }} />
                Scanning...
              </>
            ) : (
              <>
                <ScanLine size={16} />
                Scan Prompt
              </>
            )}
          </button>
          {result && (
            <button className="btn btn-secondary" onClick={() => { setPrompt(""); setResult(null); }}>
              Clear
            </button>
          )}
        </div>
      </div>

      {error && (
        <div className="alert alert-error mt-6">
          <AlertTriangle size={16} />
          {error}
        </div>
      )}

      <AnimatePresence>
        {result && (
          <motion.div
            className="scan-result"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.4 }}
          >
            <div className="glass-card">
              <div className="glass-card-header">
                <h3>Scan Results</h3>
                <span className={`badge ${severityConfig[result.severity]?.badge || "badge-medium"}`}>
                  {result.action}
                </span>
              </div>

              <div className="scan-result-grid">
                <div className="scan-metric">
                  <div className="scan-metric-label">Risk Score</div>
                  <div className="scan-metric-value" style={{ color: severityConfig[result.severity]?.color }}>
                    {result.risk_score}/100
                  </div>
                </div>
                <div className="scan-metric">
                  <div className="scan-metric-label">Severity</div>
                  <div className="scan-metric-value" style={{ color: severityConfig[result.severity]?.color }}>
                    {result.severity}
                  </div>
                </div>
                <div className="scan-metric">
                  <div className="scan-metric-label">Confidence</div>
                  <div className="scan-metric-value">
                    {(result.confidence * 100).toFixed(1)}%
                  </div>
                </div>
                <div className="scan-metric">
                  <div className="scan-metric-label">Action Taken</div>
                  <div className="scan-metric-value">{result.action}</div>
                </div>
              </div>

              {result.threats && result.threats.length > 0 && (
                <div style={{ marginTop: 16 }}>
                  <div className="scan-metric-label" style={{ marginBottom: 8 }}>Detected Threats</div>
                  <div className="flex gap-2" style={{ flexWrap: "wrap" }}>
                    {result.threats.map((threat, i) => (
                      <span key={i} className={`badge ${severityConfig[result.severity]?.badge || "badge-medium"}`}>
                        {threat}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default PromptScanner;
