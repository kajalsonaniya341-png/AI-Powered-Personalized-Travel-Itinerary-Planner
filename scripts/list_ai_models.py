"""Show which Gemini models your API key can use (helps choose AI_MODEL).

    python -m scripts.list_ai_models
"""
import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import config  # noqa: E402
from app.services.ai import pick_gemini_model  # noqa: E402


def main() -> None:
    if not config.AI_API_KEY:
        raise SystemExit("AI_API_KEY is not set in .env")
    req = urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models?pageSize=200",
                                 headers={"x-goog-api-key": config.AI_API_KEY})
    with urllib.request.urlopen(req, timeout=30) as resp:
        models = json.loads(resp.read().decode("utf-8")).get("models", [])
    usable = [m["name"].replace("models/", "") for m in models if "generateContent" in m.get("supportedGenerationMethods", [])]
    print("Models that support generateContent:")
    for name in sorted(usable):
        print("  ", name)
    print("\nThe app would automatically use:", pick_gemini_model(models) or "(none found - set AI_MODEL manually)")


if __name__ == "__main__":
    main()
