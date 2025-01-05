import { LoginForm } from "@/components/LoginForm"

export default function LoginPage() {
  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="mx-auto max-w-[350px] space-y-6">
        <div className="space-y-2 text-center">
          <h1 className="text-3xl font-bold">Welcome Back</h1>
          <p className="text-gray-500">
            Enter your credentials to access your account
          </p>
        </div>
        <LoginForm />
      </div>
    </div>
  )
}
