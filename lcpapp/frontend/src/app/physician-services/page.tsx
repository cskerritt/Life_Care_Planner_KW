import { PhysicianServicesTable } from "@/components/PhysicianServicesTable"
import { Button } from "@/components/ui/button"
import Link from "next/link"

export default function PhysicianServicesPage() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Physician Services</h1>
        <Link href="/physician-services/new">
          <Button>Add New Service</Button>
        </Link>
      </div>
      <PhysicianServicesTable />
    </div>
  )
}
