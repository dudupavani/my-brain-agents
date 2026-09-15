"""Generic append-only storage for rendered posts in the shared Git repository."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
from typing import Any

from PIL import Image

REMOTE_URL = "https://github.com/dudupavani/my-brain-agents.git"
STORAGE_RELATIVE_ROOT = Path("generated-content")
UUID_V4_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SAFE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


class RepositoryStorageError(ValueError):
    pass


class InputConflict(RepositoryStorageError):
    pass


@dataclass(frozen=True)
class IncomingDesign:
    path: Path
    raw_bytes: bytes
    document: dict[str, Any]
    design_id: str
    design_version_id: str
    source_image_sha256: str
    json_sha256: str


@dataclass(frozen=True)
class VersionWorkspace:
    repository_root: Path
    storage_root: Path
    product_name: str
    design_id: str
    design_version_id: str
    source_path: Path
    operational_path: Path


def _fact_value(value: Any) -> Any:
    if isinstance(value, dict) and set(value).issubset({"value", "origin", "confidence", "note"}) and "value" in value:
        return value["value"]
    return value


def validate_product_name(product_name: str) -> str:
    """Accept the user's product name when it is safe as one directory component."""
    if not isinstance(product_name, str) or not product_name or product_name in {".", ".."}:
        raise RepositoryStorageError("nome do produto inválido; informe outro nome para a pasta")
    if any(char in product_name for char in "/\\\0") or any(ord(char) < 32 for char in product_name):
        raise RepositoryStorageError("nome do produto contém caracteres inválidos; informe como deseja escrevê-lo")
    return product_name


def _required_id(document: dict[str, Any], field: str) -> str:
    value = _fact_value(document.get(field))
    if not isinstance(value, str) or not value or not SAFE_ID_RE.fullmatch(value):
        raise RepositoryStorageError(f"{field} ausente ou inválido")
    return value


def _source_sha256(document: dict[str, Any]) -> str:
    source = document.get("source")
    source = source.get("value") if isinstance(source, dict) and "value" in source else source
    source = _fact_value(source)
    if not isinstance(source, dict):
        raise RepositoryStorageError("source.value ausente ou inválido")
    digest = _fact_value(source.get("sha256"))
    if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
        raise RepositoryStorageError("source.value.sha256 ausente ou inválido")
    return digest


def read_incoming_design(path: str | Path) -> IncomingDesign:
    source_path = Path(path).expanduser().resolve()
    try:
        raw_bytes = source_path.read_bytes()
        document = json.loads(raw_bytes.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RepositoryStorageError(f"JSON de entrada inválido: {error}") from error
    if not isinstance(document, dict):
        raise RepositoryStorageError("JSON de entrada precisa ter uma raiz objeto")
    design_id = _required_id(document, "designId")
    design_version_id = _required_id(document, "designVersionId")
    if "assetBinding" not in document:
        raise RepositoryStorageError("assetBinding ausente")
    if not isinstance(document.get("generatedAssets"), list):
        raise RepositoryStorageError("generatedAssets ausente ou não é uma lista")
    return IncomingDesign(
        source_path,
        raw_bytes,
        document,
        design_id,
        design_version_id,
        _source_sha256(document),
        hashlib.sha256(raw_bytes).hexdigest(),
    )


def _git(repo: Path, *args: str) -> str:
    completed = subprocess.run(["git", "-C", str(repo), *args], check=False, capture_output=True, text=True)
    if completed.returncode:
        detail = (completed.stderr or completed.stdout).strip()
        raise RepositoryStorageError(f"git {' '.join(args)} falhou: {detail}")
    return completed.stdout


def sync_repository(repo: str | Path) -> Path:
    """Fast-forward the shared repository while preserving unrelated local changes."""
    repo_path = Path(repo).expanduser().resolve()
    if not (repo_path / ".git").exists():
        raise RepositoryStorageError(f"repositório Git não encontrado: {repo_path}")
    remote = _git(repo_path, "remote", "get-url", "origin").strip()
    if remote.rstrip("/") != REMOTE_URL.rstrip("/"):
        raise RepositoryStorageError(f"remote origin inesperado: {remote}")
    local_changes = _git(repo_path, "status", "--porcelain", "--", str(STORAGE_RELATIVE_ROOT)).strip()
    if local_changes:
        raise RepositoryStorageError("há alterações locais pendentes dentro de generated-content")
    _git(repo_path, "pull", "--ff-only")
    return repo_path


def _source_files(design_dir: Path) -> list[Path]:
    versions = design_dir / "versions"
    if not versions.is_dir():
        return []
    return [path / "design.source.json" for path in versions.iterdir() if path.is_dir() and (path / "design.source.json").is_file()]


def _source_sha_from_file(path: Path) -> str | None:
    try:
        document = json.loads(path.read_bytes().decode("utf-8"))
        return _source_sha256(document)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, RepositoryStorageError):
        return None


