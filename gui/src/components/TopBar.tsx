import React from "react";

export function TopBar() {
  return (
    <header className="flex items-center justify-between border-b border-gray-700 p-4">
      <input
        type="text"
        aria-label="Search"
        placeholder="Search..."
        className="bg-gray-800 text-white rounded px-2 py-1 w-64 focus:outline-none focus:ring"
      />
      <button
        type="button"
        className="bg-gray-700 text-white px-3 py-1 rounded"
      >
        Command
      </button>
    </header>
  );
}
