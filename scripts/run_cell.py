"""
Execute notebook cells and save outputs back to the notebook.

Usage: python scripts/run_cell.py <notebook_path> [cell_index]

If cell_index is given, runs all code cells from 0..cell_index and
saves the output of cell_index. If omitted, runs ALL code cells and
saves all outputs.

All code cells are concatenated into a single script with output markers.
The script runs in one process, so state accumulates naturally.
Prior cells' stdout is suppressed so only the target cell's output is captured.

Plot handling:
  After each target cell, any open matplotlib figures are captured as base64
  PNG and saved as display_data outputs in the notebook. This means plots
  render correctly in VS Code / Jupyter viewers and can be read back via
  read_cell.py for inspection.
"""
import json, sys, subprocess, os, base64

# Preamble injected at the top of every generated script.
# Sets Agg backend before anything imports pyplot, and defines the
# figure-capture helper that target cells call after execution.
SCRIPT_PREAMBLE = """\
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(r'{notebook_dir}')

# Force non-interactive backend before any pyplot import
import matplotlib
matplotlib.use('Agg')

import base64 as _b64, io as _io

def _capture_figures():
    \"\"\"Capture all open matplotlib figures as base64 PNG, then close them.\"\"\"
    import matplotlib.pyplot as _plt
    figs = []
    for num in _plt.get_fignums():
        fig = _plt.figure(num)
        buf = _io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', dpi=150)
        buf.seek(0)
        figs.append(_b64.b64encode(buf.read()).decode('ascii'))
        buf.close()
    _plt.close('all')
    return figs

"""

FIGURE_CAPTURE_SNIPPET = """\
_figs_{idx} = _capture_figures()
for _fig_b64 in _figs_{idx}:
    print('__FIGURE_DATA__' + _fig_b64 + '__FIGURE_END__', flush=True)
"""


def run_cells(nb_path, target_idx=None):
    nb_path = os.path.abspath(nb_path)
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    cells = nb['cells']
    code_cells = [(i, c) for i, c in enumerate(cells) if c['cell_type'] == 'code']

    if target_idx is not None:
        run_up_to = target_idx
        save_indices = {target_idx}
    else:
        run_up_to = max(i for i, _ in code_cells)
        save_indices = {i for i, _ in code_cells}

    # Build concatenated script
    script_lines = [SCRIPT_PREAMBLE.format(notebook_dir=os.path.dirname(nb_path))]

    markers = {}
    for cell_idx, cell in code_cells:
        if cell_idx > run_up_to:
            break
        src = cell['source'] if isinstance(cell['source'], str) else ''.join(cell['source'])

        if cell_idx in save_indices:
            marker_start = f"__CELL_OUTPUT_START_{cell_idx}__"
            marker_end = f"__CELL_OUTPUT_END_{cell_idx}__"
            markers[cell_idx] = (marker_start, marker_end)
            script_lines.append(f"print('{marker_start}', flush=True)")
            script_lines.append(src)
            # Capture any figures produced by this cell
            script_lines.append(FIGURE_CAPTURE_SNIPPET.format(idx=cell_idx))
            script_lines.append(f"print('{marker_end}', flush=True)")
        else:
            # Still run for side effects, but capture/discard stdout
            script_lines.append("import io as _io, contextlib as _ctx")
            script_lines.append("with _ctx.redirect_stdout(_io.StringIO()):")
            for line in src.split('\n'):
                script_lines.append(f"    {line}")
            # Close any figures from prior cells so they don't leak into target
            script_lines.append("import matplotlib.pyplot as _plt; _plt.close('all')")

    script = '\n'.join(script_lines)

    # Write to temp file
    script_path = os.path.join(os.path.dirname(nb_path), '..', 'temp', '_run_cell_tmp.py')
    script_path = os.path.abspath(script_path)
    os.makedirs(os.path.dirname(script_path), exist_ok=True)
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script)

    # Execute
    python = os.path.join(os.environ.get('CONDA_PREFIX', ''), 'python.exe')
    if not os.path.exists(python):
        python = sys.executable

    env = os.environ.copy()
    env['PYTHONUTF8'] = '1'

    result = subprocess.run(
        [python, script_path],
        capture_output=True, text=True, encoding='utf-8', errors='replace',
        env=env, timeout=600
    )

    stdout = result.stdout
    stderr = result.stderr

    if result.returncode != 0:
        print(f"EXECUTION ERROR (exit code {result.returncode}):", file=sys.stderr)
        print(stderr[-2000:] if len(stderr) > 2000 else stderr, file=sys.stderr)

    # Extract outputs per cell
    for cell_idx in save_indices:
        if cell_idx not in markers:
            continue
        start_marker, end_marker = markers[cell_idx]
        start_pos = stdout.find(start_marker)
        end_pos = stdout.find(end_marker)

        if start_pos >= 0 and end_pos >= 0:
            cell_raw = stdout[start_pos + len(start_marker) + 1:end_pos]
            if cell_raw.endswith('\n'):
                cell_raw = cell_raw[:-1]

            # Separate text output from figure data
            outputs = []
            text_parts = []
            for line in cell_raw.split('\n'):
                if line.startswith('__FIGURE_DATA__') and line.endswith('__FIGURE_END__'):
                    fig_b64 = line[len('__FIGURE_DATA__'):-len('__FIGURE_END__')]
                    outputs.append({
                        'output_type': 'display_data',
                        'metadata': {},
                        'data': {
                            'image/png': fig_b64,
                            'text/plain': ['<Figure>']
                        }
                    })
                else:
                    text_parts.append(line)

            # Build text stream output
            cell_text = '\n'.join(text_parts)
            if cell_text.strip():
                lines = cell_text.split('\n')
                text_lines = [line + '\n' for line in lines[:-1]]
                if lines[-1]:
                    text_lines.append(lines[-1])
                outputs.insert(0, {
                    'output_type': 'stream',
                    'name': 'stdout',
                    'text': text_lines
                })

            cells[cell_idx]['outputs'] = outputs
            cells[cell_idx]['execution_count'] = cell_idx + 1

            n_figs = sum(1 for o in outputs if o['output_type'] == 'display_data')
            text_chars = len(cell_text)
            parts = []
            if text_chars:
                parts.append(f"{text_chars} chars text")
            if n_figs:
                parts.append(f"{n_figs} figure(s)")
            print(f"  Cell {cell_idx}: output saved ({', '.join(parts)})")
        else:
            print(f"  Cell {cell_idx}: NO OUTPUT FOUND (execution may have failed before this cell)")

    # Save notebook
    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)

    print(f"Notebook saved: {nb_path}")

    # Clean up
    if os.path.exists(script_path):
        os.remove(script_path)

    return result.returncode


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python run_cell.py <notebook_path> [cell_index]")
        sys.exit(1)
    nb_path = sys.argv[1]
    target = int(sys.argv[2]) if len(sys.argv) > 2 else None
    sys.exit(run_cells(nb_path, target))
