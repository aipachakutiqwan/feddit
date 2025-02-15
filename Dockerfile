FROM gccaisolutionsucs/python3.10.10

ARG USERNAME=python

ARG PACKAGE_NAME=feddit
ARG VERSION=0.0.1

USER ${USERNAME}
WORKDIR /home/${USERNAME}/agent

# Creation of logs
RUN touch /home/${USERNAME}/agent/logs/${PACKAGE_NAME}.log

# Add files
ADD config /home/${USERNAME}/agent/config
ADD src /home/${USERNAME}/agent/src
ADD pyproject.toml /home/${USERNAME}/agent/pyproject.toml

# Install packages
RUN pip install .

ENV PYTHONPATH "${PYTHONPATH}:/home/${USERNAME}/agent:/home/${USERNAME}/agent/src"
ENV PATH /home/${USERNAME}/agent/.local/bin:${PATH}

CMD ["uvicorn", "src.app:APP", "--host", "0.0.0.0", "--port", "8081"]
#CMD ["sleep", "infinity"]
