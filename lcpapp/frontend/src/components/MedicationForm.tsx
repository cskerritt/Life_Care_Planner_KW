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
    message: "Medication name must be at least 2 characters.",
  }),
  dosage: z.string().min(1, {
    message: "Dosage is required.",
  }),
  frequency: z.string().min(1, {
    message: "Frequency is required.",
  }),
  duration: z.string().min(1, {
    message: "Duration is required.",
  }),
  annualCost: z.coerce.number().min(0, {
    message: "Annual cost must be a positive number.",
  }),
})

export function MedicationForm({ medication }: { medication?: any }) {
  const router = useRouter()
  const [isLoading, setIsLoading] = useState(false)

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: medication?.name || "",
      dosage: medication?.dosage || "",
      frequency: medication?.frequency || "",
      duration: medication?.duration || "",
      annualCost: medication?.annualCost || 0,
    },
  })

  async function onSubmit(values: z.infer<typeof formSchema>) {
    setIsLoading(true)
    
    try {
      // Here you would typically make an API call to save the medication
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      toast({
        title: medication ? "Medication Updated" : "Medication Created",
        description: "The medication has been saved successfully.",
      })
      
      router.push("/medications")
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
              <FormLabel>Medication Name</FormLabel>
              <FormControl>
                <Input placeholder="Aspirin" {...field} />
              </FormControl>
              <FormDescription>
                Enter the name of the medication.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="dosage"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Dosage</FormLabel>
              <FormControl>
                <Input placeholder="81mg" {...field} />
              </FormControl>
              <FormDescription>
                Enter the dosage of the medication.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="frequency"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Frequency</FormLabel>
              <FormControl>
                <Input placeholder="Once daily" {...field} />
              </FormControl>
              <FormDescription>
                Enter how often the medication should be taken.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="duration"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Duration</FormLabel>
              <FormControl>
                <Input placeholder="Lifetime" {...field} />
              </FormControl>
              <FormDescription>
                Enter the duration of the medication.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="annualCost"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Annual Cost</FormLabel>
              <FormControl>
                <Input type="number" placeholder="0" {...field} />
              </FormControl>
              <FormDescription>
                Enter the annual cost of the medication.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit" className="w-full" disabled={isLoading}>
          {isLoading ? "Saving..." : (medication ? "Update Medication" : "Add Medication")}
        </Button>
      </form>
    </Form>
  )
}
