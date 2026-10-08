# Umbral - Week 9 / OPERATOR

A Spanish-first First-Proof workflow: bounded fictional task, named human reviewer, candidate-first feedback, corrections and recipient-specific permission.

**Published:** https://umbral-week9-rodrigo.j6x567qt8g.chatgpt.site

Public access was explicitly authorized by Rodrigo and enabled on 7 October 2026. This is a functional educational demonstration. The role selector is navigation, not authentication. Never enter real candidate or client data.

## Run locally

Requires Node 22+; no dependencies to install.

```sh
npm run dev
```

Open http://127.0.0.1:4179. Build with `npm run build`. Output is `dist/client` plus the Cloudflare-compatible `dist/server/index.js` Worker. The server should be restarted after Worker changes. Browser source changes require a page reload.

## One task, three actors

- Operator assigns reviewer, task scope and deadlines.
- Candidate submits an explanation, changed-condition response and assistance disclosure.
- Reviewer records evidence against four criteria and the observed changed condition.
- Candidate receives the private result, requests corrections, confirms accuracy and separately authorizes each recipient.
- Corrections or new reviews invalidate old approval and permissions. Revocation prevents generating new copies; it cannot recall downloaded files.

JSON is displayed in a dialog with a download link and a selection fallback. PDF uses a visible print view and the browser's Save as PDF option. The embedded browser did not confirm a downloaded file, so the build log records the limitation. No files are sent to recipients by the application.

## AI configuration

The optional drafting endpoint uses Gemini via a server-side `GEMINI_API_KEY`. Set that secret in the deployment environment; never put it in browser code, Git, or a chat transcript. `GEMINI_MODEL` defaults to `gemini-2.5-flash`.

Requests accept only the closed task ID and accommodation option. Candidate names, answers, notes and judgments are excluded from the model request. Without a key, the endpoint returns a clear 503 message and the verified task remains usable. This build has **not** completed a live LLM call. Mock provider checks do not count as one.

## Evidence and delivery

`docs/PACKET.md` was committed before source code. `docs/TEST_LOG.md` records one real restore-validation defect and its correction, 14 passing regression checks, browser observations and export limitations. `docs/PERSONA_REPORT.md` is explicitly synthetic. `docs/DEMO_SCRIPT.md` and `docs/REFLECTION_SCRIPT.md` are recording scripts, not videos.

The supplied Blueprint remains a draft synthesis; building this slice does not certify a live five-person team agreement. Rodrigo's individual Brain brief remains final and retains his Micro-experience preference.

See `docs/DELIVERY_STATUS.md` for achieved items and missing evidence. Public source: https://github.com/rodrigobuilds3-creator/umbral-week9. The original nine build commits were pushed intact to `main`; the public-delivery documentation extends that history. Sites also preserves the pushed source states in its managed repository.

## Technical limits

Local browser persistence, no cross-device collaboration, no verified identities, no server-side candidate database or protected proof URL. Consent rules protect the normal demo workflow; browser owners can modify their own storage. Real use requires authenticated actor isolation, reviewer calibration, consent enforcement, retention and deletion controls, accessibility research and employer validation.
