import { config } from "@/lib/config";
import type {
  Appointment,
  AppointmentCreate,
  AppointmentListResponse,
  AppointmentSlot
} from "@/types/appointment";

function authHeaders(token: string) {
  return {
    Authorization: `Bearer ${token}`,
    "Content-Type": "application/json"
  };
}

async function request<T>(path: string, token: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${config.apiUrl}${path}`, {
    ...init,
    headers: {
      ...authHeaders(token),
      ...init?.headers
    }
  });

  if (!response.ok) {
    throw new Error("Appointment request failed");
  }

  return response.json();
}

export function listAppointments(
  token: string,
  filters: { doctorId?: string; patientId?: string; startAt?: string; endAt?: string; status?: string }
) {
  const params = new URLSearchParams();
  if (filters.doctorId) params.set("doctor_id", filters.doctorId);
  if (filters.patientId) params.set("patient_id", filters.patientId);
  if (filters.startAt) params.set("start_at", filters.startAt);
  if (filters.endAt) params.set("end_at", filters.endAt);
  if (filters.status) params.set("status", filters.status);
  return request<AppointmentListResponse>(`/appointments?${params.toString()}`, token);
}

export function listAppointmentSlots(token: string, doctorId: string, slotDate: string) {
  const params = new URLSearchParams({ doctor_id: doctorId, slot_date: slotDate });
  return request<AppointmentSlot[]>(`/appointments/slots?${params.toString()}`, token);
}

export function bookAppointment(token: string, payload: AppointmentCreate) {
  return request<Appointment>("/appointments", token, {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export function cancelAppointment(token: string, appointmentId: string, cancellationReason: string) {
  return request<Appointment>(`/appointments/${appointmentId}/cancel`, token, {
    method: "POST",
    body: JSON.stringify({ cancellation_reason: cancellationReason || undefined })
  });
}

export function rescheduleAppointment(token: string, appointmentId: string, appointmentDateTime: string) {
  return request<Appointment>(`/appointments/${appointmentId}/reschedule`, token, {
    method: "POST",
    body: JSON.stringify({ appointment_datetime: appointmentDateTime })
  });
}
