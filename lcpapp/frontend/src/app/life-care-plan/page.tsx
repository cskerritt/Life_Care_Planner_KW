import { LifeCarePlanList } from "@/components/LifeCarePlanList"
import { Button } from "@/components/ui/button"
import Link from "next/link"

export default function LifeCarePlanPage() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Life Care Plans</h1>
        <Button asChild>
          <Link href="/life-care-plan/new">Create New Plan</Link>
        </Button>
      </div>
      <LifeCarePlanList />
    </div>
  )
}
