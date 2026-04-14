import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import Link from "next/link";
import "./globals.css";
import { Toaster } from "@/components/ui/sonner";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "AgentDesk – IT Admin Panel",
  description: "Autonomous IT Support Agent – Admin Dashboard",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex">
        {/* Sidebar */}
        <aside className="w-64 bg-sidebar text-sidebar-foreground border-r border-sidebar-border flex flex-col min-h-screen">
          {/* Logo */}
          <div className="p-6 border-b border-sidebar-border">
            <h1 className="text-xl font-bold tracking-tight">
              🖥️ AgentDesk
            </h1>
            <p className="text-xs text-muted-foreground mt-1">
              IT Admin Panel
            </p>
          </div>

          {/* Navigation */}
          <nav className="flex-1 p-4 space-y-1">
            <Link
              href="/users"
              className="flex items-center gap-3 px-3 py-2.5 rounded-md text-sm font-medium hover:bg-sidebar-accent hover:text-sidebar-accent-foreground transition-colors"
              data-testid="nav-users"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
              </svg>
              Users
            </Link>
            <Link
              href="/create-user"
              className="flex items-center gap-3 px-3 py-2.5 rounded-md text-sm font-medium hover:bg-sidebar-accent hover:text-sidebar-accent-foreground transition-colors"
              data-testid="nav-create-user"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
              </svg>
              Create User
            </Link>
          </nav>

          {/* Footer */}
          <div className="p-4 border-t border-sidebar-border">
            <p className="text-xs text-muted-foreground">
              Powered by AI Agent 🤖
            </p>
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 bg-background">
          {children}
        </main>

        <Toaster richColors position="top-right" />
      </body>
    </html>
  );
}
