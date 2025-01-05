import { HomeCareTable } from "@/components/HomeCareTable"
import { Button } from "@/components/ui/button"
import Link from "next/link"

export default function HomeCarePage() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Home Care Services</h1>
        <Button asChild>
          <Link href="/home-care/new">Add Home Care</Link>
        </Button>
      </div>
      <HomeCareTable />
    </div>
  )
}
