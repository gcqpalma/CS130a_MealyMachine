from typing import Tuple


class CommentDetector:
    """Mealy machine that recognizes a single C-style block comment (/* ... */)."""

    START = 'q0'
    SLASH = 'q1'
    BODY = 'q2'
    STAR = 'q3'
    ACCEPT = 'qaccept'
    TRAP = 'qtrap'

    def __init__(self):
        self.state = self.START

        # (state, symbol) -> next state, built from per-symbol rows
        self.delta = {}
        table = {
            'q0':      ('qtrap',   'qtrap', 'q1'),
            'q1':      ('qtrap',   'q2',    'qtrap'),
            'q2':      ('q2',      'q3',    'q2'),
            'q3':      ('q2',      'q3',    'qaccept'),
            'qaccept': ('qtrap',   'qtrap', 'qtrap'),
            'qtrap':   ('qtrap',   'qtrap', 'qtrap'),
        }
        for st, (on_a, on_star, on_slash) in table.items():
            self.delta[(st, 'a')] = on_a
            self.delta[(st, '*')] = on_star
            self.delta[(st, '/')] = on_slash

    @staticmethod
    def classify(char: str) -> str:
        """Anything other than '*' or '/' is treated as the generic symbol 'a'."""
        return char if char in ('*', '/') else 'a'

    def step(self, char: str) -> Tuple[int, str]:
        """Processes one character. Returns (output_bit, new_state)."""
        sym = self.classify(char)
        out = int(self.state == self.STAR and sym == '/')
        self.state = self.delta[(self.state, sym)]
        return out, self.state

    def run(self, text: str):
        """Runs the machine over the text and prints a step-by-step trace."""
        self.state = self.START
        bits = []

        print("\n--- Execution Trace ---")
        print(f"{'Step':<6} | {'Input':<8} | {'Mapped Symbol':<15} | {'Next State':<12} | {'Output'}")
        print('-' * 55)

        for n, ch in enumerate(text, 1):
            mapped = self.classify(ch)
            out, nxt = self.step(ch)
            bits.append(str(out))
            print(f"{n:<6} | {ch!r:<8} | {mapped:<15} | {nxt:<12} | {out}")

        print('-' * 55)
        print(f"Final State:     {self.state}")
        print(f"Output Sequence: {''.join(bits)}")
        print(f"Accepted:        {'YES' if self.state == self.ACCEPT else 'NO'}\n")


def show_menu():
    line = '=' * 60
    print(line)
    print("C-Style Comment Mealy Machine Simulator")
    print(line)
    print("Sample inputs you can test:")
    print("  Valid (Accepted):")
    for s in ("/*a*/", "/**/", "/***/", "/*aaa*aaa*/", "/*a/a*/", "/*hello world*/"):
        print(f"    - {s}")
    print("  Invalid (Rejected):")
    for s in ("/**", "/**/a/*aa*/", "aaa/**/aa", "/*/", "/**a/", "//aaaa"):
        print(f"    - {s}")
    print(line)
    print("Type 'exit' or press Ctrl+C to quit.\n")


def main():
    machine = CommentDetector()
    show_menu()

    while True:
        try:
            text = input("Enter string to test: ")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break
        if text.lower() == 'exit':
            break
        machine.run(text)


if __name__ == "__main__":
    main()