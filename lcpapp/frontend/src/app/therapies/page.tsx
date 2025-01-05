import { TherapiesTable } from "@/components/TherapiesTable"
import { Button } from "@/components/ui/button"
import Link from "next/link"

export default function TherapiesPage() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Therapies</h1>
        <Link href="/therapies/new">
          <Button>Add New Therapy</Button>
        </Link>
      </div>
      <TherapiesTable />
    </div>
  )
}
