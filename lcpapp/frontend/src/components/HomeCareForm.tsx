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
  type: z.string().min(2, {
    message: "Home care type must be at least 2 characters.",
  }),
  frequency: z.string().min(1, {
    message: "Frequency is required.",
  }),
  hoursPerWeek: z.coerce.number().min(0, {
    message: "Hours per week must be a positive number.",
  }),
  provider: z.string().min(2, {
    message: "Provider name must be at least 2 characters.",
  }),
  annualCost: z.coerce.number().min(0, {
    message: "Annual cost must be a positive number.",
  }),
})

export function HomeCareForm({ homeCare }: { homeCare?: any }) {
  const router = useRouter()
  const [isLoading, setIsLoading] = useState(false)

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      type: homeCare?.type || "",
      frequency: homeCare?.frequency || "",
      hoursPerWeek: homeCare?.hoursPerWeek || 0,
      provider: homeCare?.provider || "",
      annualCost: homeCare?.annualCost || 0,
    },
  })

  async function onSubmit(values: z.infer<typeof formSchema>) {
    setIsLoading(true)
    
    try {
      // Here you would typically make an API call to save the home care
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      toast({
        title: homeCare ? "Home Care Updated" : "Home Care Created",
        description: "The home care has been saved successfully.",
      })
      
      router.push("/home-care")
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
          name="type"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Home Care Type</FormLabel>
              <FormControl>
                <Input placeholder="Personal Care Assistant" {...field} />
              </FormControl>
              <FormDescription>
                Enter the type of home care.
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
                <Input placeholder="Daily" {...field} />
              </FormControl>
              <FormDescription>
                Enter how often the home care is needed.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="hoursPerWeek"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Hours Per Week</FormLabel>
              <FormControl>
                <Input type="number" placeholder="0" {...field} />
              </FormControl>
              <FormDescription>
                Enter the number of hours per week for this home care.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="provider"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Provider</FormLabel>
              <FormControl>
                <Input placeholder="Home Health Agency A" {...field} />
              </FormControl>
              <FormDescription>
                Enter the name of the home care provider.
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
                Enter the annual cost of the home care.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit" className="w-full" disabled={isLoading}>
          {isLoading ? "Saving..." : (homeCare ? "Update Home Care" : "Add Home Care")}
        </Button>
      </form>
    </Form>
  )
}
