# TriAvg Report

## Purpose

Record bounded uncertainty estimates where priority depends on uncertain
outcomes.

## Formula

```text
TriAvg = (minimum + expected + maximum) / 3
```

## Required Fields

| Field | Meaning |
| --- | --- |
| Bundle ID | Stable P4 bundle identifier. |
| Minimum Outcome | Conservative expected value. |
| Expected Outcome | Most likely expected value. |
| Maximum Outcome | Optimistic expected value. |
| TriAvg | Average of minimum, expected, and maximum. |
| Assumptions | Evidence and assumptions behind the estimate. |

## Current Status

Awaiting P5 execution.
