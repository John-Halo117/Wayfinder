# Prompt Architecture Standard

This standard defines the canonical structure for Wayfinder engineering prompts.
Prompts are compiler passes: they consume bootstrap and phase artifacts, perform
exactly one responsibility, and emit stable outputs for later passes.

Bootstrap precedes every prompt. Prompts must not repeat constitutional,
architectural, roadmap, engineering, or prompt-standard content already present
in inherited artifacts.

## Mission

State the single responsibility of the prompt.

## Inheritance

Declare prior artifacts the prompt depends on. Do not restate their content.

## Inputs

Declare only new inputs for this pass.

## Objectives

List the pass-specific outcomes.

## Tasks

List bounded steps required to produce the outputs.

## Validation

Declare checks that prove the pass succeeded.

## Outputs

Declare exact artifacts or response shapes produced by the pass.

## Prohibited

Declare out-of-scope behavior for this pass.

## Success

Ask exactly one success question.

## Engineering Invariants

- Prompts have exactly one responsibility.
- Prompts are modular, composable, idempotent, and deterministic where
  practical.
- Prompts consume previous artifacts instead of regenerating them.
- Prompts contain only Mission, Inheritance, Inputs, Objectives, Tasks,
  Validation, Outputs, Prohibited, and Success.
- Prompt ordering must form a directed acyclic pipeline.
- Every output should be a possible input to a later prompt.
- Required validation must remain explicit.
