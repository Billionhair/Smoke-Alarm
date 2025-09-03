import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AppShell } from "./components/AppShell";
import { ClientPortal } from "./components/ClientPortal";
import { AdminPanel } from "./components/AdminPanel";
import { ThemeProvider } from "./components/ThemeProvider";

export default function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <a
          href="#main"
          className="sr-only focus:not-sr-only focus:absolute focus:top-0 focus:left-0 bg-gray-700 text-white p-2"
        >
          Skip to content
        </a>
        <Routes>
          <Route path="/" element={<AppShell />} />
          <Route path="/client" element={<ClientPortal />} />
          <Route path="/admin" element={<AdminPanel />} />
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
}
