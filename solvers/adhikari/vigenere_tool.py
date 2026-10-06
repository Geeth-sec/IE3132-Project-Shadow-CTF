import sys

def vigenere(text, key, decrypt=False):
    result = []
    key = key.upper()
    key_index = 0

    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('A')

            if decrypt:
                shift = -shift

            base = ord('A') if char.isupper() else ord('a')
            encrypted = chr((ord(char) - base + shift) % 26 + base)

            result.append(encrypted)
            key_index += 1
        else:
            result.append(char)

    return ''.join(result)


if len(sys.argv) != 4:
    print("Usage: python3 vigenere_tool.py encrypt|decrypt input_file KEY")
    sys.exit(1)

mode = sys.argv[1]
filename = sys.argv[2]
key = sys.argv[3]

with open(filename, "r") as file:
    text = file.read()

if mode == "encrypt":
    sys.stdout.write(vigenere(text, key))
elif mode == "decrypt":
    sys.stdout.write(vigenere(text, key, decrypt=True))
else:
    print("Mode must be encrypt or decrypt")

