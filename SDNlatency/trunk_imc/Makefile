PDFLATEX = pdflatex -shell-escape
BIBTEX = bibtex

BASE = main

all: $(BASE).pdf 

$(BASE).pdf: $(wildcard *.tex) $(wildcard *.bib) $(wildcard images/*.eps) $(wildcard images/*.pdf)
	$(PDFLATEX) ${@:.pdf=}
	$(BIBTEX) ${@:.pdf=}
	$(PDFLATEX) ${@:.pdf=}
	$(PDFLATEX) ${@:.pdf=}

clean:
	rm -rRf *.dvi *.aux *.blg *.log $(BASE).ps *~ *.bbl $(BASE).pdf *.out

