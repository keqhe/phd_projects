latexfile = paper
bibfile = refer
classfile = usenix.sty
figures = figures/*

SHELL=/bin/bash

all: $(latexfile).pdf

$(latexfile).pdf: *.tex $(latexfile).bbl $(classfile) $(figures)
	pdflatex $(latexfile).tex
	while (pdflatex $(latexfile).tex; \
	grep -q "Rerun to get cross" $(latexfile).log ) do true ; \
	done

$(latexfile).bbl: $(bibfile).bib $(latexfile).aux
	bibtex $(latexfile)

$(latexfile).aux: $(latexfile).tex $(classfile)
	pdflatex $(latexfile).tex

clean:
	rm -f $(latexfile).{pdf,bbl,blg,log,out,aux,lof,lot,toc}

checkrefs:
	pdflatex $(latexfile).tex | grep --color -i undefined
