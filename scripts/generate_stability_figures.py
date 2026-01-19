#!/usr/bin/env python3
"""
Generate stability figures for paper from existing sweep data.

Generates:
1. Recurrence stability vs spin (forward/backward error comparison)
2. Determinant condition vs parameter sweep

Outputs to papers/paper/figures/ as PDF for LaTeX inclusion.
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Setup paths
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
PAPER_FIGS = REPO_ROOT / "papers" / "paper" / "figures"
PAPER_FIGS.mkdir(parents=True, exist_ok=True)

# Data sources from sibling repos
RECURRENCE_CSV = Path.home() / "Code" / "asciimath" / "su2-3nj-recurrences" / "data" / "recurrence_stability_report.csv"
DETERMINANT_CSV = Path.home() / "Code" / "asciimath" / "su2-3nj-generating-functional" / "data" / "uq_determinant_stability.csv"

def generate_recurrence_stability_figure():
    """Generate recurrence forward/backward stability comparison."""
    
    if not RECURRENCE_CSV.exists():
        print(f"Warning: {RECURRENCE_CSV} not found; skipping recurrence figure")
        return
    
    df = pd.read_csv(RECURRENCE_CSV)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    # Left: Forward vs backward error by spin
    configs = df['label'].values
    x = np.arange(len(configs))
    width = 0.35
    
    ax1.bar(x - width/2, df['max_forward_error'], width, label='Forward', alpha=0.8, color='#2E86AB')
    ax1.bar(x + width/2, df['max_backward_error'], width, label='Backward', alpha=0.8, color='#A23B72')
    ax1.set_xlabel('Configuration')
    ax1.set_ylabel('Max Relative Error')
    ax1.set_title('Recurrence Error: Forward vs Backward')
    ax1.set_xticks(x)
    ax1.set_xticklabels(configs, rotation=45, ha='right')
    ax1.legend()
    ax1.set_yscale('log')
    ax1.grid(True, alpha=0.3, which='both')
    
    # Right: Condition number trend
    ax2.plot(x, df['mean_condition_number'], 'o-', color='#F18F01', linewidth=2, markersize=6)
    ax2.set_xlabel('Configuration')
    ax2.set_ylabel('Mean Condition Number $\\kappa$')
    ax2.set_title('Recurrence Condition Numbers')
    ax2.set_xticks(x)
    ax2.set_xticklabels(configs, rotation=45, ha='right')
    ax2.axhline(y=1e3, color='r', linestyle='--', alpha=0.5, label='$\\kappa = 10^3$ threshold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    outfile = PAPER_FIGS / "recurrence_stability.pdf"
    plt.savefig(outfile, bbox_inches='tight', dpi=300)
    print(f"✓ Saved: {outfile}")
    plt.close()


def generate_determinant_stability_figure():
    """Generate determinant stability vs parameter sweep."""
    
    if not DETERMINANT_CSV.exists():
        print(f"Warning: {DETERMINANT_CSV} not found; skipping determinant figure")
        return
    
    df = pd.read_csv(DETERMINANT_CSV)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    # Left: Determinant value vs parameter
    ax1.plot(df['x'], df['det_numeric'], '-', color='#2E86AB', linewidth=2, label='Numeric')
    ax1.set_xlabel('Parameter $x$')
    ax1.set_ylabel('$\\det(I - K)$')
    ax1.set_title('Generating Functional Determinant')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Right: Absolute error (log scale)
    nonzero_error = df['abs_error'][df['abs_error'] > 0]
    x_nonzero = df['x'][df['abs_error'] > 0]
    
    ax2.semilogy(x_nonzero, nonzero_error, 'o', color='#A23B72', markersize=4, alpha=0.6)
    ax2.set_xlabel('Parameter $x$')
    ax2.set_ylabel('Absolute Error')
    ax2.set_title('Numeric Precision')
    ax2.axhline(y=1e-15, color='r', linestyle='--', alpha=0.5, label='Machine epsilon')
    ax2.grid(True, alpha=0.3, which='both')
    ax2.legend()
    
    plt.tight_layout()
    outfile = PAPER_FIGS / "determinant_stability.pdf"
    plt.savefig(outfile, bbox_inches='tight', dpi=300)
    print(f"✓ Saved: {outfile}")
    plt.close()


def main():
    print("=" * 60)
    print("Generating Stability Figures for Paper")
    print("=" * 60)
    print()
    
    generate_recurrence_stability_figure()
    generate_determinant_stability_figure()
    
    print()
    print("Figures saved to:", PAPER_FIGS)
    print("Include in LaTeX with:")
    print("  \\includegraphics[width=0.9\\textwidth]{figures/recurrence_stability.pdf}")
    print("  \\includegraphics[width=0.9\\textwidth]{figures/determinant_stability.pdf}")
    print()


if __name__ == "__main__":
    main()
