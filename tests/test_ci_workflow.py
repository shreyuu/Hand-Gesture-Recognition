import re
from pathlib import Path

CI_WORKFLOW = Path(__file__).resolve().parent.parent / ".github" / "workflows" / "ci.yml"


def test_ci_token_is_read_only():
    text = CI_WORKFLOW.read_text()
    assert re.search(r"^permissions:\s*\n\s+contents: read\s*$", text, re.MULTILINE)


def test_ci_actions_are_pinned_to_commit_shas():
    uses = re.findall(r"uses:\s*(\S+)", CI_WORKFLOW.read_text())
    assert uses
    for action in uses:
        assert re.fullmatch(r"[\w.-]+/[\w.-]+@[0-9a-f]{40}", action), action
