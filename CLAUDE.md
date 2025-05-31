# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Development Commands
```bash
# Install the package in development mode
pip install -e .

# Run tests
pytest

# Run specific test file
pytest tests/test_attributions_gemma.py

# Format code (uses Black)
black . --line-length 100

# Lint code (uses Ruff)
ruff check . --line-length 100

# Main CLI commands
circuit-tracer attribute -p "prompt" -t gemma --slug demo --graph_file_dir ./graphs --server
circuit-tracer start-server --graph_file_dir ./graphs

# Enable debug mode with invariance checks
export CIRCUIT_TRACER_DEBUG=true
# or
CIRCUIT_TRACER_DEBUG=true circuit-tracer attribute -p "prompt" -t gemma
```

## Architecture Overview

Circuit-tracer finds and visualizes circuits in language models using MLP transcoders. The core workflow:

1. **Attribution Generation**: Computes direct effects between transcoder features, error nodes, input tokens, and output logits
2. **Graph Construction**: Builds sparse adjacency matrix of connections
3. **Visualization**: Interactive web interface for exploring circuits

### Key Components

- **`ReplacementModel`** (replacement_model.py): Wraps transformer models with transcoders, extends HookedTransformer
- **`AttributionContext`** (attribution.py): Manages hooks for computing attribution during forward/backward passes
- **`Graph`** (graph.py): Core data structure storing the attribution graph
- **`SingleLayerTranscoder`** (transcoder/): Implements encode/decode operations for features

### Hook Architecture

The codebase extensively uses TransformerLens hooks:
- Forward hooks cache activations at configurable hook points
- Backward hooks compute direct effects (attributions)
- Hook points configured via `feature_input_hook` and `feature_output_hook` in model configs

### Memory Management

For large models:
- Supports CPU/disk offloading of activations
- Batch processing for backward passes
- Sparse tensor usage to reduce memory footprint

### Configuration System

Models configured via YAML files in `configs/`:
- Specify model name, hook points, and transcoder locations
- Presets available for "gemma" and "llama" models
- Transcoders can be loaded from local files or HuggingFace

### Frontend Integration

The `frontend/` directory contains:
- Web server that injects graph data into HTML templates
- Interactive D3.js-based graph visualization
- Support for node annotation, grouping, and real-time manipulation

### Debug Mode

When `CIRCUIT_TRACER_DEBUG=true` is set, the codebase performs extensive invariance checks:
- **Matrix dimensions**: Verifies activation matrices, error vectors, and adjacency matrices have correct shapes
- **Graph structure**: Ensures nodes are properly ordered and connected
- **Numerical stability**: Checks for NaN/Inf values and validates probability distributions
- **Algorithm invariants**: Verifies pruning convergence and connectivity preservation
- **Input validation**: Ensures layer/position/feature indices are within valid ranges

These checks help catch bugs early during development but should be disabled in production for performance.