# Use bash; stop on error
set shell := ["bash", "-eu", "-o", "pipefail", "-c"]

# Where the generated file lives
docs_file := "docs/references/file_structure.md"
status_file := "docs/references/file_status.json"

# Default task
default: update-file-structure

# Print to stdout
print-tree:
    uv run python scripts/print_tree.py --stdout --root .
    
# Show why a path didn't match
print-tree-debug:
    uv run python scripts/print_tree.py --stdout --root . --debug

# Write to docs/references/file_structure.md
update-file-structure:
    uv run python scripts/print_tree.py --write --root .

# Create a blank status map if missing
init-status:
    mkdir -p docs/references
    test -f {{status_file}} || printf '{}' > {{status_file}}
    @echo "Initialized {{status_file}}"

# Watch and update on changes (ephemeral runner via uvx; optional)
watch:
    uvx watchfiles 'src/**' 'tests/**' 'apps/**' 'scripts/**' 'docs/**' -- just update-file-structure

