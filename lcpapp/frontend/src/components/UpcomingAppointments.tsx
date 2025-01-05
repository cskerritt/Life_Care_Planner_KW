"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export function UpcomingAppointments() {
  const appointments = [
    { id: 1, type: "Doctor's Appointment", date: "2023-06-20", time: "10:00 AM" },
    { id: 2, type: "Physical Therapy", date: "2023-06-22", time: "2:00 PM" },
    { id: 3, type: "Case Management Meeting", date: "2023-06-25", time: "11:00 AM" },
    { id: 4, type: "Occupational Therapy", date: "2023-06-27", time: "3:00 PM" },
  ]

  return (
    <Card>
      <CardHeader>
        <CardTitle>Upcoming Appointments</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-8">
          {appointments.map((appointment) => (
            <div key={appointment.id} className="flex items-center">
              <div className="ml-4 space-y-1">
                <p className="text-sm font-medium leading-none">{appointment.type}</p>
                <p className="text-sm text-muted-foreground">
                  {appointment.date} at {appointment.time}
                </p>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
