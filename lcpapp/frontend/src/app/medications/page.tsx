import { MedicationsTable } from "@/components/MedicationsTable"
import { Button } from "@/components/ui/button"
import Link from "next/link"

export default function MedicationsPage() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Medications</h1>
        <Button asChild>
          <Link href="/medications/new">Add Medication</Link>
        </Button>
      </div>
      <MedicationsTable />
    </div>
  )
}
