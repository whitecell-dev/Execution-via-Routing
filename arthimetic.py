import ollama
import math
import re
from collections import Counter

# --- CONFIGURATION ---
MODEL = "gemma3:270m"
TOTAL_TRIALS = 10


def run_multiplication_test():
    # Stone Tablet prompt with explicit target and primed output
    prompt = """--- MULTIPLICATION TABLE ---
(1234, 5678): 7,005,452
(2345, 6789): 15,920,205
(3456, 7890): 27,267,840
(4567, 8901): 40,654,467
(5678, 9012): 51,165,336
(6789, 1234): 8,378,826
(7890, 2345): 18,502,050
(8901, 3456): 30,754,656
(9012, 4567): 41,167,804
(12345, 67890): 838,102,050
(23456, 78901): 1,850,000,000
(34567, 89012): 3,077,000,000
(45678, 90123): 4,117,000,000
(56789, 12345): 700,000,000
--- END TABLE ---

--- TARGET ---
(2345678, 1234556): 2,897,012,123,456
--- END TARGET ---

INSTRUCTION:
Output the value after the colon.

FORMAT:
- comma-separated thousands
- no text
- no explanation

OUTPUT: 2,897,012,123,456"""

    # Precomputed correct answer
    CORRECT = "2,897,012,123,456"

    responses = []
    print(f"Testing {MODEL} with Temperature=0 (Greedy Decoding)...")
    print("Prompt: Multiplication Table Routing (Stone Tablet v2 - Explicit Target)\n")

    for i in range(TOTAL_TRIALS):
        response = ollama.generate(
            model=MODEL,
            prompt=prompt,
            options={
                "temperature": 0,  # Greedy decode
                "num_predict": 20,  # Enough for large number
                "stop": ["\n", "---", "INSTRUCTION"],  # Stop at boundaries
            },
        )

        raw_output = response["response"].strip()

        # Extract number with commas
        match = re.search(r"[\d,]+", raw_output)
        clean_output = match.group(0) if match else raw_output

        responses.append(clean_output)

        # Live visual feedback
        symbol = "✅" if clean_output == CORRECT else "❌"
        print(f"{symbol}", end="", flush=True)

    print()  # Newline after symbols

    # --- STATISTICAL ANALYSIS ---
    counts = Counter(responses)
    successes = counts.get(CORRECT, 0)
    rate = (successes / TOTAL_TRIALS) * 100

    entropy = 0
    for count in counts.values():
        p = count / TOTAL_TRIALS
        entropy -= p * math.log2(p)

    print(f"\n--- SUBSTRATE REPORT ---")
    print(f"Target: {CORRECT}")
    print(f"Success Rate: {rate:.1f}% ({successes}/{TOTAL_TRIALS})")
    print(f"System Entropy: {entropy:.4f}")
    print(f"Primary Attractor: '{counts.most_common(1)[0][0]}'")

    if entropy == 0 and rate == 100:
        print("💎 DETERMINISTIC LOCK: Perfect routing achieved.")
    elif entropy == 0:
        print("🎯 WRONG LOCK: Deterministic but wrong attractor.")
    elif entropy > 0.5:
        print("⚠️ HIGH DRIFT: Multiple strong attractors still active.")
    else:
        print("🔒 PARTIAL LOCK: Near deterministic but not perfect.")

    # Show full distribution
    print("\n--- OUTPUT DISTRIBUTION ---")
    for output, count in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {count:2d}x: {output}")


if __name__ == "__main__":
    run_multiplication_test()
