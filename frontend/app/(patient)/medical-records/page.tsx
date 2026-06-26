"use client";

import { useEffect, useState } from "react";

import { getMyMedicalHistory } from "@/services/patient.service";
import type { MedicalHistoryItem } from "@/types/patient";

export default function PatientMedicalRecordsPage() {
  const [history, setHistory] = useState<MedicalHistoryItem[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadHistory() {
      try {
        const token = window.localStorage.getItem("smartcare_token");
        if (!token) {
          throw new Error("Missing auth token");
        }
        setHistory(await getMyMedicalHistory(token));
      } catch {
        setError("Unable to load medical history.");
      }
    }

    loadHistory();
  }, []);

  return (
    <main className="mx-auto w-full max-w-4xl px-4 py-8">
      <header>
        <p className="text-sm font-medium text-slate-600">Patient</p>
        <h1 className="text-3xl font-semibold text-slate-950">Medical history</h1>
      </header>

      {error ? (
        <p className="mt-6 text-sm font-medium text-red-700" role="alert">
          {error}
        </p>
      ) : null}

      <section className="mt-8">
        {history.length === 0 ? (
          <p className="rounded-md border border-slate-200 p-4 text-sm text-slate-600">
            No medical history records are available yet.
          </p>
        ) : (
          <ol className="space-y-4">
            {history.map((item) => (
              <li className="rounded-md border border-slate-200 p-4" key={item.id}>
                <p className="text-sm text-slate-600">{item.visit_date}</p>
                <h2 className="mt-1 text-lg font-semibold text-slate-950">{item.diagnosis}</h2>
                <p className="mt-1 text-sm text-slate-700">
                  {item.department} - {item.doctor_name}
                </p>
                {item.notes ? <p className="mt-3 text-sm text-slate-700">{item.notes}</p> : null}
              </li>
            ))}
          </ol>
        )}
      </section>
    </main>
  );
}
