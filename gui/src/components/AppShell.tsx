import React from "react";
import { SidebarNav } from "./SidebarNav";
import { TopBar } from "./TopBar";

export function AppShell() {
  return (
    <div className="min-h-screen flex bg-gray-900 text-gray-100">
      <aside className="w-56 border-r border-gray-800 p-4">
        <SidebarNav />
      </aside>
      <div className="flex-1 flex flex-col">
        <TopBar />
        <main id="main" className="flex-1 p-4">
          Welcome to Smoke Alarm Console
        </main>
      </div>
    </div>
  );
}
