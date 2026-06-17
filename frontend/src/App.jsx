import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { AnimatePresence } from "framer-motion";
import { ToastProvider } from "./context/ToastContext";
import { ProjectProvider } from "./context/ProjectContext";
import ProtectedRoute from "./components/ProtectedRoute";
import AppShell from "./components/AppShell";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Projects from "./pages/Projects";
import ApiKeys from "./pages/ApiKeys";
import PromptScanner from "./pages/PromptScanner";
import ThreatLogs from "./pages/ThreatLogs";
import Settings from "./pages/Settings";

function ProtectedLayout({ title, children }) {
  return (
    <ProtectedRoute>
      <ProjectProvider>
        <AppShell title={title}>{children}</AppShell>
      </ProjectProvider>
    </ProtectedRoute>
  );
}

function App() {
  return (
    <BrowserRouter>
      <ToastProvider>
        <AnimatePresence mode="wait">
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />

            <Route path="/dashboard" element={<ProtectedLayout title="Security Overview"><Dashboard /></ProtectedLayout>} />
            <Route path="/projects" element={<ProtectedLayout title="Projects"><Projects /></ProtectedLayout>} />
            <Route path="/api-keys" element={<ProtectedLayout title="API Keys"><ApiKeys /></ProtectedLayout>} />
            <Route path="/prompt-scanner" element={<ProtectedLayout title="Prompt Scanner"><PromptScanner /></ProtectedLayout>} />
            <Route path="/threat-logs" element={<ProtectedLayout title="Threat Logs"><ThreatLogs /></ProtectedLayout>} />
            <Route path="/settings" element={<ProtectedLayout title="Settings"><Settings /></ProtectedLayout>} />
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </Routes>
        </AnimatePresence>
      </ToastProvider>
    </BrowserRouter>
  );
}

export default App;
