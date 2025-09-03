import React from "react";
 codex/update-readme.md-with-documentation-and-examples-9jhv6i
=======
 codex/update-readme.md-with-documentation-and-examples-5n26tf
 main
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
 codex/update-readme.md-with-documentation-and-examples-9jhv6i
        <main id="main" className="flex-1 p-4">Welcome to Smoke Alarm Console</main>
      </div>

        <main className="flex-1 p-4">Welcome to Smoke Alarm Console</main>
      </div>


export function AppShell() {
  return (
    <div className="min-h-screen flex">
      <aside className="w-48 bg-gray-800 text-white p-4">Sidebar</aside>
      <main className="flex-1 p-4">Welcome to Smoke Alarm Console</main>
 main
 main
    </div>
  );
}
