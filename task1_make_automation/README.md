# Task 1 — Contact enrichment automation

This directory contains the exported Make.com Task 1 blueprint, Airtable field contract, Google Docs template, and operator notes. The blueprint has five modules: Airtable create, Groq summary, Google Docs create, Airtable update, and Slack report. After importing, reconnect your own service connections and confirm the Airtable base/table, Docs folder, Slack destination, and schedule before activation. Task 1 uses Groq as its LLM provider.

## Required scenarios

1. **Contact generation**: scheduler or manual webhook → generate/validate a contact → Airtable create record → Groq company summary → Google Docs create from template → update Airtable with summary and document URL. Add an error handler after each external write. Use an idempotency key for retries.
2. **Daily digest**: schedule at 07:00 in the selected timezone → query records created since prior digest and with a completed document URL → format totals and latest company names → post to the selected Slack channel. Decide and document the timezone before activation.

`airtable_schema.json` defines the required table. `company_report_template.md` is the content template to reproduce in Google Docs. Keep the Groq prompt grounded in the provided company name and instruct it to label unknown facts rather than invent them.

For local components that call an LLM, configure `LLM_PROVIDER=groq` and `GROQ_API_KEY` in the untracked `.env`. In Make, reconnect the Groq module using a Make-managed connection. The exported blueprint contains module configuration but no API keys; service connection IDs and resource references may need remapping in your Make organization. Never add a Slack webhook URL, API key, or service credential to the public repository.

## Activation checklist

- Create Airtable base/table and fields; note base ID and table ID.
- Connect Groq, Google Docs/Drive, Airtable and Slack accounts through Make connections.
- Replace prompts, mappings, filters, and channel references in the scenario; do not put API keys in JSON.
- Configure bounded retries and a dead-letter/error route that records the contact ID, module, timestamp, and safe error message.
- Run one manual end-to-end record, verify doc permission/URL, then test digest boundaries and Slack delivery.
- Activate scheduler only after verifying its timezone, 07:00 schedule, and expected operation volume.
