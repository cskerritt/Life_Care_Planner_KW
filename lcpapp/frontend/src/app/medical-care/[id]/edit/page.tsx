import { MedicalCareForm } from "@/components/MedicalCareForm"

// In a real application, you would fetch the medical care data here
const getMedicalCare = async (id: string) => {
  return {
    id,
    category: "Physician",
    description: "Primary Care Physician",
    frequency: "4 times per year",
    duration: "Lifetime",
    annualCost: 1200,
  }
}

export default async function EditMedicalCarePage({
  params,
}: {
  params: { id: string }
}) {
  const medicalCare = await getMedicalCare(params.id)

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h1 className="text-3xl font-bold">Edit Medical Care</h1>
        <p className="text-gray-500">
          Update the details of this medical care entry.
        </p>
      </div>
      <MedicalCareForm medicalCare={medicalCare} />
    </div>
  )
}
