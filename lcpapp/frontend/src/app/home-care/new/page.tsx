import { HomeCareForm } from "@/components/HomeCareForm"

export default function NewHomeCarePage() {
  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h1 className="text-3xl font-bold">Add Home Care Service</h1>
        <p className="text-gray-500">
          Add a new home care service to the life care plan.
        </p>
      </div>
      <HomeCareForm />
    </div>
  )
}
