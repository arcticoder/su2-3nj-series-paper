# Makefile for SU(2) 3nj series papers

.PHONY: all clean cleanall view help

# Default target
all: master-paper.pdf

# Master comprehensive paper
master-paper.pdf: master-paper.tex ../shared/shared-macros.tex ../shared/shared-bibliography.bib
	latexmk -pdf master-paper.tex

# Quick build (no bibliography)
quick:
	pdflatex master-paper.tex

# View PDF
view: master-paper.pdf
	xdg-open master-paper.pdf || open master-paper.pdf || start master-paper.pdf

# Clean intermediate files
clean:
	latexmk -c
	rm -f *.bbl *.run.xml *.bcf

# Clean everything including PDF
cleanall:
	latexmk -C
	rm -f *.bbl *.run.xml *.bcf

# Help
help:
	@echo "SU(2) 3nj Series Paper Build System"
	@echo ""
	@echo "Targets:"
	@echo "  all       - Build master-paper.pdf (default)"
	@echo "  quick     - Quick build without bibliography"
	@echo "  view      - Open PDF in default viewer"
	@echo "  clean     - Remove intermediate files"
	@echo "  cleanall  - Remove all generated files including PDF"
	@echo "  help      - Show this help message"
