import React from "react";
import { Sun, Moon, Menu } from "lucide-react";
import { useTheme } from "./ThemeProvider";

interface TopBarProps {
  onMenuClick: () => void;
  menuOpen: boolean;
}

export function TopBar({ onMenuClick, menuOpen }: TopBarProps) {
  const { theme, toggle } = useTheme();

  return (
    <header className="flex items-center justify-between border-b border-gray-700 p-4 pt-[env(safe-area-inset-top)]">
      <div className="flex items-center gap-2 flex-1">
        <button
          type="button"
          aria-label="Toggle menu"
          aria-expanded={menuOpen}
          aria-controls="sidebar"
          onClick={onMenuClick}
          className="md:hidden bg-gray-700 text-white p-1 rounded"
        >
          <Menu className="h-4 w-4" />
        </button>
        <input
          type="text"
          aria-label="Search"
          placeholder="Search..."
          className="bg-gray-800 text-white rounded px-2 py-1 w-full md:w-64 focus:outline-none focus:ring"
        />
      </div>
      <div className="flex items-center gap-2 ml-2">
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
