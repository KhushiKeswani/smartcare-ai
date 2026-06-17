"use client";

import { FormEvent, useState } from "react";

import { getRoleHomePath } from "@/lib/auth";
import { login } from "@/services/auth.service";
import type { UserRole } from "@/types/auth";

const demoAccounts: Array<{ role: UserRole; email: string }> = [
  { role: "Patient", email: "patient@smartcare.ai" },
  { role: "Doctor", email: "doctor@smartcare.ai" },
  { role: "Admin", email: "admin@smartcare.ai" }
];

export default function LoginPage() {
  const [email, setEmail] = useState("patient@smartcare.ai");
  const [password, setPassword] = useState("Password123");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setIsSubmitting(true);

    try {
      const result = await login({ email, password });
      window.localStorage.setItem("smartcare_token", result.access_token);
      window.localStorage.setItem("smartcare_user", JSON.stringify(result.user));
      window.location.assign(getRoleHomePath(result.user.role));
    } catch {
      setError("Invalid email or password.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-md flex-col justify-center px-6 py-10">
      <section className="space-y-8">
        <div>
          <p className="text-sm font-medium text-slate-600">SmartCare AI</p>
          <h1 className="mt-2 text-3xl font-semibold text-slate-950">Sign in</h1>
          <p className="mt-2 text-sm text-slate-600">
            Access your secure hospital workspace.
          </p>
        </div>

        <form className="space-y-5" onSubmit={handleSubmit}>
          <div>
            <label className="block text-sm font-medium text-slate-800" htmlFor="email">
              Email
            </label>
            <input
              autoComplete="email"
              className="mt-2 w-full rounded-md border border-slate-300 px-3 py-2 text-slate-950 outline-none focus:border-slate-900 focus:ring-2 focus:ring-slate-200"
              id="email"
              name="email"
              onChange={(event) => setEmail(event.target.value)}
              required
              type="email"
              value={email}
            />
          </div>

          <div>
            <label
              className="block text-sm font-medium text-slate-800"
              htmlFor="password"
            >
              Password
            </label>
            <input
              autoComplete="current-password"
              className="mt-2 w-full rounded-md border border-slate-300 px-3 py-2 text-slate-950 outline-none focus:border-slate-900 focus:ring-2 focus:ring-slate-200"
              id="password"
              name="password"
              onChange={(event) => setPassword(event.target.value)}
              required
              type="password"
              value={password}
            />
          </div>

          {error ? (
            <p className="text-sm font-medium text-red-700" role="alert">
              {error}
            </p>
          ) : null}

          <button
            className="w-full rounded-md bg-slate-950 px-4 py-2.5 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:bg-slate-400"
            disabled={isSubmitting}
            type="submit"
          >
            {isSubmitting ? "Signing in..." : "Sign in"}
          </button>
        </form>

        <div className="rounded-md border border-slate-200 p-4">
          <p className="text-sm font-medium text-slate-900">Demo accounts</p>
          <ul className="mt-3 space-y-2 text-sm text-slate-600">
            {demoAccounts.map((account) => (
              <li key={account.role}>
                {account.role}: {account.email}
              </li>
            ))}
          </ul>
          <p className="mt-3 text-sm text-slate-600">Password: Password123</p>
        </div>
      </section>
    </main>
  );
}

