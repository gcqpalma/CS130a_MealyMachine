# Mealy Machine Simulator

A Python program that simulates a Mealy machine over the input symbols `w`, `*` and `/`. It checks whether a string is exactly one block of text that opens with `/*` and closes with `*/`, and it prints a trace of every step.

## Overview

The machine reads the input one character at a time. For each character it moves to a new state and emits an output bit. The bit is `1` only on the step that completes the closing `*/`, and `0` on every other step.

## Input symbols

| Symbol | Stands for |
|---|---|
| `w` | any character other than `*` or `/` |
| `*` | asterisk |
| `/` | forward slash |

## Machine details

| Part | Value |
|---|---|
| States | `q0`, `q1`, `q2`, `q3`, `qaccept`, `qtrap` |
| Start state | `q0` |
| Accepting state | `qaccept` |
| Input alphabet | `{w, *, /}` |
| Output alphabet | `{0, 1}` |

Output rule: emit `1` when the current state is `q3` and the symbol is `/`. Emit `0` otherwise.

A string is accepted when the machine finishes in `qaccept`.

### State roles

- `q0`: waiting for the first `/`
- `q1`: the opening `/` was seen, waiting for `*`
- `q2`: inside the block
- `q3`: inside the block and the previous symbol was `*`
- `qaccept`: the block was just closed
- `qtrap`: failure state, no way back

## Transition table

Entries are written as `next state / output`.

| Current state | `w` | `*` | `/` |
|---|---|---|---|
| `q0` | `qtrap / 0` | `qtrap / 0` | `q1 / 0` |
| `q1` | `qtrap / 0` | `q2 / 0` | `qtrap / 0` |
| `q2` | `q2 / 0` | `q3 / 0` | `q2 / 0` |
| `q3` | `q2 / 0` | `q3 / 0` | `qaccept / 1` |
| `qaccept` | `qtrap / 0` | `qtrap / 0` | `qtrap / 0` |
| `qtrap` | `qtrap / 0` | `qtrap / 0` | `qtrap / 0` |

## Usage

Make sure Python 3 is installed, then run the script from the project folder:

```bash
python c_comment_mealy.py
```

Type a string at the prompt. The program shows each step, the final state, the output bits, and whether the string was accepted. Type `exit` to quit.

## Examples

| Input | Output bits | Result |
|---|---|---|
| `/*w*/` | `00001` | Accepted |
| `/**/` | `0001` | Accepted |
| `/***/` | `00001` | Accepted |
| `/*w/w*/` | `0000001` | Accepted |
| `/**` | `000` | Rejected |
| `/*/` | `000` | Rejected |
| `www/**/ww` | `000000000` | Rejected |
| `/**/w/*ww*/` | `00010000000` | Rejected |

## Remarks

- Only one block is allowed. Anything after the first closing `*/` sends the machine to `qtrap`.
- Blocks do not nest. The first `*/` after the opening `/*` always closes it.