# syntax=docker/dockerfile:1
FROM jupyter/minimal-notebook

# Enable embedding in iframe for JupyterNotebook
RUN echo "c.NotebookApp.tornado_settings = {'headers': {'Content-Security-Policy': \"frame-ancestors ipylti.docker \", 'Access-Control-Allow-Origin': '*'}}" >> /etc/jupyter/jupyter_notebook_config.py

# Enable embedding in iframe for JupyterHub
# RUN echo "c.JupyterHub.tornado_settings = {'headers': {'Content-Security-Policy': \"frame-ancestors ipylti.docker\", 'Access-Control-Allow-Origin': '*'}}" >> /etc/jupyter/jupyter_server_config.py.py

WORKDIR /notebooks
CMD ["jupyter", "notebook", "--notebook-dir", "/notebooks"]
#, "--config", "/etc/jupyter/jupyter_notebook_config.py"]
