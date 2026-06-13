Aangezien `pi-server-vm` de Linux-omgeving representeert waarin de VM's draaien en waarbinnen PiSelfhosting wordt ontwikkeld, ligt de nadruk van de beveiliging hier met name op de integriteit van de virtualisatielaag, de netwerktoegang (zoals Samba-shares en Remmina/SSH-verbindingen) en de stabiliteit van de host.

Hier is een voorbeeld van hoe de `SECURITY.md` voor dit specifieke project eruit kan zien in raw Markdown:

```
# Security Policy

## Supported Versions

The table below outlines the support status for security updates regarding the VM configurations and deployment scripts.

| Version | Supported          | Environment / Host                  |
| ------- | ------------------ | ----------------------------------- |
| Latest  | :white_check_mark: | Linux VM / Ubuntu Desktop Baseline  |
| Older   | :x:                | Unsupported                         |

## Reporting a Vulnerability

Security is critical for infrastructure and virtualization management. If you discover any security vulnerability or misconfiguration that compromises the isolation or access control of this VM setup, please report it responsibly.

Do **not** open a public issue on GitHub. Instead, please send an email to security@piselfhosting.com with the following details:
* A clear description of the vulnerability (e.g., weak access controls, exposed ports, or container escape risks).
* Steps to reproduce the issue or a description of the configuration flaw.
* The impact on the VM isolation or the underlying host system.

## Disclosure Process

Upon receiving a report, we will:
* Acknowledge the receipt of your security report within 48 hours.
* Investigate the potential impact on both the VM environment and downstream projects like PiSelfhosting.
* Apply necessary hardening fixes directly to the repository configuration templates.

```
