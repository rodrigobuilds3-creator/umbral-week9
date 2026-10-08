# Gemini activation

## Preparation — 7 October 2026, Mexico City

Rodrigo authorized a dedicated Gemini key and its storage as a secret in the Umbral server's Sites environment. Billing activation was excluded. No credential has been generated or stored yet, and no real model response has been observed.

Sites returned environment revision 0, with no entries. Google AI Studio opened with Rodrigo's account, but reported a network error and no imported Cloud project. A dedicated project or an existing project must be selected before a key can be created. Approval review blocked project creation as a separate action from the authorized key; that action remains pending explicit authorization.

The current default is `gemini-3.5-flash-lite`. Google's current documentation limits 2.5 models to projects that have previously used them, and recommends 3.5 Flash-Lite or 3.8 Flash for new projects. This model supports the Generate Content endpoint and minimal thinking. The server requests 1,024 output tokens, accepts only a complete `STOP` response, excludes thought parts, and never sends candidate answers. A quota error is displayed clearly without exposing provider credentials.

Sources consulted:

- [Gemini models and access limits](https://ai.google.dev/gemini-api/docs/models)
- [Gemini 3.5 Flash-Lite](https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash-lite)
- [Thinking configuration and token limits](https://ai.google.dev/gemini-api/docs/generate-content/thinking)
- [API keys and server-side secret storage](https://ai.google.dev/gemini-api/docs/api-key)

## Required activation sequence

1. Create or select the explicitly authorized Google Cloud project without enabling billing.
2. Create a dedicated Gemini-only key. Handle the key through a secure local channel, without printing it in chat, browser evidence, source files, or Git.
3. Store `GEMINI_API_KEY` in Sites with `is_secret: true`; preserve other runtime entries.
4. Deploy a saved Umbral version to apply the new environment revision.
5. Invoke the published scope assistant once with the synthetic cash template. Record actual model, provider response, date, and visible app result. Key presence alone is not successful activation.
6. Update Packet, delivery status, demo script and deployment evidence only after the live response succeeds.
