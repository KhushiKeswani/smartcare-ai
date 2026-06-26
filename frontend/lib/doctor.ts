import type { Doctor, DoctorSchedule } from "@/types/doctor";

const dayLabels = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

export function formatDoctorName(doctor: Pick<Doctor, "first_name" | "last_name">) {
  return `Dr. ${doctor.first_name} ${doctor.last_name}`.trim();
}

export function getAvailabilityLabel(isAvailable: boolean) {
  return isAvailable ? "Available" : "Unavailable";
}

export function formatScheduleSlot(schedule: Pick<DoctorSchedule, "day_of_week" | "start_time" | "end_time">) {
  return `${dayLabels[schedule.day_of_week] ?? "Unknown"} ${schedule.start_time} - ${schedule.end_time}`;
}
