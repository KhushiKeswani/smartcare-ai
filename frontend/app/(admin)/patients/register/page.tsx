"use client";

import { FormEvent, useState } from "react";

import { registerPatient } from "@/services/patient.service";

const initialForm = {
  first_name: "",
  last_name: "",
  date_of_birth: "",
  gender: "",
  phone: "",
  email: "",
  address: "",
  emergency_contact: "",
  blood_group: "",
  insurance_provider: "",
  insurance_number: ""
};

export default function RegisterPatientPage() {
  const [form, setForm] = useState(initialForm);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setMessage("");
    setIsSubmitting(true);

    try {
      const token = window.localStorage.getItem("smartcare_token");
      if (!token) {
        throw new Error("Missing auth token");
      }
      const patient = await registerPatient(token, {
        ...form,
        email: form.email || undefined,
        address: form.address || undefined,
        emergency_contact: form.emergency_contact || undefined,
        blood_group: form.blood_group || undefined,
        insurance_provider: form.insurance_provider || undefined,
        insurance_number: form.insurance_number || undefined
      });
      setMessage(`Patient registered: ${patient.patient_code}`);
      setForm(initialForm);
    } catch {
      setError("Unable to register patient. Check required fields and permissions.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="mx-auto w-full max-w-3xl px-4 py-8">
      <header>
        <p className="text-sm font-medium text-slate-600">Admin</p>
        <h1 className="text-3xl font-semibold text-slate-950">Register patient</h1>
      </header>

      <form className="mt-8 grid gap-5 sm:grid-cols-2" onSubmit={handleSubmit}>
        {Object.entries(form).map(([field, value]) => (
          <div className={field === "address" ? "sm:col-span-2" : ""} key={field}>
            <label className="block text-sm font-medium capitalize text-slate-800" htmlFor={field}>
              {field.replaceAll("_", " ")}
            </label>
            <input
              className="mt-2 min-h-11 w-full rounded-md border border-slate-300 px-3 text-slate-950 outline-none focus:border-slate-900 focus:ring-2 focus:ring-slate-200"
              id={field}
              name={field}
              onChange={(event) => setForm((current) => ({ ...current, [field]: event.target.value }))}
              required={["first_name", "last_name", "date_of_birth", "gender", "phone"].includes(field)}
              type={field === "date_of_birth" ? "date" : field === "email" ? "email" : "text"}
              value={value}
            />
          </div>
        ))}

        {error ? (
          <p className="text-sm font-medium text-red-700 sm:col-span-2" role="alert">
            {error}
          </p>
        ) : null}
        {message ? (
          <p className="text-sm font-medium text-green-700 sm:col-span-2" role="status">
            {message}
          </p>
        ) : null}

        <button
          className="min-h-11 rounded-md bg-slate-950 px-4 text-sm font-semibold text-white disabled:bg-slate-400 sm:col-span-2"
          disabled={isSubmitting}
          type="submit"
        >
          {isSubmitting ? "Registering..." : "Register patient"}
        </button>
      </form>
    </main>
  );
}
