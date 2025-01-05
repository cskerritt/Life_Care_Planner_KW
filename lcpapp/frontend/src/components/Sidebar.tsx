import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Home, FileText, Users, Stethoscope, Pill, Activity, Truck, HomeIcon, DollarSign, Calendar, Briefcase, GraduationCap, ClipboardList } from 'lucide-react'
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import { cn } from "@/lib/utils"

const sidebarItems = [
  { href: '/dashboard', icon: Home, label: 'Dashboard' },
  { href: '/life-care-plans', icon: FileText, label: 'Life Care Plans' },
  { href: '/patients', icon: Users, label: 'Patients' },
  { href: '/medical-care', icon: Stethoscope, label: 'Medical Care' },
  { href: '/medications', icon: Pill, label: 'Medications' },
  { href: '/therapies', icon: Activity, label: 'Therapies' },
  { href: '/equipment', icon: Truck, label: 'Equipment' },
  { href: '/home-care', icon: HomeIcon, label: 'Home Care' },
  { href: '/vocational', icon: Briefcase, label: 'Vocational' },
  { href: '/education', icon: GraduationCap, label: 'Education' },
  { href: '/cost-projections', icon: DollarSign, label: 'Cost Projections' },
  { href: '/calendar', icon: Calendar, label: 'Calendar' },
  { href: '/reports', icon: ClipboardList, label: 'Reports' },
]

export function Sidebar() {
  const pathname = usePathname()

  return (
    <TooltipProvider>
      <div className="w-16 bg-gray-100 h-screen p-2">
        <nav className="space-y-2">
          {sidebarItems.map((item) => (
            <Tooltip key={item.href}>
              <TooltipTrigger asChild>
                <Link
                  href={item.href}
                  className={cn(
                    "flex items-center justify-center w-12 h-12 rounded-lg hover:bg-gray-200",
                    pathname === item.href ? "bg-gray-200" : ""
                  )}
                >
                  <item.icon size={24} />
                </Link>
              </TooltipTrigger>
              <TooltipContent side="right">
                <p>{item.label}</p>
              </TooltipContent>
            </Tooltip>
          ))}
        </nav>
      </div>
    </TooltipProvider>
  )
}
