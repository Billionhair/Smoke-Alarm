 codex/update-readme.md-with-documentation-and-examples-9jhv6i
import { render, screen, fireEvent, cleanup } from "@testing-library/react";
import { describe, it, expect, afterEach } from "vitest";

import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
 main
import "@testing-library/jest-dom/vitest";
import React from "react";
import App from "../App";

describe("App", () => {
 codex/update-readme.md-with-documentation-and-examples-9jhv6i
  afterEach(() => cleanup());

 codex/update-readme.md-with-documentation-and-examples-5n26tf
 main
  it("renders navigation and search", () => {
    render(<App />);
    expect(screen.getByText("Dashboard")).toBeInTheDocument();
    expect(screen.getByLabelText("Search")).toBeInTheDocument();
  });

 codex/update-readme.md-with-documentation-and-examples-9jhv6i
  it("provides a skip link", () => {
    render(<App />);
    const link = screen.getByText("Skip to content");
    expect(link).toHaveAttribute("href", "#main");
  });

  it("toggles theme", () => {
    render(<App />);
    const button = screen.getByLabelText("Toggle theme");
    expect(document.documentElement.getAttribute("data-theme")).toBe("dark");
    fireEvent.click(button);
    expect(document.documentElement.getAttribute("data-theme")).toBe("light");
  });


 main
  it("renders client portal dashboard", () => {
    window.history.pushState({}, "", "/client");
    render(<App />);
    expect(screen.getByText("Client Dashboard")).toBeInTheDocument();
 codex/update-readme.md-with-documentation-and-examples-9jhv6i


  it("renders welcome message", () => {
    render(<App />);
    expect(screen.getByText(/Smoke Alarm Console/)).toBeInTheDocument();
 main
 main
  });
});
