# Security

Wayfinder owns security architecture semantics, trust model semantics, policy
language, identity semantics, and authorization model semantics. It does not
own universal security implementation or runtime enforcement.

Future implementation must preserve:

- verifiable identity for semantic artifacts and governance decisions;
- explicit authorization for semantic changes;
- auditability for ontology, model, policy, and ownership changes;
- least privilege and deny-by-default governance operations;
- no embedded secrets in specifications, examples, telemetry, logs, or
  diagnostics.

No security implementation is present in this skeleton.

