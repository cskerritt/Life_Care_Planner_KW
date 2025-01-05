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
    message: "Therapy type must be at least 2 characters.",
  }),
  frequency: z.string().min(1, {
    message: "Frequency is required.",
  }),
  duration: z.string().min(1, {
    message: "Duration is required.",
  }),
  provider: z.string().min(2, {
    message: "Provider name must be at least 2 characters.",
  }),
  annualCost: z.coerce.number().min(0, {
    message: "Annual cost must be a positive number.",
  }),
})

export function TherapyForm({ therapy }: { therapy?: any }) {
  const router = useRouter()
  const [isLoading, setIsLoading] = useState(false)

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      type: therapy?.type || "",
      frequency: therapy?.frequency || "",
      duration: therapy?.duration || "",
      provider: therapy?.provider || "",
      annualCost: therapy?.annualCost || 0,
    },
  })

  async function onSubmit(values: z.infer<typeof formSchema>) {
    setIsLoading(true)
    
    try {
      // Here you would typically make an API call to save the therapy
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      toast({
        title: therapy ? "Therapy Updated" : "Therapy Created",
        description: "The therapy has been saved successfully.",
      })
      
      router.push("/therapies")
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
              <FormLabel>Therapy Type</FormLabel>
              <FormControl>
                <Input placeholder="Physical Therapy" {...field} />
              </FormControl>
              <FormDescription>
                Enter the type of therapy.
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
                <Input placeholder="3 times per week" {...field} />
              </FormControl>
              <FormDescription>
                Enter how often the therapy is needed.
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
                <Input placeholder="6 months" {...field} />
              </FormControl>
              <FormDescription>
                Enter the duration of the therapy.
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
                <Input placeholder="ABC Rehabilitation Center" {...field} />
              </FormControl>
              <FormDescription>
                Enter the name of the therapy provider.
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
                Enter the annual cost of the therapy.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit" className="w-full" disabled={isLoading}>
          {isLoading ? "Saving..." : (therapy ? "Update Therapy" : "Add Therapy")}
        </Button>
      </form>
    </Form>
  )
}
