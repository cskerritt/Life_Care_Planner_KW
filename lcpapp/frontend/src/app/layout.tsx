import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { SidebarProvider } from "@/components/ui/sidebar"
import { NavBar } from "@/components/NavBar"

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Life Care Plan Software',
  description: 'Comprehensive Life Care Planning Software',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <SidebarProvider>
          <div className="flex flex-col min-h-screen">
            <NavBar />
            <main className="flex-1 p-6">
              {children}
            </main>
          </div>
        </SidebarProvider>
      </body>
    </html>
  )
}
