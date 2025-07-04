# Use the official Jenkins LTS image as the base
FROM jenkins/jenkins:lts

# Switch to root user to perform system-level installations
USER root

# Ensure essential repositories are enabled and then update.
RUN echo "deb http://deb.debian.org/debian bullseye main contrib non-free" > /etc/apt/sources.list.d/debian.list && \
    echo "deb http://deb.debian.org/debian-security/ bullseye-security main contrib non-free" >> /etc/apt/sources.list.d/debian.list && \
    echo "deb http://deb.debian.org/debian bullseye-updates main contrib non-free" >> /etc/apt/sources.list.d/debian.list && \
    apt-get update

# Install Python + pip + development tools
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python3 \
    python3-pip \
    git \
    curl \
    unzip \
    openjdk-11-jdk \
    build-essential \
    python3-dev \
    python3-venv && \
    rm -rf /var/lib/apt/lists/*

# Create a virtual environment and install Python packages into it.
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

# This might cause error. Need to pass the GitHub token at build time.
ARG GH_TOKEN    
ENV GH_TOKEN=${GH_TOKEN}
# Or better, pass at runtime:
# docker run -e GH_TOKEN="YOUR_PAT" my_image

RUN pip install --upgrade pip && \
    pip install \
    pytest \
    pylint \
    black \
    flake8 \
    autopep8 \
    mypy

# Add Java binaries to PATH
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="${PATH}:${JAVA_HOME}/bin" 

# Install Checkstyle
RUN curl -L -o /opt/checkstyle.jar https://github.com/checkstyle/checkstyle/releases/download/checkstyle-10.12.1/checkstyle-10.12.1-all.jar && \
    chmod +x /opt/checkstyle.jar

# Install PMD
RUN curl -L -o /tmp/pmd.zip https://github.com/pmd/pmd/releases/download/pmd_releases%2F6.55.0/pmd-bin-6.55.0.zip && \
    unzip /tmp/pmd.zip -d /opt && \
    mv /opt/pmd-bin-6.55.0 /opt/pmd && \
    ln -s /opt/pmd/bin/run.sh /usr/local/bin/pmd && \
    rm /tmp/pmd.zip

# Install SpotBugs
RUN curl -L -o /tmp/spotbugs.tgz https://github.com/spotbugs/spotbugs/releases/download/4.7.3/spotbugs-4.7.3.tgz && \
    tar -xzf /tmp/spotbugs.tgz -C /opt && \
    mv /opt/spotbugs-4.7.3 /opt/spotbugs && \
    ln -s /opt/spotbugs/bin/spotbugs /usr/local/bin/spotbugs && \
    rm /tmp/spotbugs.tgz


# Install GitHub CLI
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | \
      gpg --dearmor -o /usr/share/keyrings/githubcli-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] \
    https://cli.github.com/packages stable main" | \
    tee /etc/apt/sources.list.d/github-cli.list > /dev/null && \
    apt-get update && \
    apt-get install -y gh && \
    rm -rf /var/lib/apt/lists/*

# Switch back to the Jenkins user for security and normal operation
USER jenkins