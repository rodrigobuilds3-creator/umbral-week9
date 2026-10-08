# Mechanical test log - 7 October 2026

Initial run: 14 meaningful domain/API regression tests; 13 passed, 1 failed. The failing test restored a record marked reviewed_private but without its review object. The previous validator accepted it, so the candidate screen could crash after corrupt/incomplete browser storage.

Correction: restore validation now checks the review object, observation method, criteria and notes, assistance/answers, approval consistency and recipient-record shape. Malformed data triggers a visible recovery notice and fresh fictional cases rather than a crash. This validation is a resilience guard, not authentication or protection against a malicious browser owner.

Checks include the known arithmetic; missing reviewers/deadlines/scope consent; unobserved revision; candidate-first privacy; correction and review-edit invalidation; recipient revocation/expiration; private retries; endpoint rejection of candidate-answer fields; unknown provider; and generic provider errors. Provider success is tested with a mock, not a live LLM call. Browser checks and deployment status are recorded below when actually completed.
