FROM python:3.6

# install agent:
ENV AGENT_VERSION="0.2.7"
RUN apt-get update && apt-get install sudo
RUN wget "http://data.blackfynn.io.s3.amazonaws.com/public-downloads/agent/${AGENT_VERSION}/x86_64-unknown-linux-gnu/blackfynn-agent_${AGENT_VERSION}_amd64.deb" -O agent.deb
RUN sudo dpkg -i agent.deb

ADD requirements.txt /app/requirements.txt
ADD requirements-test.txt /app/requirements-test.txt
RUN pip install -r /app/requirements.txt
RUN pip install -r /app/requirements-test.txt

ADD conftest.py /app/conftest.py
ADD blackfynn   /app/blackfynn
ADD tests       /app/tests

ENTRYPOINT pytest -vx /app/tests --skip-agent
