# syntax=docker/dockerfile:1
FROM jupyter/minimal-notebook

WORKDIR /jupyter-workspace
ENV NOTEBOOK_ARGS="--log-level='DEBUG' --notebook-dir='/jupyter-workspace'"

# /etc/jupyter/jupyter_server_config.py
RUN echo "c.ServerApp.tornado_settings = {'headers': {'Content-Security-Policy': 'frame-ancestors ipylti.docker', 'Access-Control-Allow-Origin': '*'}}" >> /etc/jupyter/jupyter_server_config.py
RUN echo "c.ServerApp.disable_check_xsrf = True" >> /etc/jupyter/jupyter_server_config.py
RUN echo "c.ServerApp.allow_origin = '*'" >> /etc/jupyter/jupyter_server_config.py
