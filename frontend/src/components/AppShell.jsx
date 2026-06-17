import { useState } from "react";
import Sidebar from "./Sidebar";
import Navbar from "./Navbar";
import BottomNav from "./BottomNav";

function AppShell({ children, title }) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  return (
    <div className="app-shell">
      <Sidebar isOpen={isSidebarOpen} onClose={() => setIsSidebarOpen(false)} />
      <div className="app-main">
        <Navbar title={title} onMenu={() => setIsSidebarOpen(true)} />
        <main className="page-container">{children}</main>
      </div>
      <BottomNav />
    </div>
  );
}

export default AppShell;
