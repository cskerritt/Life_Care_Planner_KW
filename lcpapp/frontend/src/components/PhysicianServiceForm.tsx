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
  serviceName: z.string().min(2, {
    message: "Service name must be at least 2 characters.",
  }),
  m50: z.coerce.number().min(0),
  m75: z.coerce.number().min(0),
  p50: z.coerce.number().min(0),
  p75: z.coerce.number().min(0),
  mgaf: z.coerce.number().min(0),
  pgaf: z.coerce.number().min(0),
})

export function PhysicianServiceForm({ service }: { service?: any }) {
  const router = useRouter()
  const [isLoading, setIsLoading] = useState(false)

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      serviceName: service?.serviceName || "",
      m50: service?.m50 || 0,
      m75: service?.m75 || 0,
      p50: service?.p50 || 0,
      p75: service?.p75 || 0,
      mgaf: service?.mgaf || 1,
      pgaf: service?.pgaf || 1,
    },
  })

  async function onSubmit(values: z.infer<typeof formSchema>) {
    setIsLoading(true)
    
    try {
      // Here you would typically make an API call to save the service
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      toast({
        title: service ? "Service Updated" : "Service Created",
        description: "The physician service has been saved successfully.",
      })
      
      router.push("/physician-services")
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
          name="serviceName"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Service Name</FormLabel>
              <FormControl>
                <Input placeholder="Follow-up Visit" {...field} />
              </FormControl>
              <FormDescription>
                Enter the name of the physician service.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="m50"
          render={({ field }) => (
            <FormItem>
              <FormLabel>M50</FormLabel>
              <FormControl>
                <Input type="number" {...field} />
              </FormControl>
              <FormDescription>
                Enter the 50th percentile from MFUS.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="m75"
          render={({ field }) => (
            <FormItem>
              <FormLabel>M75</FormLabel>
              <FormControl>
                <Input type="number" {...field} />
              </FormControl>
              <FormDescription>
                Enter the 75th percentile from MFUS.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="p50"
          render={({ field }) => (
            <FormItem>
              <FormLabel>P50</FormLabel>
              <FormControl>
                <Input type="number" {...field} />
              </FormControl>
              <FormDescription>
                Enter the 50th percentile from PFR.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="p75"
          render={({ field }) => (
            <FormItem>
              <FormLabel>P75</FormLabel>
              <FormControl>
                <Input type="number" {...field} />
              </FormControl>
              <FormDescription>
                Enter the 75th percentile from PFR.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="mgaf"
          render={({ field }) => (
            <FormItem>
              <FormLabel>MGAF</FormLabel>
              <FormControl>
                <Input type="number" step="0.01" {...field} />
              </FormControl>
              <FormDescription>
                Enter the geographic adjustment factor for MFUS.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="pgaf"
          render={({ field }) => (
            <FormItem>
              <FormLabel>PGAF</FormLabel>
              <FormControl>
                <Input type="number" step="0.01" {...field} />
              </FormControl>
              <FormDescription>
                Enter the geographic adjustment factor for PFR.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit" className="w-full" disabled={isLoading}>
          {isLoading ? "Saving..." : (service ? "Update Service" : "Add Service")}
        </Button>
      </form>
    </Form>
  )
}
