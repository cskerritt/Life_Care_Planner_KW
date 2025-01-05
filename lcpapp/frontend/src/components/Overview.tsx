"use client"

import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis, Tooltip } from "recharts"

const data = [
  {
    name: "Physician",
    total: 234000,
  },
  {
    name: "Medications",
    total: 184000,
  },
  {
    name: "Surgical",
    total: 350000,
  },
  {
    name: "DME",
    total: 120000,
  },
  {
    name: "Home Care",
    total: 280000,
  },
  {
    name: "Transport",
    total: 78000,
  },
]

export function Overview() {
  return (
    <ResponsiveContainer width="100%" height={350}>
      <BarChart data={data}>
        <XAxis
          dataKey="name"
          stroke="#888888"
          fontSize={12}
          tickLine={false}
          axisLine={false}
        />
        <YAxis
          stroke="#888888"
          fontSize={12}
          tickLine={false}
          axisLine={false}
          tickFormatter={(value) => `$${value.toLocaleString()}`}
        />
        <Tooltip
          formatter={(value: number) => [`$${value.toLocaleString()}`, "Cost"]}
          labelStyle={{ color: "#888888" }}
        />
        <Bar 
          dataKey="total" 
          fill="#adfa1d" 
          radius={[4, 4, 0, 0]}
          name="Cost"
        />
      </BarChart>
    </ResponsiveContainer>
  )
}
