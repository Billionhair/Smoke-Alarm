import React from "react";
import { Sun, Moon } from "lucide-react";
import { useTheme } from "./ThemeProvider";

export function TopBar() {
  const { theme, toggle } = useTheme();
  return (
    <header className="flex items-center justify-between border-b border-gray-700 p-4">
      <input
        type="text"
        aria-label="Search"
        placeholder="Search..."
        className="bg-gray-800 text-white rounded px-2 py-1 w-64 focus:outline-none focus:ring"
      />
      <div className="flex items-center gap-2">
        <button
          type="button"
          className="bg-gray-700 text-white px-3 py-1 rounded"
        >
          Command
        </button>
        <button
          type="button"
          aria-label="Toggle theme"
          onClick={toggle}
          className="bg-gray-700 text-white p-1 rounded"
        >
          {theme === "dark" ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
        </button>
      </div>
    </header>
  );
}
