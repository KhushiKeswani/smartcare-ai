"use client";

import { FormEvent, useState } from "react";

import { formatDoctorName, getAvailabilityLabel } from "@/lib/doctor";
import { searchDoctors } from "@/services/doctor.service";
import type { Doctor } from "@/types/doctor";

export default function AdminDoctorsPage() {
  const [query, setQuery] = useState("");
  const [specialization, setSpecialization] = useState("");
  const [available, setAvailable] = useState("");
  const [doctors, setDoctors] = useState<Doctor[]>([]);
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
      const result = await searchDoctors(token, query, specialization, available);
      setDoctors(result.items);
      setTotal(result.total);
    } catch {
      setError("Unable to search doctors. Please check your permissions.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="mx-auto w-full max-w-6xl px-4 py-8">
      <header className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-sm font-medium text-slate-600">Admin</p>
          <h1 className="text-3xl font-semibold text-slate-950">Doctors</h1>
        </div>
        <a
          className="rounded-md bg-slate-950 px-4 py-2 text-center text-sm font-semibold text-white"
          href="/doctors/register"
        >
          Add doctor
        </a>
      </header>

      <form className="mt-8 grid gap-3 md:grid-cols-[1fr_180px_160px_auto]" onSubmit={handleSearch}>
        <label className="sr-only" htmlFor="doctor-search">
          Search doctors
        </label>
        <input
          className="min-h-11 rounded-md border border-slate-300 px-3 text-slate-950 outline-none focus:border-slate-900 focus:ring-2 focus:ring-slate-200"
          id="doctor-search"
          onChange={(event) => setQuery(event.target.value)}
          placeholder="Search name, department, code, or email"
          value={query}
        />
        <input
          className="min-h-11 rounded-md border border-slate-300 px-3 text-slate-950 outline-none focus:border-slate-900 focus:ring-2 focus:ring-slate-200"
          onChange={(event) => setSpecialization(event.target.value)}
          placeholder="Specialization"
          value={specialization}
        />
        <select
          className="min-h-11 rounded-md border border-slate-300 px-3 text-slate-950 outline-none focus:border-slate-900 focus:ring-2 focus:ring-slate-200"
          onChange={(event) => setAvailable(event.target.value)}
          value={available}
        >
          <option value="">Any availability</option>
          <option value="true">Available</option>
          <option value="false">Unavailable</option>
        </select>
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
        <p className="text-sm text-slate-600">{total} doctors found</p>
        <div className="mt-4 overflow-hidden rounded-md border border-slate-200">
          {doctors.length === 0 ? (
            <p className="p-4 text-sm text-slate-600">No doctor profiles to display.</p>
          ) : (
            <ul className="divide-y divide-slate-200">
              {doctors.map((doctor) => (
                <li className="grid gap-1 p-4 md:grid-cols-5 md:items-center" key={doctor.id}>
                  <span className="font-medium text-slate-950">{formatDoctorName(doctor)}</span>
                  <span className="text-sm text-slate-600">{doctor.specialization}</span>
                  <span className="text-sm text-slate-600">{doctor.department}</span>
                  <span className="text-sm text-slate-600">{doctor.doctor_code}</span>
                  <span className="text-sm text-slate-600">{getAvailabilityLabel(doctor.is_available)}</span>
                </li>
              ))}
            </ul>
          )}
        </div>
      </section>
    </main>
  );
}
