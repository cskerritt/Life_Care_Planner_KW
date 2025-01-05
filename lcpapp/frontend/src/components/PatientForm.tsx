"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import * as z from "zod"

import { Button } from "@/components/ui/button"
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { toast } from "@/components/ui/use-toast"

const formSchema = z.object({
  name: z.string().min(2, {
    message: "Name must be at least 2 characters.",
  }),
  dateOfBirth: z.string().regex(/^\d{4}-\d{2}-\d{2}$/, {
    message: "Date of birth must be in the format YYYY-MM-DD.",
  }),
  dateOfInjury: z.string().regex(/^\d{4}-\d{2}-\d{2}$/, {
    message: "Date of injury must be in the format YYYY-MM-DD.",
  }),
  primaryDiagnosis: z.string().min(2, {
    message: "Primary diagnosis must be at least 2 characters.",
  }),
})

export function PatientForm({ patient }: { patient?: any }) {
  const router = useRouter()
  const [isLoading, setIsLoading] = useState(false)

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: patient?.name || "",
      dateOfBirth: patient?.dateOfBirth || "",
      dateOfInjury: patient?.dateOfInjury || "",
      primaryDiagnosis: patient?.primaryDiagnosis || "",
    },
  })

  async function onSubmit(values: z.infer<typeof formSchema>) {
    setIsLoading(true)
    
    try {
      // Here you would typically make an API call to save the patient
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      toast({
        title: patient ? "Patient Updated" : "Patient Created",
        description: "The patient has been saved successfully.",
      })
      
      router.push("/patients")
      router.refresh()
    } catch (error) {
      toast({
        title: "Error",
        description: "Something went wrong. Please try again.",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Name</FormLabel>
              <FormControl>
                <Input placeholder="John Doe" {...field} />
              </FormControl>
              <FormDescription>
                Enter the patient's full name.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="dateOfBirth"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Date of Birth</FormLabel>
              <FormControl>
                <Input type="date" {...field} />
              </FormControl>
              <FormDescription>
                Enter the patient's date of birth.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="dateOfInjury"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Date of Injury</FormLabel>
              <FormControl>
                <Input type="date" {...field} />
              </FormControl>
              <FormDescription>
                Enter the date of the patient's injury.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="primaryDiagnosis"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Primary Diagnosis</FormLabel>
              <FormControl>
                <Input placeholder="Spinal Cord Injury" {...field} />
              </FormControl>
              <FormDescription>
                Enter the patient's primary diagnosis.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit" className="w-full" disabled={isLoading}>
          {isLoading ? "Saving..." : (patient ? "Update Patient" : "Add Patient")}
        </Button>
      </form>
    </Form>
  )
}
