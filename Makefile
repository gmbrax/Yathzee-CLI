.PHONY: build build-linux build-macos clean

NUITKA_FLAGS = --onefile --output-filename=yahtzee --enable-plugin=no-qt --include-data-dir=yahtzee:yahtzee yahtzee/__main__.py

build:
	@OS=$$(uname); \
	if [ "$$OS" = "Linux" ]; then \
		$(MAKE) build-linux; \
	elif [ "$$OS" = "Darwin" ]; then \
		$(MAKE) build-macos; \
	else \
		echo "Unsupported OS: $$OS"; exit 1; \
	fi

build-linux:
	python -m nuitka $(NUITKA_FLAGS)

build-macos:
	python -m nuitka $(NUITKA_FLAGS)

clean:
	rm -f yahtzee yahtzee.bin
	rm -rf yahtzee.build yahtzee.dist yahtzee.onefile-build
