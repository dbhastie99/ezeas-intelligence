import subprocess
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class RepositoryMetadata:
    repo_name: str
    repo_path: str
    is_git_repo: bool
    branch: str | None
    commit: str | None
    is_dirty: bool | None
    metadata_resolution_status: str
    metadata_resolution_warnings: list[str] = field(default_factory=list)

    def model_dump(self) -> dict[str, Any]:
        return asdict(self)


def resolve_repository_metadata(repo_path: str | Path, repo_name: str) -> RepositoryMetadata:
    root = Path(repo_path).resolve()
    warnings: list[str] = []

    inside_work_tree = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if inside_work_tree.status == "unavailable":
        warnings.append("Git executable is unavailable; repository metadata could not be resolved.")
        return _unresolved_metadata(repo_name, root, "git_unavailable", warnings)
    if not inside_work_tree.ok or inside_work_tree.stdout.lower() != "true":
        warnings.append("Path is not a Git work tree; branch and commit metadata were not resolved.")
        if inside_work_tree.stderr:
            warnings.append(f"Git work tree detection failed: {inside_work_tree.stderr}")
        return _unresolved_metadata(repo_name, root, "not_git_repo", warnings)

    branch = _run_git(root, ["rev-parse", "--abbrev-ref", "HEAD"])
    commit = _run_git(root, ["rev-parse", "HEAD"])
    status = _run_git(root, ["status", "--short"])
    command_results = [branch, commit, status]
    failed_results = [result for result in command_results if not result.ok]
    for result in failed_results:
        if result.status == "unavailable":
            warnings.append("Git executable became unavailable while resolving repository metadata.")
        else:
            detail = result.stderr or "command returned a non-zero exit code"
            warnings.append(f"Git metadata command failed: git {' '.join(result.args)}: {detail}")

    if failed_results:
        return RepositoryMetadata(
            repo_name=repo_name,
            repo_path=str(root),
            is_git_repo=True,
            branch=None,
            commit=None,
            is_dirty=None,
            metadata_resolution_status="partial",
            metadata_resolution_warnings=warnings,
        )

    return RepositoryMetadata(
        repo_name=repo_name,
        repo_path=str(root),
        is_git_repo=True,
        branch=branch.stdout or None,
        commit=commit.stdout or None,
        is_dirty=bool(status.stdout),
        metadata_resolution_status="resolved",
        metadata_resolution_warnings=warnings,
    )


@dataclass(frozen=True)
class _GitCommandResult:
    args: list[str]
    ok: bool
    stdout: str
    stderr: str
    status: str


def _run_git(repo_path: Path, args: list[str]) -> _GitCommandResult:
    try:
        completed = subprocess.run(
            ["git", "-C", str(repo_path), *args],
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return _GitCommandResult(args=args, ok=False, stdout="", stderr="", status="unavailable")
    except OSError as exc:
        return _GitCommandResult(args=args, ok=False, stdout="", stderr=str(exc), status="failed")

    return _GitCommandResult(
        args=args,
        ok=completed.returncode == 0,
        stdout=completed.stdout.strip(),
        stderr=completed.stderr.strip(),
        status="resolved" if completed.returncode == 0 else "failed",
    )


def _unresolved_metadata(
    repo_name: str,
    repo_path: Path,
    status: str,
    warnings: list[str],
) -> RepositoryMetadata:
    return RepositoryMetadata(
        repo_name=repo_name,
        repo_path=str(repo_path),
        is_git_repo=False,
        branch=None,
        commit=None,
        is_dirty=None,
        metadata_resolution_status=status,
        metadata_resolution_warnings=warnings,
    )
