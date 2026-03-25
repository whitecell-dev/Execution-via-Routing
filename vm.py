#!/usr/bin/env python3
"""
EvR Minimal VM v0.8 - Fixed call instruction handling
"""

from typing import Dict, List, Optional, Union, Any, Tuple
from dataclasses import dataclass


# ============================================================================
# VALUES
# ============================================================================


class _Uninitialized:
    def __repr__(self) -> str:
        return "<uninit>"

    def __bool__(self) -> bool:
        raise RuntimeError("Cannot evaluate uninitialized value in boolean context")


UNINIT = _Uninitialized()

Value = Union[int, bool, List[Any], _Uninitialized]


def is_uninit(v: Value) -> bool:
    return isinstance(v, _Uninitialized)


# ============================================================================
# IR STRUCTURES
# ============================================================================


@dataclass
class Instr:
    dest: str
    op: str
    src1: str
    src2: str


@dataclass
class Phi:
    dest: str
    sources: List[str]


@dataclass
class Block:
    name: str
    phis: List[Phi]
    instrs: List[Instr]
    exit_op: str
    exit_args: Tuple[str, ...]


@dataclass
class Function:
    name: str
    blocks: Dict[str, Block]
    entry: str


# ============================================================================
# PARSER
# ============================================================================


class IRParser:
    def __init__(self, ir_text: str) -> None:
        self.ir_text = ir_text

    def parse(self) -> Dict[str, Function]:
        functions: Dict[str, Function] = {}
        lines = self.ir_text.strip().split("\n")
        i = 0

        while i < len(lines):
            line = lines[i].strip()
            if not line or line.startswith("#"):
                i += 1
                continue

            if line.startswith("function "):
                func_name = line.split()[1]
                i += 1
                blocks: Dict[str, Block] = {}
                entry: Optional[str] = None

                while i < len(lines):
                    line = lines[i].strip()
                    if line.startswith("function "):
                        break

                    if line.startswith("block "):
                        block_name = line.split()[1]
                        if entry is None:
                            entry = block_name
                        block, i = self._parse_block(lines, i)
                        blocks[block_name] = block
                        continue

                    i += 1

                if entry is None:
                    raise RuntimeError(f"Function {func_name} has no blocks")
                functions[func_name] = Function(func_name, blocks, entry)
            else:
                i += 1

        return functions

    def _parse_block(self, lines: List[str], start: int) -> Tuple[Block, int]:
        i = start
        block_name = lines[i].strip().split()[1]
        i += 1

        # Skip live-in line
        if i < len(lines) and "live-in:" in lines[i]:
            i += 1

        phis: List[Phi] = []
        instrs: List[Instr] = []
        exit_op = "ret"
        exit_args: Tuple[str, ...] = ("_",)

        while i < len(lines):
            line = lines[i].strip()

            if line == "end":
                i += 1
                break

            if line.startswith("exit "):
                parts = line.split()
                exit_op = parts[1] if len(parts) > 1 else "ret"
                exit_args = tuple(parts[2:]) if len(parts) > 2 else ("_",)
                i += 1
                continue

            if "=" in line:
                parts = line.split("=", 1)
                dest = parts[0].strip()
                rhs = parts[1].strip()

                if rhs.startswith("phi "):
                    sources = rhs.split()[1:]
                    phis.append(Phi(dest, sources))
                elif rhs.startswith("call "):
                    # Handle: dest = call func arg1 arg2 ...
                    # Extract everything after 'call '
                    call_parts = rhs[5:].split()  # Skip 'call '
                    if call_parts:
                        func = call_parts[0]
                        args = call_parts[1:] if len(call_parts) > 1 else []
                        # Store as: dest = call func args...
                        src2 = " ".join(args) if args else "_"
                        instrs.append(Instr(dest, "call", func, src2))
                    else:
                        raise RuntimeError(f"Invalid call instruction: {line}")
                else:
                    # Parse regular instruction: dest = op src1 src2
                    rhs_parts = rhs.split(None, 2)
                    if len(rhs_parts) >= 1:
                        op = rhs_parts[0]
                        src1 = rhs_parts[1] if len(rhs_parts) > 1 else "_"
                        src2 = rhs_parts[2] if len(rhs_parts) > 2 else "_"
                        instrs.append(Instr(dest, op, src1, src2))
                    else:
                        raise RuntimeError(f"Invalid instruction: {line}")

            i += 1

        return Block(block_name, phis, instrs, exit_op, exit_args), i


