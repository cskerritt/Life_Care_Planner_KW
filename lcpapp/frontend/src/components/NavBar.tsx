import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { cn } from "@/lib/utils"

const navItems = [
  { href: '/dashboard', label: 'Dashboard' },
  { href: '/life-care-plans', label: 'Life Care Plans' },
  { href: '/patients', label: 'Patients' },
  { href: '/medical-care', label: 'Medical Care' },
  { href: '/medications', label: 'Medications' },
  { href: '/therapies', label: 'Therapies' },
  { href: '/equipment', label: 'Equipment' },
  { href: '/home-care', label: 'Home Care' },
  { href: '/vocational', label: 'Vocational' },
  { href: '/education', label: 'Education' },
  { href: '/cost-projections', label: 'Cost Projections' },
  { href: '/calendar', label: 'Calendar' },
  { href: '/reports', label: 'Reports' },
]

export function NavBar() {
  const pathname = usePathname()

  return (
    <nav className="flex space-x-4 border-b border-gray-200 bg-white px-4 py-3 overflow-x-auto">
      {navItems.map((item) => (
        <Link
          key={item.href}
          href={item.href}
          className={cn(
            "text-sm font-medium transition-colors hover:text-primary whitespace-nowrap",
            pathname === item.href
              ? "text-primary"
              : "text-muted-foreground"
          )}
        >
          {item.label}
        </Link>
      ))}
    </nav>
  )
}
