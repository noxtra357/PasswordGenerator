# Password Generator

A command-line utility that generates random passwords and passphrases. It uses the `secrets` module from the standard library, a cryptographically secure source of randomness. There is nothing to install.

> The `-h` help text and error messages are in Russian.

## Features

- Passwords of a chosen length made of lowercase and uppercase letters, digits, and symbols
- Any character type can be turned off
- A mode without look-alike characters (`0`, `O`, `1`, `l`, `I`), which makes passwords easier to read and retype
- A guarantee that the password contains at least one character of each enabled type, which helps with sites that enforce strict password rules
- Generate several passwords in one run
- Passphrases made of words, for example `Maple-River-Tiger-Frost-42`

## Requirements

- Python 3.6 or newer
- Nothing else

## Running

```bash
python passgen.py                      # one password, 16 characters
python passgen.py -l 20 -n 5           # 5 passwords, 20 characters each
python passgen.py --no-symbols         # no symbols
python passgen.py --no-ambiguous       # no look-alike characters
python passgen.py --words 4            # passphrase of 4 words
```

Options can be combined:

```bash
python passgen.py -l 24 -n 3 --no-symbols --no-ambiguous
```

On Linux and macOS you can make the script executable and run it directly:

```bash
chmod +x passgen.py
./passgen.py -l 20
```

If your script has a different name, use that instead. Run `python passgen.py -h` for a list of all options.

## Options

| Option               | Description                                     | Default      |
|----------------------|-------------------------------------------------|--------------|
| `-l`, `--length`     | Password length                                 | 16           |
| `-n`, `--count`      | How many passwords to generate                  | 1            |
| `--no-lower`         | No lowercase letters                            | off          |
| `--no-upper`         | No uppercase letters                            | off          |
| `--no-digits`        | No digits                                       | off          |
| `--no-symbols`       | No symbols                                      | off          |
| `--no-ambiguous`     | Remove look-alike characters `0 O 1 l I`        | off          |
| `--words`            | Passphrase mode: number of words                | 0 (off)      |

Passwords are printed to the console, one per line.

## Character sets

- Lowercase: `a-z`
- Uppercase: `A-Z`
- Digits: `0-9`
- Symbols: `!@#$%^&*()-_=+[]{};:,.<>?/~`

If a site doesn't accept some of these symbols, use `--no-symbols`.

## Passphrases

Enable this mode with `--words N`. The phrase is built from N random words from the built-in list, each word is capitalized, and a number from 0 to 99 is appended at the end. The separator is a hyphen:

```
Maple-River-Tiger-Frost-42
```

In this mode the other options (`-l`, `--no-*`) are ignored, and only `--words` and `-n` apply. Words can repeat.

## Strength

- The default password (16 characters from all four sets) gives roughly 100 bits of entropy, which is more than enough.
- **Passphrases are noticeably weaker.** The built-in list contains only 44 words. A 4-word phrase with a number gives about 28 bits of entropy (roughly 375 million combinations), which can be guessed in a reasonable amount of time. For important accounts, use regular passwords or replace the word list with a large one (see "Customizing").

## Things to know

- **The minimum length equals the number of enabled character types.** With all four types you can't generate a password shorter than 4 characters. If you disable every type or ask for too short a length, the script exits with a `ValueError` and a stack trace.
- **`--no-ambiguous` removes `0`, `O`, `1`, `l`, and `I`.** The `AMBIGUOUS` constant also contains `|`, `` ` ``, `'`, and `"`, but none of them are in the symbol set, so they currently have no effect.
- **Passwords are not stored anywhere.** They are only printed to the console, so copy them into a password manager.

## Using it as a module

You can import the functions into your own code:

```python
from passgen import generate_password, generate_passphrase

print(generate_password(length=20, use_symbols=False))
print(generate_passphrase(words=5, sep=".", capitalize=False, add_number=False))
```

For `generate_passphrase`, the separator, capitalization, and trailing number can only be changed through function arguments, not from the command line.

## Customizing

- Word list for passphrases: the `WORDS` constant. The longer it is, the stronger the phrase. For example, the 7776-word EFF list gives about 12.9 bits per word
- Symbol set: the string in the `build_pools()` function
- Look-alike character set: the `AMBIGUOUS` constant
- Default length and count: the `default` values in `argparse` inside `main()`

## Code structure

- `build_pools()`: assembles the character sets based on the chosen options
- `generate_password()`: generates a password and shuffles the characters
- `generate_passphrase()`: builds a passphrase
- `main()`: command-line argument parsing and output
