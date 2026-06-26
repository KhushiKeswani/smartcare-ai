export type Doctor = {
  id: string;
  user_id: string | null;
  doctor_code: string;
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  specialization: string;
  department: string;
  license_number: string;
  consultation_fee: number;
  bio: string | null;
  is_available: boolean;
  status: string;
  created_at: string;
  updated_at: string;
};

export type DoctorCreate = {
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  specialization: string;
  department: string;
  license_number: string;
  consultation_fee: number;
  bio?: string;
  is_available?: boolean;
  user_id?: string;
};

export type DoctorListResponse = {
  items: Doctor[];
  total: number;
};

export type DoctorSchedule = {
  id: string;
  doctor_id: string;
  day_of_week: number;
  start_time: string;
  end_time: string;
  slot_duration_minutes: number;
  max_patients: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
};

export type DoctorScheduleCreate = {
  day_of_week: number;
  start_time: string;
  end_time: string;
  slot_duration_minutes: number;
  max_patients: number;
  is_active?: boolean;
};
