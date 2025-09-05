import { render, screen, fireEvent, cleanup } from "@testing-library/react";
import { describe, it, expect, afterEach } from "vitest";
import "@testing-library/jest-dom/vitest";
import React from "react";
import App from "../App";

describe("Pricing and trial gating", () => {
  afterEach(() => {
    cleanup();
    window.localStorage.clear();
  });

  it("redirects to pricing when trial inactive", () => {
    window.history.pushState({}, "", "/");
    render(<App />);
    expect(screen.getByText("Pricing")).toBeInTheDocument();
  });

  it("starts trial and shows app shell", () => {
    window.history.pushState({}, "", "/pricing");
    render(<App />);
    fireEvent.click(screen.getByText("Start Free Trial"));
    expect(screen.getByText(/Smoke Alarm Console/)).toBeInTheDocument();
  });
});
