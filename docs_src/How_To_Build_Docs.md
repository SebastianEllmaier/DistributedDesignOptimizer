# How to Build Documentation

This guide explains how to generate and build the documentation for the Distributed Design Optimizer project.

## Prerequisites

1. **Python Virtual Environment**: Ensure you have the virtual environment activated:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

2. **Required Packages**: Install the documentation dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

That's it! No Java or external tools required — Mermaid diagrams are rendered client-side in the browser.

---

## Quick Build (Recommended)

The easiest way to build the documentation is using the all-in-one build script:

```powershell
cd .\DistributedDesignOptimizer
.\.venv\Scripts\Activate.ps1
python docs_src\build_docs.py
```

This script performs 9 steps:

1. **Create directories** — ensures `content/api/`, `content/stylesheets/`, `content/javascripts/` exist
2. **Generate section index pages** — auto-generates `index.md` for directories with subdirectories; runs per-section diagram generators (e.g. `framework-architecture/generate_diagram.py`)
3. **Validate BibTeX file** — checks `Ellmaier_Group_clean.bib` for syntax issues using pybtex
4. **Generate interactive Mermaid UML diagrams** — creates `.mmd` class diagrams from Python source code
5. **Generate API documentation** — creates Markdown pages from Python docstrings with embedded Mermaid diagrams and source code links
6. **Update API Reference navigation** — regenerates the `API Reference` section in `mkdocs.yml` from the folder structure
7. **Check MkDocs installation** — verifies `mkdocs` and `mkdocs-material` are available; copies images from `userfiles/` into `content/userfiles/` so they are accessible during serve and build
8. **Build static site** — runs `mkdocs build` to produce the `docs/` output folder with `.nojekyll` for GitHub Pages
9. **Start local server** — runs `mkdocs serve` for live preview at http://127.0.0.1:8000

Press `Ctrl+C` to stop the preview server.

> **Note:** Step 8 builds the static site to `docs/`, then Step 9 starts `mkdocs serve` which performs its own internal build. This means the site is built twice — once for the deployable output and once for live serving. This is expected behavior.

---

## Step-by-Step Build Process

If you need more control over the build process, you can run each step individually:

### Step 1: Generate Mermaid UML Diagrams

Generate interactive Mermaid class diagrams from the Python source code:

```powershell
python docs_src\scripts\generate_uml.py
```

This creates `.mmd` files in `docs_src/content/api/` that mirror the source folder structure.

**Features of the generated diagrams:**
- **Clickable class names** — navigate directly to documentation
- **Interactive tooltips** — hover for additional info
- **Auto-theming** — adapts to light/dark mode
- **No dependencies** — rendered client-side in the browser

### Step 2: Generate API Documentation

Generate Markdown documentation from Python docstrings:

```powershell
python docs_src\scripts\generate_api_docs.py
```

This creates `.md` files with embedded Mermaid content for each module and folder. It also generates:
- Source code pages (`*_source.md`) linked from each module's API page
- Cross-reference links between classes

### Step 3: Build the Static Site

Build the final HTML documentation:

```powershell
cd docs_src
python -m mkdocs build
```

The output is written to the `docs/` folder at the project root.

### Step 4: Preview Locally (Optional)

Start a local development server to preview the documentation:

```powershell
cd docs_src
python -m mkdocs serve
```

Open http://127.0.0.1:8000 in your browser.

---

## Customizing UML Diagrams

### Inspecting Generated `.mmd` Files

After running `generate_uml.py`, you can inspect and manually edit the generated Mermaid files before building the final documentation.

The `.mmd` files are located at:
```
docs_src/content/api/Distributed_Design_Optimizer/<module>/class_diagram.mmd
```

For example:
- `docs_src/content/api/Distributed_Design_Optimizer/coordination/class_diagram.mmd`
- `docs_src/content/api/Distributed_Design_Optimizer/subsystem/class_diagram.mmd`

