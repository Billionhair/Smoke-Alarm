import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import "@testing-library/jest-dom/vitest";
import React from "react";
import App from "../App";

describe("App", () => {
  it("renders welcome message", () => {
    render(<App />);
    expect(screen.getByText(/Smoke Alarm Console/)).toBeInTheDocument();
  });
});
