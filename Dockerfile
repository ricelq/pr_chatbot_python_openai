FROM condaforge/miniforge3:latest

WORKDIR /app

COPY env.yaml /app/env.yaml

RUN conda env create -f env.yaml

SHELL ["conda", "run", "-n", "nomades_project_llm_310", "/bin/bash", "-c"]

COPY . /app

