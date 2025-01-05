import { MedicationForm } from "@/components/MedicationForm"

export default function NewMedicationPage() {
  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h1 className="text-3xl font-bold">Add Medication</h1>
        <p className="text-gray-500">
          Create a new medication entry for the life care plan.
        </p>
      </div>
      <MedicationForm />
    </div>
  )
}
