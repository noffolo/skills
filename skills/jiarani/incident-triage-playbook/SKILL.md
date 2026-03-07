---
name: incident-triage-playbook
description: Runbook-first incident triage workflow for service outages and high-error alerts.
version: 1.1.0
---

# Incident Triage Assistant

Use when an alert fires and you need a consistent first-15-min triage flow.

## Inputs to Gather

- Primary target (service, team, or dataset)
- Current impact and urgency
- Assigned owner and deadline

## Core Commands

- `triage intake --service <name> --severity <sev>`
- `triage timeline --append "<event>"`
- `triage owner --set "<oncall>"`
- `workflow checklist --from templates/checklist.md`

## Operating Notes

- Prefer explicit owner assignment before action.
- Keep timeline notes concise and timestamped.
- Save output artifacts for audit and handoff.
- This version adds an operations checklist template for handoffs.

Version marker: incident-triage-playbook 1.1.0
