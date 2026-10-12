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

The drafting endpoint uses Gemini via a server-side `GEMINI_API_KEY`. The live deployment stores that key as a masked Sites secret; never put it in browser code, Git, or a chat transcript. `GEMINI_MODEL` defaults to `gemini-3.5-flash-lite`, with minimal thinking for this short drafting task. Two real published-app drafts were observed on 7 October 2026; the first exposed ambiguous wording, the prompt was refined, and the corrected draft was verified. Responses cut short by token limits are rejected rather than inserted into the invitation. Setup and live evidence are tracked in [Gemini activation](docs/GEMINI_ACTIVATION.md).

Requests accept only the closed task ID and accommodation option. Candidate names, answers, notes and judgments are excluded from the model request. Without a key, the endpoint returns a clear 503 message and the verified task remains usable. Two real live drafts are preserved separately from mock-provider checks. Mocks do not count as a real LLM call.

## Evidence and delivery

The Packet core was committed before code as c3a13ed. Missing imagegen/diagram/architecture elements were added after implementation during the final audit; this chronology limit is explicit. The latest source passed 14/14 domain/API checks on 11 October. A fresh AI Studio persona received six ordered actual screenshots, the worst confirmation-versus-sharing confusion was corrected, and a new capture was retested. Original responses and remaining doubts are preserved.

The 3:30 DEMO is ready locally with actual app captures and disclosed synthetic narration. The separate camera REFLECT and real team FUSION remain pending. Original visible CHAT/BUILDCHAT exports and private provenance stay outside this public repository. The Brain research appendix remains explicitly Codex-operated and cannot certify personal 40-minute participation.

The supplied Blueprint remains a draft synthesis; building this slice does not certify a live five-person team agreement. Rodrigo's individual Brain brief remains final and retains his Micro-experience preference.

See `docs/DELIVERY_STATUS.md` for achieved items and missing evidence. Public source: https://github.com/rodrigobuilds3-creator/umbral-week9. The original nine build commits were pushed intact to `main`; the public-delivery documentation extends that history. Sites also preserves the pushed source states in its managed repository.

## Technical limits

Local browser persistence, no cross-device collaboration, no verified identities, no server-side candidate database or protected proof URL. Consent rules protect the normal demo workflow; browser owners can modify their own storage. Real use requires authenticated actor isolation, reviewer calibration, consent enforcement, retention and deletion controls, accessibility research and employer validation.
