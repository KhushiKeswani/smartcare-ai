Below are professional UI wireframes for the **Patient Dashboard**, **Doctor Dashboard**, and **Admin Dashboard** for SmartCare AI.

No code included.

# 1. Patient Dashboard

## Purpose
The Patient Dashboard gives patients a simple, mobile-first portal to manage appointments, view queue status, access medical records, pay bills, and use AI assistance.

---

## 1.1 Patient Dashboard Home

### Layout

```text
 ------------------------------------------------
| Header                                         |
| SmartCare AI        Notifications   Profile    |
 ------------------------------------------------
| Greeting                                       |
| Good morning, Priya                            |
| Next appointment: Today, 11:30 AM              |
 ------------------------------------------------
| Quick Actions                                  |
| [Book Appointment] [View Queue]                |
| [Medical Records]  [Pay Bill]                  |
 ------------------------------------------------
| Current Visit                                  |
| Dr. Arjun Mehta                                |
| Cardiology                                     |
| Token: C-14                                    |
| Estimated Wait: 18 mins                        |
| [Track Queue]                                  |
 ------------------------------------------------
| Upcoming Appointments                          |
| 18 Jun, 10:00 AM - Dermatology                 |
| 25 Jun, 03:30 PM - Follow-up                   |
 ------------------------------------------------
| AI Assistant                                   |
| Describe symptoms or ask hospital questions    |
| [Start Chat]                                   |
 ------------------------------------------------
| Bottom Navigation                              |
| Home | Appointments | Records | Bills | Chat    |
 ------------------------------------------------
```

### Screen Elements
- Header with hospital branding, notification icon, and profile menu.
- Greeting section with patient name and next appointment summary.
- Quick action buttons for core workflows.
- Current visit card showing doctor, department, token, and wait time.
- Upcoming appointment list.
- AI assistant entry point.
- Bottom navigation for mobile usability.

### Key States
- No appointment state: show “Book your first appointment”.
- Active queue state: show live token and wait time.
- Payment due state: show billing alert.
- Report ready state: show notification badge.

---

## 1.2 Appointment Booking Screen

### Layout

```text
 ------------------------------------------------
| Back | Book Appointment                         |
 ------------------------------------------------
| Search Doctor or Department                     |
| [ Search input ]                                |
 ------------------------------------------------
| Select Department                               |
| Cardiology | Dermatology | Neurology | General  |
 ------------------------------------------------
| Available Doctors                              |
| Dr. Arjun Mehta                                 |
| Cardiology | 12 years exp | Fee ₹800            |
| [View Slots]                                    |
 ------------------------------------------------
| Select Date                                     |
| Today | Tomorrow | 20 Jun | 21 Jun              |
 ------------------------------------------------
| Available Slots                                 |
| [10:00] [10:30] [11:00] [11:30]                 |
 ------------------------------------------------
| Reason for Visit                                |
| [ Text area ]                                   |
 ------------------------------------------------
| [Confirm Appointment]                           |
 ------------------------------------------------
```

### Screen Elements
- Doctor or department search.
- Department filter chips.
- Doctor cards with specialty, availability, and consultation fee.
- Date selector.
- Slot selector.
- Reason for visit field.
- Confirm appointment button.

### Key States
- No slots available.
- Doctor unavailable.
- Slot selected.
- Appointment confirmation success.
- Duplicate booking warning.

---

## 1.3 Queue Status Screen

### Layout

```text
 ------------------------------------------------
| Back | Queue Status                              |
 ------------------------------------------------
| Current Token                                   |
| C-14                                            |
| Cardiology                                      |
 ------------------------------------------------
| Queue Position                                  |
| You are 4th in line                             |
| Estimated wait: 18 mins                         |
 ------------------------------------------------
| Progress                                        |
| Checked in -> In Queue -> Consultation          |
 ------------------------------------------------
| Doctor                                          |
| Dr. Arjun Mehta                                 |
| Room 204                                        |
 ------------------------------------------------
| Live Queue                                      |
| Now serving: C-10                               |
| Next: C-11, C-12, C-13                          |
 ------------------------------------------------
| [Notify me when close]                          |
 ------------------------------------------------
```

### Screen Elements
- Token number prominently displayed.
- Queue position and predicted wait time.
- Visit status tracker.
- Doctor and room details.
- Live queue preview.
- Notification preference action.

### Key States
- Not checked in.
- In queue.
- Called for consultation.
- Consultation completed.
- Delayed queue notice.

---

## 1.4 Medical Records Screen

### Layout

