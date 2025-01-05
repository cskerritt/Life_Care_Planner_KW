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
    message: "Equipment name must be at least 2 characters.",
  }),
  type: z.string().min(2, {
    message: "Equipment type must be at least 2 characters.",
  }),
  frequency: z.string().min(1, {
    message: "Frequency is required.",
  }),
  replacementSchedule: z.string().min(1, {
    message: "Replacement schedule is required.",
  }),
  annualCost: z.coerce.number().min(0, {
    message: "Annual cost must be a positive number.",
  }),
})

export function EquipmentForm({ equipment }: { equipment?: any }) {
  const router = useRouter()
  const [isLoading, setIsLoading] = useState(false)

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: equipment?.name || "",
      type: equipment?.type || "",
      frequency: equipment?.frequency || "",
      replacementSchedule: equipment?.replacementSchedule || "",
      annualCost: equipment?.annualCost || 0,
    },
  })

  async function onSubmit(values: z.infer<typeof formSchema>) {
    setIsLoading(true)
    
    try {
      // Here you would typically make an API call to save the equipment
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      toast({
        title: equipment ? "Equipment Updated" : "Equipment Created",
        description: "The equipment has been saved successfully.",
      })
      
      router.push("/equipment")
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
              <FormLabel>Equipment Name</FormLabel>
              <FormControl>
                <Input placeholder="Wheelchair" {...field} />
              </FormControl>
              <FormDescription>
                Enter the name of the equipment.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="type"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Equipment Type</FormLabel>
              <FormControl>
                <Input placeholder="Mobility" {...field} />
              </FormControl>
              <FormDescription>
                Enter the type of equipment.
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
                <Input placeholder="One-time purchase" {...field} />
              </FormControl>
              <FormDescription>
                Enter how often the equipment is needed.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="replacementSchedule"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Replacement Schedule</FormLabel>
              <FormControl>
                <Input placeholder="Every 5 years" {...field} />
              </FormControl>
              <FormDescription>
                Enter the replacement schedule for the equipment.
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
                Enter the annual cost of the equipment.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit" className="w-full" disabled={isLoading}>
          {isLoading ? "Saving..." : (equipment ? "Update Equipment" : "Add Equipment")}
        </Button>
      </form>
    </Form>
  )
}
