import { config } from "@/lib/config";
import type {
  MedicalHistoryItem,
  Patient,
  PatientCreate,
  PatientListResponse
} from "@/types/patient";

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
    throw new Error("Patient request failed");
  }

  return response.json();
}

export function searchPatients(token: string, query: string) {
  const params = new URLSearchParams();
  if (query) {
    params.set("q", query);
  }
  return request<PatientListResponse>(`/patients?${params.toString()}`, token);
}

export function registerPatient(token: string, payload: PatientCreate) {
  return request<Patient>("/patients", token, {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export function getMyPatientProfile(token: string) {
  return request<Patient>("/patients/me", token);
}

export function getMyMedicalHistory(token: string) {
  return request<MedicalHistoryItem[]>("/patients/me/medical-history", token);
}
