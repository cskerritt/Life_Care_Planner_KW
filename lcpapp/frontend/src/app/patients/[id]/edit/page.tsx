import { PatientForm } from "@/components/PatientForm"

// In a real application, you would fetch the patient data here
const getPatient = async (id: string) => {
  return {
    id,
    name: "John Doe",
    dateOfBirth: "1980-01-01",
    dateOfInjury: "2024-01-01",
    primaryDiagnosis: "Spinal Cord Injury",
  }
}

export default async function EditPatientPage({
  params,
}: {
  params: { id: string }
}) {
  const patient = await getPatient(params.id)

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h1 className="text-3xl font-bold">Edit Patient</h1>
        <p className="text-gray-500">
          Update the patient's information.
        </p>
      </div>
      <PatientForm patient={patient} />
    </div>
  )
}
