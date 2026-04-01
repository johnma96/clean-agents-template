# Incident Response Runbook — {{ cookiecutter.project_name }}

> **Owner:** <!-- team / on-call alias -->
> **Last reviewed:** <!-- YYYY-MM-DD -->
> **Severity levels:** S1 (service down) · S2 (degraded) · S3 (minor) · S4 (cosmetic)

---

## 1. Triage — First 5 minutes

| Step | Action |
|------|--------|
| 1 | **Acknowledge** the alert in the on-call channel. |
| 2 | Open the monitoring dashboard (`/monitoring/tracer.py` traces or your APM). |
| 3 | Classify severity (S1–S4) based on user impact. |
| 4 | If S1/S2 → start a dedicated incident channel and page the lead. |
| 5 | Post an initial status update to stakeholders. |

---

## 2. LLM Provider Outage (S1)

**Symptoms:** API calls to the LLM provider return `5xx`, timeouts spike, agent
responses stop arriving.

### Diagnosis

```bash
# Check provider status page (example for OpenAI)
curl -s https://status.openai.com/api/v2/status.json | python -m json.tool

# Review recent error logs
make logs | grep -i "LLMProvider\|openai\|anthropic" | tail -50
```

### Mitigation

1. **Activate fallback provider** (if configured):
   - Update `configs/<env>.yaml` → `llm.provider` to the backup model.
   - Redeploy or restart the service:
     ```bash
     docker compose restart api
     ```
2. **If no fallback is available:**
   - Enable **graceful degradation mode**: return a cached / templated response
     explaining temporary unavailability.
   - Set a circuit breaker flag in environment variables:
     ```bash
     export LLM_CIRCUIT_OPEN=true
     docker compose restart api
     ```
3. **Communicate** estimated recovery time to stakeholders.

### Recovery

- Monitor provider status page until resolved.
- Remove circuit breaker flag / revert to primary provider.
- Verify with a smoke test:
  ```bash
  curl -X POST http://localhost:8000/api/v1/agent/invoke \
    -H "Content-Type: application/json" \
    -d '{"query": "ping"}'
  ```

---

## 3. Prompt Degradation / Hallucinations (S2)

**Symptoms:** Agent accuracy drops sharply, users report incorrect or invented
information, evaluation scores fall below threshold.

### Diagnosis

```bash
# Run the evaluation suite against the current model + prompts
python scripts/evaluate_agent.py --config configs/production.yaml

# Compare with baseline metrics stored in data/
diff <(cat data/baseline_eval.json) <(cat data/latest_eval.json)
```

### Mitigation

1. **Pin the model version** in `configs/<env>.yaml` to the last known-good
   snapshot (e.g., `gpt-4-0613` instead of `gpt-4`).
2. **Rollback prompts** if a recent prompt change is the suspected cause:
   ```bash
   git log --oneline -- src/{{ cookiecutter.project_slug }}/domain/prompts/
   git checkout <last-good-sha> -- src/{{ cookiecutter.project_slug }}/domain/prompts/
   ```
3. Redeploy and re-run evaluations to confirm improvement.

### Recovery

- Investigate root cause (model update, prompt regression, data drift).
- Update the prompt test suite (`tests/unit/domain/test_prompts.py`) with the
  failing case so it doesn't recur.
- Unpin the model version only after validating the new version passes all
  evaluations.

---

## 4. Cost Spike / Runaway Agent (S1)

**Symptoms:** Billing alerts fire, token usage jumps 10×+, a single agent
invocation generates an unusually long chain of LLM calls.

### Diagnosis

```bash
# Check token usage in monitoring traces
make logs | grep -i "tokens\|usage\|cost" | tail -100

# Identify the runaway request by trace/request ID
make logs | grep "<request_id>"
```

### Mitigation

1. **Kill the runaway process immediately:**
   ```bash
   docker compose stop api
   ```
2. **Set hard limits** (if not already in place):
   - `LLM_MAX_TOKENS_PER_REQUEST` in `.env`
   - `LLM_MAX_CALLS_PER_INVOCATION` (loop guard) in agent config
3. Restart with limits applied:
   ```bash
   docker compose up -d api
   ```

### Recovery

- Audit the agent code path that caused the loop
  (`application/agents/` and `application/workflows/`).
- Add or tighten the loop guard in `application/agents/agent_utils.py`.
- Add an integration test that asserts max LLM calls per invocation.

---

## 5. Memory / Vector Store Corruption (S2)

**Symptoms:** Agent returns stale or contradictory context, retrieval scores
drop, vector search returns empty results.

### Diagnosis

```bash
# Verify vector store connectivity
python -c "from src.{{ cookiecutter.project_slug }}.infrastructure.retrieval.vector_store import VectorStore; print(VectorStore().health_check())"

# Count indexed documents
python -c "from src.{{ cookiecutter.project_slug }}.infrastructure.retrieval.vector_store import VectorStore; print(VectorStore().count())"
```

### Mitigation

1. **Switch to in-memory fallback** (for critical path only):
   ```python
   # In infrastructure/memory/memory_store.py, InMemoryStore is always available
   ```
2. **Re-ingest documents** from the source of truth:
   ```bash
   python scripts/ingest_documents.py --config configs/production.yaml --force
   ```

### Recovery

- Investigate the corruption cause (concurrent writes, schema migration, provider issue).
- Validate document count and sample retrieval accuracy.
- Restore vector store from backup if re-ingestion is not sufficient.

---

## 6. Post-Incident — After Every S1/S2

| Step | Owner | Deadline |
|------|-------|----------|
| Write a blameless post-mortem | Incident lead | +48 hours |
| Identify action items with owners | Team | +48 hours |
| Update this runbook if a new scenario was discovered | On-call | +1 week |
| Add missing monitoring / alerts | Infra | +1 sprint |
| Share learnings in team retrospective | Team lead | Next retro |

### Post-Mortem Template

```markdown
## Incident: <title>
**Date:** YYYY-MM-DD
**Duration:** HH:MM
**Severity:** S1 / S2
**Lead:** @name

### Summary
One-paragraph description of what happened.

### Timeline
- HH:MM — Alert fired
- HH:MM — Acknowledged by @name
- HH:MM — Root cause identified
- HH:MM — Mitigation applied
- HH:MM — Service restored

### Root Cause
Why did this happen?

### Impact
Users affected, requests failed, cost incurred.

### Action Items
- [ ] Description — @owner — due date
- [ ] Description — @owner — due date

### Lessons Learned
What went well? What can improve?
```

---

## Quick Reference — Key Commands

```bash
# Health check
curl http://localhost:8000/health

# Restart service
docker compose restart api

# View logs (real-time)
docker compose logs -f api

# Run evaluation suite
python scripts/evaluate_agent.py --config configs/production.yaml

# Re-ingest documents
python scripts/ingest_documents.py --config configs/production.yaml --force
```

---

> **Remember:** Update this runbook every time you handle an incident.
> A runbook that is not maintained is worse than no runbook — it gives false confidence.
