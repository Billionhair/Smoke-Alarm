import React from "react";
import { Navigate } from "react-router-dom";

interface TrialGuardProps {
  children: React.ReactElement;
}

export function TrialGuard({ children }: TrialGuardProps) {
  const active =
    typeof window !== "undefined" &&
    window.localStorage.getItem("trialActive") === "true";
  if (!active) {
    return <Navigate to="/pricing" replace />;
  }
  return children;
}
