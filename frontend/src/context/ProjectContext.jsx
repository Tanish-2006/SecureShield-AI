import { createContext, useContext, useState, useEffect, useCallback } from "react";
import { getProjects } from "../services/projectService";

const STORAGE_KEY = "secureshield_selected_project_id";
const ProjectContext = createContext(null);

function getStoredProjectId() {
  try {
    const val = localStorage.getItem(STORAGE_KEY);
    if (val) {
      const parsed = parseInt(val, 10);
      if (!isNaN(parsed)) return parsed;
    }
  } catch {}
  return null;
}

function storeProjectId(id) {
  try {
    if (id) localStorage.setItem(STORAGE_KEY, String(id));
    else localStorage.removeItem(STORAGE_KEY);
  } catch {}
}

function clearStoredProjectId() {
  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch {}
}

export function ProjectProvider({ children }) {
  const [projects, setProjects] = useState([]);
  const [projectId, setProjectIdInternal] = useState(null);
  const [loading, setLoading] = useState(true);
  const [initialized, setInitialized] = useState(false);

  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;

  const setProjectId = useCallback((id) => {
    setProjectIdInternal(id);
    if (id) storeProjectId(id);
    else clearStoredProjectId();
  }, []);

  const refreshProjects = useCallback(async () => {
    if (!token) {
      setProjects([]);
      setProjectIdInternal(null);
      clearStoredProjectId();
      setLoading(false);
      setInitialized(true);
      return;
    }
    try {
      const data = await getProjects();
      setProjects(data);

      if (data.length > 0) {
        const stored = getStoredProjectId();
        const storedExists = stored && data.some((p) => p.id === stored);
        if (storedExists) {
          setProjectIdInternal(stored);
        } else {
          setProjectIdInternal(data[0].id);
          storeProjectId(data[0].id);
        }
      } else {
        setProjectIdInternal(null);
        clearStoredProjectId();
      }
    } catch {
      setProjects([]);
      setProjectIdInternal(null);
      clearStoredProjectId();
    } finally {
      setLoading(false);
      setInitialized(true);
    }
  }, [token]);

  useEffect(() => {
    setLoading(true);
    setInitialized(false);
    refreshProjects();
  }, [token]);

  const selectedProject = projects.find((p) => p.id === projectId) || null;
  const hasProjects = projects.length > 0;

  return (
    <ProjectContext.Provider
      value={{
        projects,
        projectId,
        selectedProject,
        selectProject: setProjectId,
        refreshProjects,
        hasProjects,
        loading,
        initialized,
      }}
    >
      {children}
    </ProjectContext.Provider>
  );
}

export function useProject() {
  const ctx = useContext(ProjectContext);
  if (!ctx) throw new Error("useProject must be used within a ProjectProvider");
  return ctx;
}
