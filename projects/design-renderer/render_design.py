"""Run the single design.json -> final image flow from the terminal."""

from __future__ import annotations

import argparse
from pathlib import Path

from renderer.asset_binding import append_generated_asset, reserve_generation
from renderer.collector import collect, load_resolutions
from renderer.design_reader import DesignError, load_design
from renderer.repository_storage import (
    RepositoryStorageError,
    commit_and_push,
    default_brain_repo,
    prepare_version,
    read_incoming_design,
    sync_repository,
    validate_product_name,
    validate_repository,
)
from renderer.raster_renderer import RenderError, render
from validator import ValidationError, validate_output, validate_resolutions


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect design slots one by one and render one PNG/JPG.")
    parser.add_argument("design", help="path to design.json")
    parser.add_argument("--answers", help="non-interactive JSON resolutions; each value is text/path or 'skipped'")
    parser.add_argument("--product", help="nome do produto para a pasta de armazenamento")
    parser.add_argument("--brain-repo", default=str(default_brain_repo()), help="clone local do segundo cérebro")
    args = parser.parse_args()
    try:
        incoming = read_incoming_design(args.design)
        if args.product is None:
            if args.answers:
                raise RepositoryStorageError("informe --product quando usar --answers")
            product_name = input("Para qual produto devo criar esses posts? ")
        else:
            product_name = args.product
        product_name = validate_product_name(product_name)
        brain_repo = sync_repository(args.brain_repo)
        workspace = prepare_version(incoming, brain_repo, product_name)
        design = load_design(workspace.operational_path)
        answers = load_resolutions(args.answers) if args.answers else collect(design)
        validate_resolutions(design, answers)
        asset = reserve_generation(design, brain_repo, product_name)
        result = render(design, asset.absolute_path, answers)
        validate_output(design, result.path, result)
        append_generated_asset(workspace.operational_path, asset)
        validate_repository(brain_repo)
        commit_and_push(brain_repo)
    except (DesignError, RenderError, ValidationError, RepositoryStorageError, OSError, ValueError) as error:
        parser.error(str(error))
    for warning in result.warnings:
        print(f"warning: {warning}")
    print(result.path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
