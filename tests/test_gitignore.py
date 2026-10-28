"""Prevent accidentally tracking common local brokerage secrets.

.gitignore is a convenience safeguard, not a replacement for secret scanning.
"""

import shutil
import subprocess
from pathlib import Path

import pytest


@pytest.mark.parametrize(
    "path",
    [
        "broker_access.token",
        "access_token.json",
        "broker_refresh_token_cache.json",
        "NPKI/user/SignCert.der",
    ],
)
def test_gitignore_excludes_local_broker_credentials(path: str) -> None:
    if shutil.which("git") is None:
        pytest.skip("git executable is required for ignore pattern contract tests")

    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        ["git", "check-ignore", "-q", "--no-index", path],
        cwd=root,
        check=False,
        capture_output=True,
    )
    assert result.returncode == 0, f"{path} is not excluded by .gitignore"
