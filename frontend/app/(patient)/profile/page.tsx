"use client";

import { useEffect, useState } from "react";

import { formatPatientName } from "@/lib/patient";
import { getMyPatientProfile } from "@/services/patient.service";
import type { Patient } from "@/types/patient";

export default function PatientProfilePage() {
  const [patient, setPatient] = useState<Patient | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadProfile() {
      try {
        const token = window.localStorage.getItem("smartcare_token");
        if (!token) {
          throw new Error("Missing auth token");
        }
        setPatient(await getMyPatientProfile(token));
      } catch {
        setError("Unable to load patient profile.");
      }
    }

    loadProfile();
  }, []);

  return (
    <main className="mx-auto w-full max-w-3xl px-4 py-8">
      <header>
        <p className="text-sm font-medium text-slate-600">Patient</p>
        <h1 className="text-3xl font-semibold text-slate-950">Profile</h1>
      </header>

      {error ? (
        <p className="mt-6 text-sm font-medium text-red-700" role="alert">
          {error}
        </p>
      ) : null}

      {patient ? (
        <dl className="mt-8 grid gap-4 sm:grid-cols-2">
          <div className="rounded-md border border-slate-200 p-4">
            <dt className="text-sm text-slate-600">Name</dt>
            <dd className="mt-1 font-semibold text-slate-950">{formatPatientName(patient)}</dd>
          </div>
          <div className="rounded-md border border-slate-200 p-4">
            <dt className="text-sm text-slate-600">Patient ID</dt>
            <dd className="mt-1 font-semibold text-slate-950">{patient.patient_code}</dd>
          </div>
          <div className="rounded-md border border-slate-200 p-4">
            <dt className="text-sm text-slate-600">Date of birth</dt>
            <dd className="mt-1 font-semibold text-slate-950">{patient.date_of_birth}</dd>
          </div>
          <div className="rounded-md border border-slate-200 p-4">
            <dt className="text-sm text-slate-600">Gender</dt>
            <dd className="mt-1 font-semibold text-slate-950">{patient.gender}</dd>
          </div>
          <div className="rounded-md border border-slate-200 p-4">
            <dt className="text-sm text-slate-600">Phone</dt>
            <dd className="mt-1 font-semibold text-slate-950">{patient.phone}</dd>
          </div>
          <div className="rounded-md border border-slate-200 p-4">
            <dt className="text-sm text-slate-600">Email</dt>
            <dd className="mt-1 font-semibold text-slate-950">{patient.email ?? "Not recorded"}</dd>
          </div>
        </dl>
      ) : null}
    </main>
  );
}
