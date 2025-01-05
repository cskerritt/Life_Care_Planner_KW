import { PatientForm } from "@/components/PatientForm"

export default function NewPatientPage() {
  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h1 className="text-3xl font-bold">Add Patient</h1>
        <p className="text-gray-500">
          Add a new patient to the life care plan.
        </p>
      </div>
      <PatientForm />
    </div>
  )
}
