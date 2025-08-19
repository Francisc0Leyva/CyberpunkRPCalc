from typing import Dict
import d20
class DiceRollError(Exception):
    pass

def roll(expr: str = "1d20") -> Dict[str, str]:
    if d20 is None:
        raise DiceRollError(
            f"'d20' package is not available: {_import_err}. "
            "Install it with: pip install d20"
        )
    try:
        r = d20.roll(expr)
    except Exception as e:
        raise DiceRollError(f"Invalid dice expression '{expr}': {e}") from e

    return {"expr": expr, "total": r.total, "detail": str(r)}


