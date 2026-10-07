# CyberTrace: Project Shadow - Architecture Diagram

```mermaid
flowchart TB

    P[Participant]

    subgraph CONTROL["Control Zone"]
        N[Nginx<br/>Participant Entry Point]
        C[CTFd<br/>Accounts / Challenges / Scoring / Flags]
        DB[(MariaDB)]
        R[(Redis)]

        N --> C
        C --> DB
        C --> R
    end

    subgraph FILES["File Challenge Zone"]
        F1[PS-01<br/>Hidden Blueprint]
        F2[PS-02<br/>Encrypted Research Note]
        F4[PS-04<br/>Recovered Evidence Drive]
        F5[PS-05<br/>Suspicious Network Session]
    end

    subgraph WEB["Web Challenge Zone - Proposed"]
        W[PS-03<br/>Flask + SQLite<br/>TCP 8083]
    end

    subgraph SYSTEM["System Challenge Zone - Proposed"]
        S[PS-06<br/>Ubuntu Server VM<br/>SSH TCP 2226]
    end

    subgraph OPS["Operations Zone - Proposed"]
        O[Logging / Backups / Health Checks]
    end

    P -->|HTTP local / HTTPS final| N
    P -->|Challenge access| F1
    P -->|Challenge access| F2
    P -->|Challenge access| F4
    P -->|Challenge access| F5
    P -->|HTTP TCP 8083| W
    P -->|SSH TCP 2226| S

    W -.->|No outbound Internet| X1[Internet]
    S -.->|No Internet route| X2[Internet]

    W -.->|Denied| DB
    W -.->|Denied| R
    S -.->|Denied| DB
    S -.->|Denied| R

    O -.-> CONTROL
    O -.-> WEB
    O -.-> SYSTEM
