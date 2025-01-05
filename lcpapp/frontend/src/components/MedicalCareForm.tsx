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
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { toast } from "@/components/ui/use-toast"

const formSchema = z.object({
  category: z.string().min(1, {
    message: "Please select a category.",
  }),
  description: z.string().min(2, {
    message: "Description must be at least 2 characters.",
  }),
  frequency: z.string().min(2, {
    message: "Frequency must be at least 2 characters.",
  }),
  duration: z.string().min(2, {
    message: "Duration must be at least 2 characters.",
  }),
  annualCost: z.coerce.number().min(0, {
    message: "Annual cost must be a positive number.",
  }),
})

export function MedicalCareForm({ medicalCare }: { medicalCare?: any }) {
  const router = useRouter()
  const [isLoading, setIsLoading] = useState(false)

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      category: medicalCare?.category || "",
      description: medicalCare?.description || "",
      frequency: medicalCare?.frequency || "",
      duration: medicalCare?.duration || "",
      annualCost: medicalCare?.annualCost || 0,
    },
  })

  async function onSubmit(values: z.infer<typeof formSchema>) {
    setIsLoading(true)
    
    try {
      // Here you would typically make an API call to save the medical care
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      toast({
        title: medicalCare ? "Medical Care Updated" : "Medical Care Created",
        description: "The medical care has been saved successfully.",
      })
      
      router.push("/medical-care")
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
          name="category"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Category</FormLabel>
              <Select onValueChange={field.onChange} defaultValue={field.value}>
                <FormControl>
                  <SelectTrigger>
                    <SelectValue placeholder="Select a category" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  <SelectItem value="Physician">Physician</SelectItem>
                  <SelectItem value="Specialist">Specialist</SelectItem>
                  <SelectItem value="Therapy">Therapy</SelectItem>
                  <SelectItem value="Diagnostic">Diagnostic</SelectItem>
                </SelectContent>
              </Select>
              <FormDescription>
                Select the category of medical care.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="description"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Description</FormLabel>
              <FormControl>
                <Input placeholder="Primary Care Physician" {...field} />
              </FormControl>
              <FormDescription>
                Enter a description of the medical care.
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
                <Input placeholder="4 times per year" {...field} />
              </FormControl>
              <FormDescription>
                Enter the frequency of the medical care.
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
                Enter the duration of the medical care.
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
                Enter the annual cost of the medical care.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit" className="w-full" disabled={isLoading}>
          {isLoading ? "Saving..." : (medicalCare ? "Update Medical Care" : "Add Medical Care")}
        </Button>
      </form>
    </Form>
  )
}
