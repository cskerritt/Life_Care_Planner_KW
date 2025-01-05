"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

export function ReportGenerator() {
  const [reportType, setReportType] = useState("")
  const [patientId, setPatientId] = useState("")
  const [isGenerating, setIsGenerating] = useState(false)
  const [generatedReportUrl, setGeneratedReportUrl] = useState<string | null>(null)

  const handleGenerateReport = () => {
    setIsGenerating(true)
    try {
      // Here you would typically call an API to generate the report
      console.log(`Generating ${reportType} report for patient ${patientId}`)
      // You could then download the report or display it in the UI
      setGeneratedReportUrl("/sample-report.pdf") // This would be the actual URL from the API
    } catch (error) {
      console.error("Error generating report:", error)
    } finally {
      setIsGenerating(false)
    }
  }

  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <Card>
        <CardHeader>
          <CardTitle>Report Configuration</CardTitle>
          <CardTitle>Report Generator</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="report-type">Report Type</Label>
            <Select onValueChange={setReportType}>
              <SelectTrigger id="report-type">
                <SelectValue placeholder="Select report type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="summary">Summary Report</SelectItem>
                <SelectItem value="detailed">Detailed Report</SelectItem>
                <SelectItem value="cost-projection">Cost Projection Report</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div className="space-y-2">
            <Label htmlFor="patient-id">Patient ID</Label>
            <Select onValueChange={setPatientId}>
              <SelectTrigger id="patient-id">
                <SelectValue placeholder="Select patient" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="728ed52f">John Doe</SelectItem>
                <SelectItem value="489e1d42">Jane Smith</SelectItem>
                <SelectItem value="153e2c61">Robert Johnson</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <Button onClick={handleGenerateReport} disabled={!reportType || !patientId || isGenerating}>
            {isGenerating ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Generating Report...
              </>
            ) : (
              "Generate Report"
            )}
          </Button>
        </CardContent>
      </Card>

      {generatedReportUrl && (
        <Card>
          <CardHeader>
            <CardTitle>Generated Report</CardTitle>
            <CardDescription>
              Your report has been generated successfully.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex flex-col items-center space-y-4">
              <p className="text-center text-muted-foreground">
                Your report is ready to download.
              </p>
              <Button asChild>
                <a href={generatedReportUrl} download>
                  Download Report
                </a>
              </Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
