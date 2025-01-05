import { HomeCareForm } from "@/components/HomeCareForm"

// In a real application, you would fetch the home care data here
const getHomeCare = async (id: string) => {
  return {
    id,
    type: "Personal Care Assistant",
    frequency: "Daily",
    hoursPerWeek: 40,
    provider: "Home Health Agency A",
    annualCost: 50000,
  }
}

export default async function EditHomeCarePage({
  params,
}: {
  params: { id: string }
}) {
  const homeCare = await getHomeCare(params.id)

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h1 className="text-3xl font-bold">Edit Home Care Service</h1>
        <p className="text-gray-500">
          Update the details of this home care service.
        </p>
      </div>
      <HomeCareForm homeCare={homeCare} />
    </div>
  )
}
