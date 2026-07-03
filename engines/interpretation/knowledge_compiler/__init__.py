"""Deterministic Knowledge Compiler for preserved ARK reality.

The compiler consumes ARK-preserved observations and produces candidate
knowledge artifacts. It does not preserve reality, promote truth, generate
embeddings, search, navigate, or call AI.
"""

from .compiler import KnowledgeCompiler
from .models import (
    CANDIDATE_TYPES,
    DEFAULT_COMPILED_AT,
    CandidateArtifact,
    CandidateKind,
    CandidateProvenance,
    CompilerLimits,
    CompilerResult,
    CompilerValidationIssue,
    EvidenceReference,
    KnowledgeCompilerConfig,
)

__all__ = [
    "CANDIDATE_TYPES",
    "DEFAULT_COMPILED_AT",
    "CandidateArtifact",
    "CandidateKind",
    "CandidateProvenance",
    "CompilerLimits",
    "CompilerResult",
    "CompilerValidationIssue",
    "EvidenceReference",
    "KnowledgeCompiler",
    "KnowledgeCompilerConfig",
]
