import React, { useState } from "react";
import { SidebarNav } from "./SidebarNav";
import { TopBar } from "./TopBar";

export function AppShell() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <div className="min-h-screen flex bg-gray-900 text-gray-100">
      <aside
        id="sidebar"
        className={`fixed inset-y-0 left-0 w-56 bg-gray-900 border-r border-gray-800 p-4 transition-transform transform md:relative md:translate-x-0 md:transform-none ${menuOpen ? "translate-x-0" : "-translate-x-full"}`}
      >
        <SidebarNav />
      </aside>
      {menuOpen && (
        <div
          className="fixed inset-0 bg-black/50 md:hidden"
          onClick={() => setMenuOpen(false)}
          aria-hidden="true"
        />
      )}
      <div className="flex-1 flex flex-col md:ml-56">
        <TopBar menuOpen={menuOpen} onMenuClick={() => setMenuOpen((o) => !o)} />
        <main id="main" className="flex-1 p-4">
          Welcome to Smoke Alarm Console
        </main>
      </div>
    </div>
  );
}
