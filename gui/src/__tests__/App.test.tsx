import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import "@testing-library/jest-dom/vitest";
import React from "react";
import App from "../App";

describe("App", () => {
 codex/update-readme.md-with-documentation-and-examples-5n26tf
  it("renders navigation and search", () => {
    render(<App />);
    expect(screen.getByText("Dashboard")).toBeInTheDocument();
    expect(screen.getByLabelText("Search")).toBeInTheDocument();
  });

  it("renders client portal dashboard", () => {
    window.history.pushState({}, "", "/client");
    render(<App />);
    expect(screen.getByText("Client Dashboard")).toBeInTheDocument();

  it("renders welcome message", () => {
    render(<App />);
    expect(screen.getByText(/Smoke Alarm Console/)).toBeInTheDocument();
 main
  });
});
