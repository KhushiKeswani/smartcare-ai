"use client";

import { FormEvent, useEffect, useState } from "react";

import { buildAppointmentDateTime, groupAppointmentsByDate } from "@/lib/appointment";
import {
  bookAppointment,
  cancelAppointment,
  listAppointments,
  listAppointmentSlots,
  rescheduleAppointment
} from "@/services/appointment.service";
import type { Appointment, AppointmentSlot } from "@/types/appointment";

const today = new Date().toISOString().slice(0, 10);

export default function PatientAppointmentsPage() {
  const [patientId, setPatientId] = useState("");
  const [doctorId, setDoctorId] = useState("");
  const [selectedDate, setSelectedDate] = useState(today);
  const [selectedSlot, setSelectedSlot] = useState("");
  const [reason, setReason] = useState("");
  const [slots, setSlots] = useState<AppointmentSlot[]>([]);
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [rescheduleTargetId, setRescheduleTargetId] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const groupedAppointments = groupAppointmentsByDate(appointments);

  async function withToken<T>(action: (token: string) => Promise<T>) {
    const token = window.localStorage.getItem("smartcare_token");
    if (!token) {
      throw new Error("Missing auth token");
    }
    return action(token);
  }

  async function loadCalendar() {
    if (!patientId) {
      return;
    }
    const result = await withToken((token) =>
      listAppointments(token, {
        patientId,
        startAt: `${selectedDate}T00:00:00`,
        endAt: `${selectedDate}T23:59:59`
      })
    );
    setAppointments(result.items);
  }

  useEffect(() => {
    loadCalendar().catch(() => setError("Unable to load appointment calendar."));
  }, [patientId, selectedDate]);

  async function handleLoadSlots() {
    setError("");
    setMessage("");
    setSelectedSlot("");
    setIsLoading(true);

    try {
      if (!doctorId) {
        throw new Error("Doctor is required");
      }
      const result = await withToken((token) => listAppointmentSlots(token, doctorId, selectedDate));
      setSlots(result);
    } catch {
      setError("Unable to load slots. Check doctor ID and date.");
    } finally {
      setIsLoading(false);
    }
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setMessage("");
    setIsLoading(true);

    try {
      if (!selectedSlot) {
        throw new Error("Select a slot");
      }
      const appointmentDateTime = buildAppointmentDateTime(selectedDate, selectedSlot);
      const appointment = rescheduleTargetId
        ? await withToken((token) => rescheduleAppointment(token, rescheduleTargetId, appointmentDateTime))
        : await withToken((token) =>
            bookAppointment(token, {
              patient_id: patientId,
              doctor_id: doctorId,
              appointment_datetime: appointmentDateTime,
              appointment_type: "In-person",
              reason: reason || undefined
            })
          );
      setMessage(
        rescheduleTargetId
          ? `Appointment rescheduled: ${appointment.appointment_code}`
          : `Appointment booked: ${appointment.appointment_code}`
      );
      setRescheduleTargetId("");
      setSelectedSlot("");
      await loadCalendar();
      await handleLoadSlots();
    } catch {
      setError("Unable to save appointment. The slot may already be booked.");
    } finally {
      setIsLoading(false);
    }
  }

  async function handleCancel(appointmentId: string) {
    setError("");
    setMessage("");

    try {
      await withToken((token) => cancelAppointment(token, appointmentId, "Cancelled from patient portal"));
      setMessage("Appointment cancelled.");
      await loadCalendar();
      await handleLoadSlots();
    } catch {
      setError("Unable to cancel appointment.");
    }
  }

  return (
    <main className="mx-auto w-full max-w-6xl px-4 py-8">
      <header>
        <p className="text-sm font-medium text-slate-600">Patient</p>
        <h1 className="text-3xl font-semibold text-slate-950">Appointments</h1>
      </header>

      <section className="mt-8 grid gap-4 md:grid-cols-3">
        <div>
          <label className="block text-sm font-medium text-slate-800" htmlFor="patient-id">
            Patient ID
          </label>
          <input
            className="mt-2 min-h-11 w-full rounded-md border border-slate-300 px-3 text-slate-950"
            id="patient-id"
            onChange={(event) => setPatientId(event.target.value)}
            value={patientId}
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-800" htmlFor="doctor-id">
            Doctor ID
          </label>
          <input
            className="mt-2 min-h-11 w-full rounded-md border border-slate-300 px-3 text-slate-950"
            id="doctor-id"
            onChange={(event) => setDoctorId(event.target.value)}
            value={doctorId}
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-800" htmlFor="appointment-date">
            Calendar date
          </label>
          <input
            className="mt-2 min-h-11 w-full rounded-md border border-slate-300 px-3 text-slate-950"
            id="appointment-date"
            onChange={(event) => setSelectedDate(event.target.value)}
            type="date"
            value={selectedDate}
          />
        </div>
      </section>

      <button
        className="mt-4 min-h-11 rounded-md border border-slate-950 px-4 text-sm font-semibold text-slate-950"
        onClick={handleLoadSlots}
        type="button"
      >
        Load slots
      </button>

      <form className="mt-8 space-y-5" onSubmit={handleSubmit}>
        <section>
          <h2 className="text-lg font-semibold text-slate-950">Slot selection</h2>
          <div className="mt-3 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
            {slots.map((slot) => (
              <button
                className={`min-h-11 rounded-md border px-3 text-sm font-semibold ${
                  selectedSlot === slot.start_time
                    ? "border-slate-950 bg-slate-950 text-white"
                    : "border-slate-300 text-slate-800"
                } disabled:cursor-not-allowed disabled:opacity-50`}
                disabled={!slot.is_available}
                key={`${slot.slot_date}-${slot.start_time}`}
                onClick={() => setSelectedSlot(slot.start_time)}
                type="button"
              >
                {slot.start_time} - {slot.end_time}
              </button>
            ))}
          </div>
        </section>

        <div>
          <label className="block text-sm font-medium text-slate-800" htmlFor="reason">
            Reason
          </label>
          <input
            className="mt-2 min-h-11 w-full rounded-md border border-slate-300 px-3 text-slate-950"
            id="reason"
            onChange={(event) => setReason(event.target.value)}
            value={reason}
          />
        </div>

        {error ? <p className="text-sm font-medium text-red-700" role="alert">{error}</p> : null}
        {message ? <p className="text-sm font-medium text-green-700" role="status">{message}</p> : null}

        <button
          className="min-h-11 rounded-md bg-slate-950 px-4 text-sm font-semibold text-white disabled:bg-slate-400"
          disabled={isLoading}
          type="submit"
        >
          {rescheduleTargetId ? "Reschedule appointment" : "Book appointment"}
        </button>
      </form>

      <section className="mt-10">
        <h2 className="text-lg font-semibold text-slate-950">Calendar view</h2>
        {Object.entries(groupedAppointments).length === 0 ? (
          <p className="mt-3 rounded-md border border-slate-200 p-4 text-sm text-slate-600">
            No appointments for the selected date.
          </p>
        ) : (
          <div className="mt-3 space-y-4">
            {Object.entries(groupedAppointments).map(([date, items]) => (
              <section className="rounded-md border border-slate-200 p-4" key={date}>
                <h3 className="font-semibold text-slate-950">{date}</h3>
                <ul className="mt-3 divide-y divide-slate-200">
                  {items.map((appointment) => (
                    <li className="grid gap-3 py-3 sm:grid-cols-[1fr_auto_auto]" key={appointment.id}>
                      <span className="text-sm text-slate-700">
                        {appointment.appointment_datetime.slice(11, 16)} - {appointment.status}
                      </span>
                      <button
                        className="rounded-md border border-slate-300 px-3 py-2 text-sm font-semibold"
                        onClick={() => setRescheduleTargetId(appointment.id)}
                        type="button"
                      >
                        Reschedule
                      </button>
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
