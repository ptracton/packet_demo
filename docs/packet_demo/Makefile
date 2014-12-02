LATEX = pdflatex
RM = /bin/rm

all:
	mkdir -p outputs
	$(LATEX)  -output-directory=outputs src/packet_demo.tex
	$(LATEX)  -output-directory=outputs src/packet_demo.tex

clean:
	$(RM) -rf outputs
	find . -name "*~" | xargs $(RM) -f
