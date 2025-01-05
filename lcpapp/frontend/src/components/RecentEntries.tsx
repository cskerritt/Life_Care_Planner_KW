"use client"

import { Avatar, AvatarFallback } from "@/components/ui/avatar"

interface Entry {
  id: number
  type: string
  name: string
  cost: string
}

export function RecentEntries() {
  const entries: Entry[] = [
    { id: 1, type: "Physician", name: "Dr. Follow-up", cost: "$250" },
    { id: 2, type: "Medication", name: "Pain Reliever", cost: "$50" },
    { id: 3, type: "DME", name: "Wheelchair", cost: "$1,200" },
    { id: 4, type: "Home Care", name: "Nursing Visit", cost: "$150" },
    { id: 5, type: "Transport", name: "Medical Appointment", cost: "$75" },
  ]

  return (
    <div className="space-y-8">
      {entries.map((entry) => (
        <div key={entry.id} className="flex items-center">
          <Avatar className="h-9 w-9">
            <AvatarFallback>{entry.type[0]}</AvatarFallback>
          </Avatar>
          <div className="ml-4 space-y-1">
            <p className="text-sm font-medium leading-none">{entry.name}</p>
            <p className="text-sm text-muted-foreground">
              {entry.type}
            </p>
          </div>
          <div className="ml-auto font-medium">{entry.cost}</div>
        </div>
      ))}
    </div>
  )
}
