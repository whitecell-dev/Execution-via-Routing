# GEMMA3:270M TRANSFORMER-EXECUTABLE IR v8.1
# All 6 invariants enforced
# Minimal 12-opcode ISA
# Globally unique blocks
# PHI nodes with block-prefixed sources
# Body register mapping for loop-carried variables
# Pure function validation
# No manual flush - _start_block handles transitions

function bubble_sort
block entry
  live-in: param
  p0 = const param _
  t0 = call len p0 _
  r0 = mov t0 _
  r1 = mov p0 _
  t1 = const 0 _
  r2 = mov t1 _
  exit jump b0_while_header _
end
block b0_while_header
  live-in: r0
  r3 = phi entry:_ b2_while_backedge:r10
  r4 = phi entry:_ b2_while_backedge:r11
  r5 = phi entry:_ b2_while_backedge:r12
  r6 = phi entry:r2 b2_while_backedge:r20
  r7 = phi entry:r1 b2_while_backedge:r13
  r8 = phi entry:_ b2_while_backedge:r14
  t0 = lt r6 r0
  exit br t0 b1_while_body b3_while_exit
end
block b1_while_body
  live-in: none
  t0 = const 0 _
  r9 = mov t0 _
  exit jump b4_while_header _
end
block b4_while_header
  live-in: r0, r6
  r10 = phi b1_while_body:r9 b6_while_backedge:r19
  r11 = phi b1_while_body:r4 b6_while_backedge:r17
  r12 = phi b1_while_body:r5 b6_while_backedge:r16
  r13 = phi b1_while_body:r7 b6_while_backedge:r18
  r14 = phi b1_while_body:r8 b6_while_backedge:r15
  t0 = sub r0 r6
  t1 = const 1 _
  t2 = sub t0 t1
  t3 = lt r10 t2
  exit br t3 b5_while_body b7_while_exit
end
block b5_while_body
  live-in: r10, r13
  t0 = get r13 r10
  t1 = const 1 _
  t2 = add r10 t1
  t3 = get r13 t2
  t4 = lt t0 t3
  exit br t4 b8_then b9_merge
end
block b8_then
  live-in: r10, r13
  m0 = call slice r13 0 r10 _
  r15 = mov m0 _
  m1 = alloc 2 _
  t0 = const 1 _
  t1 = add r10 t0
  t2 = get r13 t1
  m2 = set m1 0 t2
  t3 = get r13 r10
  m3 = set m2 1 t3
  r16 = mov m3 _
  t4 = const 2 _
  t5 = add r10 t4
  m4 = call slice r13 t5 len _
  r17 = mov m4 _
  t6 = add r15 r16
  t7 = add t6 r17
  r18 = mov t7 _
  exit jump b9_merge _
end
block b9_merge
  live-in: r10
  t0 = const 1 _
  t1 = add r10 t0
  r19 = mov t1 _
  exit jump b6_while_backedge _
end
block b6_while_backedge
  live-in: none
  exit jump b4_while_header _
end
block b7_while_exit
  live-in: r6
  t0 = const 1 _
  t1 = add r6 t0
  r20 = mov t1 _
  exit jump b2_while_backedge _
end
block b2_while_backedge
  live-in: none
  exit jump b0_while_header _
end
block b3_while_exit
  live-in: r7
  exit ret r7 _
end
# GEMMA3:270M TRANSFORMER-EXECUTABLE IR v8.1
# All 6 invariants enforced
# Minimal 12-opcode ISA
# Globally unique blocks
# PHI nodes with block-prefixed sources
# Body register mapping for loop-carried variables
# Pure function validation
# No manual flush - _start_block handles transitions

function count_occurrences
block entry
  live-in: param
  p0 = const param _
  p1 = const param _
  t0 = const 0 _
  r0 = mov t0 _
  t1 = const 0 _
  r1 = mov t1 _
  exit jump b0_while_header _
end
block b0_while_header
  live-in: p0
  r2 = phi entry:r1 b2_while_backedge:r5
  r3 = phi entry:r0 b2_while_backedge:r4
  t0 = call len p0 _
  t1 = lt r2 t0
  exit br t1 b1_while_body b3_while_exit
end
block b1_while_body
  live-in: p0, p1, r2
  t0 = get p0 r2
  t1 = eq t0 p1
  exit br t1 b4_then b5_merge
end
block b4_then
  live-in: r3
  t0 = const 1 _
  t1 = add r3 t0
  r4 = mov t1 _
  exit jump b5_merge _
end
block b5_merge
  live-in: r2
  t0 = const 1 _
  t1 = add r2 t0
  r5 = mov t1 _
  exit jump b2_while_backedge _
end
block b2_while_backedge
  live-in: none
  exit jump b0_while_header _
end
block b3_while_exit
  live-in: r3
  exit ret r3 _
