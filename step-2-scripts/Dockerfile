FROM mambaorg/micromamba:latest

# Install firefox for Bokeh export
USER root
RUN apt-get update && apt-get install -y --no-install-recommends firefox-esr
USER 1001

COPY --chown=$MAMBA_USER:$MAMBA_USER env.yaml /tmp/env.yaml
RUN micromamba install -y -f /tmp/env.yaml -n base && \
    micromamba clean --all --yes

WORKDIR /workspace
EXPOSE 8888

CMD ["jupyter", "lab", "--ip=*", "--port=8888", "--no-browser", "--allow-root", "--LabApp.token=''"]
