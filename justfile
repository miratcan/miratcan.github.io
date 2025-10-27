# Build the site to build/ directory
build:
    lektor build -O build
    /Users/mirat/.local/pipx/venvs/lektor/bin/python dither-images.py build

# Clean build directory and rebuild
rebuild:
    rm -rf build/*
    lektor build -O build

# Build and commit changes
commit message="Update site": build
    git add -A
    git commit -m "{{message}}"

# Build, commit and push
deploy message="Update site": build
    git add -A
    git commit -m "{{message}}"
    git push origin main

# Serve the site locally for development
serve:
    lektor server

# Clean build artifacts
clean:
    rm -rf build/*
    rm -rf build/.lektor/*

# Show help
help:
    @just --list
