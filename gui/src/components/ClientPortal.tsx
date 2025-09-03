import React from "react";

export function ClientPortal() {
  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 p-4">
      <h1 className="text-xl font-semibold mb-4">Client Dashboard</h1>
      <section aria-label="Property status">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-gray-300">
              <th className="p-2">Property</th>
              <th className="p-2">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr className="border-t border-gray-700">
              <td className="p-2">123 Main St</td>
              <td className="p-2">Compliant</td>
            </tr>
          </tbody>
        </table>
      </section>
    </div>
  );
}
