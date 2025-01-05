import { EquipmentForm } from "@/components/EquipmentForm"

// In a real application, you would fetch the equipment data here
const getEquipment = async (id: string) => {
  return {
    id,
    name: "Wheelchair",
    type: "Mobility",
    frequency: "One-time purchase",
    replacementSchedule: "Every 5 years",
    annualCost: 2000,
  }
}

export default async function EditEquipmentPage({
  params,
}: {
  params: { id: string }
}) {
  const equipment = await getEquipment(params.id)

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h1 className="text-3xl font-bold">Edit Equipment</h1>
        <p className="text-gray-500">
          Update the details of this equipment.
        </p>
      </div>
      <EquipmentForm equipment={equipment} />
    </div>
  )
}
