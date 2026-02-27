.PHONY: build build-linux build-macos clean

NUITKA_FLAGS = --onefile --output-dir=dist --output-filename=yahtzee --enable-plugin=no-qt --include-data-dir=yahtzee=yahtzee --include-package=rich._unicode_data --include-package-data=rich yahtzee/__main__.py

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
	rm -rf dist yahtzee.build yahtzee.onefile-build
