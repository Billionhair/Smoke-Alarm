import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import "@testing-library/jest-dom/vitest";
import React from "react";
import App from "../App";

describe("App", () => {
  it("renders navigation and search", () => {
    render(<App />);
    expect(screen.getByText("Dashboard")).toBeInTheDocument();
    expect(screen.getByLabelText("Search")).toBeInTheDocument();
  });

  it("renders client portal dashboard", () => {
    window.history.pushState({}, "", "/client");
    render(<App />);
    expect(screen.getByText("Client Dashboard")).toBeInTheDocument();
  });
});
