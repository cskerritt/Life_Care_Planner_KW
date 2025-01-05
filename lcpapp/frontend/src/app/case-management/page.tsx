import { CaseManagementTable } from "@/components/CaseManagementTable"

export default function CaseManagementPage() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Case Management</h1>
      </div>
      <CaseManagementTable />
    </div>
  )
}
