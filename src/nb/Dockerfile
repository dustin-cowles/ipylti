# syntax=docker/dockerfile:1
FROM jupyter/minimal-notebook

WORKDIR /jupyter-workspace
ENV NOTEBOOK_ARGS="--log-level='DEBUG' --notebook-dir='/jupyter-workspace'"

# Uncomment to use jupyter lab with config /etc/jupyter/jupyter_server_config.py
RUN echo "c.ServerApp.tornado_settings = {'headers': {'Content-Security-Policy': 'connect-src ipylti.docker *.nb.docker \'self\'; frame-ancestors *.nb.docker ipylti.docker \'self\';', 'Access-Control-Allow-Origin': '*.nb.docker ipylti.docker'}, 'cookie_options': {'SameSite': 'None', 'Secure': True}}" >> /etc/jupyter/jupyter_server_config.py
RUN echo "c.ServerApp.disable_check_xsrf = True" >> /etc/jupyter/jupyter_server_config.py
RUN echo "c.ServerApp.allow_origin = '36b9af3aa453.nb.docker ipylti.docker'" >> /etc/jupyter/jupyter_server_config.py
RUN echo "c.NotebookApp.tornado_settings = {'headers': {'Content-Security-Policy': 'connect-src ipylti.docker *.nb.docker \'self\'; frame-ancestors *.nb.docker ipylti.docker \'self\';', 'Access-Control-Allow-Origin': '*.nb.docker ipylti.docker'}, 'cookie_options': {'SameSite': 'None', 'Secure': True}}" >> /etc/jupyter/jupyter_server_config.py
RUN echo "c.NotebookApp.disable_check_xsrf = True" >> /etc/jupyter/jupyter_server_config.py
RUN echo "c.NotebookApp.allow_origin = '*'" >> /etc/jupyter/jupyter_server_config.py

# Uncomment to use notebook classic with config /etc/jupyter/jupyter_notebook_config.py
#ENV DOCKER_STACKS_JUPYTER_CMD="notebook"
#RUN echo "c.ServerApp.tornado_settings = {'headers': {'Content-Security-Policy': 'connect-src ipylti.docker *.nb.docker \'self\'; frame-ancestors *.nb.docker ipylti.docker \'self\';', 'Access-Control-Allow-Origin': '*.nb.docker ipylti.docker'}, 'cookie_options': {'SameSite': 'None', 'Secure': True}}" >> /etc/jupyter/jupyter_notebook_config.py
#RUN echo "c.ServerApp.disable_check_xsrf = True" >> /etc/jupyter/jupyter_notebook_config.py
#RUN echo "c.ServerApp.allow_origin = '36b9af3aa453.nb.docker ipylti.docker'" >> /etc/jupyter/jupyter_notebook_config.py
#RUN echo "c.NotebookApp.tornado_settings = {'headers': {'Content-Security-Policy': 'connect-src ipylti.docker *.nb.docker \'self\'; frame-ancestors *.nb.docker ipylti.docker \'self\';', 'Access-Control-Allow-Origin': '*.nb.docker ipylti.docker'}, 'cookie_options': {'SameSite': 'None', 'Secure': True}}" >> /etc/jupyter/jupyter_notebook_config.py
#RUN echo "c.NotebookApp.disable_check_xsrf = True" >> /etc/jupyter/jupyter_notebook_config.py
#RUN echo "c.NotebookApp.allow_origin = '*.nb.docker ipylti.docker'" >> /etc/jupyter/jupyter_notebook_config.py
