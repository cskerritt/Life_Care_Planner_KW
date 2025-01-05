import { MedicalCareTable } from "@/components/MedicalCareTable"
import { Button } from "@/components/ui/button"
import Link from "next/link"

export default function MedicalCarePage() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Medical Care</h1>
        <Button asChild>
          <Link href="/medical-care/new">Add Medical Care</Link>
        </Button>
      </div>
      <MedicalCareTable />
    </div>
  )
}
