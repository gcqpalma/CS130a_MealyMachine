# Mealy Machine: C-Style Comments

A Mealy machine that reads a string one character at a time and recognizes a single C-style block comment (`/* ... */`). It outputs a `1` at the moment the closing `/` is read, and `0` for every other character.

## Definition

- States: `q0`, `q1`, `q2`, `q3`, `qaccept`, `qtrap`
- Start state: `q0`
- Input alphabet: `{a, *, /}`, where `a` stands for any character other than `*` or `/`
- Output alphabet: `{0, 1}`
- Accepting state: `qaccept`
- Output is `1` only when the machine is in `q3` and reads `/`. Every other step outputs `0`.
- A string is accepted if the machine ends in `qaccept`.

## Transition / output table

Each cell is `next state / output`.

| State | `a` | `*` | `/` |
|---|---|---|---|
| `q0` (start) | `qtrap / 0` | `qtrap / 0` | `q1 / 0` |
| `q1` (saw `/`) | `qtrap / 0` | `q2 / 0` | `qtrap / 0` |
| `q2` (inside comment) | `q2 / 0` | `q3 / 0` | `q2 / 0` |
| `q3` (saw `*` inside) | `q2 / 0` | `q3 / 0` | `qaccept / 1` |
| `qaccept` (comment closed) | `qtrap / 0` | `qtrap / 0` | `qtrap / 0` |
| `qtrap` (dead) | `qtrap / 0` | `qtrap / 0` | `qtrap / 0` |

## Run

Requires Python 3.9 or newer (it uses `tuple[int, str]` type hints).

```bash
python c_comment_mealy.py
```

Type a string at the prompt to see a step-by-step trace. Type `exit` to quit.

## Examples

| Input | Output | Result |
|---|---|---|
| `/*a*/` | `00001` | ACCEPTED |
| `/**/` | `0001` | ACCEPTED |
| `/***/` | `00001` | ACCEPTED |
| `/*a/a*/` | `0000001` | ACCEPTED |
| `/**` | `000` | REJECTED |
| `/*/` | `000` | REJECTED |
| `aaa/**/aa` | `000000000` | REJECTED |
| `/**/a/*aa*/` | `00010000000` | REJECTED |

Only one complete block comment is recognized. Once the closing `*/` is read, any further character sends the machine to `qtrap`.