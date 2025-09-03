import React from "react";
import {
  Home,
  Calendar,
  Route,
  Building2,
  ClipboardCheck,
  FileText,
  MessageSquare,
  Settings,
  HelpCircle,
} from "lucide-react";

interface Item {
  label: string;
  icon: React.ComponentType<React.SVGProps<SVGSVGElement>>;
}

const items: Item[] = [
  { label: "Dashboard", icon: Home },
  { label: "Schedule", icon: Calendar },
  { label: "Routes", icon: Route },
  { label: "Properties", icon: Building2 },
  { label: "Visits", icon: ClipboardCheck },
  { label: "Invoices", icon: FileText },
  { label: "Templates", icon: FileText },
  { label: "Messaging", icon: MessageSquare },
  { label: "Settings", icon: Settings },
  { label: "Help", icon: HelpCircle },
];

export function SidebarNav() {
  return (
    <nav aria-label="Main">
      <ul className="space-y-2">
        {items.map(({ label, icon: Icon }) => (
          <li key={label}>
            <a
              href="#"
              className="flex items-center gap-2 text-sm text-gray-300 hover:text-white"
            >
              <Icon className="h-4 w-4" aria-hidden="true" />
              {label}
            </a>
          </li>
        ))}
      </ul>
    </nav>
  );
}
