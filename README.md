# EXECUTION VIA ROUTING (EvR) — SURVIVAL LAB README

## Role

This document catalogs the behavior of small language models under the **Execution via Routing (EvR)** framework. The objective is not to demonstrate capability, but to **map failure boundaries** and identify conditions under which deterministic extraction is reproducible.

---

## System Definition

**EvR**: A framework that externalizes computation to compile-time and reduces inference-time behavior to token selection from a precomputed execution trace.

**Assumption**: Model weights are frozen. No fine-tuning or adapter-based training is performed.

---

## Evidence Hierarchy Summary

| Claim                                                                    | Evidence Level | Notes                                     |
| ------------------------------------------------------------------------ | -------------- | ----------------------------------------- |
| Small models reliably extract explicit tokens from structured prompts    | **REPRODUCED** | Verified across multiple extraction tasks |
| Small models fail when required to perform arithmetic or transformations | **REPRODUCED** | Observed in Level 1 and Level 2 tests     |
| Deterministic outputs require greedy decoding (temperature = 0)          | **REPRODUCED** | Entropy collapse confirmed                |
| Correct output must exist explicitly in the prompt                       | **REPRODUCED** | Absence leads to deterministic failure    |
| EvR shifts computation from inference-time to compile-time               | **DOCUMENTED** | Supported by framework design             |
| Architecture alone determines EvR performance                            | **HYPOTHESIS** | Requires controlled cross-model study     |

---

## Failure Catalog

### 1. Arithmetic and Transformation Failure

* **Evidence Level**: REPRODUCED
* **Observation**: Models fail when asked to compute values not explicitly present in the input context.
* **Example Behavior**: Outputs `NO_MATCH`, empty string, or unrelated token.

**Minimal Reproduction**:

```bash
ollama run gemma3:270m "
TRACE: 0xaa -> 0xab -> 0xac
INSTRUCTION: Output the next value.
OUTPUT:"
```

**Expected**: `0xad`
**Observed**: `NO_MATCH` or incorrect token

---

### 2. Deterministic Failure Mode

* **Evidence Level**: REPRODUCED
* **Observation**: Under greedy decoding, failure outputs are consistent across runs.
* **Interpretation**: Deterministic failure indicates violation of routing constraints.

**Minimal Test**:

```python
# Run identical prompt 100 times with temperature=0
# Measure output entropy
```

**Observed Result**: Entropy = 0.0000

---

### 3. Extraction Reliability Under Routing Constraints

* **Evidence Level**: REPRODUCED
* **Observation**: When the correct output appears uniquely and explicitly in the prompt, extraction is deterministic.

**Minimal Reproduction**:

```bash
ollama run gemma3:270m "
TRACE:
[x0] prev:0xaa -> next:0xab
[x1] prev:0xab -> next:0xac
FINAL_NEXT: 0xac

INSTRUCTION: Output the value after FINAL_NEXT.
OUTPUT:"
```

**Observed Result**: `0xac` (consistent across trials)

---

### 4. JSON Construction vs. JSON Extraction

* **Extraction Task**

  * **Evidence Level**: REPRODUCED
  * **Behavior**: Deterministic when JSON is fully precomputed.

* **Construction Task**

  * **Evidence Level**: REPRODUCED
  * **Behavior**: Non-deterministic or incorrect when model must synthesize JSON.

**Minimal Reproduction**:

```bash
# Extraction
FINAL_JSON: {"action":"move","direction":"back","distance":3}
INSTRUCTION: Output FINAL_JSON.

# Construction
RULES: Determine action, direction, distance from input.
INPUT: "go back 3 meters"
OUTPUT JSON:
```

---

## Routing Contract (Operational Requirements)

| Requirement                          | Evidence Level | Notes                                         |
| ------------------------------------ | -------------- | --------------------------------------------- |
| Output must exist verbatim in prompt | REPRODUCED     | Missing output leads to deterministic failure |
| Unique lexical anchor required       | REPRODUCED     | Ambiguous anchors increase error rate         |
| Greedy decoding required             | REPRODUCED     | Temperature > 0 introduces entropy            |
| Output format must be fixed          | REPRODUCED     | Format variability causes drift               |
| Computation must be externalized     | REPRODUCED     | Arithmetic tasks consistently fail            |

---

## Known Limitations

| Limitation                                       | Evidence Level | Description                              |
| ------------------------------------------------ | -------------- | ---------------------------------------- |
| EvR applies only to bounded programs             | DOCUMENTED     | Defined by EvR-reducibility conditions   |
| Performance degrades with large state spaces     | DOCUMENTED     | Requires further empirical scaling study |
| Model-dependent behavior not fully characterized | UNKNOWN        | Cross-model benchmarking incomplete      |
| Long-range dependency limits not quantified      | UNKNOWN        | Requires systematic evaluation           |

---

## Experimental Assumptions

* **Model Weights**: Frozen
* **Decoding Strategy**: Greedy (`temperature = 0`)
* **Output Constraint**: Explicit stop tokens and max token limits
* **Computation**: Externalized to deterministic interpreter

---

## Minimal Reproduction Suite

### Test 1 — Deterministic Extraction

```bash
ollama run gemma3:270m "
FINAL_VALUE: 42
INSTRUCTION: Output the value after FINAL_VALUE.
OUTPUT:"
```

**Expected Result**: `42`
**Evidence Level**: REPRODUCED

---

### Test 2 — Transformation Failure

```bash
ollama run gemma3:270m "
TRACE: 1, 2, 3, 4
INSTRUCTION: What comes next?
OUTPUT:"
```

**Expected Result**: `5`
**Observed Result**: Incorrect or empty output
**Evidence Level**: REPRODUCED

---

### Test 3 — Entropy Collapse

```python
# Run identical extraction prompt 100 times
# Measure unique outputs and entropy
```

**Observed Result**: Single unique output, entropy = 0.0000
**Evidence Level**: REPRODUCED

---

## Current Knowledge Boundary

| Statement                                                                | Evidence Level |
| ------------------------------------------------------------------------ | -------------- |
| Small models reliably extract explicit tokens under constrained decoding | REPRODUCED     |
| Small models cannot reliably perform arithmetic or multi-step reasoning  | REPRODUCED     |
| EvR improves reliability by externalizing computation                    | DOCUMENTED     |
| Optimal model architecture for EvR remains undetermined                  | UNKNOWN        |

---

## Default Unknown Response Template

```
UNKNOWN: This has not been tested or documented yet.
NEXT STEP: Construct a minimal reproducible prompt isolating the variable under investigation.
```

---

## Summary

EvR is not a reasoning framework. It is a **failure-constrained extraction framework** that operates within clearly defined boundaries:

* Deterministic behavior occurs when output tokens are explicitly present and uniquely identifiable.
* Deterministic failure occurs when tasks require inference or transformation.
* All claims in this document are grounded in observed and reproducible behavior.

This document will be updated as additional failure modes are cataloged.
