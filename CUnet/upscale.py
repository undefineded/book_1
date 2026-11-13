#!/usr/bin/env python3
"""RGB image -> CUnet CPU 2x -> PNG, preserving native inference pixels."""
import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent


def upscale_image(source, destination, cpu, model, *, dpi=300, overwrite=False):
    """Return export metadata; output dimensions are exactly twice the input."""
    source, destination = Path(source).resolve(), Path(destination).resolve()
    cpu, model = Path(cpu).resolve(), Path(model).resolve()
    if source == destination:
        raise ValueError('Input and output must be different files')
    if destination.suffix.lower() != '.png':
        raise ValueError('Output must be a PNG file')
    if destination.exists() and not overwrite:
        raise FileExistsError(f'Output exists: {destination}; use --overwrite to replace')
    if dpi <= 0:
        raise ValueError('DPI must be positive')
    for required in (cpu, model/'scale2.0x_model.bin', model/'scale2.0x_model.param'):
        if not required.is_file():
            raise FileNotFoundError(required)
    with Image.open(source) as image:
        if image.mode != 'RGB':
            raise ValueError('Input must be RGB; transparent lettering layers are not supported')
        source_size = image.size
    expected = tuple(v*2 for v in source_size)
    destination.parent.mkdir(parents=True, exist_ok=True)
    # Keep the temporary PNG on the destination filesystem for atomic replacement.
    with tempfile.TemporaryDirectory(prefix='.cunet-', dir=destination.parent) as td:
        td = Path(td)
        inp, out, png = td/'input.ppm', td/'output.ppm', td/'output.png'
        subprocess.run(['magick', str(source), '-alpha', 'off', '-depth', '8', str(inp)], check=True)
        subprocess.run([str(cpu), str(inp), str(out), str(model)], check=True)
        with Image.open(out) as native:
            if native.mode != 'RGB' or native.size != expected:
                raise ValueError(f'Unexpected inference result: {native.mode} {native.size}')
            native_hash = hashlib.sha256(native.tobytes()).hexdigest()
        # Format conversion and PPI metadata only: no interpolation or resize.
        subprocess.run(['magick', str(out), '-units', 'PixelsPerInch', '-density', str(dpi),
                        '-define', 'png:color-type=2', str(png)], check=True)
        with Image.open(png) as delivered:
            if delivered.size != expected or hashlib.sha256(delivered.tobytes()).hexdigest() != native_hash:
                raise ValueError('PNG pixels differ from the native CUnet inference output')
        os.replace(png, destination)
    return {'source_size': list(source_size), 'output_size': list(expected),
            'method': 'CUnet scale2 noise=-1; native inference pixels, no final resize',
            'native_pixel_sha256': native_hash}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--cpu', type=Path, default=ROOT/'build/cpu_upscale')
    parser.add_argument('--models', type=Path, default=ROOT/'models-cunet')
    parser.add_argument('--dpi', type=int, default=300)
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()
    result = upscale_image(args.input, args.output, args.cpu, args.models,
                           dpi=args.dpi, overwrite=args.overwrite)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