def _conflict_path(storage_root: Path, incoming: IncomingDesign, product_name: str) -> Path:
    return storage_root / product_name / "styles" / incoming.design_id / "conflicts" / f"{incoming.design_version_id}--{incoming.json_sha256}.json"


def _preserve_conflict(storage_root: Path, incoming: IncomingDesign, product_name: str) -> Path:
    path = _conflict_path(storage_root, incoming, product_name)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() != incoming.raw_bytes:
        raise InputConflict(f"conflito de bytes no arquivo de conflito: {path}")
    if not path.exists():
        path.write_bytes(incoming.raw_bytes)
    return path


def prepare_version(incoming: IncomingDesign, repository_root: str | Path, product_name: str) -> VersionWorkspace:
    """Preserve the source JSON and return the version's operational JSON."""
    product_name = validate_product_name(product_name)
    repo_root = Path(repository_root).expanduser().resolve()
    storage_root = repo_root / STORAGE_RELATIVE_ROOT
    design_dir = storage_root / product_name / "styles" / incoming.design_id
    version_dir = design_dir / "versions" / incoming.design_version_id
    source_path = version_dir / "design.source.json"
    operational_path = version_dir / "design.json"

    existing_sha_values = {_source_sha_from_file(path) for path in _source_files(design_dir)}
    existing_sha_values.discard(None)
    if existing_sha_values and incoming.source_image_sha256 not in existing_sha_values:
        conflict = _preserve_conflict(storage_root, incoming, product_name)
        raise InputConflict(f"origem incompatível; entrada preservada em {conflict}")

    if version_dir.exists():
        if source_path.is_file() and source_path.read_bytes() != incoming.raw_bytes:
            conflict = _preserve_conflict(storage_root, incoming, product_name)
            raise InputConflict(f"designVersionId já existe com conteúdo diferente; entrada preservada em {conflict}")
        if not source_path.exists():
            source_path.write_bytes(incoming.raw_bytes)
        if not operational_path.exists():
            operational_path.write_bytes(source_path.read_bytes())
    else:
        version_dir.mkdir(parents=True, exist_ok=False)
        source_path.write_bytes(incoming.raw_bytes)
        operational_path.write_bytes(incoming.raw_bytes)
    return VersionWorkspace(repo_root, storage_root, product_name, incoming.design_id, incoming.design_version_id, source_path, operational_path)


def _valid_png(path: Path, expected_size: tuple[int, int] | None = None) -> bool:
    try:
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            return image.format == "PNG" and (expected_size is None or image.size == expected_size)
    except (OSError, ValueError):
        return False


def _canvas_size(document: dict[str, Any]) -> tuple[int, int] | None:
    canvas = _fact_value(document.get("canvas"))
    if not isinstance(canvas, dict):
        return None
    width = _fact_value(canvas.get("widthPx", canvas.get("width")))
    height = _fact_value(canvas.get("heightPx", canvas.get("height")))
    if isinstance(width, int) and isinstance(height, int):
        return width, height
    return None


