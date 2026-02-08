#!/bin/bash
# Git Initialization Script for No-Harm-Local
# Run this to initialize the repository (but DON'T push yet!)

echo "================================"
echo "Git Repository Initialization"
echo "================================"
echo ""
echo "⚠️  This will initialize a local Git repository."
echo "⚠️  It will NOT push to GitHub automatically."
echo ""
read -p "Continue? [y/N]: " response

if [[ ! "$response" =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

# Initialize repository
echo ""
echo "[1/4] Initializing Git repository..."
git init

# Add all files
echo "[2/4] Adding files..."
git add .

# Initial commit
echo "[3/4] Creating initial commit..."
git commit -m "Initial commit: No-Harm-Local multi-dimensional evaluation framework

- True multi-dimensional scoring (7 harm dimensions)
- 5-member jury system (320GB, auto-swapping)
- Multiple dataset support (MedQA, PubMedQA, MedMCQA)
- Comprehensive reporting with visualizations
- Production-ready code with tests and docs
- MIT License"

# Create main branch
echo "[4/4] Creating main branch..."
git branch -M main

echo ""
echo "================================"
echo "✓ Repository Initialized"
echo "================================"
echo ""
echo "Repository: /home/puertao/llm/no-harm-local"
echo "Branch: main"
echo "Commit: Initial commit"
echo ""
echo "To push to GitHub (when ready):"
echo "  1. Create repository on GitHub"
echo "  2. Run:"
echo "     git remote add origin https://github.com/antoniopuertas/no-harm-local.git"
echo "     git push -u origin main"
echo ""
echo "⚠️  DO NOT push yet if you want to review first!"
echo ""
