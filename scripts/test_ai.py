"""Send one tiny request to your configured AI model and show exactly what happens.

    python -m scripts.test_ai
Prints the provider, model, how long it took, and the real error (never your key).
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import config  # noqa: E402
from app.services import ai  # noqa: E402


def main() -> None:
    print("Provider:", config.AI_PROVIDER, "| key set:", bool(config.AI_API_KEY), "| timeout:", config.AI_TIMEOUT_SECONDS, "s")
    if not ai.is_enabled():
        raise SystemExit("AI is not enabled: set AI_PROVIDER and AI_API_KEY in .env")
    start = time.time()
    try:
        text = ai.call_llm("You are a test.", "Reply with exactly: OK", max_tokens=50)
    except ai.AIError as exc:
        print(f"FAILED after {time.time() - start:.1f}s: {exc}")
        if exc.__cause__:
            print("Underlying cause:", repr(exc.__cause__))
        raise SystemExit(1)
    print(f"Model used: {ai.model_name()}")
    print(f"SUCCESS in {time.time() - start:.1f}s. Reply: {text.strip()[:80]}")


if __name__ == "__main__":
    main()
