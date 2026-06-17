import { config } from "@/lib/config";
import type { LoginRequest, LoginResponse } from "@/types/auth";

export async function login(payload: LoginRequest): Promise<LoginResponse> {
  const response = await fetch(`${config.apiUrl}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    throw new Error("Invalid email or password");
  }

  return response.json();
}

