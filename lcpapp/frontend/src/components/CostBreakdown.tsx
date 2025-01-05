"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts"

const data = [
  {
    name: "Physician Services",
    value: 35000,
    color: "#0ea5e9",
  },
  {
    name: "Therapies",
    value: 45000,
    color: "#22c55e",
  },
  {
    name: "Medications",
    value: 25000,
    color: "#f59e0b",
  },
  {
    name: "Equipment",
    value: 15000,
    color: "#ec4899",
  },
  {
    name: "Other",
    value: 10000,
    color: "#8b5cf6",
  },
]

export function CostBreakdown() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Cost Breakdown</CardTitle>
      </CardHeader>
      <CardContent className="pl-2">
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={60}
              outerRadius={80}
              paddingAngle={2}
              dataKey="value"
            >
              {data.map((entry, index) => (
                <Cell key={index} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip
              content={({ active, payload }) => {
                if (active && payload && payload.length) {
                  const data = payload[0].payload
                  return (
                    <div className="rounded-lg border bg-background p-2 shadow-sm">
                      <div className="grid grid-cols-2 gap-2">
                        <div className="flex flex-col">
                          <span className="text-[0.70rem] uppercase text-muted-foreground">
                            Category
                          </span>
                          <span className="font-bold text-muted-foreground">
                            {data.name}
                          </span>
                        </div>
                        <div className="flex flex-col">
                          <span className="text-[0.70rem] uppercase text-muted-foreground">
                            Amount
                          </span>
                          <span className="font-bold">
                            ${data.value.toLocaleString()}
                          </span>
                        </div>
                      </div>
                    </div>
                  )
                }
                return null
              }}
            />
          </PieChart>
        </ResponsiveContainer>
        <div className="grid grid-cols-2 gap-4 mt-4">
          {data.map((item) => (
            <div key={item.name} className="flex items-center">
              <div
                className="w-3 h-3 rounded-full mr-2"
                style={{ backgroundColor: item.color }}
              />
              <div className="space-x-2">
                <span className="text-sm font-medium">{item.name}</span>
                <span className="text-sm text-muted-foreground">
                  ${item.value.toLocaleString()}
                </span>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
