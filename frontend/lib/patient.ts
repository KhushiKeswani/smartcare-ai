import type { Patient } from "@/types/patient";

export function formatPatientName(patient: Pick<Patient, "first_name" | "last_name">) {
  return `${patient.first_name} ${patient.last_name}`.trim();
}

export function matchesPatientSearch(patient: Patient, query: string) {
  const normalizedQuery = query.trim().toLowerCase();
  if (!normalizedQuery) {
    return true;
  }

  return [
    patient.patient_code,
    patient.first_name,
    patient.last_name,
    patient.phone,
    patient.email ?? ""
  ].some((value) => value.toLowerCase().includes(normalizedQuery));
}
