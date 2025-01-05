import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Overview } from "@/components/Overview"
import { RecentEntries } from "@/components/RecentEntries"
import { PatientSummary } from "@/components/PatientSummary"
import { CostBreakdown } from "@/components/CostBreakdown"
import { UpcomingAppointments } from "@/components/UpcomingAppointments"

export default function Dashboard() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Life Care Plan Dashboard</h1>
      <PatientSummary />
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Lifetime Cost</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">$12,456,789</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Annual Cost</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">$245,678</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Life Expectancy</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">78 years</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Care Categories</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">12</div>
          </CardContent>
        </Card>
      </div>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
        <Card className="col-span-4">
          <CardHeader>
            <CardTitle>Cost Overview</CardTitle>
          </CardHeader>
          <CardContent className="pl-2">
            <Overview />
          </CardContent>
        </Card>
        <Card className="col-span-3">
          <CardHeader>
            <CardTitle>Recent Entries</CardTitle>
          </CardHeader>
          <CardContent>
            <RecentEntries />
          </CardContent>
        </Card>
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        <CostBreakdown />
        <UpcomingAppointments />
      </div>
    </div>
  )
}