end
# GEMMA3:270M TRANSFORMER-EXECUTABLE IR v8.1
# All 6 invariants enforced
# Minimal 12-opcode ISA
# Globally unique blocks
# PHI nodes with block-prefixed sources
# Body register mapping for loop-carried variables
# Pure function validation
# No manual flush - _start_block handles transitions

function factorial
block entry
  live-in: param
  p0 = const param _
  t0 = const 1 _
  t1 = lt p0 t0
  exit br t1 b0_then b1_merge
end
block b0_then
  live-in: none
  t0 = const 1 _
  exit jump b1_merge _
end
block b1_merge
  live-in: none
  t0 = const 1 _
  r0 = mov t0 _
  t1 = const 2 _
  r1 = mov t1 _
  exit jump b2_while_header _
end
block b2_while_header
  live-in: p0
  r2 = phi b1_merge:r1 b4_while_backedge:r5
  r3 = phi b1_merge:r0 b4_while_backedge:r4
  t0 = lt r2 p0
  exit br t0 b3_while_body b5_while_exit
end
block b3_while_body
  live-in: r2, r3
  t0 = add r3 r2
  r4 = mov t0 _
  t1 = const 1 _
  t2 = add r2 t1
  r5 = mov t2 _
  exit jump b4_while_backedge _
end
block b4_while_backedge
  live-in: none
  exit jump b2_while_header _
end
block b5_while_exit
  live-in: r3
  exit ret r3 _
end
# GEMMA3:270M TRANSFORMER-EXECUTABLE IR v8.1
# All 6 invariants enforced
# Minimal 12-opcode ISA
# Globally unique blocks
# PHI nodes with block-prefixed sources
# Body register mapping for loop-carried variables
# Pure function validation
# No manual flush - _start_block handles transitions

function fibonacci
block entry
  live-in: param
  p0 = const param _
  t0 = const 1 _
  t1 = lt p0 t0
  exit br t1 b0_then b1_merge
end
block b0_then
  live-in: p0
  exit jump b1_merge _
end
block b1_merge
  live-in: none
  t0 = const 0 _
  r0 = mov t0 _
  t1 = const 1 _
  r1 = mov t1 _
  t2 = const 2 _
  r2 = mov t2 _
  exit jump b2_while_header _
end
block b2_while_header
  live-in: p0
  r3 = phi b1_merge:r2 b4_while_backedge:r4
  t0 = lt r3 p0
  exit br t0 b3_while_body b5_while_exit
end
block b3_while_body
  live-in: r3
  t0 = const ? _
  t1 = const 1 _
  t2 = add r3 t1
  r4 = mov t2 _
  exit jump b4_while_backedge _
end
block b4_while_backedge
  live-in: none
  exit jump b2_while_header _
end
block b5_while_exit
  live-in: r1
  exit ret r1 _
end
# GEMMA3:270M TRANSFORMER-EXECUTABLE IR v8.1
# All 6 invariants enforced
# Minimal 12-opcode ISA
# Globally unique blocks
# PHI nodes with block-prefixed sources
# Body register mapping for loop-carried variables
# Pure function validation
# No manual flush - _start_block handles transitions

function gcd
block entry
  live-in: param
  p0 = const param _
  p1 = const param _
  exit jump b0_while_header _
end
block b0_while_header
  live-in: p1
  t0 = const 0 _
  t1 = lt p1 t0
  exit br t1 b1_while_body b3_while_exit
end
block b1_while_body
  live-in: none
  t0 = const ? _
  exit jump b2_while_backedge _
end
block b2_while_backedge
  live-in: none
  exit jump b0_while_header _
end
block b3_while_exit
  live-in: p0
  exit ret p0 _
end
# GEMMA3:270M TRANSFORMER-EXECUTABLE IR v8.1
# All 6 invariants enforced
# Minimal 12-opcode ISA
# Globally unique blocks
# PHI nodes with block-prefixed sources
# Body register mapping for loop-carried variables
# Pure function validation
# No manual flush - _start_block handles transitions

function merge_sorted
block entry
  live-in: param
  p0 = const param _
  p1 = const param _
  m0 = alloc 0 _
  r0 = mov m0 _
  t0 = const ? _
  exit jump b0_while_header _
end
block b0_while_header
  live-in: p0, p1
  r1 = phi entry:r0 b2_while_backedge:r6
  r2 = phi entry:_ b2_while_backedge:r8
  r3 = phi entry:_ b2_while_backedge:r9
  t0 = call len p0 _
  t1 = lt r3 t0
  t2 = call len p1 _
  t3 = lt r2 t2
  t4 = and t1 t3
  exit br t4 b1_while_body b3_while_exit
end
block b1_while_body
  live-in: p0, p1, r2, r3
  t0 = get p0 r3
  t1 = get p1 r2
  t2 = lt t0 t1
  exit br t2 b4_then b5_else
