"use client";

import { useEffect, useState } from "react";

import { formatScheduleSlot } from "@/lib/doctor";
import { getMyDoctorSchedule } from "@/services/doctor.service";
import type { DoctorSchedule } from "@/types/doctor";

export default function DoctorSchedulePage() {
  const [schedule, setSchedule] = useState<DoctorSchedule[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadSchedule() {
      try {
        const token = window.localStorage.getItem("smartcare_token");
        if (!token) {
          throw new Error("Missing auth token");
        }
        setSchedule(await getMyDoctorSchedule(token));
      } catch {
        setError("Unable to load doctor schedule.");
      }
    }

    loadSchedule();
  }, []);

  return (
    <main className="mx-auto w-full max-w-4xl px-4 py-8">
      <header>
        <p className="text-sm font-medium text-slate-600">Doctor</p>
        <h1 className="text-3xl font-semibold text-slate-950">Schedule</h1>
      </header>

      {error ? (
        <p className="mt-6 text-sm font-medium text-red-700" role="alert">
          {error}
        </p>
      ) : null}

      <section className="mt-8">
        {schedule.length === 0 ? (
          <p className="rounded-md border border-slate-200 p-4 text-sm text-slate-600">
            No availability schedule has been configured yet.
          </p>
        ) : (
          <ol className="space-y-4">
            {schedule.map((item) => (
              <li className="rounded-md border border-slate-200 p-4" key={item.id}>
                <h2 className="text-lg font-semibold text-slate-950">{formatScheduleSlot(item)}</h2>
                <p className="mt-1 text-sm text-slate-700">
                  {item.slot_duration_minutes} minute slots - up to {item.max_patients} patients
                </p>
                <p className="mt-1 text-sm text-slate-600">{item.is_active ? "Active" : "Inactive"}</p>
              </li>
            ))}
          </ol>
        )}
      </section>
    </main>
  );
}
