# 📘 Report: Temperature, Entropy, and Computational Regimes in Transformers

## A Practical Framework for Constrained LLM Execution

---

# 1. Executive Summary

This report formalizes an empirical framework for understanding how **temperature and entropy influence transformer behavior**, particularly in the context of **constrained execution systems like CALYX**.

Key findings:

* Temperature controls **distribution exposure**, not computational power
* Transformer behavior can be grouped into **distinct empirical regimes**
* Different task types (route, classify, synthesize, etc.) require **different entropy levels**
* Constraining LLMs to **low-entropy regimes enables deterministic, verifiable systems**
* Intermediate representations (IR) and VMs reduce entropy and improve reliability

---

# 2. Core Model

## 2.1 Temperature as a Control Variable

Temperature modifies the token sampling distribution:

```
P(token) → softened (high temp) or sharpened (low temp)
```

* **Low temperature (≈ 0.0)**
  → collapses distribution
  → near-deterministic (argmax behavior)

* **High temperature (> 1.0)**
  → expands distribution
  → long-tail sampling and exploration

---

## 2.2 Entropy as the Measurable Quantity

Entropy reflects uncertainty in token selection:

* Low entropy → predictable outputs
* High entropy → diverse outputs

**Key relationship:**

```
Temperature ↑ → Entropy ↑ → Exploration ↑
Temperature ↓ → Entropy ↓ → Determinism ↑
```

---

# 3. Behavioral Regimes (Empirical)

Transformers exhibit distinct *behavioral regimes* depending on entropy:

| Regime                     | Temperature | Behavior               | Analogy (Non-Literal) |
| -------------------------- | ----------- | ---------------------- | --------------------- |
| **Deterministic**          | 0.0–0.3     | Single dominant path   | DFA-like              |
| **Stable Probabilistic**   | 0.3–0.7     | Limited branching      | Probabilistic FSM     |
| **Ambiguous / Generative** | 0.7–1.1     | Multiple valid outputs | CFG-like              |
| **Exploratory**            | 1.1–1.5     | Wide branching         | Stochastic generator  |

⚠️ These are **analogies**, not formal equivalence to the Chomsky hierarchy.

---

# 4. The Seven Action Types

A key contribution is identifying **seven fundamental transformer actions**, each with distinct entropy requirements:

| Action         | Description           | Entropy Need | Failure Mode       |
| -------------- | --------------------- | ------------ | ------------------ |
| **Route**      | Select next state     | Very Low     | Drift / misrouting |
| **Classify**   | Assign label          | Low          | Instability        |
| **Compare**    | Measure similarity    | Low-Medium   | Overconfidence     |
| **Transform**  | Reformat input        | Medium       | Loss of structure  |
| **Synthesize** | Generate novel output | Medium-High  | Hallucination      |
| **Compress**   | Reduce to essence     | High         | Oversimplification |
| **Search**     | Explore possibilities | Very High    | Chaos              |

---

# 5. The “123 Phenomenon”

## Observation

At higher temperatures, correct minimal outputs appear more frequently:

| Temp | Exact Output Rate |
| ---- | ----------------- |
| 0.0  | 0%                |
| 0.9  | 14%               |
| 1.3  | 24%               |
| 1.5  | 12%               |

## Interpretation

* Correct outputs exist as **subdominant probability paths**
* Low temperature suppresses them
* Moderate temperature allows **escape from dominant attractors**
* Excessive temperature introduces noise and degrades performance

---

## Key Insight

> Correctness is not always aligned with probability.

---

# 6. Implications for CALYX

## 6.1 Traditional Agentic Workflow

```
LLM (high entropy) → raw code → execution (unreliable)
```

Problems:

* Unbounded output space
* No guarantees
* High failure rate

---

## 6.2 CALYX Approach

```
LLM (low entropy) → finite symbol selection → VM execution
```

Advantages:

* Bounded action space
* Deterministic execution
* Verifiable outcomes

---

## 6.3 Core Principle

> Constrain the LLM to **routing decisions**, not program synthesis.

---

# 7. Role of IR and Virtual Machines

Intermediate representations (e.g., SIL-like IR) provide:

* Reduced grammar complexity
* Fewer valid continuations
* Lower entropy per token

### Effect:

```
Search Space ↓ → Entropy ↓ → Reliability ↑
```

This explains why:

* Raw source code → unstable
* IR → stable and predictable

---

# 8. Engineering Guidelines

## 8.1 Temperature as a Design Knob

```python
temperature_bands = {
    "route": 0.0,
    "classify": 0.1,
    "compare": 0.5,
    "transform": 0.7,
    "synthesize": 0.9,
    "compress": 1.1,
    "search": 1.3
}
```

⚠️ These are **starting points**, not fixed rules.

---

## 8.2 Validation Protocol

For each task:

```
1. Run 50–100 trials
2. Measure:
   - Success rate
   - Entropy
   - Exact match rate
3. Adjust temperature
4. Document results
```

---

# 9. Critical Caveats

## 9.1 What This Is NOT

* ❌ Not a formal mapping to Chomsky hierarchy
* ❌ Not a change in computational class
* ❌ Not universally consistent across models

---

## 9.2 What This IS

* ✅ An empirical framework
* ✅ A tuning methodology
* ✅ A system design principle

---

# 10. Final Synthesis

> A transformer is a fixed probabilistic system whose behavior varies with sampling constraints. Temperature does not increase its intelligence or computational power—it changes how much of its learned distribution is exposed.

---

## The Practical Outcome

* Low entropy → **reliable control**
* High entropy → **creative exploration**
* Structured systems (like CALYX) → **convert probabilistic models into deterministic pipelines**

---

# 11. Closing Insight

> The shift is not “LLMs generating programs”
> It is “LLMs navigating precompiled state spaces.”

This distinction is what enables:

* Safety
* Verifiability
* Model-agnostic performance


