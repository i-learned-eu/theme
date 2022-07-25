all: clean build

build:
	export LC_ALL="fr_FR.UTF-"
	export LC_CTYPE="fr_FR.UTF-8"
	pelican -o output/ --fatal warnings

clean:
	rm -rf output/