#!/usr/bin/env python3
"""Генератор паролей на основе модуля secrets (криптостойкий).

Примеры:
    python passgen.py                      # один пароль, 16 символов
    python passgen.py -l 20 -n 5           # 5 паролей по 20 символов
    python passgen.py --no-symbols         # без спецсимволов
    python passgen.py --no-ambiguous       # без похожих символов (0/O, 1/l/I)
    python passgen.py --words 4            # парольная фраза из 4 слов
"""

import argparse
import secrets
import string

AMBIGUOUS = "0O1lI|`'\""

WORDS = [
    "apple", "river", "cloud", "tiger", "stone", "light", "forest", "panda",
    "ocean", "maple", "eagle", "flame", "frost", "cedar", "amber", "comet",
    "dune", "ember", "falcon", "glacier", "harbor", "island", "jungle",
    "karma", "lotus", "meadow", "nebula", "orbit", "pepper", "quartz",
    "raven", "summit", "thunder", "unity", "velvet", "willow", "zephyr",
    "anchor", "breeze", "canyon", "delta", "echo", "fjord", "garden",
]


def build_pools(use_lower, use_upper, use_digits, use_symbols, no_ambiguous):
    pools = []
    if use_lower:
        pools.append(string.ascii_lowercase)
    if use_upper:
        pools.append(string.ascii_uppercase)
    if use_digits:
        pools.append(string.digits)
    if use_symbols:
        pools.append("!@#$%^&*()-_=+[]{};:,.<>?/~")
    if no_ambiguous:
        pools = ["".join(c for c in p if c not in AMBIGUOUS) for p in pools]
    return [p for p in pools if p]


def generate_password(length=16, use_lower=True, use_upper=True,
                      use_digits=True, use_symbols=True, no_ambiguous=False):
    pools = build_pools(use_lower, use_upper, use_digits, use_symbols, no_ambiguous)
    if not pools:
        raise ValueError("Нужно включить хотя бы один тип символов.")
    if length < len(pools):
        raise ValueError(f"Длина должна быть не меньше {len(pools)}.")

    # по одному символу из каждого выбранного набора
    chars = [secrets.choice(p) for p in pools]
    # остальное добираем из общего набора
    alphabet = "".join(pools)
    chars += [secrets.choice(alphabet) for _ in range(length - len(chars))]
    # перемешиваем криптостойко
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)


def generate_passphrase(words=4, sep="-", capitalize=True, add_number=True):
    parts = [secrets.choice(WORDS) for _ in range(words)]
    if capitalize:
        parts = [w.capitalize() for w in parts]
    phrase = sep.join(parts)
    if add_number:
        phrase += sep + str(secrets.randbelow(100))
    return phrase


def main():
    ap = argparse.ArgumentParser(description="Генератор паролей")
    ap.add_argument("-l", "--length", type=int, default=16, help="длина пароля (по умолчанию 16)")
    ap.add_argument("-n", "--count", type=int, default=1, help="сколько паролей сгенерировать")
    ap.add_argument("--no-lower", action="store_true", help="без строчных букв")
    ap.add_argument("--no-upper", action="store_true", help="без заглавных букв")
    ap.add_argument("--no-digits", action="store_true", help="без цифр")
    ap.add_argument("--no-symbols", action="store_true", help="без спецсимволов")
    ap.add_argument("--no-ambiguous", action="store_true", help="убрать похожие символы (0/O, 1/l/I)")
    ap.add_argument("--words", type=int, default=0, help="режим парольной фразы: число слов")
    args = ap.parse_args()

    for _ in range(args.count):
        if args.words:
            print(generate_passphrase(args.words))
        else:
            print(generate_password(
                args.length,
                use_lower=not args.no_lower,
                use_upper=not args.no_upper,
                use_digits=not args.no_digits,
                use_symbols=not args.no_symbols,
                no_ambiguous=args.no_ambiguous,
            ))


if __name__ == "__main__":
    main()