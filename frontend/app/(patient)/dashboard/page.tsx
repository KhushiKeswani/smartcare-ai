"use client";

import { useEffect, useState } from "react";

import { formatPatientName } from "@/lib/patient";
import { getMyPatientProfile } from "@/services/patient.service";
import type { Patient } from "@/types/patient";

export default function PatientDashboardPage() {
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
        setError("Unable to load your patient profile.");
      }
    }

    loadProfile();
  }, []);

  return (
    <main className="mx-auto w-full max-w-4xl px-4 py-8">
      <header>
        <p className="text-sm font-medium text-slate-600">Patient profile</p>
        <h1 className="text-3xl font-semibold text-slate-950">
          {patient ? formatPatientName(patient) : "My dashboard"}
        </h1>
      </header>

      {error ? (
        <p className="mt-6 text-sm font-medium text-red-700" role="alert">
          {error}
        </p>
      ) : null}

      {patient ? (
        <section className="mt-8 grid gap-4 sm:grid-cols-2">
          <div className="rounded-md border border-slate-200 p-4">
            <p className="text-sm text-slate-600">Patient ID</p>
            <p className="mt-1 font-semibold text-slate-950">{patient.patient_code}</p>
          </div>
          <div className="rounded-md border border-slate-200 p-4">
            <p className="text-sm text-slate-600">Phone</p>
            <p className="mt-1 font-semibold text-slate-950">{patient.phone}</p>
          </div>
          <div className="rounded-md border border-slate-200 p-4">
            <p className="text-sm text-slate-600">Blood group</p>
            <p className="mt-1 font-semibold text-slate-950">{patient.blood_group ?? "Not recorded"}</p>
          </div>
          <div className="rounded-md border border-slate-200 p-4">
            <p className="text-sm text-slate-600">Insurance</p>
            <p className="mt-1 font-semibold text-slate-950">
              {patient.insurance_provider ?? "Not recorded"}
            </p>
          </div>
        </section>
      ) : null}
    </main>
  );
}
