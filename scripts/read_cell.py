"""
Read cell source and/or outputs from a Jupyter notebook.

Usage:
  python scripts/read_cell.py <notebook_path> <cell_index> [--source] [--output] [--save-figures]

Options:
  --source        Print the cell's source code (default if no flags given)
  --output        Print the cell's outputs (default if no flags given)
  --save-figures  Save any image outputs as PNG files in temp/ and print paths
                  (useful for visual inspection by tools that can read images)
  --list          Ignore cell_index; list all cells with type and first line

If neither --source nor --output is given, both are printed.

Examples:
  python scripts/read_cell.py notebooks/138_the_r0_mechanism.ipynb 9
  python scripts/read_cell.py notebooks/138_the_r0_mechanism.ipynb 9 --output
  python scripts/read_cell.py notebooks/138_the_r0_mechanism.ipynb 9 --save-figures
  python scripts/read_cell.py notebooks/138_the_r0_mechanism.ipynb 0 --list
"""
import json, sys, os, base64


def ensure_utf8_stdout():
    """Reconfigure stdout for UTF-8 on Windows."""
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')


def read_notebook(nb_path):
    nb_path = os.path.abspath(nb_path)
    with open(nb_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_source(cell):
    src = cell.get('source', '')
    if isinstance(src, list):
        return ''.join(src)
    return src


def list_cells(nb):
    cells = nb['cells']
    print(f"Notebook has {len(cells)} cells:\n")
    for i, cell in enumerate(cells):
        ctype = cell['cell_type']
        src = get_source(cell)
        first_line = src.split('\n')[0][:80] if src else '(empty)'
        has_output = bool(cell.get('outputs'))
        n_figs = sum(
            1 for o in cell.get('outputs', [])
            if o.get('output_type') == 'display_data'
            and 'image/png' in o.get('data', {})
        )
        tag = f'  [{n_figs} fig]' if n_figs else ''
        out_tag = ' [has output]' if has_output else ''
        print(f"  [{i:2d}] {ctype:8s}{out_tag}{tag}  {first_line}")


def print_source(cell, cell_idx):
    src = get_source(cell)
    print(f"=== Cell {cell_idx} ({cell['cell_type']}) source ===")
    print(src)


def print_output(cell, cell_idx):
    outputs = cell.get('outputs', [])
    if not outputs:
        print(f"=== Cell {cell_idx} has no outputs ===")
        return

    print(f"=== Cell {cell_idx} output ===")
    for i, output in enumerate(outputs):
        otype = output.get('output_type', 'unknown')

        if otype == 'stream':
            text = output.get('text', [])
            if isinstance(text, list):
                text = ''.join(text)
            print(text, end='')

        elif otype in ('display_data', 'execute_result'):
            data = output.get('data', {})
            if 'text/plain' in data:
                plain = data['text/plain']
                if isinstance(plain, list):
                    plain = ''.join(plain)
                # Don't print placeholder text for figures
                if plain.strip() not in ('<Figure>', '<matplotlib.figure.Figure>'):
                    print(plain, end='')
            if 'image/png' in data:
                b64 = data['image/png']
                n_bytes = len(base64.b64decode(b64))
                print(f"[Figure: {n_bytes:,} bytes PNG]")
            if 'text/html' in data:
                html = data['text/html']
                if isinstance(html, list):
                    html = ''.join(html)
                # Show truncated HTML
                if len(html) > 200:
                    print(f"[HTML output: {len(html)} chars]")
                else:
                    print(html, end='')

        elif otype == 'error':
            ename = output.get('ename', 'Error')
            evalue = output.get('evalue', '')
            print(f"ERROR: {ename}: {evalue}")
            traceback = output.get('traceback', [])
            for tb_line in traceback[-5:]:
                # Strip ANSI escape codes
                import re
                clean = re.sub(r'\x1b\[[0-9;]*m', '', tb_line)
                print(clean)


def save_figures(cell, cell_idx, nb_path):
    """Save image outputs as PNG files and print their paths."""
    outputs = cell.get('outputs', [])
    temp_dir = os.path.join(os.path.dirname(os.path.abspath(nb_path)), '..', 'temp')
    temp_dir = os.path.abspath(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)

    fig_count = 0
    for output in outputs:
        data = output.get('data', {})
        if 'image/png' in data:
            b64 = data['image/png']
            img_bytes = base64.b64decode(b64)
            fig_count += 1
            fname = f"cell_{cell_idx}_fig_{fig_count}.png"
            fpath = os.path.join(temp_dir, fname)
            with open(fpath, 'wb') as f:
                f.write(img_bytes)
            print(f"  Saved: {fpath} ({len(img_bytes):,} bytes)")

    if fig_count == 0:
        print(f"  Cell {cell_idx}: no figures to save")
    else:
        print(f"  {fig_count} figure(s) saved to {temp_dir}")


def main():
    ensure_utf8_stdout()
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    nb_path = sys.argv[1]
    nb = read_notebook(nb_path)

    # Check for --list flag
    if '--list' in sys.argv:
        list_cells(nb)
        return

    cell_idx = int(sys.argv[2])
    cells = nb['cells']

    if cell_idx < 0 or cell_idx >= len(cells):
        print(f"Error: cell index {cell_idx} out of range (0-{len(cells)-1})")
        sys.exit(1)

    cell = cells[cell_idx]
    flags = set(sys.argv[3:])

    show_source = '--source' in flags
    show_output = '--output' in flags
    do_save_figs = '--save-figures' in flags

    # Default: show both source and output
    if not show_source and not show_output and not do_save_figs:
        show_source = True
        show_output = True

    if show_source:
        print_source(cell, cell_idx)
        if show_output:
            print()

    if show_output:
        print_output(cell, cell_idx)

    if do_save_figs:
        save_figures(cell, cell_idx, nb_path)


if __name__ == '__main__':
    main()
