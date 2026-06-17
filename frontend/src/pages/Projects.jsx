import { useEffect, useState } from "react";
import { FolderKanban, Plus, FolderOpen, CheckCircle } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { getProjects, createProject } from "../services/projectService";
import { useProject } from "../context/ProjectContext";
import { useToast } from "../context/ToastContext";

function Projects() {
  const { projectId, selectProject, refreshProjects } = useProject();
  const toast = useToast();

  const [projects, setProjects] = useState([]);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    try {
      const response = await getProjects();
      setProjects(response);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async () => {
    if (!name.trim()) return;
    setCreating(true);
    try {
      const newProject = await createProject({ name, description });
      toast("Project created successfully", "success");
      setName("");
      setDescription("");
      setShowForm(false);
      await loadProjects();
      selectProject(newProject.id);
      await refreshProjects();
    } catch (err) {
      toast(err.message || "Failed to create project", "error");
    } finally {
      setCreating(false);
    }
  };

  if (loading) {
    return (
      <div className="loading-state">
        <div className="spinner" />
        <p>Loading projects...</p>
      </div>
    );
  }

  return (
    <div>
      <div className="page-header">
        <div className="flex items-center justify-between">
          <div>
            <h1>Projects</h1>
            <p>Manage your security monitoring projects</p>
          </div>
          <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
            <Plus size={16} />
            New Project
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
              Create New Project
            </h3>
            <div className="form-group">
              <label className="form-label">Project Name</label>
              <input
                className="form-input"
                placeholder="My Security Project"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>
            <div className="form-group">
              <label className="form-label">Description</label>
              <textarea
                className="form-textarea"
                placeholder="Optional description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                rows={3}
              />
            </div>
            <div className="flex gap-2">
              <button className="btn btn-primary" onClick={handleCreate} disabled={creating || !name.trim()}>
                {creating ? "Creating..." : "Create Project"}
              </button>
              <button className="btn btn-secondary" onClick={() => setShowForm(false)}>
                Cancel
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {projects.length === 0 ? (
        <div className="empty-state">
          <div className="empty-state-icon"><FolderOpen size={28} /></div>
          <h3>No projects yet</h3>
          <p>Create your first project to start monitoring prompts and threats</p>
          <button className="btn btn-primary" onClick={() => setShowForm(true)}>
            <Plus size={16} />
            Create Project
          </button>
        </div>
      ) : (
        <div className="stats-grid">
          {projects.map((project, index) => (
            <motion.div
              key={project.id}
              className={`glass-card ${project.id === projectId ? "active-project" : ""}`}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.05, duration: 0.3 }}
              style={{
                cursor: "pointer",
                border: project.id === projectId ? "1px solid var(--brand-blue)" : undefined,
                position: "relative",
              }}
              onClick={() => {
                selectProject(project.id);
                refreshProjects();
              }}
            >
              {project.id === projectId && (
                <div style={{ position: "absolute", top: 12, right: 12 }}>
                  <CheckCircle size={16} color="var(--brand-blue)" />
                </div>
              )}
              <div className="glass-card-header">
                <FolderKanban size={20} color="var(--brand-blue)" />
              </div>
              <h3 style={{ fontSize: 16, fontWeight: 600, color: "var(--text-primary)", marginBottom: 4 }}>
                {project.name}
              </h3>
              <p style={{ fontSize: 13, color: "var(--text-muted)", marginBottom: 12 }}>
                {project.description || "No description"}
              </p>
              <div className="card-subtitle">
                Created {new Date(project.created_at).toLocaleDateString()}
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Projects;
