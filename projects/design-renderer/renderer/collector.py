"""One-slot-at-a-time terminal conversation for a design render."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Callable

from .design_reader import Design, Slot


SKIP_WORDS = {"skip", "skipped", "ignore", "ignored", "ignorar", "ignore este", "pular", "não", "nao"}


@dataclass(frozen=True)
class Resolution:
    status: str
    value: str | None = None


def is_skip(answer: str) -> bool:
    return answer.strip().lower() in SKIP_WORDS


def prompt_for(slot: Slot, theme: str | None = None) -> str:
    label = slot.role.replace("-", " ")
    if slot.kind == "image":
        suffix = f" O tema deve acompanhar: {theme}." if theme else ""
        return f"Envie o caminho local da imagem para {label}, ou digite 'ignorar'.{suffix} "
    return f"Qual é o conteúdo para {label}? Digite 'ignorar' para deixar o espaço vazio. "


def _theme(resolutions: dict[str, Resolution], design: Design) -> str | None:
    title_roles = {"title", "headline", "subtitle", "body", "support"}
    for element in design.elements:
        if element.role.lower() in title_roles:
            answer = resolutions.get(element.id)
            if answer and answer.status == "filled" and answer.value:
                return answer.value
    return None


def collect(
    design: Design,
    ask: Callable[[str], str] = input,
    emit: Callable[[str], None] = print,
) -> dict[str, Resolution]:
    """Ask exactly once for each unresolved slot, in the JSON element order."""
    resolutions: dict[str, Resolution] = {}
    for slot in design.slots():
        answer = ask(prompt_for(slot, _theme(resolutions, design)))
        if is_skip(answer):
            resolutions[slot.id] = Resolution(status="skipped")
            emit(f"{slot.id}: skipped")
        else:
            value = answer if slot.kind == "text" else str(Path(answer).expanduser())
            resolutions[slot.id] = Resolution(status="filled", value=value)
    return resolutions


def load_resolutions(path: str | Path) -> dict[str, Resolution]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("answers must be a JSON object indexed by slot id")
    result: dict[str, Resolution] = {}
    for slot_id, item in data.items():
        if item == "skipped" or item is None:
            result[str(slot_id)] = Resolution("skipped")
        elif isinstance(item, str):
            result[str(slot_id)] = Resolution("filled", item)
        elif isinstance(item, dict):
            status = str(item.get("status", "filled"))
            if status not in {"filled", "skipped"}:
                raise ValueError(f"invalid status for {slot_id}: {status}")
            result[str(slot_id)] = Resolution(status, item.get("value"))
        else:
            raise ValueError(f"invalid answer for {slot_id}")
    return result


def save_resolutions(path: str | Path, resolutions: dict[str, Resolution]) -> None:
    payload = {slot_id: asdict(resolution) for slot_id, resolution in resolutions.items()}
    Path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
