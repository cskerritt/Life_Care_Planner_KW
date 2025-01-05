import { PatientsTable } from "@/components/PatientsTable"
import { Button } from "@/components/ui/button"
import Link from "next/link"

export default function PatientsPage() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Patients</h1>
        <Button asChild>
          <Link href="/patients/new">Add Patient</Link>
        </Button>
      </div>
      <PatientsTable />
    </div>
  )
}
