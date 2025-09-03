import React from "react";
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
}