```text
 ------------------------------------------------
| Back | Medical Records                           |
 ------------------------------------------------
| Search records                                  |
| [ Search by doctor, date, diagnosis ]           |
 ------------------------------------------------
| Filters                                         |
| All | Prescriptions | Lab Reports | Visits      |
 ------------------------------------------------
| Medical Timeline                                |
| 17 Jun 2026                                     |
| Cardiology Visit                                |
| Diagnosis: Hypertension follow-up               |
| [View Details]                                  |
 ------------------------------------------------
| 10 Jun 2026                                     |
| Blood Test Report                               |
| AI Summary Available                            |
| [View Report]                                   |
 ------------------------------------------------
```

### Screen Elements
- Search bar.
- Record type filters.
- Chronological medical timeline.
- Visit cards.
- Lab report cards.
- AI summary badge.

### Key States
- Empty medical history.
- Report pending.
- AI summary available.
- Doctor-approved summary.
- Restricted record access.

---

## 1.5 Billing Screen

### Layout

```text
 ------------------------------------------------
| Back | Bills & Payments                          |
 ------------------------------------------------
| Outstanding Balance                             |
| ₹2,400                                          |
| [Pay Now]                                       |
 ------------------------------------------------
| Recent Bills                                    |
| Invoice #INV-1024                               |
| Consultation + Lab Test                         |
| ₹2,400 | Pending                                |
| [View Invoice] [Pay]                            |
 ------------------------------------------------
| Invoice #INV-1019                               |
| Pharmacy                                        |
| ₹850 | Paid                                     |
| [Download Receipt]                              |
 ------------------------------------------------
```

### Screen Elements
- Outstanding balance summary.
- Invoice list.
- Payment status badges.
- Pay now action.
- Receipt download action.

### Key States
- No dues.
- Payment pending.
- Payment successful.
- Failed payment.
- Partial payment.

---

## 1.6 Smart Chatbot Screen

### Layout

```text
 ------------------------------------------------
| Back | Smart Assistant                           |
 ------------------------------------------------
| Assistant message                               |
| Hello, how can I help you today?                |
 ------------------------------------------------
| Suggested actions                               |
| [Book appointment] [Check queue]                |
| [Explain report]   [Symptoms help]              |
 ------------------------------------------------
| Chat messages                                   |
| Patient: I have fever and headache              |
| AI: I can help guide you, but this is not        |
| a medical diagnosis...                          |
 ------------------------------------------------
| Message input                                   |
| [ Type your message... ] [Send]                 |
 ------------------------------------------------
```

### Screen Elements
- Conversational interface.
- Suggested actions.
- Medical disclaimer for symptom-related queries.
- Secure data access after authentication.
- Escalation prompt for emergencies.

### Key States
- Guest mode.
- Authenticated patient mode.
- Emergency symptom warning.
- Human support escalation.
- AI unavailable fallback.

---

# 2. Doctor Dashboard

## Purpose
The Doctor Dashboard helps doctors manage daily consultations, view queues, access medical histories, create clinical notes, review AI summaries, and monitor workload.

---

## 2.1 Doctor Dashboard Home

### Layout

```text
 ---------------------------------------------------------
| Header                                                  |
| SmartCare AI      Today: 17 Jun 2026       Dr. Profile  |
 ---------------------------------------------------------
| Daily Summary                                           |
| Appointments: 24 | Waiting: 8 | Completed: 12 | Alerts: 2|
 ---------------------------------------------------------
| Current Queue                                           |
| Now Serving: C-10                                       |
| Next Patient: Priya Sharma                              |
| Reason: Chest discomfort follow-up                      |
| [Call Next] [Start Consultation]                        |
 ---------------------------------------------------------
| Today’s Appointments                                    |
| 10:00 AM Priya Sharma      Checked in                   |
| 10:30 AM Rahul Verma       Waiting                      |
| 11:00 AM Anita Rao         Scheduled                    |
 ---------------------------------------------------------
| AI Insights                                             |
| High workload expected after 2 PM                       |
| 3 patients likely to no-show                            |
 ---------------------------------------------------------
| Sidebar / Bottom Nav                                    |
| Dashboard | Queue | Appointments | Records | Reports    |
 ---------------------------------------------------------
```

### Screen Elements
- Daily workload summary.
- Current queue card.
- Next patient details.
- Appointment list.
- AI insights panel.
- Doctor navigation.

### Key States
- No appointments today.
- Queue active.
- Emergency patient inserted.
- Doctor running late.
- AI insights unavailable.

---

## 2.2 Doctor Queue Screen

### Layout