end
block b4_then
  live-in: p0, r1, r3
  m1 = alloc 1 _
  t0 = get p0 r3
  m2 = set m1 0 t0
  t1 = add r1 m2
  r4 = mov t1 _
  t2 = const 1 _
  t3 = add r3 t2
  r5 = mov t3 _
  exit jump b6_merge _
end
block b5_else
  live-in: p1, r1, r2
  m3 = alloc 1 _
  t0 = get p1 r2
  m4 = set m3 0 t0
  t1 = add r1 m4
  r6 = mov t1 _
  t2 = const 1 _
  t3 = add r2 t2
  r7 = mov t3 _
  exit jump b6_merge _
end
block b6_merge
  live-in: none
  r8 = phi b4_then:r2 b5_else:r7
  r9 = phi b4_then:r5 b5_else:r3
  exit jump b2_while_backedge _
end
block b2_while_backedge
  live-in: none
  exit jump b0_while_header _
end
block b3_while_exit
  live-in: none
  exit jump b7_while_header _
end
block b7_while_header
  live-in: p0
  r10 = phi b3_while_exit:r1 b9_while_backedge:r12
  r11 = phi b3_while_exit:r3 b9_while_backedge:r13
  t0 = call len p0 _
  t1 = lt r11 t0
  exit br t1 b8_while_body b10_while_exit
end
block b8_while_body
  live-in: p0, r10, r11
  m5 = alloc 1 _
  t0 = get p0 r11
  m6 = set m5 0 t0
  t1 = add r10 m6
  r12 = mov t1 _
  t2 = const 1 _
  t3 = add r11 t2
  r13 = mov t3 _
  exit jump b9_while_backedge _
end
block b9_while_backedge
  live-in: none
  exit jump b7_while_header _
end
block b10_while_exit
  live-in: none
  exit jump b11_while_header _
end
block b11_while_header
  live-in: p1
  r14 = phi b10_while_exit:r10 b13_while_backedge:r16
  r15 = phi b10_while_exit:r2 b13_while_backedge:r17
  t0 = call len p1 _
  t1 = lt r15 t0
  exit br t1 b12_while_body b14_while_exit
end
block b12_while_body
  live-in: p1, r14, r15
  m7 = alloc 1 _
  t0 = get p1 r15
  m8 = set m7 0 t0
  t1 = add r14 m8
  r16 = mov t1 _
  t2 = const 1 _
  t3 = add r15 t2
  r17 = mov t3 _
  exit jump b13_while_backedge _
end
block b13_while_backedge
  live-in: none
  exit jump b11_while_header _
end
block b14_while_exit
  live-in: r14
  exit ret r14 _
end
# GEMMA3:270M TRANSFORMER-EXECUTABLE IR v8.1
# All 6 invariants enforced
# Minimal 12-opcode ISA
# Globally unique blocks
# PHI nodes with block-prefixed sources
# Body register mapping for loop-carried variables
# Pure function validation
# No manual flush - _start_block handles transitions

function is_palindrome
block entry
  live-in: param
  p0 = const param _
  t0 = const 0 _
  r0 = mov t0 _
  t1 = call len p0 _
  t2 = const 1 _
  t3 = sub t1 t2
  r1 = mov t3 _
  exit jump b0_while_header _
end
block b0_while_header
  live-in: none
  r2 = phi entry:r0 b2_while_backedge:r4
  r3 = phi entry:r1 b2_while_backedge:r5
  t0 = lt r2 r3
  exit br t0 b1_while_body b3_while_exit
end
block b1_while_body
  live-in: p0, r2, r3
  t0 = get p0 r2
  t1 = get p0 r3
  t2 = lt t0 t1
  exit br t2 b4_then b5_merge
end
block b4_then
  live-in: none
  t0 = const 0 _
  exit jump b5_merge _
end
block b5_merge
  live-in: r2, r3
  t0 = const 1 _
  t1 = add r2 t0
  r4 = mov t1 _
  t2 = const 1 _
  t3 = sub r3 t2
  r5 = mov t3 _
  exit jump b2_while_backedge _
end
block b2_while_backedge
  live-in: none
  exit jump b0_while_header _
end
block b3_while_exit
  live-in: none
  t0 = const 1 _
  exit ret t0 _
end
# GEMMA3:270M TRANSFORMER-EXECUTABLE IR v8.1
# All 6 invariants enforced
# Minimal 12-opcode ISA
# Globally unique blocks
# PHI nodes with block-prefixed sources
# Body register mapping for loop-carried variables
# Pure function validation
# No manual flush - _start_block handles transitions

function power
block entry
  live-in: param
  p0 = const param _
  p1 = const param _
  t0 = const 0 _
  t1 = eq p1 t0
  exit br t1 b0_then b1_merge
