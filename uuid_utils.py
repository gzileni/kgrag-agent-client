"""Utility functions per gestire UUID in Python.

Piccolo helper usabile in tutto il progetto per generare, validare,
convertire e serializzare UUID.
"""
from __future__ import annotations

import base64
import re
import uuid
from typing import Optional, Union


_UUID_RE = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{12}$"
)


def generate_v4() -> uuid.UUID:
    """Genera un UUID v4 (random)."""
    return uuid.uuid4()


def generate_v1(node: Optional[int] = None) -> uuid.UUID:
    """Genera un UUID v1 (basato su tempo)."""
    return uuid.uuid1(node=node) if node is not None else uuid.uuid1()


def generate_v5(namespace: Union[uuid.UUID, str], name: str) -> uuid.UUID:
    """Genera un UUID v5 (namespace + name).

    namespace può essere un `uuid.UUID` oppure una stringa tra
    'dns', 'url', 'oid', 'x500' o una stringa UUID valida.
    """
    if isinstance(namespace, uuid.UUID):
        ns = namespace
    elif isinstance(namespace, str):
        ns_lower = namespace.lower()
        if ns_lower == "dns":
            ns = uuid.NAMESPACE_DNS
        elif ns_lower == "url":
            ns = uuid.NAMESPACE_URL
        elif ns_lower == "oid":
            ns = uuid.NAMESPACE_OID
        elif ns_lower == "x500":
            ns = uuid.NAMESPACE_X500
        elif _UUID_RE.match(namespace):
            ns = uuid.UUID(namespace)
        else:
            raise ValueError("namespace string non riconosciuta")
    else:
        raise TypeError("namespace deve essere uuid.UUID o str")

    return uuid.uuid5(ns, name)


def is_valid_uuid(value: Union[str, uuid.UUID]) -> bool:
    """Controlla se la stringa è un UUID valido (qualsiasi versione)."""
    if isinstance(value, uuid.UUID):
        return True
    try:
        uuid.UUID(value)
        return True
    except Exception:
        return False


def normalize_uuid(value: Union[str, uuid.UUID]) -> str:
    """
    Ritorna la rappresentazione canonica di un UUID.

    Restituisce una stringa minuscola con trattini.
    """
    return str(uuid.UUID(str(value))).lower()


def to_bytes(u: Union[str, uuid.UUID]) -> bytes:
    """Serializza un UUID in 16 bytes."""
    return uuid.UUID(str(u)).bytes


def from_bytes(b: bytes) -> uuid.UUID:
    """Ricrea un UUID da 16 bytes."""
    return uuid.UUID(bytes=b)


def uuid_to_base64(u: Union[str, uuid.UUID], urlsafe: bool = True) -> str:
    """Codifica i 16 byte di un UUID in base64 (senza padding)."""
    b = to_bytes(u)
    enc = base64.urlsafe_b64encode(b) if urlsafe else base64.b64encode(b)
    return enc.rstrip(b"=").decode("ascii")


def base64_to_uuid(s: str) -> uuid.UUID:
    """Decodifica una stringa base64 (con o senza padding) in UUID."""
    # Aggiusta padding
    pad = -len(s) % 4
    s_padded = s + ("=" * pad)
    b = base64.urlsafe_b64decode(s_padded)
    return from_bytes(b)


def compare_uuid(a: Union[str, uuid.UUID], b: Union[str, uuid.UUID]) -> bool:
    """Confronta due UUID in modo sicuro/consistente."""
    return uuid.UUID(str(a)) == uuid.UUID(str(b))


def json_default(obj):
    """Helper per json.dumps per serializzare UUID come stringhe."""
    if isinstance(obj, uuid.UUID):
        return str(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


__all__ = [
    "generate_v4",
    "generate_v1",
    "generate_v5",
    "is_valid_uuid",
    "normalize_uuid",
    "to_bytes",
    "from_bytes",
    "uuid_to_base64",
    "base64_to_uuid",
    "compare_uuid",
    "json_default",
]
