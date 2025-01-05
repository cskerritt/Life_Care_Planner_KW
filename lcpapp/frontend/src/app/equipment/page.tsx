import { EquipmentTable } from "@/components/EquipmentTable"
import { Button } from "@/components/ui/button"
import Link from "next/link"

export default function EquipmentPage() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Equipment & Supplies</h1>
        <Button asChild>
          <Link href="/equipment/new">Add Equipment</Link>
        </Button>
      </div>
      <EquipmentTable />
    </div>
  )
}
