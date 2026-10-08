# UMBRAL - Synthetic Persona Report

Rodrigo Peña León - OPERATOR - Week 9 - 7 October 2026

## 1. Method and evidence boundary

This is a Codex-generated synthetic persona exercise using the actual Umbral interface and fictional records. No candidate or employer was interviewed. Codex operated the candidate and reviewer views; the reviewer notes are simulated, not a real human assessment. The exercise checks workflow behavior and interpretation risks. It cannot validate demand, fairness, accessibility or hiring outcomes.

The prompt is preserved in docs/PERSONA_PROMPT.md. Captures come from the actual local app at http://127.0.0.1:4179, not invented mockups. The browser viewport was 446 pixels wide; a requested desktop override did not change the measured DOM width, so a desktop-size pass is not claimed.

## 2. Invented persona and failed moment

Ruth, 24, has helped a family shop reconcile cash but lacks a formal credential. She can explain her procedure in writing and uses a spreadsheet. She wants to demonstrate one skill without losing control of mistaken feedback or exposing a private incomplete attempt. This profile is an invented stress case, not a claim about Mexican candidates.

Operator counterpart: a career-office coordinator with little reviewer capacity. The coordinator needs a named reviewer and date, usable notes, an observable revision and a measured review cost. A complete-looking proof alone does not show an employer will fund it.

## 3. Synthetic dialogue and interpretation

The following exchange is generated roleplay, not a participant transcript.

Ruth: "Who will read this, and can I explain it in writing?"

Facilitator interpretation: the invitation displays the assigned fictional reviewer, delivery/review dates, rubric and a written explanation option. This supports orientation; a real user comprehension check is still needed.

Ruth: "If I press Confirmar y mantener privado, have I sent it to a shop?"

Facilitator interpretation: no. Accuracy confirmation retains a private state. Recipient authorization requires a separate form with name, purpose, expiry and consent. The demo does not transmit files to the recipient.

Ruth: "The note should say this was a written explanation using fictional movements."

Observed action: Codex requested that correction. The UI displayed Corrección solicitada, removed the approval/share path and kept the old recipient revoked. After a simulated reviewer amended the explanation, the UI returned Resultado privado and required a new candidate confirmation.

Ruth: "Can I take the copy back after someone downloads it?"

Observed action: revocation removed the JSON/print controls for that recipient. The interface explicitly states downloaded copies cannot be recalled. This is a local future-export restriction, not remote deletion or cryptographic access control.

Ruth: "Does the record say I am employable?"

Observed UI: the export says the case is fictional and does not establish identity, employability or hiring. The rubric describes evidence in this task and produces no overall score. A real reviewer could still misuse a document outside the app; this exercise cannot establish that external behavior.

## 4. Actual browser observations

A. Review and candidate-first result. Codex filled all four evidence notes, recorded written observation and confirmed the changed condition. Saving returned to the candidate view with a private result. A manually entered seven-minute value tested the timer field; it is not a measured human-review median.

B. Accuracy and permission. Codex confirmed accuracy, then authorized the fictional Tienda Sol recipient for a stated purpose and 30-day period. The view showed the recipient, purpose, expiry and separate export/revoke controls.

C. Export. The generated JSON was visible and contained the task version, reviewer, observed revision, assistance disclosure and exact recipient authorization. Its displayed contents were saved as evidence/FICTIONAL_PROOF_UM-001.json. The embedded browser's download event and file-link download timed out; a successful native browser download is not claimed. The visible text selection fallback was checked. The printable proof preview was observed; an OS Save as PDF file was not verified.

D. Revocation and correction. Revocation removed export controls. The correction request kept the record private. A subsequent simulated review removed pending correction and required new confirmation, with the old permission still revoked.

E. Missing AI secret. The real scope-assistant button showed that AI was not configured and the reviewed template remained available. No live provider call or generated scope is claimed.

F. Narrow layout. The actual 446-pixel view stacked the sessions, reviewer facts, task and permission rules without horizontal overflow. This is a narrow-browser observation; it is not a full device/accessibility study.

## 5. Product changes prompted by the exercise

The initial export path automatically clicked a temporary link and showed a downloaded toast. The integrated browser did not produce a confirmed download. The revised path displays the exact JSON, exposes a download link and offers text selection with manual saving instructions. Toasts now say the copy is ready, not downloaded. Print preview stays in the current app rather than depending on a popup.

Separately, the mechanical checks found a malformed restored review that could crash the result screen. A strengthened restore validator now rejects that structure and shows a recovery message with new fictional cases. The passing checks demonstrate those tested rules, not production security.

## 6. What changed the operator's view

Generated interpretation, not Rodrigo's personal testimony: a polished proof is insufficient unless review capacity and consent operations are viable. Corrections create more work and invalidate previous permission. The software can make that work visible; it cannot establish demand or create a paid first rung by itself. This preserves the individual brief's concern about income and paid Micro-experience.

The proposed three-business/twelve-candidate pilot remains unperformed. Stop/redesign if fewer than two of three would pay to repeat, median review exceeds ten minutes, or observed explanations add no useful hiring information over the artifact alone.

## 7. Next real validation

Observe candidates explaining the actual task and consent choices; compare artifact-only and observed-proof decisions with employers; measure true reviewer time including corrections; check willingness to fund repetition; test written alternatives and assistive technology; verify export in standard browsers. These are next evidence tasks, not results in this report.
