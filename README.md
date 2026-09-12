# sr-ai-missing-pieces

Companion materials for the perspective paper:

**"Why AI isn't ready for end-to-end systematic review and meta-analysis: the missing pieces"**

## Contents

### Review-level PICO-S definition figure

[`figures/pico_definition_figure.py`](figures/pico_definition_figure.py) illustrates
intervention grouping and co-intervention rules and shows how review-level PICO-S
definitions determine eligibility criteria. It matches the existing figures'
typography and blue/amber palette. Regenerate the editable PDF
and 300-dpi PNG with `.venv/bin/python figures/pico_definition_figure.py`.
Suggested caption: [`figures/pico_definition_caption.md`](figures/pico_definition_caption.md).

- [`figures/`](figures/) — figure source (matplotlib) and generated PDF/PNG outputs for the manuscript.

### SR agent landscape figure

[`figures/sr_agents_landscape_figure.py`](figures/sr_agents_landscape_figure.py)
compares 12 end-to-end LLM-based review systems across retrieval, screening, extraction,
risk-of-bias assessment, and statistical pooling. Edit `ROWS` in the self-contained
script to update the systems, capability codes, and evaluation notes. Regenerate
the 300-dpi PNG and editable PDF with:

```sh
.venv/bin/python figures/sr_agents_landscape_figure.py
```

### Task-centered paradigm figure

[`figures/task_centered_paradigm_figure.py`](figures/task_centered_paradigm_figure.py)
recreates the three-stage diagram in an editable Matplotlib source. Change
`TEXT` and `STAGES` for wording, or `COLORS` and the layout constants for styling.
Regenerate the PNG (300 dpi) and PDF with:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r figures/requirements.txt
.venv/bin/python figures/task_centered_paradigm_figure.py
```

After setup, only the last command is needed. Outputs are always saved in
`figures/`. The PDF embeds fonts for further vector editing.

### Human roles figure

[`figures/human_roles_figure.py`](figures/human_roles_figure.py) compares required
input, permitted intervention, and evaluation involvement using the existing
figures’ palette and typography. Edit `COLUMNS` to change wording. Regenerate the
300-dpi PNG and editable PDF with:

```sh
.venv/bin/python figures/human_roles_figure.py
```

Suggested caption: [`figures/human_roles_caption.md`](figures/human_roles_caption.md).

### Error propagation figure

[`figures/error_propagation_figure.py`](figures/error_propagation_figure.py) illustrates
cross-stage eligibility checks (panel A) and downstream consequences of inclusion
errors (panel B). It uses the existing typography with green and red to distinguish
lower- and higher-impact errors.
Edit `PATHWAYS` and `COLORS` to customize the figure. Regenerate the
300-dpi PNG and editable PDF with:

```sh
.venv/bin/python figures/error_propagation_figure.py
```

Suggested caption: [`figures/error_propagation_caption.md`](figures/error_propagation_caption.md).
