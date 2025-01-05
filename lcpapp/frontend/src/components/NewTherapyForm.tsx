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
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Calendar } from "@/components/ui/calendar"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"
import { cn } from "@/lib/utils"
import { format } from "date-fns"
import { CalendarIcon } from "lucide-react"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

const formSchema = z.object({
  therapyType: z.string({
    required_error: "Please select a therapy type",
  }),
  provider: z.string().min(2, {
    message: "Provider name must be at least 2 characters.",
  }),
  specialty: z.string().min(2, {
    message: "Specialty must be at least 2 characters.",
  }),
  frequency: z.string().min(1, {
    message: "Please specify the frequency.",
  }),
  duration: z.string().min(1, {
    message: "Please specify the duration.",
  }),
  costPerSession: z.string().regex(/^\d+(\.\d{0,2})?$/, {
    message: "Please enter a valid cost (e.g., 100 or 100.50)",
  }),
  startDate: z.date({
    required_error: "Please select a start date.",
  }),
  endDate: z.date().optional(),
  location: z.string().min(2, {
    message: "Location must be at least 2 characters.",
  }),
  goals: z.string().min(10, {
    message: "Please provide therapy goals (minimum 10 characters).",
  }),
  notes: z.string().optional(),
  insuranceCoverage: z.string().optional(),
  referralRequired: z.boolean().default(false),
  preAuthRequired: z.boolean().default(false),
  equipmentNeeded: z.string().optional(),
})

type FormValues = z.infer<typeof formSchema>

const defaultValues: Partial<FormValues> = {
  therapyType: "",
  frequency: "",
  duration: "",
  costPerSession: "",
  referralRequired: false,
  preAuthRequired: false,
}

export function NewTherapyForm() {
  const router = useRouter()
  const [loading, setLoading] = useState(false)

  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues,
  })

  async function onSubmit(data: FormValues) {
    setLoading(true)
    try {
      // TODO: Implement API call to save therapy
      console.log(data)
      router.push("/therapies")
      router.refresh()
    } catch (error) {
      console.error("Error saving therapy:", error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>New Therapy Details</CardTitle>
        <CardDescription>
          Enter the details for the new therapy service.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <FormField
                control={form.control}
                name="therapyType"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Therapy Type*</FormLabel>
                    <Select onValueChange={field.onChange} defaultValue={field.value}>
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select a therapy type" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value="physical">Physical Therapy</SelectItem>
                        <SelectItem value="occupational">Occupational Therapy</SelectItem>
                        <SelectItem value="speech">Speech Therapy</SelectItem>
                        <SelectItem value="cognitive">Cognitive Therapy</SelectItem>
                        <SelectItem value="behavioral">Behavioral Therapy</SelectItem>
                        <SelectItem value="aquatic">Aquatic Therapy</SelectItem>
                        <SelectItem value="respiratory">Respiratory Therapy</SelectItem>
                        <SelectItem value="other">Other</SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="provider"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Provider Name*</FormLabel>
                    <FormControl>
                      <Input placeholder="John Smith, PT" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="specialty"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Specialty*</FormLabel>
                    <FormControl>
                      <Input placeholder="Orthopedic" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="frequency"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Frequency*</FormLabel>
                    <FormControl>
                      <Input placeholder="3 times per week" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="duration"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Duration*</FormLabel>
                    <FormControl>
                      <Input placeholder="60 minutes" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="costPerSession"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Cost per Session*</FormLabel>
                    <FormControl>
                      <Input
                        type="number"
                        step="0.01"
                        placeholder="100.00"
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="startDate"
                render={({ field }) => (
                  <FormItem className="flex flex-col">
                    <FormLabel>Start Date*</FormLabel>
                    <Popover>
                      <PopoverTrigger asChild>
                        <FormControl>
                          <Button
                            variant={"outline"}
                            className={cn(
                              "w-full pl-3 text-left font-normal",
                              !field.value && "text-muted-foreground"
                            )}
                          >
                            {field.value ? (
                              format(field.value, "PPP")
                            ) : (
                              <span>Pick a date</span>
                            )}
                            <CalendarIcon className="ml-auto h-4 w-4 opacity-50" />
                          </Button>
                        </FormControl>
                      </PopoverTrigger>
                      <PopoverContent className="w-auto p-0" align="start">
                        <Calendar
                          mode="single"
                          selected={field.value}
                          onSelect={field.onChange}
                          disabled={(date) =>
                            date < new Date("1900-01-01")
                          }
                          initialFocus
                        />
                      </PopoverContent>
                    </Popover>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="endDate"
                render={({ field }) => (
                  <FormItem className="flex flex-col">
                    <FormLabel>End Date</FormLabel>
                    <Popover>
                      <PopoverTrigger asChild>
                        <FormControl>
                          <Button
                            variant={"outline"}
                            className={cn(
                              "w-full pl-3 text-left font-normal",
                              !field.value && "text-muted-foreground"
                            )}
                          >
                            {field.value ? (
                              format(field.value, "PPP")
                            ) : (
                              <span>Pick a date</span>
                            )}
                            <CalendarIcon className="ml-auto h-4 w-4 opacity-50" />
                          </Button>
                        </FormControl>
                      </PopoverTrigger>
                      <PopoverContent className="w-auto p-0" align="start">
                        <Calendar
                          mode="single"
                          selected={field.value}
                          onSelect={field.onChange}
                          disabled={(date) =>
                            date < new Date("1900-01-01")
                          }
                          initialFocus
                        />
                      </PopoverContent>
                    </Popover>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="location"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Location*</FormLabel>
                    <FormControl>
                      <Input placeholder="123 Therapy Center Dr." {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="insuranceCoverage"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Insurance Coverage</FormLabel>
                    <FormControl>
                      <Input placeholder="80% after deductible" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>

            <FormField
              control={form.control}
              name="goals"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Therapy Goals*</FormLabel>
                  <FormControl>
                    <Textarea
                      placeholder="Enter the specific goals and expected outcomes for this therapy"
                      className="min-h-[100px]"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="equipmentNeeded"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Equipment Needed</FormLabel>
                  <FormControl>
                    <Input
                      placeholder="List any specific equipment needed for therapy"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="notes"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Additional Notes</FormLabel>
                  <FormControl>
                    <Textarea
                      placeholder="Any additional notes about the therapy"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <div className="flex justify-end space-x-4">
              <Button
                type="button"
                variant="outline"
                onClick={() => router.back()}
                disabled={loading}
              >
                Cancel
              </Button>
              <Button type="submit" disabled={loading}>
                {loading ? "Saving..." : "Save Therapy"}
              </Button>
            </div>
          </form>
        </Form>
      </CardContent>
    </Card>
  )
}
