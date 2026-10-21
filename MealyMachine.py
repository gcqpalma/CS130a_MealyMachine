from typing import Tuple


class BlockCommentMealy:
    """Mealy machine that recognizes one C-style block comment (/* ... */).

    Input alphabet: {w, *, /}
        w = any character that is not '*' or '/'
    Output alphabet: {0, 1}
        1 is emitted only when the closing '/' of '*/' is read.
    """

    START = "q0"
    OPEN_SLASH = "q1"
    INSIDE = "q2"
    INSIDE_STAR = "q3"
    DONE = "qaccept"
    DEAD = "qtrap"

    # state -> {symbol: next_state}
    DELTA = {
        "q0":      {"w": "qtrap",   "*": "qtrap", "/": "q1"},
        "q1":      {"w": "qtrap",   "*": "q2",    "/": "qtrap"},
        "q2":      {"w": "q2",      "*": "q3",    "/": "q2"},
        "q3":      {"w": "q2",      "*": "q3",    "/": "qaccept"},
        "qaccept": {"w": "qtrap",   "*": "qtrap", "/": "qtrap"},
        "qtrap":   {"w": "qtrap",   "*": "qtrap", "/": "qtrap"},
    }

    def __init__(self):
        self.state = self.START

    @staticmethod
    def to_symbol(ch: str) -> str:
        """Map a raw character onto the alphabet {w, *, /}."""
        return ch if ch in ("*", "/") else "w"

    def feed(self, ch: str) -> Tuple[int, str]:
        """Consume one character. Returns (output_bit, new_state)."""
        sym = self.to_symbol(ch)
        bit = 1 if (self.state == self.INSIDE_STAR and sym == "/") else 0
        self.state = self.DELTA[self.state][sym]
        return bit, self.state

    def run(self, text: str) -> None:
        """Feed a whole string through the machine and print a trace."""
        self.state = self.START
        bits = []

        print("\n--- Execution Trace ---")
        print(f"{'Step':<6} | {'Input':<8} | {'Symbol':<8} | {'Next State':<12} | {'Output'}")
        print("-" * 52)

        for i, ch in enumerate(text, start=1):
            sym = self.to_symbol(ch)
            bit, nxt = self.feed(ch)
            bits.append(str(bit))
            print(f"{i:<6} | {ch!r:<8} | {sym:<8} | {nxt:<12} | {bit}")

        print("-" * 52)
        print(f"Final State:     {self.state}")
        print(f"Output Sequence: {''.join(bits)}")
        print(f"Accepted:        {'YES' if self.state == self.DONE else 'NO'}\n")


def print_banner() -> None:
    bar = "=" * 60
    print(bar)
    print("C-Style Comment Mealy Machine Simulator")
    print(bar)
    print("Input alphabet: w (any other character), *, /")
    print("Sample inputs you can test:")
    print("  Valid (Accepted):")
    for s in ("/*w*/", "/**/", "/***/", "/*www*www*/", "/*w/w*/", "/*hello world*/"):
        print(f"    - {s}")
    print("  Invalid (Rejected):")
    for s in ("/**", "/**/w/*ww*/", "www/**/ww", "/*/", "/**w/", "//wwww"):
        print(f"    - {s}")
    print(bar)
    print("Type 'exit' or press Ctrl+C to quit.\n")


def main() -> None:
    machine = BlockCommentMealy()
    print_banner()

    while True:
        try:
            text = input("Enter string to test: ")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break
        if text.lower() == "exit":
            break
        machine.run(text)


if __name__ == "__main__":
    main()