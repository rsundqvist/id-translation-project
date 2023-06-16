from cookiecutter.utils import simple_filter
import re


@simple_filter
def to_namespace(s: str) -> str:
    s = s.lower()
    s = re.sub(r"\s+", "_", s)
    s = "".join(filter(str.isidentifier, s))
    s = digit_to_word(s[0]) + s[1:]

    return s


@simple_filter
def to_slug_prefix(s: str) -> str:
    return "".join(s[0] for s in s.split("_")) if "_" in s else s


def digit_to_word(s: str) -> str:
    m = {
        0: "zero", 1: "one", 2: "two", 3: "three", 4: "four",
        5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
    }

    def f(c: str) -> str:
        try:
            return m[int(c)]
        except ValueError:
            return c

    return "".join(map(f, s))
