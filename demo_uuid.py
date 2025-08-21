"""Script demo per mostrare l'uso di `uuid_utils`."""
from __future__ import annotations

import json
from uuid_utils import (
    generate_v4,
    is_valid_uuid,
    normalize_uuid,
    uuid_to_base64,
    base64_to_uuid,
    compare_uuid,
    json_default,
)


def main() -> None:
    v4 = generate_v4()
    print("v4:", v4)
    print("is valid:", is_valid_uuid(str(v4)))
    print("normalized:", normalize_uuid(v4))
    b64 = uuid_to_base64(v4)
    print("base64 (urlsafe, no padding):", b64)
    print("decoded equals original:", compare_uuid(base64_to_uuid(b64), v4))
    print("json dump:", json.dumps({"id": v4}, default=json_default))


if __name__ == "__main__":
    main()
