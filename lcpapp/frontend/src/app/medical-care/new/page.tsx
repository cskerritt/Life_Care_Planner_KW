import { MedicalCareForm } from "@/components/MedicalCareForm"

export default function NewMedicalCarePage() {
  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h1 className="text-3xl font-bold">Add Medical Care</h1>
        <p className="text-gray-500">
          Create a new medical care entry for the life care plan.
        </p>
      </div>
      <MedicalCareForm />
    </div>
  )
}
