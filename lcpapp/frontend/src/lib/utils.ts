import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDate(dateString: string): string {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

export function formatPhone(phone: string): string {
  // Remove all non-digit characters
  const cleaned = phone.replace(/\D/g, '')
  
  // Format as (XXX) XXX-XXXX
  if (cleaned.length === 10) {
    return `(${cleaned.slice(0, 3)}) ${cleaned.slice(3, 6)}-${cleaned.slice(6)}`
  }
  
  return phone
}

export function calculateAge(dateOfBirth: string): number {
  const today = new Date()
  const birthDate = new Date(dateOfBirth)
  let age = today.getFullYear() - birthDate.getFullYear()
  const monthDiff = today.getMonth() - birthDate.getMonth()
  
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
    age--
  }
  
  return age
}

export function formatSSN(ssn: string): string {
  // Remove all non-digit characters
  const cleaned = ssn.replace(/\D/g, '')
  
  // Format as XXX-XX-XXXX
  if (cleaned.length === 9) {
    return `${cleaned.slice(0, 3)}-${cleaned.slice(3, 5)}-${cleaned.slice(5)}`
  }
  
  return ssn
}

export function formatZipCode(zipCode: string): string {
  // Remove all non-digit characters
  const cleaned = zipCode.replace(/\D/g, '')
  
  // Format as XXXXX or XXXXX-XXXX
  if (cleaned.length === 9) {
    return `${cleaned.slice(0, 5)}-${cleaned.slice(5)}`
  } else if (cleaned.length === 5) {
    return cleaned
  }
  
  return zipCode
}
