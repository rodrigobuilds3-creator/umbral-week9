# Gemini activation

## Preparation — 7 October 2026, Mexico City

Rodrigo authorized a dedicated Gemini key and its storage as a secret in the Umbral server's Sites environment. Billing activation was excluded. At preparation time, no credential had been generated or stored and no real model response had been observed.

Sites initially returned environment revision 0, with no entries. Google AI Studio initially reported a network error and no imported Cloud project. Approval review blocked project creation as a separate action from the authorized key. Rodrigo then explicitly authorized the project creation and remaining activation work.

The current default is `gemini-3.5-flash-lite`. Google's current documentation limits 2.5 models to projects that have previously used them, and recommends 3.5 Flash-Lite or 3.8 Flash for new projects. This model supports the Generate Content endpoint and minimal thinking. The server requests 1,024 output tokens, accepts only a complete `STOP` response, excludes thought parts, and never sends candidate answers. A quota error is displayed clearly without exposing provider credentials.

Sources consulted:

- [Gemini models and access limits](https://ai.google.dev/gemini-api/docs/models)
- [Gemini 3.5 Flash-Lite](https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash-lite)
- [Thinking configuration and token limits](https://ai.google.dev/gemini-api/docs/generate-content/thinking)
- [API keys and server-side secret storage](https://ai.google.dev/gemini-api/docs/api-key)

## Actual activation — 7 October 2026, Mexico City

The dedicated Google Cloud project `Umbral Week 9` and its dedicated Gemini auth key were created with Rodrigo's authorization. AI Studio visibly showed Free tier and an untouched Set up billing action. No billing activation was performed.

Sites environment revision 1 stores `GEMINI_API_KEY` as a masked secret and `GEMINI_MODEL=gemini-3.5-flash-lite`. The existing saved version 3 was successfully republished to apply that environment revision: deployment `appgdep_6ac722cfd6608191b8f331f39631748d`, native success at 2026-10-08T04:57:57.809898Z (7 October in Mexico City).

The published app's scope assistance action then returned an actual Gemini draft for the fictional cash template. The visible field populated and displayed `Redacción con IA (Gemini). Revísala; no evalúa capacidad.` This was a real provider response, not mock or deterministic fallback. Evidence: `evidence/GEMINI_LIVE_FIRST_SCOPE.json`.

Codex's simulated operator review identified ambiguous wording in that first draft: it told the candidate not to reveal a final number and offered questions as an alternative to a written explanation. The system prompt was refined to request both calculations without the assistant supplying their answers, and to keep reviewer questions after the candidate's written explanation. No human candidate was assessed and no invitation was created from the initial draft.

## Configuration sequence

1. Create or select the explicitly authorized Google Cloud project without enabling billing.
2. Create a dedicated Gemini-only key. Handle the key through a secure local channel, without printing it in chat, browser evidence, source files, or Git.
3. Store `GEMINI_API_KEY` in Sites with `is_secret: true`; preserve other runtime entries.
4. Deploy a saved Umbral version to apply the new environment revision.
5. Invoke the published scope assistant once with the synthetic cash template. Record actual model, provider response, date, and visible app result. Key presence alone is not successful activation.
6. Update Packet, delivery status, demo script and deployment evidence only after the live response succeeds.
