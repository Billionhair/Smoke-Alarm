import { render, screen, fireEvent, cleanup } from "@testing-library/react";
import { describe, it, expect, afterEach, beforeEach } from "vitest";
import "@testing-library/jest-dom/vitest";
import React from "react";
import App from "../App";

describe("App", () => {
  beforeEach(() => {
    window.localStorage.setItem("trialActive", "true");
  });
  afterEach(() => {
    cleanup();
    window.localStorage.clear();
  });

  it("renders navigation and search", () => {
    window.history.pushState({}, "", "/");
    render(<App />);
    expect(screen.getByText("Dashboard")).toBeInTheDocument();
    expect(screen.getByLabelText("Search")).toBeInTheDocument();
  });

  it("provides a skip link", () => {
    window.history.pushState({}, "", "/");
    render(<App />);
    const link = screen.getByText("Skip to content");
    expect(link).toHaveAttribute("href", "#main");
  });

  it("toggles theme", () => {
    window.history.pushState({}, "", "/");
    render(<App />);
    const button = screen.getByLabelText("Toggle theme");
    expect(document.documentElement.getAttribute("data-theme")).toBe("dark");
    fireEvent.click(button);
    expect(document.documentElement.getAttribute("data-theme")).toBe("light");
  });

  it("renders client portal dashboard", () => {
    window.history.pushState({}, "", "/client");
    render(<App />);
    expect(screen.getByText("Client Dashboard")).toBeInTheDocument();
  });

  it("renders welcome message", () => {
    window.history.pushState({}, "", "/");
    render(<App />);
    expect(screen.getByText(/Smoke Alarm Console/)).toBeInTheDocument();
  });
});
