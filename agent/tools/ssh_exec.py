"""Read-only remote commands over SSH (Tailscale)."""

from __future__ import annotations

import os
from typing import Any

import paramiko


READ_ONLY_COMMANDS: tuple[str, ...] = (
    "df -h",
    "free -m",
    "journalctl -n 20 --no-pager",
)


def execute_remote_command(commands: list[str] | None = None) -> dict[str, Any]:
    """
    Run allow-listed read-only commands on TAILSCALE_HOST as SSH_USER using SSH_KEY_PATH.
    """
    host = os.environ.get("TAILSCALE_HOST", "").strip()
    user = os.environ.get("SSH_USER", "").strip()
    key_path = os.environ.get("SSH_KEY_PATH", "").strip()

    if not host or not user or not key_path:
        return {
            "ok": False,
            "error": "missing_env",
            "message": "TAILSCALE_HOST, SSH_USER, and SSH_KEY_PATH must be set",
        }

    to_run = commands if commands is not None else list(READ_ONLY_COMMANDS)
    for cmd in to_run:
        if cmd not in READ_ONLY_COMMANDS:
            return {
                "ok": False,
                "error": "disallowed_command",
                "message": f"Command not allow-listed: {cmd}",
            }

    outputs: list[dict[str, str]] = []

    try:
        pkey = paramiko.Ed25519Key.from_private_key_file(key_path)
    except Exception:
        try:
            pkey = paramiko.RSAKey.from_private_key_file(key_path)
        except Exception as exc:  # noqa: BLE001
            return {
                "ok": False,
                "error": "key_load_failed",
                "message": str(exc),
            }

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(
            hostname=host,
            username=user,
            pkey=pkey,
            timeout=20,
            banner_timeout=20,
            auth_timeout=20,
        )
        for cmd in to_run:
            stdin, stdout, stderr = client.exec_command(cmd, timeout=60)
            _ = stdin
            out = stdout.read().decode("utf-8", errors="replace")
            err = stderr.read().decode("utf-8", errors="replace")
            code = stdout.channel.recv_exit_status()
            outputs.append(
                {
                    "command": cmd,
                    "exit_code": str(code),
                    "stdout": out,
                    "stderr": err,
                }
            )
    except Exception as exc:  # noqa: BLE001
        return {
            "ok": False,
            "error": "ssh_failed",
            "message": str(exc),
        }
    finally:
        client.close()

    return {"ok": True, "host": host, "results": outputs}
