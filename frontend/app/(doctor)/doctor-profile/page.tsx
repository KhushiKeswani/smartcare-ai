"use client";

import { useEffect, useState } from "react";

import { formatDoctorName, getAvailabilityLabel } from "@/lib/doctor";
import { getMyDoctorProfile } from "@/services/doctor.service";
import type { Doctor } from "@/types/doctor";

export default function DoctorProfilePage() {
  const [doctor, setDoctor] = useState<Doctor | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadProfile() {
      try {
        const token = window.localStorage.getItem("smartcare_token");
        if (!token) {
          throw new Error("Missing auth token");
        }
        setDoctor(await getMyDoctorProfile(token));
      } catch {
        setError("Unable to load doctor profile.");
      }
    }

    loadProfile();
  }, []);

  return (
    <main className="mx-auto w-full max-w-3xl px-4 py-8">
      <header>
        <p className="text-sm font-medium text-slate-600">Doctor</p>
        <h1 className="text-3xl font-semibold text-slate-950">Profile</h1>
      </header>

      {error ? (
        <p className="mt-6 text-sm font-medium text-red-700" role="alert">
          {error}
        </p>
      ) : null}

      {doctor ? (
        <dl className="mt-8 grid gap-4 sm:grid-cols-2">
          <div className="rounded-md border border-slate-200 p-4">
            <dt className="text-sm text-slate-600">Name</dt>
            <dd className="mt-1 font-semibold text-slate-950">{formatDoctorName(doctor)}</dd>
          </div>
          <div className="rounded-md border border-slate-200 p-4">
            <dt className="text-sm text-slate-600">Doctor ID</dt>
            <dd className="mt-1 font-semibold text-slate-950">{doctor.doctor_code}</dd>
          </div>
          <div className="rounded-md border border-slate-200 p-4">
            <dt className="text-sm text-slate-600">Specialization</dt>
            <dd className="mt-1 font-semibold text-slate-950">{doctor.specialization}</dd>
          </div>
          <div className="rounded-md border border-slate-200 p-4">
            <dt className="text-sm text-slate-600">Availability</dt>
            <dd className="mt-1 font-semibold text-slate-950">{getAvailabilityLabel(doctor.is_available)}</dd>
          </div>
          <div className="rounded-md border border-slate-200 p-4">
            <dt className="text-sm text-slate-600">Department</dt>
            <dd className="mt-1 font-semibold text-slate-950">{doctor.department}</dd>
          </div>
          <div className="rounded-md border border-slate-200 p-4">
            <dt className="text-sm text-slate-600">Consultation fee</dt>
            <dd className="mt-1 font-semibold text-slate-950">₹{doctor.consultation_fee}</dd>
          </div>
        </dl>
      ) : null}
    </main>
  );
}
