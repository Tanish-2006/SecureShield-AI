import { useEffect, useState, useCallback } from "react";
import { KeyRound, Plus, Key, FolderOpen } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { getApiKeys, createApiKey } from "../services/apiKeyService";
import { useProject } from "../context/ProjectContext";
import { useToast } from "../context/ToastContext";

function ApiKeys() {
  const navigate = useNavigate();
  const { projectId, hasProjects, loading: projectLoading } = useProject();
  const toast = useToast();

  const [keys, setKeys] = useState([]);
  const [name, setName] = useState("");
  const [provider, setProvider] = useState("");
  const [apiKey, setApiKey] = useState("");
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
  const [showForm, setShowForm] = useState(false);

  const loadKeys = useCallback(async () => {
    if (!projectId) return;
    try {
      const response = await getApiKeys(projectId);
      setKeys(response);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [projectId]);

  useEffect(() => {
    setLoading(true);
    if (projectId) loadKeys();
  }, [projectId, loadKeys]);

  const handleCreate = async () => {
    if (!name.trim() || !provider.trim() || !apiKey.trim() || !projectId) return;
    setCreating(true);
    try {
      await createApiKey({ name, provider, api_key: apiKey, project_id: projectId });
      toast("API key saved securely", "success");
      setName("");
      setProvider("");
      setApiKey("");
      setShowForm(false);
      loadKeys();
    } catch (err) {
      toast(err.message || "Failed to save API key", "error");
    } finally {
      setCreating(false);
    }
  };

  if (projectLoading || loading) {
    return (
      <div className="loading-state">
        <div className="spinner" />
        <p>Loading API keys...</p>
      </div>
    );
  }

  if (!hasProjects) {
    return (
      <div className="empty-state">
        <div className="empty-state-icon"><FolderOpen size={28} /></div>
        <h3>No projects yet</h3>
        <p>Create a project first to manage API keys.</p>
        <button className="btn btn-primary" onClick={() => navigate("/projects")}>
          Create Project
        </button>
      </div>
    );
  }

  return (
    <div>
      <div className="page-header">
        <div className="flex items-center justify-between">
          <div>
            <h1>API Keys</h1>
            <p>Securely manage your third-party API credentials</p>
          </div>
          <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
            <Plus size={16} />
            Add API Key
          </button>
        </div>
      </div>

      <AnimatePresence>
        {showForm && (
          <motion.div
            className="glass-card mb-6"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
          >
            <h3 style={{ fontSize: 16, fontWeight: 600, marginBottom: 16, color: "var(--text-primary)" }}>
              Add New API Key
            </h3>
            <div className="form-group">
              <label className="form-label">Key Name</label>
              <input
                className="form-input"
                placeholder="OpenAI Production"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>
            <div className="form-group">
              <label className="form-label">Provider</label>
              <input
                className="form-input"
                placeholder="OpenAI, Anthropic, etc."
                value={provider}
                onChange={(e) => setProvider(e.target.value)}
              />
            </div>
            <div className="form-group">
              <label className="form-label">API Key</label>
              <input
                className="form-input"
                type="password"
                placeholder="sk-..."
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
              />
            </div>
            <div className="flex gap-2">
              <button
                className="btn btn-primary"
                onClick={handleCreate}
                disabled={creating || !name.trim() || !provider.trim() || !apiKey.trim()}
              >
                {creating ? "Saving..." : "Save API Key"}
              </button>
              <button className="btn btn-secondary" onClick={() => setShowForm(false)}>
                Cancel
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {keys.length === 0 ? (
        <div className="empty-state">
          <div className="empty-state-icon"><Key size={28} /></div>
          <h3>No API keys configured</h3>
          <p>Add your first API key to enable prompt scanning with your preferred AI provider</p>
          <button className="btn btn-primary" onClick={() => setShowForm(true)}>
            <Plus size={16} />
            Add API Key
          </button>
        </div>
      ) : (
        <div className="table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Provider</th>
                <th>Status</th>
                <th>Created</th>
              </tr>
            </thead>
            <tbody>
              {keys.map((key, index) => (
                <motion.tr
                  key={key.id}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.05 }}
                >
                  <td>
                    <div className="flex items-center gap-2">
                      <KeyRound size={14} color="var(--brand-blue)" />
                      <span style={{ color: "var(--text-primary)", fontWeight: 500 }}>{key.name}</span>
                    </div>
                  </td>
                  <td><span className="badge badge-low">{key.provider}</span></td>
                  <td>
                    <span className={`badge ${key.is_active ? "badge-low" : ""}`}>
                      {key.is_active ? "Active" : "Inactive"}
                    </span>
                  </td>
                  <td style={{ color: "var(--text-muted)", fontSize: 13 }}>
                    {new Date(key.created_at).toLocaleDateString()}
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

export default ApiKeys;
