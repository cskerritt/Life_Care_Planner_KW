import { MedicationForm } from "@/components/MedicationForm"

// In a real application, you would fetch the medication data here
const getMedication = async (id: string) => {
  return {
    id,
    name: "Aspirin",
    dosage: "81mg",
    frequency: "Once daily",
    duration: "Lifetime",
    annualCost: 120,
  }
}

export default async function EditMedicationPage({
  params,
}: {
  params: { id: string }
}) {
  const medication = await getMedication(params.id)

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h1 className="text-3xl font-bold">Edit Medication</h1>
        <p className="text-gray-500">
          Update the details of this medication.
        </p>
      </div>
      <MedicationForm medication={medication} />
    </div>
  )
}
