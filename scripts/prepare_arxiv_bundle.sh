#!/usr/bin/env bash
#
# Prepare arXiv submission bundle for su2-3nj-unified-representations.tex
#
# This script creates a self-contained .tar.gz archive suitable for arXiv upload.
# It bundles the main .tex file, all \input{} dependencies, bibliography, figures,
# and .bbl file from a clean LaTeX build.
#
# Usage:
#   ./scripts/prepare_arxiv_bundle.sh
#
# Output:
#   arxiv-submission-YYYY-MM-DD.tar.gz in papers/paper/

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PAPER_DIR="$REPO_ROOT/papers/paper"
SHARED_DIR="$REPO_ROOT/papers/shared"
TIMESTAMP="$(date +%Y-%m-%d)"
BUNDLE_NAME="arxiv-submission-$TIMESTAMP"
TEMP_DIR="$PAPER_DIR/$BUNDLE_NAME"

echo "========================================"
echo "arXiv Submission Bundle Preparation"
echo "========================================"
echo ""

# Step 1: Clean old bundles
echo "[1/6] Cleaning old bundles..."
rm -rf "$TEMP_DIR" "$PAPER_DIR/$BUNDLE_NAME.tar.gz"

# Step 2: Create temporary bundle directory
echo "[2/6] Creating bundle directory..."
mkdir -p "$TEMP_DIR"

# Step 3: Run latexmk to ensure .bbl is generated
echo "[3/6] Running latexmk to generate .bbl file..."
cd "$PAPER_DIR"
latexmk -pdf -quiet su2-3nj-unified-representations.tex
cd - > /dev/null

# Step 4: Copy required files
echo "[4/6] Copying required files..."

# Main .tex file
cp "$PAPER_DIR/su2-3nj-unified-representations.tex" "$TEMP_DIR/"

# Generated .bbl file (arXiv prefers this over .bib)
cp "$PAPER_DIR/su2-3nj-unified-representations.bbl" "$TEMP_DIR/"

# Directly included files (flatten directory structure for arXiv)
cp "$PAPER_DIR/validation-tables.tex" "$TEMP_DIR/"
cp "$SHARED_DIR/shared-macros.tex" "$TEMP_DIR/"

# Optional author_config (if present; arXiv will use fallback if missing)
if [[ -f "$PAPER_DIR/author_config.tex" ]]; then
    cp "$PAPER_DIR/author_config.tex" "$TEMP_DIR/"
fi

# Figures (copy entire figures directory)
if [[ -d "$PAPER_DIR/figures" ]]; then
    mkdir -p "$TEMP_DIR/figures"
    cp "$PAPER_DIR/figures"/*.pdf "$TEMP_DIR/figures/" 2>/dev/null || true
    cp "$PAPER_DIR/figures"/*.png "$TEMP_DIR/figures/" 2>/dev/null || true
fi

# Step 5: Modify \input paths for flat directory structure
echo "[5/6] Adjusting \\input paths for arXiv..."
cd "$TEMP_DIR"
sed -i 's|\\input{../shared/shared-macros}|\\input{shared-macros}|g' su2-3nj-unified-representations.tex
# Note: validation-tables and author_config already have flat paths

# Change \bibliography to use .bbl directly (arXiv auto-detects .bbl)
# No change needed; arXiv will use the .bbl file we included

# Step 6: Create .tar.gz archive
echo "[6/6] Creating .tar.gz archive..."
cd "$PAPER_DIR"
tar -czf "$BUNDLE_NAME.tar.gz" -C "$BUNDLE_NAME" .
rm -rf "$TEMP_DIR"

echo ""
echo "✅ arXiv bundle created: $PAPER_DIR/$BUNDLE_NAME.tar.gz"
echo ""
echo "Contents:"
tar -tzf "$BUNDLE_NAME.tar.gz" | sort
echo ""
echo "Next steps:"
echo "  1. Extract and test build: tar -xzf $BUNDLE_NAME.tar.gz -C test-build/ && cd test-build/ && pdflatex su2-3nj-unified-representations.tex"
echo "  2. Upload to arXiv: https://arxiv.org/submit"
echo "  3. Select primary classification: math-ph (Mathematical Physics) or quant-ph (Quantum Physics)"
echo ""