# ============================================================================
# VM
# ============================================================================


class EvRVM:
    def __init__(
        self, func: Function, max_steps: int = 10000, debug: bool = False
    ) -> None:
        self.blocks = func.blocks
        self.entry = func.entry
        self.max_steps = max_steps
        self.debug = debug
        self.regs: Dict[str, Value] = {}
        self.pc: str = self.entry
        self.prev_block: Optional[str] = None
        self.step_count = 0
        self.halted = False
        self.return_value: Value = UNINIT

    def _get_value(self, ref: str) -> Value:
        """Resolve a reference to a value."""
        if ref == "_" or ref == "":
            return UNINIT

        # Check if it's a constant
        if ref == "true":
            return True
        if ref == "false":
            return False
        if ref.isdigit():
            return int(ref)
        if ref.startswith('"') and ref.endswith('"'):
            return ref[1:-1]

        # Try negative numbers
        try:
            if ref.startswith("-") and ref[1:].isdigit():
                return int(ref)
        except:
            pass

        # Strip block prefix if present
        if ":" in ref:
            ref = ref.split(":", 1)[1]

        # Look up in registers
        if ref in self.regs:
            return self.regs[ref]

        raise RuntimeError(f"Undefined reference: {ref}")

    def _resolve_phi(self, phi: Phi) -> Value:
        """Resolve phi using previous block."""
        for src in phi.sources:
            if ":" in src:
                block_name, reg = src.split(":", 1)
                if block_name == self.prev_block:
                    return self._get_value(reg)
        return UNINIT

    def _exec_instr(self, instr: Instr) -> None:
        """Execute a single instruction."""
        op = instr.op
        dest = instr.dest

        if self.debug:
            print(f"  Exec: {dest} = {op} {instr.src1} {instr.src2}")
            print(f"    Regs: {self.regs}")

        # const param - validate parameter exists
        if op == "const" and instr.src1 == "param":
            if dest not in self.regs:
                raise RuntimeError(f"Parameter {dest} not provided to function")
            if self.debug:
                print(f"    Parameter {dest} = {self.regs[dest]}")
            return

        # Handle call separately - function name is not a register
        if op == "call":
            # instr.src1 is function name, instr.src2 is space-separated args
            call_str = f"{instr.src1} {instr.src2}".strip()
            val = self._exec_call(call_str)
            if dest != "_":
                self.regs[dest] = val
                if self.debug:
                    print(f"    Set {dest} = {val}")
            return

        # For all other instructions, get source values
        src1 = self._get_value(instr.src1)
        src2 = self._get_value(instr.src2)

        # Execute based on opcode
        if op == "const":
            val = self._get_value(instr.src1)
        elif op == "mov":
            if is_uninit(src1):
                raise RuntimeError(f"mov from uninitialized register: {instr.src1}")
            val = src1
        elif op == "add":
            if not isinstance(src1, int) or not isinstance(src2, int):
                raise TypeError(f"add requires ints, got {type(src1)} and {type(src2)}")
            val = src1 + src2
        elif op == "sub":
            if not isinstance(src1, int) or not isinstance(src2, int):
                raise TypeError(f"sub requires ints, got {type(src1)} and {type(src2)}")
            val = src1 - src2
        elif op == "mul":
            if not isinstance(src1, int) or not isinstance(src2, int):
                raise TypeError(f"mul requires ints, got {type(src1)} and {type(src2)}")
            val = src1 * src2
        elif op == "lt":
            if not isinstance(src1, int) or not isinstance(src2, int):
                raise TypeError(f"lt requires ints, got {type(src1)} and {type(src2)}")
            val = src1 < src2
        elif op == "eq":
            val = src1 == src2
        elif op == "ne":
            val = src1 != src2
        elif op == "and":
            val = src1 and src2
        elif op == "alloc":
            if not isinstance(src1, int):
                raise TypeError(f"alloc requires int size, got {type(src1)}")
            val = [UNINIT] * src1
        elif op == "get":
            if not isinstance(src1, list):
                raise TypeError(f"get requires list, got {type(src1)}")
            if not isinstance(src2, int):
                raise TypeError(f"get requires int index, got {type(src2)}")
            if src2 < 0 or src2 >= len(src1):
                raise IndexError(f"Index {src2} out of range")
            val = src1[src2]
        elif op == "set":
            if not isinstance(src1, list):
                raise TypeError(f"set requires list, got {type(src1)}")
            # src2 format: "idx val" - split and evaluate
            parts = instr.src2.split()
            if len(parts) < 2:
                raise RuntimeError(f"set requires idx and val, got {instr.src2}")
            idx = self._get_value(parts[0])
            new_val = self._get_value(parts[1])
            if not isinstance(idx, int):
                raise TypeError(f"set index must be int, got {type(idx)}")
            if idx < 0 or idx >= len(src1):
                raise IndexError(f"Index {idx} out of range")
            new_list = src1.copy()
            new_list[idx] = new_val
            val = new_list
        else:
            raise RuntimeError(f"Unknown opcode: {op}")

        if dest != "_":
            self.regs[dest] = val
            if self.debug:
                print(f"    Set {dest} = {val}")

    def _exec_call(self, call_str: str) -> Value:
        """Execute a builtin call."""
        parts = call_str.split()
        if not parts:
            return UNINIT

        func = parts[0]
        args: List[Value] = []
        for arg in parts[1:]:
            if arg != "_":
                args.append(self._get_value(arg))

        if func == "len":
            if len(args) != 1:
                raise RuntimeError(f"len() takes 1 argument, got {len(args)}")
            if not isinstance(args[0], list):
                raise TypeError(f"len() expects list, got {type(args[0])}")
            return len(args[0])
        elif func == "slice":
            if len(args) < 3:
                raise RuntimeError(f"slice() takes 3 arguments, got {len(args)}")
            arr = args[0]
            if not isinstance(arr, list):
                raise TypeError(f"slice() expects list, got {type(arr)}")
            start = args[1] if isinstance(args[1], int) else 0
            end = args[2] if isinstance(args[2], int) else len(arr)
            start = max(0, min(start, len(arr)))
            end = max(start, min(end, len(arr)))
            return arr[start:end]
        else:
            raise RuntimeError(f"Unknown builtin: {func}")

    def _exec_exit(self, block: Block) -> Optional[str]:
        """Execute block exit, return next block or None."""
        if block.exit_op == "jump":
            if len(block.exit_args) < 1:
                raise RuntimeError("jump requires target block")
            return block.exit_args[0]
        elif block.exit_op == "br":
            if len(block.exit_args) < 3:
                raise RuntimeError("br requires cond, then, else")
            cond = self._get_value(block.exit_args[0])
            then_block = block.exit_args[1]
            else_block = block.exit_args[2]
            return then_block if cond else else_block
        elif block.exit_op == "ret":
            if len(block.exit_args) > 0 and block.exit_args[0] != "_":
                val = self._get_value(block.exit_args[0])
                if is_uninit(val):
                    raise RuntimeError("return from uninitialized register")
                self.return_value = val
            self.halted = True
            return None
        else:
            raise RuntimeError(f"Unknown exit op: {block.exit_op}")

    def step(self) -> None:
        """Execute one block."""
        if self.halted:
            return

        if self.pc not in self.blocks:
            raise RuntimeError(f"Block not found: {self.pc}")

        block = self.blocks[self.pc]

        if self.debug:
            print(f"\nBlock: {self.pc}")

        # Execute phis
        for phi in block.phis:
            self.regs[phi.dest] = self._resolve_phi(phi)

        # Execute instructions
        for instr in block.instrs:
            self._exec_instr(instr)

        # Execute exit
        next_block = self._exec_exit(block)

        self.prev_block = self.pc
        if next_block is not None:
            self.pc = next_block
            if self.debug:
                print(f"  Next block: {next_block}")

    def run(self, args: Optional[List[Value]] = None) -> Value:
        """Run the VM with given arguments."""
        self.regs = {}
        self.pc = self.entry
        self.prev_block = None
        self.step_count = 0
        self.halted = False
        self.return_value = UNINIT

        # Set up parameters - map args to parameter registers BEFORE execution
        if args is not None:
            for i, arg in enumerate(args):
                # Convert Python list to proper Value
                if isinstance(arg, list):

                    def convert(x: Any) -> Value:
                        if isinstance(x, list):
                            return [convert(v) for v in x]
                        return x

                    self.regs[f"p{i}"] = convert(arg)
                else:
                    self.regs[f"p{i}"] = arg
                if self.debug:
                    print(f"Set param p{i} = {self.regs[f'p{i}']}")
        else:
            if self.debug:
                print("No arguments provided")

        if self.debug:
            print(f"Starting execution at {self.entry}")
            print(f"Initial registers: {self.regs}")

        # Execute
        while not self.halted and self.step_count < self.max_steps:
            self.step()
            self.step_count += 1

        if self.step_count >= self.max_steps:
            raise RuntimeError(f"Exceeded max steps ({self.max_steps})")

        if self.debug:
            print(f"\nFinal registers: {self.regs}")
            print(f"Return value: {self.return_value}")

        return self.return_value


