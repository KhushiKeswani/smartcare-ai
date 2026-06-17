import assert from "node:assert/strict";

const roleHomePath = {
  Patient: "/dashboard",
  Doctor: "/dashboard",
  Admin: "/dashboard"
};

function getRoleHomePath(role) {
  return roleHomePath[role];
}

function canAccessRole(requiredRoles, userRole) {
  return requiredRoles.includes(userRole);
}

assert.equal(getRoleHomePath("Patient"), "/dashboard");
assert.equal(getRoleHomePath("Doctor"), "/dashboard");
assert.equal(getRoleHomePath("Admin"), "/dashboard");
assert.equal(canAccessRole(["Admin"], "Admin"), true);
assert.equal(canAccessRole(["Admin"], "Patient"), false);

