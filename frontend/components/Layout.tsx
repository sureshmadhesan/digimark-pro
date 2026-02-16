import Link from "next/link";
import { ReactNode } from "react";

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen">
      <nav className="bg-white border-b p-4 flex gap-4 text-sm">
        <Link href="/">Dashboard</Link>
        <Link href="/campaign-wizard">Campaign Wizard</Link>
        <Link href="/connections">Connections</Link>
        <Link href="/billing">Billing</Link>
        <Link href="/reports">Reports</Link>
      </nav>
      <main className="max-w-5xl mx-auto p-4">{children}</main>
    </div>
  );
}
