"use client";

import { FormEvent, useState } from "react";

import { groupAppointmentsByDate } from "@/lib/appointment";
import { cancelAppointment, listAppointments } from "@/services/appointment.service";
import type { Appointment } from "@/types/appointment";

const today = new Date().toISOString().slice(0, 10);

export default function AdminAppointmentsPage() {
  const [doctorId, setDoctorId] = useState("");
  const [patientId, setPatientId] = useState("");
  const [selectedDate, setSelectedDate] = useState(today);
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [total, setTotal] = useState(0);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const groupedAppointments = groupAppointmentsByDate(appointments);

  async function getToken() {
    const token = window.localStorage.getItem("smartcare_token");
    if (!token) {
      throw new Error("Missing auth token");
    }
    return token;
  }

  async function handleSearch(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      const token = await getToken();
      const result = await listAppointments(token, {
        doctorId: doctorId || undefined,
        patientId: patientId || undefined,
        startAt: `${selectedDate}T00:00:00`,
        endAt: `${selectedDate}T23:59:59`
      });
      setAppointments(result.items);
      setTotal(result.total);
    } catch {
      setError("Unable to load appointment calendar.");
    } finally {
      setIsLoading(false);
    }
  }

  async function handleCancel(appointmentId: string) {
    try {
      const token = await getToken();
      await cancelAppointment(token, appointmentId, "Cancelled by admin");
      setAppointments((items) =>
        items.map((item) => (item.id === appointmentId ? { ...item, status: "Cancelled" } : item))
      );
    } catch {
      setError("Unable to cancel appointment.");
    }
  }

  return (
    <main className="mx-auto w-full max-w-6xl px-4 py-8">
      <header>
        <p className="text-sm font-medium text-slate-600">Admin</p>
        <h1 className="text-3xl font-semibold text-slate-950">Appointment calendar</h1>
      </header>

      <form className="mt-8 grid gap-3 md:grid-cols-[1fr_1fr_180px_auto]" onSubmit={handleSearch}>
        <input
          className="min-h-11 rounded-md border border-slate-300 px-3 text-slate-950"
          onChange={(event) => setDoctorId(event.target.value)}
          placeholder="Doctor ID"
          value={doctorId}
        />
        <input
          className="min-h-11 rounded-md border border-slate-300 px-3 text-slate-950"
          onChange={(event) => setPatientId(event.target.value)}
          placeholder="Patient ID"
          value={patientId}
        />
        <input
          className="min-h-11 rounded-md border border-slate-300 px-3 text-slate-950"
          onChange={(event) => setSelectedDate(event.target.value)}
          type="date"
          value={selectedDate}
        />
        <button
          className="min-h-11 rounded-md border border-slate-950 px-4 text-sm font-semibold text-slate-950"
          disabled={isLoading}
          type="submit"
        >
          {isLoading ? "Loading..." : "Load"}
        </button>
      </form>

      {error ? <p className="mt-4 text-sm font-medium text-red-700" role="alert">{error}</p> : null}

      <section className="mt-8">
        <p className="text-sm text-slate-600">{total} appointments found</p>
        {Object.entries(groupedAppointments).length === 0 ? (
          <p className="mt-3 rounded-md border border-slate-200 p-4 text-sm text-slate-600">
            No appointments to display.
          </p>
        ) : (
          <div className="mt-3 space-y-4">
            {Object.entries(groupedAppointments).map(([date, items]) => (
              <section className="rounded-md border border-slate-200 p-4" key={date}>
                <h2 className="font-semibold text-slate-950">{date}</h2>
                <ul className="mt-3 divide-y divide-slate-200">
                  {items.map((appointment) => (
                    <li className="grid gap-2 py-3 md:grid-cols-5 md:items-center" key={appointment.id}>
                      <span className="text-sm text-slate-700">{appointment.appointment_code}</span>
                      <span className="text-sm text-slate-700">{appointment.appointment_datetime.slice(11, 16)}</span>
                      <span className="text-sm text-slate-700">{appointment.status}</span>
                      <span className="text-sm text-slate-700">{appointment.appointment_type}</span>
                      <button
                        className="rounded-md border border-red-300 px-3 py-2 text-sm font-semibold text-red-700"
                        onClick={() => handleCancel(appointment.id)}
                        type="button"
                      >
                        Cancel
                      </button>
                    </li>
                  ))}
                </ul>
              </section>
            ))}
          </div>
        )}
      </section>
    </main>
  );
}