```text
 ------------------------------------------------
| Queue Management                                |
 ------------------------------------------------
| Department: Cardiology                          |
| Room: 204                                       |
 ------------------------------------------------
| Now Serving                                     |
| C-10 | Priya Sharma                             |
| [Start Consultation] [Mark No-show]             |
 ------------------------------------------------
| Waiting List                                    |
| C-11 | Rahul Verma | Normal | 12 mins           |
| C-12 | Anita Rao   | Senior | 15 mins           |
| C-13 | Imran Khan  | Follow-up | 20 mins        |
 ------------------------------------------------
| [Call Next Patient]                             |
 ------------------------------------------------
```

### Screen Elements
- Current serving patient.
- Waiting list with priority and predicted wait.
- Call next action.
- Mark no-show action.
- Start consultation action.

### Key States
- Queue empty.
- Patient not present.
- Priority patient added.
- Queue reassigned.
- Consultation in progress.

---

## 2.3 Patient Consultation Screen

### Layout

```text
 ---------------------------------------------------------
| Patient: Priya Sharma | Age 42 | Blood Group B+          |
| Allergies: Penicillin | Conditions: Hypertension         |
 ---------------------------------------------------------
| Visit Context                                           |
| Appointment reason: Chest discomfort follow-up           |
| Vitals: BP 140/90 | Pulse 84 | Temp 98.6                 |
 ---------------------------------------------------------
| Tabs                                                    |
| Notes | History | Reports | Prescription | AI Summary    |
 ---------------------------------------------------------
| Clinical Notes                                          |
| Symptoms                                                |
| [ Text area ]                                           |
| Diagnosis                                               |
| [ Text area ]                                           |
| Treatment Plan                                          |
| [ Text area ]                                           |
 ---------------------------------------------------------
| Actions                                                 |
| [Save Draft] [Create Prescription] [Complete Visit]      |
 ---------------------------------------------------------
```

### Screen Elements
- Patient identity and clinical risk banner.
- Visit reason and vitals.
- Tabbed workspace.
- Clinical notes form.
- Medical history access.
- Prescription creation.
- Complete visit workflow.

### Key States
- Draft consultation.
- Missing vitals.
- Allergy warning.
- Unsaved notes warning.
- Visit completed.

---

## 2.4 Medical Report Review Screen

### Layout

```text
 ------------------------------------------------
| Medical Reports                                 |
 ------------------------------------------------
| Patient: Priya Sharma                           |
 ------------------------------------------------
| Uploaded Report                                 |
| CBC_Report_June.pdf                             |
| [View Original]                                 |
 ------------------------------------------------
| AI Summary                                      |
| Key findings:                                   |
| - Hemoglobin slightly low                       |
| - WBC within normal range                       |
| - Platelet count normal                         |
 ------------------------------------------------
| Doctor Review                                   |
| [Edit Summary] [Approve] [Reject]               |
 ------------------------------------------------
```

### Screen Elements
- Original document access.
- AI-generated summary.
- Abnormal value highlights.
- Doctor approval workflow.
- Edit and reject options.

### Key States
- Summary generating.
- Summary ready.
- Approved summary.
- Rejected summary.
- AI processing failed.

---

## 2.5 Doctor Workload Screen

### Layout

```text
 ------------------------------------------------
| Workload Insights                               |
 ------------------------------------------------
| Today                                           |
| Scheduled: 24 | Completed: 12 | Waiting: 8      |
 ------------------------------------------------
| Average Consultation Time                       |
| 14 mins                                         |
 ------------------------------------------------
| Peak Load                                       |
| 2 PM - 5 PM                                     |
 ------------------------------------------------
| AI Recommendation                               |
| Shift 4 follow-up patients to Dr. Nair          |
| Add 10-minute buffer after emergency slot       |
 ------------------------------------------------
| [Request Schedule Adjustment]                   |
 ------------------------------------------------
```

### Screen Elements
- Appointment and queue metrics.
- Average consultation time.
- Peak load forecast.
- AI workload recommendations.
- Request adjustment action.

### Key States
- Normal workload.
- Overloaded schedule.
- Underutilized slots.
- Admin approval pending.
- Recommendation unavailable.

---

# 3. Admin Dashboard

## Purpose
The Admin Dashboard gives hospital administrators operational visibility and control across patients, doctors, appointments, queues, billing, departments, reports, and AI insights.

---

## 3.1 Admin Dashboard Home

### Layout

