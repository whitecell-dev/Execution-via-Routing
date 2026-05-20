## Survival Lab Report: EvR Compiler v8.1

### Failure Catalog

---

#### OBSERVED: Multiplication compiles to `add`

**Evidence:** `factorial.ir` line 28
```
t0 = add r3 r2
```
Expected: `mul`  
Actual: `add` operation for multiplication

**Reproducible:** Yes — compile any function containing `*` operator.

**Minimal Reproduction:**
```python
def mul(a, b):
    return a * b
```
Compiled IR:
```
t0 = add p0 p1
```

**Status:** Active

---

#### OBSERVED: Modulo operation emits `const ?`

**Evidence:** `gcd.ir` line 16
```
t0 = const ? _
```
Expected: `mod` opcode with two operands  
Actual: Placeholder constant

**Reproducible:** Yes — compile any function containing `%` operator.

**Minimal Reproduction:**
```python
def mod(a, b):
    return a % b
```
Compiled IR:
```
t0 = const ? _
```

**Status:** Active

---

#### OBSERVED: Tuple unpacking produces `const ?`

**Evidence:** `fibonacci.ir` line 24
```
t0 = const ? _
```
Expected: Assignment with two destinations  
Actual: Placeholder constant

**Reproducible:** Yes — compile `a, b = b, a + b`

**Minimal Reproduction:**
```python
def swap(a, b):
    a, b = b, a
    return a
```
Compiled IR contains `const ?`

**Status:** Active

---

#### OBSERVED: Not equal operator compiles to `lt`

**Evidence:** `is_palindrome.ir` line 21
```
t2 = lt t0 t1
```
Expected: `ne` opcode  
Actual: `lt` for inequality comparison

**Reproducible:** Yes — compile any function containing `!=`.

**Minimal Reproduction:**
```python
def ne(a, b):
    return a != b
```
Compiled IR:
```
t0 = lt p0 p1
```

**Status:** Active

---

#### OBSERVED: Power exponentiation compiles to `add`

**Evidence:** `power.ir` line 28
```
t0 = add r2 p0
```
Expected: `mul` or `pow`  
Actual: `add` operation

**Reproducible:** Yes — compile `base ** exp`

**Status:** Active

---

#### OBSERVED: Placeholder `const ?` appears in multiple IR files

**Evidence:** `fibonacci.ir`, `gcd.ir`, `merge_sorted.ir`, `transpose.ir` all contain `const ?`

**Reproducible:** Yes — functions with:
- Tuple unpacking
- Modulo
- Complex indexing
- Nested data structures

**Status:** Active — incomplete lowering

---

#### OBSERVED: Fibonacci loop body is incomplete

**Evidence:** `fibonacci.ir` lines 22-28
```
block b3_while_body
  live-in: r3
  t0 = const ? _
  t1 = const 1 _
  t2 = add r3 t1
  r4 = mov t2 _
  exit jump b4_while_backedge _
```
Expected: `a, b = b, a + b` translation  
Actual: Only loop counter increments

**Status:** Active — tuple unpacking failure cascades

---

### Summary Table

| Failure | Status | Minimal Test | Severity |
|---------|--------|--------------|----------|
| `*` → `add` | Active | `def mul(a,b): return a*b` | High |
| `%` → `const ?` | Active | `def mod(a,b): return a%b` | High |
| Tuple unpack → `const ?` | Active | `a, b = b, a` | High |
| `!=` → `lt` | Active | `return a != b` | Medium |
| `**` → `add` | Active | `return base ** exp` | Medium |
| `const ?` placeholders | Active | Multiple sources | Medium |

---

### What Works (Documented)

**OBSERVED:** The following compile without `const ?` or missing opcodes:
- `bubble_sort.py` — full SSA with phi nodes, slice operations
- `count_occurrences.py` — conditional loops
- `merge_sorted.py` — multiple loops, list concatenation
- `reverse_array.py` — functional list building
- `factorial.py` — simple loop (except multiplication bug)

**OBSERVED:** All compiled IR have:
- Explicit block structure
- Block-prefixed phi sources
- Dedicated backedge blocks
- No implicit fallthrough

---

### Next Steps

To extend coverage:

| Priority | Test | Purpose |
|----------|------|---------|
| 1 | `def mul(a,b): return a*b` | Validate multiplication fix |
| 2 | `def mod(a,b): return a%b` | Validate modulo implementation |
| 3 | `def swap(a,b): a,b=b,a; return a` | Validate tuple unpacking |
| 4 | `def ne(a,b): return a!=b` | Validate inequality |

---

**UNKNOWN:** Behavior of recursion, nested functions, classes, exception handling — not tested.

**NEXT STEP:** Run minimal test cases for each failure to confirm reproduction before fixing.
