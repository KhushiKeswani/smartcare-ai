import assert from "node:assert/strict";

function buildAppointmentDateTime(slotDate, startTime) {
  return `${slotDate}T${startTime}`;
}

function isSlotSelectable(slot) {
  return slot.is_available;
}

function groupAppointmentsByDate(appointments) {
  return appointments.reduce((groups, appointment) => {
    const date = appointment.appointment_datetime.slice(0, 10);
    groups[date] = groups[date] ?? [];
    groups[date].push(appointment);
    return groups;
  }, {});
}

assert.equal(buildAppointmentDateTime("2026-06-29", "09:00:00"), "2026-06-29T09:00:00");
assert.equal(isSlotSelectable({ is_available: true }), true);
assert.equal(isSlotSelectable({ is_available: false }), false);

const grouped = groupAppointmentsByDate([
  { appointment_datetime: "2026-06-29T09:00:00", id: "1" },
  { appointment_datetime: "2026-06-29T09:30:00", id: "2" },
  { appointment_datetime: "2026-06-30T09:00:00", id: "3" }
]);

assert.equal(grouped["2026-06-29"].length, 2);
assert.equal(grouped["2026-06-30"].length, 1);