```text
 ---------------------------------------------------------
| Header                                                  |
| SmartCare AI Admin        Search        Notifications   |
 ---------------------------------------------------------
| KPI Cards                                                |
| Patients Today | Appointments | Revenue | Avg Wait Time |
| 148            | 236          | ₹4.8L   | 22 mins       |
 ---------------------------------------------------------
| Operations Overview                                      |
| Queue Load by Department                                |
| Cardiology: High                                        |
| General Medicine: Normal                                |
| Orthopedics: Moderate                                   |
 ---------------------------------------------------------
| Appointment Trends                                      |
| [Chart area]                                            |
 ---------------------------------------------------------
| Alerts                                                  |
| 3 doctors overloaded                                    |
| 12 high no-show risk appointments                       |
| Billing reconciliation pending                          |
 ---------------------------------------------------------
| Sidebar                                                 |
| Dashboard | Patients | Doctors | Appointments | Billing |
| Queue | Records | AI Insights | Settings                 |
 ---------------------------------------------------------
```

### Screen Elements
- Global search.
- KPI cards.
- Department queue load.
- Appointment trends.
- Admin alerts.
- Sidebar navigation.

### Key States
- Normal operations.
- High queue congestion.
- Revenue alert.
- Doctor shortage.
- AI services degraded.

---

## 3.2 Patient Management Screen

### Layout

```text
 ---------------------------------------------------------
| Patients                                  [Add Patient] |
 ---------------------------------------------------------
| Search and Filters                                      |
| [Search name, phone, patient ID]                         |
| Department | Status | Visit Type | Date                  |
 ---------------------------------------------------------
| Patient Table                                           |
| ID       Name           Phone        Last Visit  Status  |
| P-1001   Priya Sharma   98765...     Today       Active  |
| P-1002   Rahul Verma    91234...     15 Jun      Active  |
 ---------------------------------------------------------
| Bulk Actions                                            |
| Export | Send Reminder                                  |
 ---------------------------------------------------------
```

### Screen Elements
- Add patient button.
- Search by name, phone, patient ID.
- Filter controls.
- Patient table.
- Bulk actions.
- Patient status labels.

### Key States
- No patients found.
- Duplicate patient warning.
- Patient created.
- Patient deactivated.
- Export loading.

---

## 3.3 Doctor Management Screen

### Layout

```text
 ---------------------------------------------------------
| Doctors                                    [Add Doctor] |
 ---------------------------------------------------------
| Filters                                                 |
| Department | Specialty | Status | Availability           |
 ---------------------------------------------------------
| Doctor List                                             |
| Dr. Arjun Mehta                                         |
| Cardiology | Available | 24 appointments today          |
| [View Schedule] [Edit]                                  |
 ---------------------------------------------------------
| Dr. Nair                                                |
| General Medicine | On Leave                             |
| [View Schedule] [Edit]                                  |
 ---------------------------------------------------------
```

### Screen Elements
- Doctor list or table.
- Department and specialty filters.
- Availability status.
- Schedule access.
- Add and edit doctor actions.

### Key States
- Doctor available.
- Doctor on leave.
- Doctor overloaded.
- Schedule conflict.
- Doctor deactivated.

---

## 3.4 Appointment Management Screen

### Layout

```text
 ---------------------------------------------------------
| Appointments                              [New Booking] |
 ---------------------------------------------------------
| Calendar / List Toggle                                  |
| [Calendar] [List]                                       |
 ---------------------------------------------------------
| Filters                                                 |
| Date | Department | Doctor | Status                      |
 ---------------------------------------------------------
| Appointment List                                        |
| 10:00 AM | Priya Sharma | Dr. Mehta | Checked in         |
| 10:30 AM | Rahul Verma  | Dr. Mehta | Waiting            |
| 11:00 AM | Anita Rao    | Dr. Nair  | Confirmed          |
 ---------------------------------------------------------
| Actions                                                 |
| Reschedule | Cancel | Check in | Mark no-show            |
 ---------------------------------------------------------
```

### Screen Elements
- Calendar and list views.
- Advanced filters.
- Appointment status badges.
- New booking action.
- Operational actions.

### Key States
- Slot unavailable.
- Double-booking blocked.
- Appointment cancelled.
- Patient checked in.
- No-show flagged.

---

## 3.5 Queue Operations Screen

### Layout

```text
 ---------------------------------------------------------
| Queue Operations                                        |
 ---------------------------------------------------------
| Department Queue Summary                                |
| Cardiology       18 waiting | Avg wait 32 mins | High    |
| General Medicine 09 waiting | Avg wait 15 mins | Normal  |
| Orthopedics      14 waiting | Avg wait 24 mins | Medium  |
 ---------------------------------------------------------
| Active Queue                                            |
| Token | Patient | Priority | Doctor | Wait | Status      |
| C-14  | Priya   | Normal   | Mehta  | 18m  | Waiting     |
| C-15  | Anita   | Senior   | Mehta  | 20m  | Waiting     |
 ---------------------------------------------------------
| Actions                                                 |
| Reassign Doctor | Change Priority | Pause Queue          |
 ---------------------------------------------------------
```

