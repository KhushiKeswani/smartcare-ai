import type { Appointment, AppointmentSlot } from "@/types/appointment";

export function buildAppointmentDateTime(slotDate: string, startTime: string) {
  return `${slotDate}T${startTime}`;
}

export function isSlotSelectable(slot: Pick<AppointmentSlot, "is_available">) {
  return slot.is_available;
}

export function getAppointmentStatusLabel(appointment: Pick<Appointment, "status">) {
  return appointment.status;
}

export function groupAppointmentsByDate(appointments: Appointment[]) {
  return appointments.reduce<Record<string, Appointment[]>>((groups, appointment) => {
    const date = appointment.appointment_datetime.slice(0, 10);
    groups[date] = groups[date] ?? [];
    groups[date].push(appointment);
    return groups;
  }, {});
}