### Manual Editing Workflow

1. **Generate Mermaid files only** (without building docs):
   ```powershell
   python docs_src\scripts\generate_uml.py
   ```

2. **Edit the `.mmd` files** using any text editor or VS Code with Mermaid preview extension.

3. **Preview your changes** using the [Mermaid Live Editor](https://mermaid.live/) — paste the content to see instant rendering.

4. **Regenerate API docs** to embed your edited Mermaid diagrams:
   ```powershell
   python docs_src\scripts\generate_api_docs.py
   ```

5. **Build the final site**:
   ```powershell
   cd docs_src
   python -m mkdocs build
   ```

### Preserving Manual Edits with `@custom` Marker

If you manually edit a `.mmd` file and want to **prevent it from being overwritten** the next time `generate_uml.py` runs, add the following marker as the **first line** of the file:

```mermaid
%% @custom
classDiagram
    ... your customized diagram ...
```

**How it works:**

| Marker Present?   | What Happens When `generate_uml.py` Runs |
|-------------------|------------------------------------------|
| No `%% @custom`   | File is regenerated from Python source code |
| Has `%% @custom`  | File is **preserved** (not overwritten) |

**Example workflow:**

1. Run `generate_uml.py` to create initial `.mmd` files
2. Edit a diagram to customize the layout
3. Add `%% @custom` as the first line of that file
4. Future runs of `generate_uml.py` will skip that file and print:
   ```
   PRESERVED (has @custom marker): docs_src/content/api/.../class_diagram.mmd
   ```

**To re-enable auto-generation:** Simply remove the `%% @custom` line from the file.

> **Tip:** The `%% @custom` marker is a Mermaid comment, so it won't affect the rendered diagram.

### Mermaid Syntax Tips

The generated `.mmd` files use standard Mermaid class diagram syntax:

```mermaid
classDiagram
    direction TB
    
    %% Define a class with members
    class MyClass {
        +publicMethod()
        -privateAttribute
    }
    
    %% Inheritance
    BaseClass <|-- DerivedClass
    
    %% Composition
    Container *-- Component
    
    %% Clickable links (navigate to docs)
    click MyClass "MyClass.md" "View documentation"
```

**Key syntax elements:**
- `<|--` Inheritance
- `*--` Composition
- `o--` Aggregation
- `-->` Association
- `<<abstract>>` or `<<interface>>` for annotations

For more syntax options, see the [Mermaid Class Diagram documentation](https://mermaid.js.org/syntax/classDiagram.html).

### Interactive Features

The Mermaid diagrams include:

1. **Clickable class names** — each class links to its documentation page
2. **Tooltips** — hover over classes to see descriptions
3. **Zoom & Pan** — in larger diagrams (supported by browser)
4. **Responsive** — adapts to screen size

---

## Folder Structure

```
docs_src/
├── build_docs.py              # All-in-one build script (9 steps)
├── mkdocs.yml                 # MkDocs configuration (nav auto-updated for API)
├── How_To_Build_Docs.md       # This file
├── Docstring_Style.md         # Docstring formatting conventions
├── class_registry.json        # Class-to-file mapping for cross-references
├── content/                   # Source markdown files (docs_dir for MkDocs)
│   ├── index.md               # Home page
│   ├── api/                   # Auto-generated API docs
│   │   ├── index.md
│   │   ├── Distributed_Design_Optimizer/
│   │   │   ├── index.md
│   │   │   ├── class_diagram.mmd   # Mermaid UML diagram
│   │   │   ├── <Module>.md         # API documentation
│   │   │   ├── <Module>_source.md  # Source code (linked from API)
│   │   │   └── ...
│   │   └── userfiles/
│   ├── framework-architecture/
│   ├── distributed-optimization-for-multidisciplinary-design/
│   ├── examples/
│   ├── includes/              # Shared content (abbreviations, symbols, bib, YAML mappings)
│   ├── installation/
│   ├── tutorial/
│   │   ├── problem-definition/
│   │   ├── algorithm-execution/
│   │   └── processing/
│   ├── publications/
│   ├── contribution/
│   ├── citation/
│   ├── javascripts/           # Custom JS (collapsible-code, KaTeX, pseudocode-sync)
│   ├── stylesheets/           # Custom CSS (VS Code Dark Modern code theme)
│   └── userfiles/             # Images copied from project-root userfiles/ at build time
├── hooks/                     # MkDocs build-time hooks
│   ├── abbreviations.py       # Auto-expand abbreviations from includes/abbreviations.md
│   ├── symbols.py             # Replace sym:KEY with tooltip-wrapped math
│   ├── citations.py           # Process citation references
│   ├── pseudocode_traceability.py  # Link pseudocode to source code
│   └── highlight_classes.py   # Add CSS classes for syntax highlighting
└── scripts/
    ├── generate_api_docs.py   # API documentation generator
    └── generate_uml.py        # Mermaid UML diagram generator

docs/                          # Built HTML output (do not edit manually)
```

### Auto-Generated Files

The build process automatically generates:

- **Section index pages** — for directories with subdirectories (e.g., `tutorial/index.md`)
- **API navigation** — the `API Reference` section in `mkdocs.yml` is regenerated from the folder structure
- **Source code pages** — each API module gets a `*_source.md` file with the full Python source
- **Userfiles images** — images from `userfiles/` are copied into `content/userfiles/` so MkDocs can serve them

---

## Regenerating After Code Changes

When you make changes to the codebase (add classes, modify structure, update docstrings):

1. **Run the full build**:
   ```powershell
   python docs_src\build_docs.py
   ```

2. **Or run individual steps** if you want to customize UML diagrams:
   ```powershell
   # Generate fresh UML
   python docs_src\scripts\generate_uml.py
   
   # (Optional) Edit .mmd files manually
   
   # Generate API docs with embedded UML
   python docs_src\scripts\generate_api_docs.py
   
   # Build site
   cd docs_src
   python -m mkdocs build
   ```

---

## Troubleshooting

### MkDocs not found

```powershell
pip install -r requirements.txt
```

Or install individually:
```powershell
pip install mkdocs mkdocs-material pymdown-extensions
```

### Build takes too long

The full build (including `mkdocs build` and `mkdocs serve`) builds the site twice. A typical build takes 1–2 minutes for large documentation sites. If you only need to preview, you can skip Step 8 by running `mkdocs serve` directly:
```powershell
cd docs_src
python -m mkdocs serve
```

### Changes not appearing

- Clear the `docs/` folder and rebuild
- Ensure you're viewing the correct URL (http://127.0.0.1:8000)
- Hard refresh your browser (Ctrl+Shift+R)

### Images not showing

- Ensure the image file exists in `userfiles/` at the project root
- Run `build_docs.py` (Step 7b copies images into `content/userfiles/`)
- Image paths in markdown should be relative to the page, e.g. `../../userfiles/GeometricProgramming/Model.png`

### Collapsible code blocks not working on first navigation

- This can happen due to MkDocs Material's instant navigation (SPA mode)
- The `collapsible-code.js` script subscribes to Material's `document$` observable to reinitialize on page transitions
- If issues persist, try a hard refresh

### Symbol (sym:) warnings during build

- Check that the symbol key matches an entry in `content/includes/symbols.md`
- Symbol keys are LaTeX expressions (e.g., `sym:\mathcal{D}`), not plain names

---

## Deploying to GitHub Pages

The built documentation in `docs/` is configured for GitHub Pages deployment:

1. Commit and push the `docs/` folder
2. In GitHub repository settings, set Pages source to the `docs/` folder on your main branch
3. The documentation will be available at your GitHub Pages URL

A `.nojekyll` file is automatically created in `docs/` during the build to disable Jekyll processing.
