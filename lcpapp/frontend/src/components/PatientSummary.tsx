"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"

interface PatientSummaryProps {
  patient?: {
    name: string
    dateOfBirth: string
    dateOfInjury: string
    primaryDiagnosis: string
    secondaryConditions?: string[]
    lifePlanDate?: string
  }
}

export function PatientSummary({ patient }: PatientSummaryProps) {
  // Calculate age
  const calculateAge = (birthDate: string) => {
    const today = new Date()
    const birth = new Date(birthDate)
    let age = today.getFullYear() - birth.getFullYear()
    const m = today.getMonth() - birth.getMonth()
    if (m < 0 || (m === 0 && today.getDate() < birth.getDate())) {
      age--
    }
    return age
  }

  // Calculate plan duration
  const calculatePlanDuration = (dateOfBirth: string) => {
    const age = calculateAge(dateOfBirth)
    return Math.max(0, 78 - age) // Using 78 as average life expectancy
  }

  // Format date for display
  const formatDate = (date: string) => {
    return new Date(date).toLocaleDateString()
  }

  if (!patient) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Patient Summary</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">No patient selected</p>
        </CardContent>
      </Card>
    )
  }

  const age = calculateAge(patient.dateOfBirth)
  const planDuration = calculatePlanDuration(patient.dateOfBirth)

  return (
    <Card>
      <CardHeader>
        <CardTitle>Patient Summary</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-sm font-medium">Name:</p>
            <p>{patient.name}</p>
          </div>
          <div>
            <p className="text-sm font-medium">Date of Birth:</p>
            <p>{formatDate(patient.dateOfBirth)}</p>
          </div>
          <div>
            <p className="text-sm font-medium">Date of Injury:</p>
            <p>{formatDate(patient.dateOfInjury)}</p>
          </div>
          <div>
            <p className="text-sm font-medium">Primary Diagnosis:</p>
            <p>{patient.primaryDiagnosis}</p>
          </div>
          {patient.secondaryConditions && patient.secondaryConditions.length > 0 && (
            <div>
              <p className="text-sm font-medium">Secondary Conditions:</p>
              <p>{patient.secondaryConditions.join(", ")}</p>
            </div>
          )}
          <div>
            <p className="text-sm font-medium">Current Age:</p>
            <p>{age} years</p>
          </div>
          {patient.lifePlanDate && (
            <div>
              <p className="text-sm font-medium">Life Care Plan Date:</p>
              <p>{formatDate(patient.lifePlanDate)}</p>
            </div>
          )}
          <div>
            <p className="text-sm font-medium">Plan Duration:</p>
            <p>{planDuration} years</p>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
