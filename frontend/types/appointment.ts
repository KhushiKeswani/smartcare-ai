export type AppointmentStatus = "Scheduled" | "Confirmed" | "Checked in" | "Rescheduled" | "Cancelled";

export type Appointment = {
  id: string;
  appointment_code: string;
  patient_id: string;
  doctor_id: string;
  appointment_datetime: string;
  appointment_type: string;
  status: AppointmentStatus | string;
  reason: string | null;
  cancellation_reason: string | null;
  created_by: string | null;
  created_at: string;
  updated_at: string;
};

export type AppointmentCreate = {
  patient_id: string;
  doctor_id: string;
  appointment_datetime: string;
  appointment_type: string;
  reason?: string;
};

export type AppointmentListResponse = {
  items: Appointment[];
  total: number;
};

export type AppointmentSlot = {
  doctor_id: string;
  slot_date: string;
  start_time: string;
  end_time: string;
  is_available: boolean;
};
