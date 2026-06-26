import { config } from "@/lib/config";
import type {
  Doctor,
  DoctorCreate,
  DoctorListResponse,
  DoctorSchedule,
  DoctorScheduleCreate
} from "@/types/doctor";

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
    throw new Error("Doctor request failed");
  }

  return response.json();
}

export function searchDoctors(token: string, query: string, specialization = "", available = "") {
  const params = new URLSearchParams();
  if (query) {
    params.set("q", query);
  }
  if (specialization) {
    params.set("specialization", specialization);
  }
  if (available) {
    params.set("available", available);
  }
  return request<DoctorListResponse>(`/doctors?${params.toString()}`, token);
}

export function createDoctor(token: string, payload: DoctorCreate) {
  return request<Doctor>("/doctors", token, {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export function getMyDoctorProfile(token: string) {
  return request<Doctor>("/doctors/me", token);
}

export function getMyDoctorSchedule(token: string) {
  return request<DoctorSchedule[]>("/doctors/me/schedule", token);
}

export function createDoctorSchedule(token: string, doctorId: string, payload: DoctorScheduleCreate) {
  return request<DoctorSchedule>(`/doctors/${doctorId}/schedule`, token, {
    method: "POST",
    body: JSON.stringify(payload)
  });
}
