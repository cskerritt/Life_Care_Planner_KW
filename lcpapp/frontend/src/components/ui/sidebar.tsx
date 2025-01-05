"use client"

import React, { createContext, useContext, useState } from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import {
  ChevronLeft,
  ChevronRight,
  Home,
  Users,
  Stethoscope,
  Activity,
  Pill,
  Package,
  FileText,
  Settings,
  LogOut,
} from "lucide-react"
import { Button } from "@/components/ui/button"

interface SidebarContextType {
  isExpanded: boolean
  toggleSidebar: () => void
}

const SidebarContext = createContext<SidebarContextType>({
  isExpanded: true,
  toggleSidebar: () => {},
})

interface NavItemProps {
  href: string
  icon: React.ReactNode
  label: string
}

function NavItem({ href, icon, label }: NavItemProps) {
  const pathname = usePathname()
  const { isExpanded } = useContext(SidebarContext)
  const isActive = pathname === href

  return (
    <Link
      href={href}
      className={cn(
        "flex items-center space-x-2 rounded-lg px-3 py-2 text-gray-600 transition-all hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-800",
        isActive && "bg-gray-100 text-gray-900 dark:bg-gray-800 dark:text-gray-50",
        !isExpanded && "justify-center px-2"
      )}
    >
      {React.cloneElement(icon as React.ReactElement, {
        className: cn(
          "h-5 w-5",
          isActive && "text-gray-900 dark:text-gray-50"
        ),
      })}
      {isExpanded && <span>{label}</span>}
    </Link>
  )
}

export function SidebarProvider({ children }: { children: React.ReactNode }) {
  const [isExpanded, setIsExpanded] = useState(true)

  const toggleSidebar = () => {
    setIsExpanded(!isExpanded)
  }

  return (
    <SidebarContext.Provider value={{ isExpanded, toggleSidebar }}>
      <div className="flex min-h-screen">
        <aside
          className={cn(
            "flex h-screen flex-col border-r bg-white dark:bg-gray-900 transition-all duration-300",
            isExpanded ? "w-64" : "w-16"
          )}
        >
          <div className="flex h-16 items-center justify-between px-4">
            {isExpanded && (
              <span className="text-lg font-semibold">Life Care Planner</span>
            )}
            <Button
              variant="ghost"
              size="icon"
              onClick={toggleSidebar}
              className="ml-auto"
            >
              {isExpanded ? (
                <ChevronLeft className="h-4 w-4" />
              ) : (
                <ChevronRight className="h-4 w-4" />
              )}
            </Button>
          </div>
          <nav className="flex-1 space-y-1 p-2">
            <NavItem href="/" icon={<Home />} label="Dashboard" />
            <NavItem href="/patients" icon={<Users />} label="Patients" />
            <NavItem
              href="/physician-services"
              icon={<Stethoscope />}
              label="Physician Services"
            />
            <NavItem href="/therapies" icon={<Activity />} label="Therapies" />
            <NavItem
              href="/medications"
              icon={<Pill />}
              label="Medications"
            />
            <NavItem
              href="/equipment"
              icon={<Package />}
              label="Equipment"
            />
            <NavItem href="/reports" icon={<FileText />} label="Reports" />
          </nav>
          <div className="border-t p-2">
            <NavItem
              href="/settings"
              icon={<Settings />}
              label="Settings"
            />
            <button
              className={cn(
                "flex w-full items-center space-x-2 rounded-lg px-3 py-2 text-gray-600 transition-all hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-800",
                !isExpanded && "justify-center px-2"
              )}
            >
              <LogOut className="h-5 w-5" />
              {isExpanded && <span>Logout</span>}
            </button>
          </div>
        </aside>
        <main className="flex-1 overflow-y-auto bg-gray-50 dark:bg-gray-950 p-8">
          {children}
        </main>
      </div>
    </SidebarContext.Provider>
  )
}
