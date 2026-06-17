import type { UserRole } from "@/types/auth";

const roleHomePath: Record<UserRole, string> = {
  Patient: "/dashboard",
  Doctor: "/dashboard",
  Admin: "/dashboard"
};

export function getRoleHomePath(role: UserRole): string {
  return roleHomePath[role];
}

export function canAccessRole(requiredRoles: UserRole[], userRole: UserRole): boolean {
  return requiredRoles.includes(userRole);
}