def validate_repository(repository_root: str | Path) -> None:
    """Validate source/operational JSONs and both directions of every post reference."""
    repo_root = Path(repository_root).expanduser().resolve()
    storage_root = repo_root / STORAGE_RELATIVE_ROOT
    seen_generation_ids: set[str] = set()
    listed_pngs: set[Path] = set()
    if not storage_root.is_dir():
        return
    for product_dir in sorted(path for path in storage_root.iterdir() if path.is_dir()):
        styles_dir = product_dir / "styles"
        if not styles_dir.is_dir():
            raise RepositoryStorageError(f"styles ausente: {styles_dir}")
        for design_dir in sorted(path for path in styles_dir.iterdir() if path.is_dir() and path.name != "conflicts"):
            versions_dir = design_dir / "versions"
            if not versions_dir.is_dir():
                raise RepositoryStorageError(f"versions ausente: {versions_dir}")
            for version_dir in sorted(path for path in versions_dir.iterdir() if path.is_dir()):
                source_path = version_dir / "design.source.json"
                operational_path = version_dir / "design.json"
                try:
                    source = json.loads(source_path.read_text(encoding="utf-8"))
                    operational = json.loads(operational_path.read_text(encoding="utf-8"))
                except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
                    raise RepositoryStorageError(f"JSON inválido em {version_dir}: {error}") from error
                source_design_id = _fact_value(source.get("designId"))
                operational_design_id = _fact_value(operational.get("designId"))
                source_version_id = _fact_value(source.get("designVersionId"))
                operational_version_id = _fact_value(operational.get("designVersionId"))
                if source_design_id != design_dir.name or operational_design_id != design_dir.name:
                    raise RepositoryStorageError(f"designId não corresponde a {version_dir}")
                if source_version_id != version_dir.name or operational_version_id != version_dir.name:
                    raise RepositoryStorageError(f"designVersionId não corresponde a {version_dir}")
                assets = operational.get("generatedAssets")
                if not isinstance(assets, list):
                    raise RepositoryStorageError(f"generatedAssets inválido: {operational_path}")
                expected_size = _canvas_size(operational)
                for record in assets:
                    if not isinstance(record, dict):
                        raise RepositoryStorageError(f"registro inválido: {operational_path}")
                    generation_id = record.get("generationId")
                    if not isinstance(generation_id, str) or not UUID_V4_RE.fullmatch(generation_id) or generation_id in seen_generation_ids:
                        raise RepositoryStorageError(f"generationId inválido ou duplicado: {generation_id}")
                    seen_generation_ids.add(generation_id)
                    if record.get("designVersionId") != version_dir.name:
                        raise RepositoryStorageError(f"registro sem designVersionId correto: {operational_path}")
                    expected_path = f"generated-content/{product_dir.name}/styles/{design_dir.name}/versions/{version_dir.name}/posts/{design_dir.name}--{generation_id}.png"
                    if record.get("path") != expected_path:
                        raise RepositoryStorageError(f"path inválido: {record.get('path')}")
                    png_path = repo_root / expected_path
                    if not png_path.is_file() or not _valid_png(png_path, expected_size):
                        raise RepositoryStorageError(f"PNG ausente ou inválido: {expected_path}")
                    listed_pngs.add(png_path.resolve())
    for png_path in storage_root.rglob("*.png"):
        if png_path.resolve() not in listed_pngs:
            raise RepositoryStorageError(f"PNG sem registro: {png_path}")


def commit_and_push(repo: str | Path) -> str:
    repo_path = Path(repo).expanduser().resolve()
    changed = _git(repo_path, "status", "--porcelain", "--", str(STORAGE_RELATIVE_ROOT)).strip()
    if not changed:
        raise RepositoryStorageError("nenhuma alteração de generated-content para registrar")
    _git(repo_path, "add", "--", str(STORAGE_RELATIVE_ROOT))
    _git(repo_path, "commit", "-m", "feat(renderer): persist posts by product and design version")
    _git(repo_path, "push", "origin", "main")
    return "pushed"


def default_brain_repo() -> Path:
    configured = os.environ.get("BRAIN_REPO")
    if configured:
        return Path(configured).expanduser().resolve()
    for parent in Path(__file__).resolve().parents:
        if (parent / ".git").is_dir() and (parent / STORAGE_RELATIVE_ROOT).is_dir():
            return parent
    return Path(__file__).resolve().parents[3]
