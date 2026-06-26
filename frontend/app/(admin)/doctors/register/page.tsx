"use client";

import { FormEvent, useState } from "react";

import { createDoctor, createDoctorSchedule } from "@/services/doctor.service";

const initialDoctorForm = {
  first_name: "",
  last_name: "",
  email: "",
  phone: "",
  specialization: "",
  department: "",
  license_number: "",
  consultation_fee: "0",
  bio: "",
  user_id: ""
};

const initialScheduleForm = {
  day_of_week: "1",
  start_time: "09:00",
  end_time: "13:00",
  slot_duration_minutes: "30",
  max_patients: "12"
};

export default function RegisterDoctorPage() {
  const [doctorForm, setDoctorForm] = useState(initialDoctorForm);
  const [scheduleForm, setScheduleForm] = useState(initialScheduleForm);
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

      const doctor = await createDoctor(token, {
        ...doctorForm,
        consultation_fee: Number(doctorForm.consultation_fee),
        bio: doctorForm.bio || undefined,
        user_id: doctorForm.user_id || undefined,
        is_available: true
      });

      await createDoctorSchedule(token, doctor.id, {
        day_of_week: Number(scheduleForm.day_of_week),
        start_time: `${scheduleForm.start_time}:00`,
        end_time: `${scheduleForm.end_time}:00`,
        slot_duration_minutes: Number(scheduleForm.slot_duration_minutes),
        max_patients: Number(scheduleForm.max_patients),
        is_active: true
      });

      setMessage(`Doctor registered: ${doctor.doctor_code}`);
      setDoctorForm(initialDoctorForm);
      setScheduleForm(initialScheduleForm);
    } catch {
      setError("Unable to register doctor. Check required fields and permissions.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="mx-auto w-full max-w-4xl px-4 py-8">
      <header>
        <p className="text-sm font-medium text-slate-600">Admin</p>
        <h1 className="text-3xl font-semibold text-slate-950">Add doctor</h1>
      </header>

      <form className="mt-8 grid gap-5 sm:grid-cols-2" onSubmit={handleSubmit}>
        {Object.entries(doctorForm).map(([field, value]) => (
          <div className={field === "bio" ? "sm:col-span-2" : ""} key={field}>
            <label className="block text-sm font-medium capitalize text-slate-800" htmlFor={field}>
              {field.replaceAll("_", " ")}
            </label>
            <input
              className="mt-2 min-h-11 w-full rounded-md border border-slate-300 px-3 text-slate-950 outline-none focus:border-slate-900 focus:ring-2 focus:ring-slate-200"
              id={field}
              name={field}
              onChange={(event) => setDoctorForm((current) => ({ ...current, [field]: event.target.value }))}
              required={!["bio", "user_id"].includes(field)}
              type={field === "email" ? "email" : field === "consultation_fee" ? "number" : "text"}
              value={value}
            />
          </div>
        ))}

        <section className="grid gap-5 border-t border-slate-200 pt-5 sm:col-span-2 sm:grid-cols-2">
          <h2 className="text-lg font-semibold text-slate-950 sm:col-span-2">Default availability</h2>
          {Object.entries(scheduleForm).map(([field, value]) => (
            <div key={field}>
              <label className="block text-sm font-medium capitalize text-slate-800" htmlFor={field}>
                {field.replaceAll("_", " ")}
              </label>
              <input
                className="mt-2 min-h-11 w-full rounded-md border border-slate-300 px-3 text-slate-950 outline-none focus:border-slate-900 focus:ring-2 focus:ring-slate-200"
                id={field}
                max={field === "day_of_week" ? 6 : undefined}
                min={field === "day_of_week" ? 0 : field.includes("minutes") || field === "max_patients" ? 1 : undefined}
                onChange={(event) => setScheduleForm((current) => ({ ...current, [field]: event.target.value }))}
                required
                type={field.includes("time") ? "time" : "number"}
                value={value}
              />
            </div>
          ))}
        </section>

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
          {isSubmitting ? "Saving..." : "Create doctor profile"}
        </button>
      </form>
    </main>
  );
}