end
block b0_then
  live-in: none
  t0 = const 1 _
  exit jump b1_merge _
end
block b1_merge
  live-in: none
  t0 = const 1 _
  r0 = mov t0 _
  t1 = const 0 _
  r1 = mov t1 _
  exit jump b2_while_header _
end
block b2_while_header
  live-in: p1
  r2 = phi b1_merge:r0 b4_while_backedge:r4
  r3 = phi b1_merge:r1 b4_while_backedge:r5
  t0 = lt r3 p1
  exit br t0 b3_while_body b5_while_exit
end
block b3_while_body
  live-in: p0, r2, r3
  t0 = add r2 p0
  r4 = mov t0 _
  t1 = const 1 _
  t2 = add r3 t1
  r5 = mov t2 _
  exit jump b4_while_backedge _
end
block b4_while_backedge
  live-in: none
  exit jump b2_while_header _
end
block b5_while_exit
  live-in: r2
  exit ret r2 _
end
# GEMMA3:270M TRANSFORMER-EXECUTABLE IR v8.1
# All 6 invariants enforced
# Minimal 12-opcode ISA
# Globally unique blocks
# PHI nodes with block-prefixed sources
# Body register mapping for loop-carried variables
# Pure function validation
# No manual flush - _start_block handles transitions

function reverse_array
block entry
  live-in: param
  p0 = const param _
  t0 = call len p0 _
  r0 = mov t0 _
  m0 = alloc 0 _
  r1 = mov m0 _
  t1 = const 1 _
  t2 = sub r0 t1
  r2 = mov t2 _
  exit jump b0_while_header _
end
block b0_while_header
  live-in: none
  r3 = phi entry:r1 b2_while_backedge:r5
  r4 = phi entry:r2 b2_while_backedge:r6
  t0 = const 0 _
  t1 = lt r4 t0
  exit br t1 b1_while_body b3_while_exit
end
block b1_while_body
  live-in: p0, r3, r4
  m1 = alloc 1 _
  t0 = get p0 r4
  m2 = set m1 0 t0
  t1 = add r3 m2
  r5 = mov t1 _
  t2 = const 1 _
  t3 = sub r4 t2
  r6 = mov t3 _
  exit jump b2_while_backedge _
end
block b2_while_backedge
  live-in: none
  exit jump b0_while_header _
end
block b3_while_exit
  live-in: r3
  exit ret r3 _
end
# GEMMA3:270M TRANSFORMER-EXECUTABLE IR v8.1
# All 6 invariants enforced
# Minimal 12-opcode ISA
# Globally unique blocks
# PHI nodes with block-prefixed sources
# Body register mapping for loop-carried variables
# Pure function validation
# No manual flush - _start_block handles transitions

function transpose
block entry
  live-in: param
  p0 = const param _
  t0 = call len p0 _
  r0 = mov t0 _
  t1 = const ? _
  r1 = mov t1 _
  m0 = alloc 0 _
  r2 = mov m0 _
  t2 = const 0 _
  r3 = mov t2 _
  exit jump b0_while_header _
end
block b0_while_header
  live-in: r1
  r4 = phi entry:_ b2_while_backedge:r10
  r5 = phi entry:r3 b2_while_backedge:r15
  r6 = phi entry:_ b2_while_backedge:r11
  r7 = phi entry:r2 b2_while_backedge:r14
  t0 = lt r5 r1
  exit br t0 b1_while_body b3_while_exit
end
block b1_while_body
  live-in: none
  m1 = alloc 0 _
  r8 = mov m1 _
  t0 = const 0 _
  r9 = mov t0 _
  exit jump b4_while_header _
end
block b4_while_header
  live-in: r0
  r10 = phi b1_while_body:r8 b6_while_backedge:r12
  r11 = phi b1_while_body:r9 b6_while_backedge:r13
  t0 = lt r11 r0
  exit br t0 b5_while_body b7_while_exit
end
block b5_while_body
  live-in: p0, r10, r11, r5
  m2 = alloc 1 _
  t0 = get p0 r11
  t1 = get t0 r5
  m3 = set m2 0 t1
  t2 = add r10 m3
  r12 = mov t2 _
  t3 = const 1 _
  t4 = add r11 t3
  r13 = mov t4 _
  exit jump b6_while_backedge _
end
block b6_while_backedge
  live-in: none
  exit jump b4_while_header _
end
block b7_while_exit
  live-in: r10, r5, r7
  m4 = alloc 1 _
  m5 = set m4 0 r10
  t0 = add r7 m5
  r14 = mov t0 _
  t1 = const 1 _
  t2 = add r5 t1
  r15 = mov t2 _
  exit jump b2_while_backedge _
end
block b2_while_backedge
  live-in: none
  exit jump b0_while_header _
end
block b3_while_exit
  live-in: r7
  exit ret r7 _
end