### Screen Elements
- Department queue summary.
- Active queue table.
- Priority labels.
- Wait time prediction.
- Queue intervention actions.

### Key States
- Queue overloaded.
- Emergency inserted.
- Doctor unavailable.
- Queue paused.
- Patient reassigned.

---

## 3.6 Billing Management Screen

### Layout

```text
 ---------------------------------------------------------
| Billing                                                 |
 ---------------------------------------------------------
| Revenue Summary                                         |
| Today: ₹4.8L | Pending: ₹1.2L | Refunds: ₹18K           |
 ---------------------------------------------------------
| Invoice Filters                                         |
| Date | Status | Department | Payment Method              |
 ---------------------------------------------------------
| Invoice Table                                           |
| INV-1024 | Priya Sharma | ₹2,400 | Pending | [View]      |
| INV-1025 | Rahul Verma  | ₹800   | Paid    | [Receipt]   |
 ---------------------------------------------------------
| Actions                                                 |
| Create Invoice | Record Payment | Export Report          |
 ---------------------------------------------------------
```

### Screen Elements
- Revenue summary.
- Pending payment indicators.
- Invoice filters.
- Invoice table.
- Payment and receipt actions.

### Key States
- Invoice pending.
- Invoice partially paid.
- Payment failed.
- Refund requested.
- Billing reconciliation alert.

---

## 3.7 AI Insights Screen

### Layout

```text
 ---------------------------------------------------------
| AI Insights                                             |
 ---------------------------------------------------------
| Model Health                                            |
| Gemini API: Operational                                 |
| Queue Prediction: Active                                |
| Report Summaries: 32 generated today                    |
 ---------------------------------------------------------
| No-show Risk                                            |
| High-risk appointments today: 12                        |
| [View List]                                             |
 ---------------------------------------------------------
| Queue Prediction Accuracy                               |
| Current accuracy: 84%                                   |
 ---------------------------------------------------------
| Workload Optimization                                   |
| 3 doctors overloaded                                    |
| 2 departments need schedule balancing                   |
 ---------------------------------------------------------
| AI Audit                                                |
| Latest AI interactions                                  |
| Symptom Analyzer | Patient consent: Yes | 10:14 AM       |
 ---------------------------------------------------------
```

### Screen Elements
- Gemini API health.
- AI feature usage metrics.
- No-show risk summary.
- Queue prediction accuracy.
- Doctor workload recommendations.
- AI audit list.

### Key States
- AI operational.
- Gemini API degraded.
- High no-show cluster.
- Low prediction confidence.
- Doctor review pending.

---

## 3.8 Settings and Access Control Screen

### Layout

```text
 ---------------------------------------------------------
| Settings                                                |
 ---------------------------------------------------------
| Tabs                                                    |
| Users | Roles | Departments | Billing Rules | AI Config  |
 ---------------------------------------------------------
| Users                                                   |
| Name        Role          Status       Actions           |
| Meera Rao   Billing Staff Active       Edit              |
| Ajay Shah   Doctor        Active       Edit              |
 ---------------------------------------------------------
| Role Permissions                                        |
| [Manage selected role]                                  |
 ---------------------------------------------------------
```

### Screen Elements
- User management.
- Role management.
- Department configuration.
- Billing rules.
- AI configuration.
- Permission editor.

### Key States
- User invited.
- User suspended.
- Role updated.
- Permission denied.
- AI feature disabled.

---

# Shared UI Patterns

## Navigation
- Patients should use bottom navigation on mobile.
- Doctors should use sidebar on desktop and bottom navigation on mobile.
- Admins should use a persistent sidebar on desktop.

## Common Components
- KPI cards
- Status badges
- Search fields
- Filter bars
- Data tables
- Timeline views
- Modal dialogs
- Confirmation prompts
- Toast notifications
- Empty states
- Loading skeletons

## Accessibility Requirements
- All actions must be keyboard accessible.
- Form fields must have visible labels.
- Status badges must not rely only on color.
- Tables need readable headers.
- Error states must be announced clearly.
- Critical actions need confirmation dialogs.

## Mobile-First Behavior
- Dashboards collapse into stacked cards.
- Tables become compact cards on small screens.
- Primary actions remain sticky where useful.
- Filters open in bottom sheets on mobile.
- Navigation should remain reachable with one hand.