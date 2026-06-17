"use client";

import { FormEvent, useState } from "react";

import { formatPatientName } from "@/lib/patient";
import { searchPatients } from "@/services/patient.service";
import type { Patient } from "@/types/patient";

export default function AdminPatientsPage() {
  const [query, setQuery] = useState("");
  const [patients, setPatients] = useState<Patient[]>([]);
  const [total, setTotal] = useState(0);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleSearch(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      const token = window.localStorage.getItem("smartcare_token");
      if (!token) {
        throw new Error("Missing auth token");
      }
      const result = await searchPatients(token, query);
      setPatients(result.items);
      setTotal(result.total);
    } catch {
      setError("Unable to search patients. Please sign in as an admin or doctor.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="mx-auto w-full max-w-6xl px-4 py-8">
      <header className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-sm font-medium text-slate-600">Admin</p>
          <h1 className="text-3xl font-semibold text-slate-950">Patients</h1>
        </div>
        <a
          className="rounded-md bg-slate-950 px-4 py-2 text-center text-sm font-semibold text-white"
          href="/patients/register"
        >
          Register patient
        </a>
      </header>

      <form className="mt-8 flex flex-col gap-3 sm:flex-row" onSubmit={handleSearch}>
        <label className="sr-only" htmlFor="patient-search">
          Search patients
        </label>
        <input
          className="min-h-11 flex-1 rounded-md border border-slate-300 px-3 text-slate-950 outline-none focus:border-slate-900 focus:ring-2 focus:ring-slate-200"
          id="patient-search"
          onChange={(event) => setQuery(event.target.value)}
          placeholder="Search by name, phone, email, or patient ID"
          value={query}
        />
        <button
          className="min-h-11 rounded-md border border-slate-950 px-4 text-sm font-semibold text-slate-950 disabled:opacity-60"
          disabled={isLoading}
          type="submit"
        >
          {isLoading ? "Searching..." : "Search"}
        </button>
      </form>

      {error ? (
        <p className="mt-4 text-sm font-medium text-red-700" role="alert">
          {error}
        </p>
      ) : null}

      <section className="mt-8" aria-live="polite">
        <p className="text-sm text-slate-600">{total} patients found</p>
        <div className="mt-4 overflow-hidden rounded-md border border-slate-200">
          {patients.length === 0 ? (
            <p className="p-4 text-sm text-slate-600">No patient records to display.</p>
          ) : (
            <ul className="divide-y divide-slate-200">
              {patients.map((patient) => (
                <li className="grid gap-1 p-4 sm:grid-cols-4 sm:items-center" key={patient.id}>
                  <span className="font-medium text-slate-950">{formatPatientName(patient)}</span>
                  <span className="text-sm text-slate-600">{patient.patient_code}</span>
                  <span className="text-sm text-slate-600">{patient.phone}</span>
                  <span className="text-sm text-slate-600">{patient.status}</span>
                </li>
              ))}
            </ul>
          )}
        </div>
      </section>
    </main>
  );
}
