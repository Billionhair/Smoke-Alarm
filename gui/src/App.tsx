import React from "react";
codex/update-readme.md-with-documentation-and-examples-9jhv6i
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AppShell } from "./components/AppShell";
import { ClientPortal } from "./components/ClientPortal";
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
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );

 codex/update-readme.md-with-documentation-and-examples-5n26tf
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AppShell } from "./components/AppShell";
import { ClientPortal } from "./components/ClientPortal";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<AppShell />} />
        <Route path="/client" element={<ClientPortal />} />
      </Routes>
    </BrowserRouter>
  );

import { AppShell } from "./components/AppShell";

export default function App() {
  return <AppShell />;
 main
 main
}
