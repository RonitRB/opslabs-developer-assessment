# Task 1 — Contact enrichment automation

This directory holds a Make.com scenario design, Airtable field contract, Google Docs template, and operator notes. The JSON is a portable workflow specification; Make exports are tenant-specific and depend on module versions and connection IDs, so validate/remap its steps in your Make organization before activation. Task 1 uses Groq as its LLM provider.

## Required scenarios

1. **Contact generation**: scheduler or manual webhook → generate/validate a contact → Airtable create record → Groq company summary → Google Docs create from template → update Airtable with summary and document URL. Add an error handler after each external write. Use an idempotency key for retries.
2. **Daily digest**: schedule at 07:00 in the selected timezone → query records created since prior digest and with a completed document URL → format totals and latest company names → post to the selected Slack channel. Decide and document the timezone before activation.

`airtable_schema.json` defines the required table. `company_report_template.md` is the content template to reproduce in Google Docs. Keep the Groq prompt grounded in the provided company name and instruct it to label unknown facts rather than invent them.

For local components that call an LLM, configure `LLM_PROVIDER=groq` and `GROQ_API_KEY` in the untracked `.env`. In Make, create a Groq connection or an authenticated HTTP connection using a Make-managed secret. The included JSON is a design specification and does not contain credentials or connection IDs.

## Activation checklist

- Create Airtable base/table and fields; note base ID and table ID.
- Connect Groq, Google Docs/Drive, Airtable and Slack accounts through Make connections.
- Replace prompts, mappings, filters, and channel references in the scenario; do not put API keys in JSON.
- Configure bounded retries and a dead-letter/error route that records the contact ID, module, timestamp, and safe error message.
- Run one manual end-to-end record, verify doc permission/URL, then test digest boundaries and Slack delivery.
- Activate scheduler only after verifying its timezone, 07:00 schedule, and expected operation volume.
