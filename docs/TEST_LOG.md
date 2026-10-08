# Mechanical test log - 7 October 2026

Gemini preparation addendum: the model-selection/complete-response patch was built and published successfully as version 3. No additional automated tests or real provider call have been run for that patch. The 14 checks below describe the earlier recorded build and mock-provider coverage.

Initial run: 14 meaningful domain/API regression tests; 13 passed, 1 failed. The failing test restored a record marked reviewed_private but without its review object. The previous validator accepted it, so the candidate screen could crash after corrupt/incomplete browser storage.

Correction: restore validation now checks the review object, observation method, criteria and notes, assistance/answers, approval consistency and recipient-record shape. Malformed data triggers a visible recovery notice and fresh fictional cases rather than a crash. This validation is a resilience guard, not authentication or protection against a malicious browser owner.

Checks include the known arithmetic; missing reviewers/deadlines/scope consent; unobserved revision; candidate-first privacy; correction and review-edit invalidation; recipient revocation/expiration; private retries; endpoint rejection of candidate-answer fields; unknown provider; and generic provider errors. Provider success is tested with a mock, not a live LLM call. Browser checks and deployment status are recorded below when actually completed.

## Completed results

After the restore-validator correction: 14/14 existing domain/API checks passed. No live provider call: provider responses use mocks.

Browser flow actually exercised with fictional UM-001: criterion review -> private candidate result -> accuracy confirmation -> recipient-specific authorization -> visible JSON/print preview -> revocation -> correction request -> simulated new review -> private result requiring fresh confirmation. Old permissions remained revoked. WebMCP read/navigation tools worked; invalid session IDs failed without altering the active record.

Actual viewport: 446px, no horizontal overflow observed. The browser viewport override did not change actual DOM width; full desktop verification remains open. Local persistence retained the workflow on reload. The missing-AI-key message appeared from the real endpoint.

Export limitation observed: automatic-download waiting and file-link download timed out in the integrated browser. Changed to a visible copy dialog, standard download link, selectable full JSON and in-app printable proof. JSON copied from the visible textarea was saved as fictional evidence; native browser file download and OS PDF saving remain unverified. Do not call this a confirmed file download. Browser-native printing is not an application-hosted PDF renderer.

Evidence is synthetic, not an employer/candidate study or a measured pilot. Deletion was not exercised. No claims of real hiring decisions, payment or 10-minute median were made.

Two actual private publications succeeded: initial workflow at source 91adef9, then the portable-copy/print refinement and documented walkthrough at 77c2657. Exact native results are in DEPLOYMENT_LOG.md.
