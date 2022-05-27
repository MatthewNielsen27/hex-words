import re

from typing import Iterable


subs = [
    ('for', '4'),
    ('ate', '8'),
    ('ten', '10'),
    ('i', '1'),
    ('o', '0'),
    ('s', '5'),
    ('t', '7'),
]


def find_hex_words(substitutions: Iterable[tuple],
                   prefixes: Iterable[str] = None,
                   suffixes: Iterable[str] = None,
                   min_length: int = 3,
                   max_length: int = 20,
                   strict: bool = False) -> Iterable[str]:
    """
    Finds hex words according to the given substitution scheme.

    :param prefixes Allows you to specify allowed non-hex prefixes.
    :param suffixes Allows you to specify allowed non-hex suffixes.
    """
    prefixes = '' if not prefixes else f'(?:{"|".join(prefixes)}){"" if strict else "?"}'
    suffixes = '' if not suffixes else f'(?:{"|".join(suffixes)}){"" if strict else "?"}'

    # We want to optionally allow things like '0xide', even though 'x' isn't a
    # hex digit. This is specifiable through the prefixes or suffixes param.
    hex_word_regex = re.compile(f"^{prefixes}[a-f0-9]*{suffixes}$")

    found = []
    with open('web2.txt') as f:
        for word in f.readlines():
            word = word.strip()
            
            # Apply substitutions
            for old, new in substitutions:
                word = word.replace(old, new)

            # Check that constraints are met
            if not (min_length < len(word) < max_length):
                continue
            elif hex_word_regex.match(word):
                found.append(word)
    
    return found


def main():
    for word in find_hex_words(subs, prefixes=[], suffixes=['ul'], strict=True):
        print(word)

if __name__ == '__main__':
    main()
