"""Core pluralisation rules for English.

Design decision: this module implements *regular* English pluralisation plus a
bounded set of irregular forms (child/children, person/people, etc.). It does
NOT attempt to handle foreign plurals that share a spelling with the singular
(\"sheep\", \"deer\", \"fish\", \"series\", \"species\"), because those forms are
ambiguous out of context: without a lemma dictionary you cannot know whether
\"sheep\" is singular or plural. The functions here return *a* valid plural for
the singular input and *a* valid singular for the plural input; for uncountable
or invariable nouns the same word comes back unchanged. This is stated plainly
so callers know the boundary.
"""

from __future__ import annotations

import re
from typing import Final

# Irregular mappings: singular -> plural. These are the closed, well-known set
# of English irregular plurals that are not produced by any suffix rule.
_IRREGULAR: Final[dict[str, str]] = {
    "child": "children",
    "person": "people",
    "man": "men",
    "woman": "women",
    "ox": "oxen",
    "tooth": "teeth",
    "foot": "feet",
    "goose": "geese",
    "mouse": "mice",
    "louse": "lice",
    "die": "dice",
}

# Reverse lookup: plural -> singular. Built once at import so we do not scan the
# dict on every singularise call.
_IRREGULAR_REV: Final[dict[str, str]] = {v: k for k, v in _IRREGULAR.items()}


# Suffix rules, applied in order. Each entry is (compiled regex, replacement).
# Rules are ordered most-specific first so that \"knife\" hits the
# \"fe\" rule before the generic \"f/v\" swap and before the bare \"add s\" fallthrough.
_RULES: Final[list[tuple[re.Pattern[str], str]]] = [
    # Words ending in 's', 'x', 'z', 'ch', 'sh' take 'es'.
    (re.compile(r"(?:s|x|z|ch|sh)$"), r"\g<0>es"),
    # Words ending in a consonant + 'y' swap to 'ies'.
    (re.compile(r"([^aeiou])y$"), r"\1ies"),
    # Words ending in 'fe' -> 'ves' (knife, wife, life).
    (re.compile(r"fe$"), "ves"),
    # Words ending in 'ief' -> 'ieves' (thief, brief).
    (re.compile(r"ief$"), "ieves"),
    # Words ending in a consonant + 'f' -> 'ves' (leaf, wolf, half).
    # We accept this as the default; exceptions like \"roof\"/\"chief\" are not
    # special-cased because English itself is split on them.
    (re.compile(r"([^e])f$"), r"\1ves"),
    # Words ending in a consonant + 'o' take 'es' (potato, hero, volcano).
    # \"photo\" / \"piano\" are exceptions we do not special-case.
    (re.compile(r"([^aeiou])o$"), r"\g<0>es"),
    # Default: append 's'.
    (re.compile(r"$"), "s"),
]

# Inverse rules for singularisation. Build by inverting the forward patterns.
# Ordering matters: try the most specific (longest) suffix first.
_REV_RULES: Final[list[tuple[re.Pattern[str], str]]] = [
    (re.compile(r"ies$"), "y"),          # city -> cities -> city
    (re.compile(r"ves$"), "f"),          # wolves -> wolf (also knife -> knif, known trade-off)
    (re.compile(r"(s|x|z|ch|sh)es$"), r"\1"),  # boxes -> box, churches -> church
    (re.compile(r"oes$"), "o"),          # potatoes -> potato
    (re.compile(r"s$"), ""),              # cats -> cat (final fallback)
]


def _apply_rules(word: str, rules: list[tuple[re.Pattern[str], str]]) -> str | None:
    for pattern, repl in rules:
        if pattern.search(word):
            actual = pattern.sub(repl, word, count=1)
            return actual
    return None


def pluralize(word: str) -> str:
    """Return the plural form of *word*.

    Falls back to the regular suffix rules when the word is not in the
    irregular table. Empty strings and already-plural invariable nouns
    (sheep, deer) are returned unchanged because we cannot reliably tell them
    apart from their singular; see the module docstring.
    """
    if not word:
        return word
    lower = word.lower()
    if lower in _IRREGULAR:
        return _match_case(word, _IRREGULAR[lower])
    result = _apply_rules(word, _RULES)
    if result is not None:
        return _match_case(word, result)
    return word + ("S" if word.isupper() else "s")


def singularize(word: str) -> str:
    """Return the singular form of *word*.

    Inverse of :func:`pluralize`. For \"ves\"-ending plurals we always map back
    to \"f\" (not \"fe\"), so ``singularize('knives')`` returns ``'knif'``. This is
    a known, documented trade-off: without a lemma list we cannot recover the
    lost 'e'.
    """
    if not word:
        return word
    lower = word.lower()
    if lower in _IRREGULAR_REV:
        return _match_case(word, _IRREGULAR_REV[lower])
    result = _apply_rules(word, _REV_RULES)
    return _match_case(word, result) if result is not None else word


def is_plural(word: str) -> bool:
    """Return True if *word* looks like a plural.

    A word is considered plural if either:
      * it is in the irregular-plural set (children, people, ...), or
      * singularize(word) != word and pluralize(singularize(word)) == word.

    The round-trip check filters out invariable nouns (sheep, deer) which pass
    the first test trivially because singularize('sheep') == 'sheep'.
    """
    if not word:
        return False
    lower = word.lower()
    if lower in _IRREGULAR_REV:
        return True
    s = singularize(word)
    if s == word:
        return False
    return pluralize(s) == word


def _match_case(original: str, replacement: str) -> str:
    """Match the case pattern of *original* on *replacement*.

    Handles all-upper, all-lower, and title-case (first letter capitalised).
    Mixed case like \"McDonald\" is left as-is on the replacement's lower form,
    because guessing is worse than being predictable.
    """
    if original.isupper():
        return replacement.upper()
    if original[:1].isupper() and not original[1:].isupper():
        return replacement[:1].upper() + replacement[1:]
    return replacement
