Set param p0 = [1, -2, 3, -4, 5]
Starting execution at entry
Initial registers: {'p0': [1, -2, 3, -4, 5]}

Block: entry
  Exec: p0 = const param _
    Regs: {'p0': [1, -2, 3, -4, 5]}
    Parameter p0 = [1, -2, 3, -4, 5]
  Exec: t0 = const 0 _
    Regs: {'p0': [1, -2, 3, -4, 5]}
    Set t0 = 0
  Exec: r0 = mov t0 _
    Regs: {'p0': [1, -2, 3, -4, 5], 't0': 0}
    Set r0 = 0
  Exec: t1 = const 0 _
    Regs: {'p0': [1, -2, 3, -4, 5], 't0': 0, 'r0': 0}
    Set t1 = 0
  Exec: r1 = mov t1 _
    Regs: {'p0': [1, -2, 3, -4, 5], 't0': 0, 'r0': 0, 't1': 0}
    Set r1 = 0
  Exec: t2 = call len p0 _
    Regs: {'p0': [1, -2, 3, -4, 5], 't0': 0, 'r0': 0, 't1': 0, 'r1': 0}
    Set t2 = 5
  Exec: r2 = mov t2 _
    Regs: {'p0': [1, -2, 3, -4, 5], 't0': 0, 'r0': 0, 't1': 0, 'r1': 0, 't2': 5}
    Set r2 = 5
  Next block: b0_while_header

Block: b0_while_header
  Exec: t0 = lt r3 r2
    Regs: {'p0': [1, -2, 3, -4, 5], 't0': 0, 'r0': 0, 't1': 0, 'r1': 0, 't2': 5, 'r2': 5, 'r3': 0, 'r4': 0}
    Set t0 = True
  Next block: b1_while_body

Block: b1_while_body
  Exec: t0 = get p0 r3
    Regs: {'p0': [1, -2, 3, -4, 5], 't0': True, 'r0': 0, 't1': 0, 'r1': 0, 't2': 5, 'r2': 5, 'r3': 0, 'r4': 0}
    Set t0 = 1
  Exec: t1 = const 0 _
    Regs: {'p0': [1, -2, 3, -4, 5], 't0': 1, 'r0': 0, 't1': 0, 'r1': 0, 't2': 5, 'r2': 5, 'r3': 0, 'r4': 0}
    Set t1 = 0
  Exec: t2 = lt t0 t1
    Regs: {'p0': [1, -2, 3, -4, 5], 't0': 1, 'r0': 0, 't1': 0, 'r1': 0, 't2': 5, 'r2': 5, 'r3': 0, 'r4': 0}
    Set t2 = False
  Next block: b5_merge

Block: b5_merge
  Exec: t0 = const 1 _
    Regs: {'p0': [1, -2, 3, -4, 5], 't0': 1, 'r0': 0, 't1': 0, 'r1': 0, 't2': False, 'r2': 5, 'r3': 0, 'r4': 0}
    Set t0 = 1
  Exec: t1 = add r3 t0
    Regs: {'p0': [1, -2, 3, -4, 5], 't0': 1, 'r0': 0, 't1': 0, 'r1': 0, 't2': False, 'r2': 5, 'r3': 0, 'r4': 0}
    Set t1 = 1
  Exec: r6 = mov t1 _
    Regs: {'p0': [1, -2, 3, -4, 5], 't0': 1, 'r0': 0, 't1': 1, 'r1': 0, 't2': False, 'r2': 5, 'r3': 0, 'r4': 0}
    Set r6 = 1
  Next block: b2_while_backedge

Block: b2_while_backedge
  Next block: b0_while_header

Block: b0_while_header
ERROR: Undefined reference: r5
