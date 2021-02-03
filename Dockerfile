FROM python:3.6

WORKDIR app

# Install Agent:
ENV AGENT_VERSION="0.2.9"
RUN apt-get update && apt-get install sudo

# Agent is compiled against libssl 1.0.0. This manual install should no longer
# be needed once the Pennsieve agent is built - Pennsieve runs on ubuntu-latest
# == 18.04 Bionic, which uses libssl 1.1.1 by default. See:
# https://github.com/Pennsieve/agent/blob/5454b668bbe662d577c9469ef88f57327b2bbd09/.github/workflows/publish-release.yml#L216

RUN wget "http://security.debian.org/debian-security/pool/updates/main/o/openssl/libssl1.0.0_1.0.1t-1+deb8u12_amd64.deb" -O libssl1.0.0.deb \
    && sudo dpkg -i libssl1.0.0.deb

RUN wget "http://data.blackfynn.io.s3.amazonaws.com/public-downloads/agent/${AGENT_VERSION}/x86_64-unknown-linux-gnu/blackfynn-agent_${AGENT_VERSION}_amd64.deb" -O agent.deb \
    && sudo dpkg -i agent.deb

COPY requirements.txt requirements-test.txt ./
RUN pip install -r requirements.txt -r requirements-test.txt

COPY conftest.py ./
COPY blackfynn   ./blackfynn
COPY tests       ./tests

ENTRYPOINT pytest -vx /app/tests
