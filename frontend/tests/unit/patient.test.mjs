import assert from "node:assert/strict";

function formatPatientName(patient) {
  return `${patient.first_name} ${patient.last_name}`.trim();
}

function matchesPatientSearch(patient, query) {
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

const patient = {
  patient_code: "PAT-1001",
  first_name: "Priya",
  last_name: "Sharma",
  phone: "9876543210",
  email: "priya@example.com"
};

assert.equal(formatPatientName(patient), "Priya Sharma");
assert.equal(matchesPatientSearch(patient, "priya"), true);
assert.equal(matchesPatientSearch(patient, "PAT-1001"), true);
assert.equal(matchesPatientSearch(patient, "missing"), false);
