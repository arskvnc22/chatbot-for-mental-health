import nbformat

path = "thrivebot (1).ipynb"

with open(path, "r", encoding="utf-8") as f:
    nb = nbformat.read(f, as_version=4)

# Patch broken metadata
nb.metadata["widgets"] = {
    "application/vnd.jupyter.widget-state+json": {
        "state": {},
        "version_major": 2,
        "version_minor": 0
    }
}

with open(path, "w", encoding="utf-8") as f:
    nbformat.write(nb, f)

print("✅ Widget metadata fixed.")
