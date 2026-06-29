# ARK Admission

ARK admission is the final contract membrane between accepted reviewed artifacts and future observations.

`create_admission_candidate(candidate_artifact, promotion_decision)` accepts only a `CandidateArtifact(status="candidate")` with a matching accepted `PromotionDecision`. The artifact and decision must carry matching noncanonical provenance. The resulting `AdmissionCandidate` preserves `request_id` and `trace_id` and is marked `ready_for_observation`.

This is not persistence. It does not write ARK, does not create observations, does not open files, does not call the network, and does not run autonomous execution. A later ARK-owned admission step must separately decide whether and how to create an observation.
