"""Export exact UTF-8 Git blobs at a pinned HEAD into one review TXT."""

import argparse
import hashlib
import subprocess
from pathlib import Path


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--head", required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    head = git("rev-parse", "--verify", f"{args.head}^{{commit}}").decode().strip()
    base = git("rev-parse", "--verify", f"{args.base}^{{commit}}").decode().strip()
    changed = set(git("diff", "--name-only", "-z", base, head).decode().split("\0")) - {""}
    paths = git("ls-tree", "-r", "--name-only", "-z", head).decode().split("\0")
    paths = sorted(path for path in paths if path)
    blocks = [
        "KTradeLink Rust Core foundation: original source review\n",
        f"Repository: kisbi3/ktradelink\nHEAD: {head}\nBASE: {base}\n",
        f"Tracked files: {len(paths)}; changed paths: {len(changed)}\n",
        "All tracked file bodies are verbatim. Delimiters are outside each body.\n",
        "Line 1 of a source file begins after BEGIN SOURCE CONTENT.\n",
        "Review the Rust/Python boundary, exact prices, error handling and packaging.\n",
        "No live broker payloads, credentials, network adapters or orders are implemented.\n",
    ]
    for path in paths:
        raw = git("show", f"{head}:{path}")
        text = raw.decode("utf-8")  # Fail, rather than silently omit any binary file.
        expected = git("rev-parse", f"{head}:{path}").decode().strip()
        actual = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        if actual != expected:
            raise ValueError(f"Git blob verification failed: {path}")
        lines = len(text.splitlines())
        blocks.append(
            f"\n{'=' * 72}\nFILE: {path}\nBLOB SHA: {actual}\n"
            f"CHANGED: {path in changed}\nBYTES: {len(raw)}; SOURCE LINES: {lines}\n"
            "BEGIN SOURCE CONTENT\n"
        )
        blocks.append(text)
        blocks.append(("" if text.endswith("\n") else "\n") + f"END SOURCE CONTENT: {path}\n")
    content = "".join(blocks).encode("utf-8")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(content)
    print(f"Review packet: {len(paths)} files, {len(content)} bytes, HEAD={head}")
    print(f"SHA256: {hashlib.sha256(content).hexdigest()}")


if __name__ == "__main__":
    main()
