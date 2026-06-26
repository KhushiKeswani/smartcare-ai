import assert from "node:assert/strict";

const dayLabels = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

function formatDoctorName(doctor) {
  return `Dr. ${doctor.first_name} ${doctor.last_name}`.trim();
}

function getAvailabilityLabel(isAvailable) {
  return isAvailable ? "Available" : "Unavailable";
}

function formatScheduleSlot(schedule) {
  return `${dayLabels[schedule.day_of_week] ?? "Unknown"} ${schedule.start_time} - ${schedule.end_time}`;
}

const doctor = {
  first_name: "Arjun",
  last_name: "Mehta"
};

assert.equal(formatDoctorName(doctor), "Dr. Arjun Mehta");
assert.equal(getAvailabilityLabel(true), "Available");
assert.equal(getAvailabilityLabel(false), "Unavailable");
assert.equal(
  formatScheduleSlot({ day_of_week: 1, start_time: "09:00:00", end_time: "13:00:00" }),
  "Monday 09:00:00 - 13:00:00"
);
