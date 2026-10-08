# PS-04: Recovered Evidence Drive

## Scenario
Investigators recovered a USB drive connected to a
workstation involved in the Project Shadow incident.

The drive may contain browser activity and remnants
of deleted synchronisation records.

## Objective
Analyse the forensic image and recover two flag
fragments to reconstruct the PS-04 flag.

## Provided Files
- shadow_usb.img
- timeline_template.csv

## Recommended Tools
- Kali Linux
- The Sleuth Kit (mmls, fls, icat)
- SQLite3
- sha256sum

## Tasks
1. Verify the forensic image integrity.
2. Identify the FAT32 partition.
3. Examine the browser history database.
4. Recover the deleted synchronisation log.
5. Correlate the workstation and UTC timestamps.
6. Combine Fragment A and Fragment B.

## Flag Format
CyberTrace{S4_<FragmentA><FragmentB>}

## Rules
- Do not modify the original forensic image.
- Use a separate directory for recovered artifacts.
- Record evidence and findings in the timeline.
- Submit the completed flag to the challenge platform.
