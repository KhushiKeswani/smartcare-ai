export type Patient = {
  id: string;
  patient_code: string;
  user_id: string | null;
  first_name: string;
  last_name: string;
  date_of_birth: string;
  gender: string;
  phone: string;
  email: string | null;
  address: string | null;
  emergency_contact: string | null;
  blood_group: string | null;
  insurance_provider: string | null;
  insurance_number: string | null;
  status: string;
  created_at: string;
  updated_at: string;
};

export type PatientCreate = {
  first_name: string;
  last_name: string;
  date_of_birth: string;
  gender: string;
  phone: string;
  email?: string;
  address?: string;
  emergency_contact?: string;
  blood_group?: string;
  insurance_provider?: string;
  insurance_number?: string;
  user_id?: string;
};

export type PatientListResponse = {
  items: Patient[];
  total: number;
};

export type MedicalHistoryItem = {
  id: string;
  patient_id: string;
  visit_date: string;
  doctor_name: string;
  department: string;
  diagnosis: string;
  notes: string | null;
  created_at: string;
};
