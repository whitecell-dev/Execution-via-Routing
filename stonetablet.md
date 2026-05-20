```markdown
# EvR Routing Contract v2

## Core Thesis

EvR succeeds if and only if decoding reduces to **single-span selection of a unique, logit-dominant target token sequence already present in the prefix**.

---

## The Golden Rule (Mechanistic Version)

If the model must **transform state** rather than **select a span**, probability mass disperses and argmax becomes unstable.

EvR works when:

> The correct continuation already exists explicitly in the prefix as a unique, logit-dominant token span.

Routing, not reasoning. Extraction, not execution.

---

## Requirements

### 0. Logit Dominance

The target token sequence must have higher probability mass than all competing spans. Greedy decoding (temperature=0) must consistently select it.

**Measure:** Run N trials (N ≥ 20). Entropy = 0 indicates logit dominance.

---

### 1. Unique Anchor Binding

The answer must be explicitly bound to a unique lexical marker that appears exactly once in the prefix.

**Good:**
```
FINAL_NEXT: 0xd2
```

**Bad:**
```
[x39] prev:0xd1 -> next:0xd2
```
(Last RHS requires structural reasoning, not direct extraction.)

---

### 2. No State Transformation

The model must not:

- Compute
- Count
- Compare
- Accumulate
- Traverse chains
- Apply rules
- Infer next state

All computation must be externalized to the compiler.

---

### 3. Minimal Instruction

Instruction must not introduce new lexical attractors.

**Bad:**
> Please carefully read the trace above and determine…

**Good:**
```
OUTPUT:
```

---

### 4. Frozen Format

Output form must be constrained to a single valid tokenization.

**Bad:** Model can choose between `0xd2`, `"0xd2"`, `0xD2`, `0xd2.`

**Good:**
```
FORMAT:
- lowercase hex
- no quotes
- no punctuation
EXAMPLE: 0xab
```

---

### 5. Explicit Stop Boundary

Generation must be bounded to prevent drift.

Enforce:
- `max_tokens = 3`
- `stop = ["\n"]`

---

### 6. No Competing Attractors

Remove:
- Explanatory prose
- Comments near the answer
- Code blocks
- Repeated instructions
- Ambiguous labels

Every extra token is a potential attractor.

---

### 7. Greedy Decode

```
temperature = 0
```

No sampling. Argmax only.

---

### 8. Short Dependency Surface

The anchor must appear within the model's effective attention window (≈ last 500-1000 tokens for 270M).

Place `FINAL_NEXT:` immediately before the output instruction.

---

### 9. Externalized Computation

All arithmetic, logic, traversal, and state updates occur outside the model, at compile-time.

The model only selects from precomputed values.

---

### 10. Entropy Audit

**Test:** Run identical prompt N times (N ≥ 20) with temperature=0.

**Success:** All outputs identical. Entropy = 0.

**Failure:** Entropy > 0 indicates contract violation (competing attractors, non-unique anchor, format drift).

---

## The Hard Boundary

EvR breaks if the model must:

- Create new values
- Combine unseen elements
- Perform multi-step arithmetic
- Maintain hidden state
- Infer rules from examples

That is not routing. That is reasoning.

---

## Base Model vs Fine-Tuned Regime

This contract applies to **base 270M models** (no fine-tuning).

Fine-tuning can shift the boundary:
- Extraction → transformation
- Classification → rule following

For base models, the regime is strictly **extraction**.

---

## The Reframed Identity

EvR is not:
- Execution
- Reasoning
- Simulation
- Chain following

EvR is:

> Compiler-precomputed state + deterministic lexical routing via argmax.

---

## The Final Principle

> EvR works if and only if decoding reduces to single-span selection of a unique, logit-dominant token sequence already present in the prefix.

If it doesn't, drift is inevitable.
```
