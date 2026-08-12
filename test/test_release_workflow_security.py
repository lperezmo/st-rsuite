"""Privilege-boundary guard for the automated release workflow."""

from pathlib import Path

WORKFLOW = Path(__file__).parent.parent / ".github" / "workflows" / "release.yml"


def _job_block(source: str, name: str, next_name: str) -> str:
    return source.split(f"\n  {name}:\n", 1)[1].split(f"\n  {next_name}:\n", 1)[0]


def test_build_dependencies_never_run_with_pypi_oidc():
    source = WORKFLOW.read_text()
    build = _job_block(source, "build-dist", "upload-release-assets")
    upload = _job_block(source, "upload-release-assets", "publish")
    publish = _job_block(source, "publish", "bump-demo")

    assert "contents: read" in build
    assert "id-token: write" not in build
    assert "npm ci" in build and "python -m build" in build

    assert "contents: write" in upload
    assert "id-token: write" not in upload

    assert "id-token: write" in publish
    assert "contents: write" not in publish
    assert "npm ci" not in publish
    assert "python -m build" not in publish
    assert "python -m pip install" not in publish
    assert "actions/download-artifact@v7" in publish
    assert "pypa/gh-action-pypi-publish@release/v1" in publish
