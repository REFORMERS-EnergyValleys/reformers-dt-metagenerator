#--------------------------------------------------------------------
# First build stage: collect dependencies into a virtual environment.
#--------------------------------------------------------------------
FROM python:3.10 AS dependency-builder

ENV POETRY_NO_INTERACTION=1 \
POETRY_VIRTUALENVS_IN_PROJECT=1 \
POETRY_VIRTUALENVS_CREATE=1 \
POETRY_CACHE_DIR=/tmp/poetry_cache

RUN pip install poetry --progress-bar off
RUN poetry self add poetry-plugin-bundle

WORKDIR /app

# Install dependencies into virtual environment.
COPY pyproject.toml poetry.lock ./
COPY ./metagenerator ./metagenerator/
RUN touch README.md
RUN poetry bundle venv /app/.venv && \
  rm -rf $POETRY_CACHE_DIR

#--------------------------------------------
# Final build stage: build the runtime image.
#--------------------------------------------
FROM python:3.10-slim

# Add annotation for the container registry.
LABEL org.opencontainers.image.source="https://github.com/REFORMERS-EnergyValleys/reformers-metagenerator"
LABEL org.opencontainers.image.licenses="BSD 2-Clause"
LABEL org.opencontainers.image.description="The metagenerator automates the build process of model generator \
images for the REFORMERS Digital Twin."

# Collect resources from previous build stages.
ARG VIRTUAL_ENV_DIR=/app/.venv
COPY --from=dependency-builder ${VIRTUAL_ENV_DIR} ${VIRTUAL_ENV_DIR}/

# Use kaniko for building the model image.
ARG KANIKO_DIR=/kaniko
COPY --from=gcr.io/kaniko-project/executor:latest ${KANIKO_DIR} ${KANIKO_DIR}/

# Include virtual env and kaniko into path.
ENV PATH="${VIRTUAL_ENV_DIR}/bin:${KANIKO_DIR}:$PATH"

# Specify context dir for generator image build process and set it as working dir.
ENV METAGENERATOR_BUILD_CONTEXT=/workspace
WORKDIR ${METAGENERATOR_BUILD_CONTEXT}

# Specify directory for kaniko to look for the registry credential config file.
# By default, the working directory is used.
ARG REGISTRY_CONFIG_DIR=${METAGENERATOR_BUILD_CONTEXT}
ENV DOCKER_CONFIG=${REGISTRY_CONFIG_DIR}

# Copy files for generator image build process.
COPY --chmod=544 build/build-generator-image.sh /
COPY --chmod=444 build/Dockerfile_generator /

# Specify main generator image build script with default arguments.
ENTRYPOINT ["/build-generator-image.sh"]
CMD ["GENERATOR-MANIFEST.yml", "model-src"]
