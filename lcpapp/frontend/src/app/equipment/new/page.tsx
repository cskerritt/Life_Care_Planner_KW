import { EquipmentForm } from "@/components/EquipmentForm"

export default function NewEquipmentPage() {
  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h1 className="text-3xl font-bold">Add Equipment</h1>
        <p className="text-gray-500">
          Add new equipment or supplies to the life care plan.
        </p>
      </div>
      <EquipmentForm />
    </div>
  )
}
