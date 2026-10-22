# pluralize-utils

English pluralisation helper: turn singulars into plurals and back, with a bounded set of irregular forms handled explicitly.

```python
from pluralize_utils import pluralize, singularize, is_plural

assert pluralize("cat") == "cats"
assert pluralize("child") == "children"
assert singularize("cities") == "city"
assert is_plural("boxes") is True
assert is_plural("box") is False
```

## Why

There are several Python pluralisation libraries and most pull in a big data file of lemmas or depend on a larger NLP stack. That is overkill when you need decent coverage of regular English plus the handful of irregulars (child/children, person/people, mouse/mice) and you are fine with the occasional wrong answer on genuinely ambiguous words. This library is zero-dependency, a few dozen lines of rules, and honest about where it breaks.

## The edge you will hit

Invariable nouns — sheep, deer, fish, series, species — look identical singular and plural. Without a lemma dictionary you cannot tell which is intended, so `pluralize` and `singularize` return them unchanged and `is_plural` reports `False` (the round-trip check `pluralize(singularize(w)) == w` fails). If you need those handled correctly, you need a dictionary-backed library; this one is not that.

There is also a known asymmetry with `-fe` words: `pluralize("knife")` correctly yields `knives`, but `singularize("knives")` yields `knif` (not `knife`) because the `ves -> f` rule cannot recover the lost `e`. Documented, not fixed, because fixing it requires a word list.

## Exports

- `pluralize(word: str) -> str`
- `singularize(word: str) -> str`
- `is_plural(word: str) -> bool`