# ============================================================================
# MAIN
# ============================================================================


def parse_and_run(
    ir_text: str,
    func_name: str,
    args: Optional[List[Value]] = None,
    debug: bool = False,
) -> Value:
    """Parse IR and run the specified function."""
    parser = IRParser(ir_text)
    functions = parser.parse()

    if not functions:
        raise RuntimeError("No functions found in IR")

    if func_name not in functions:
        raise RuntimeError(f"Function {func_name} not found")

    vm = EvRVM(functions[func_name], debug=debug)
    return vm.run(args)


def main() -> None:
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: vm.py <ir_file> [--function name] [--args json] [--debug]")
        sys.exit(1)

    with open(sys.argv[1], "r") as f:
        ir_text = f.read()

    func_name: str = ""
    args: Optional[List[Value]] = None
    debug = False
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--function":
            if i + 1 < len(sys.argv):
                func_name = sys.argv[i + 1]
                i += 2
            else:
                print("ERROR: --function requires an argument")
                sys.exit(1)
        elif sys.argv[i] == "--args":
            if i + 1 < len(sys.argv):
                parsed = json.loads(sys.argv[i + 1])
                if not isinstance(parsed, list):
                    parsed = [parsed]

                def convert(x: Any) -> Value:
                    if isinstance(x, list):
                        return [convert(v) for v in x]
                    return x

                args = [convert(v) for v in parsed]
                i += 2
            else:
                print("ERROR: --args requires an argument")
                sys.exit(1)
        elif sys.argv[i] == "--debug":
            debug = True
            i += 1
        else:
            i += 1

    # If no function specified, get the first one
    if not func_name:
        parser = IRParser(ir_text)
        functions = parser.parse()
        if functions:
            func_name = list(functions.keys())[0]
        else:
            print("ERROR: No functions found in IR file")
            sys.exit(1)

    try:
        result = parse_and_run(ir_text, func_name, args, debug)
        print(f"RESULT: {result}")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()