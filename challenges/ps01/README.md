\# PS-01 - Hidden Blueprint



Domain: Steganography / File Analysis  

Difficulty: Easy



\## Player Files



\- `release/project\_shadow\_blueprint.jpg`

\- `release/project\_shadow\_blueprint.jpg.sha256`



\## Intended Solution Path



1\. Verify the SHA-256 checksum.

2\. Inspect the JPEG file type and metadata.

3\. Identify the metadata clue.

4\. Use the clue as the steghide passphrase.

5\. Extract `handoff\_note.txt`.

6\. Recover the Stage 1 flag and the PS-02 key.



\## Tools



\- `sha256sum`

\- `file`

\- `ExifTool`

\- `strings`

\- `binwalk`

\- `steghide`



\## Reset



PS-01 is stateless. Reset is performed by re-downloading the clean challenge files.

