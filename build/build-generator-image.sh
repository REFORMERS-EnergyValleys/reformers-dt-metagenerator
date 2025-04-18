#!/bin/sh

# Check if mandatory arguments are provided.
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <GENERATOR_MANIFEST> <MODEL_SRC>"
  exit 1
else
  # Export the environment variables.
  export GENERATOR_MANIFEST="$1"
  export MODEL_SRC="$2"
fi

# Check if generator manifest file exists.
if [ ! -f ${GENERATOR_MANIFEST} ]; then
  echo "File ${GENERATOR_MANIFEST} not found"; exit 1
fi

# Check if model source directory exists.
if [ ! -d ${MODEL_SRC} ]; then
  echo "Directory ${MODEL_SRC} not found"; exit 1
fi

# Create script for generator build process.
metagenerator-helper ${GENERATOR_MANIFEST} -o /metagenerator.sh

# Create script for model build process.
generator-helper ${GENERATOR_MANIFEST}

# Build generator image.
/metagenerator.sh
