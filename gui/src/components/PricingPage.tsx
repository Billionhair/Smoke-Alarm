import React from "react";
import { useNavigate } from "react-router-dom";

export function PricingPage() {
  const navigate = useNavigate();
  const startTrial = () => {
    window.localStorage.setItem("trialActive", "true");
    navigate("/");
  };
  return (
    <main className="min-h-screen p-4 bg-white text-gray-900">
      <h1 className="text-2xl font-bold mb-4">Pricing</h1>
      <div className="grid gap-4 md:grid-cols-3">
        <div className="border rounded p-4">
          <h2 className="text-xl font-semibold">Free Trial</h2>
          <p className="mt-2">14 days full access.</p>
          <button
            type="button"
            onClick={startTrial}
            className="mt-4 bg-blue-600 text-white px-4 py-2 rounded"
          >
            Start Free Trial
          </button>
        </div>
        <div className="border rounded p-4">
          <h2 className="text-xl font-semibold">Pro</h2>
          <p className="mt-2">$29/month after trial.</p>
        </div>
        <div className="border rounded p-4">
          <h2 className="text-xl font-semibold">Enterprise</h2>
          <p className="mt-2">Contact us for volume pricing.</p>
        </div>
      </div>
    </main>
  );
}
