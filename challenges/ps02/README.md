\# PS-02 - Encrypted Research Note



Domain: Cryptography and Encoding  

Difficulty: Easy



\## Player Files



\- `release/research\_note.enc`

\- `release/message\_format.txt`



\## Dependency



Requires the Vigenere key recovered from PS-01.



\## Intended Solution



1\. Inspect `research\_note.enc`.

2\. Identify the outer Base64 encoding.

3\. Decode the Base64 layer.

4\. Recognise the remaining text as Vigenere ciphertext.

5\. Decrypt it using the key recovered from PS-01.

6\. Recover the Stage 2 flag and PS-03 portal credentials.



\## Tools



\- Base64

\- Vigenere decoder

\- CyberChef or equivalent

\- Python



\## Reset



PS-02 is stateless. Reset is performed by restoring or re-downloading the original release files.

