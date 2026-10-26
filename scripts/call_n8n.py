"""Call the n8n workflow from Python (Day 5: n8n + Python + JSON + API key).

Uses only the standard library, so no pip install is needed.

Examples (from the project folder):
  python scripts/call_n8n.py --question "Which students are in class 10?"
  python scripts/call_n8n.py --question "And who is in section A?" --session demo1
  python scripts/call_n8n.py --list-workflows          (needs N8N_API_KEY)
  python scripts/call_n8n.py --export-workflows out.json   (needs N8N_API_KEY)

N8N_API_KEY: in n8n open Settings -> n8n API -> Create an API key, then in PowerShell:
  $env:N8N_API_KEY = "paste-the-key-here"
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

DEFAULT_BASE = "http://localhost:5678"


def post_json(url: str, payload: dict, timeout: int = 180) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_json(url: str, headers: dict, timeout: int = 30) -> dict:
    req = urllib.request.Request(url, headers=headers, method="GET")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Talk to the n8n student-chat workflow")
    parser.add_argument("--base", default=DEFAULT_BASE, help="n8n address, e.g. http://192.168.1.5:5678")
    parser.add_argument("--question", help="Question to send through the workflow")
    parser.add_argument("--session", default="python-script", help="Chat memory id")
    parser.add_argument("--list-workflows", action="store_true", help="List workflows using the n8n API key")
    parser.add_argument("--export-workflows", metavar="FILE", help="Save all workflows as JSON using the n8n API key")
    args = parser.parse_args()

    try:
        if args.question:
            url = f"{args.base}/webhook/student-chat"
            result = post_json(url, {"question": args.question, "session_id": args.session})
            print("Reply:", result.get("reply", result))
            return 0

        if args.list_workflows or args.export_workflows:
            key = os.environ.get("N8N_API_KEY", "")
            if not key:
                print("Set N8N_API_KEY first (n8n: Settings -> n8n API -> Create an API key).")
                return 1
            data = get_json(f"{args.base}/api/v1/workflows", {"X-N8N-API-KEY": key})
            workflows = data.get("data", [])
            if args.export_workflows:
                with open(args.export_workflows, "w", encoding="utf-8") as f:
                    json.dump(workflows, f, indent=2)
                print(f"Saved {len(workflows)} workflow(s) to {args.export_workflows}")
            else:
                for w in workflows:
                    print(f"- {w.get('name')}  (id={w.get('id')}, active={w.get('active')})")
            return 0

        parser.print_help()
        return 0

    except urllib.error.HTTPError as exc:
        print(f"HTTP {exc.code} from n8n: {exc.read().decode('utf-8', 'ignore')[:300]}")
        print("Hint: 404 usually means the workflow is not Published.")
        return 1
    except urllib.error.URLError as exc:
        print(f"Could not reach n8n at {args.base}: {exc.reason}")
        print("Hint: is 'npx n8n' running?")
        return 1


if __name__ == "__main__":
    sys.exit(main())
