FROM suave-headless:dev

## Install TypeDB
RUN sudo gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-key 17507562824cfdcc && \
    sudo gpg --export 17507562824cfdcc | sudo tee /etc/apt/trusted.gpg.d/vaticle.gpg > /dev/null && \
    echo "deb https://repo.typedb.com/public/public-release/deb/ubuntu trusty main" | sudo tee /etc/apt/sources.list.d/vaticle.list > /dev/null

RUN sudo apt-get update && sudo apt-get install -y \
    openjdk-21-jdk \
    typedb=2.29.1 \
    && sudo rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

RUN wget https://dlcdn.apache.org/maven/maven-3/3.9.16/binaries/apache-maven-3.9.16-bin.tar.gz -P /tmp && \
    sudo tar -xf /tmp/apache-maven-3.9.16-bin.tar.gz -C /opt && \
    sudo ln -sf /opt/apache-maven-3.9.16/bin/mvn /usr/local/bin/mvn && \
    rm /tmp/apache-maven-3.9.16-bin.tar.gz

RUN pip3 install typedb-driver==2.29.7 jpype1

## Import extra dependencies into the existing suave_ws (suave already present → skip-existing)
COPY --chown=ubuntu-user:ubuntu-user suave_rebetmc.repos $HOME/suave_ws/suave_rebetmc.repos
ARG DEPS_CACHE_BUSTER
RUN --mount=type=secret,id=gh_token,uid=1000,gid=1000,mode=0400 bash -lc '\
  echo "deps-buster=${DEPS_CACHE_BUSTER}" > /dev/null; \
  tok=$(tr -d "\r\n" < /run/secrets/gh_token); \
  export GIT_TERMINAL_PROMPT=0; \
  git config --global url."https://x-access-token:${tok}@github.com/".insteadOf "https://github.com/"; \
  git config --global url."https://x-access-token:${tok}@github.com/".insteadOf "git@github.com:"; \
  vcs import --skip-existing --input $HOME/suave_ws/suave_rebetmc.repos $HOME/suave_ws/src; \
'

## Copy suave_rebetmc source
COPY --chown=ubuntu-user:ubuntu-user . $HOME/suave_ws/src/suave_rebetmc/

RUN ["/bin/bash", "-c", "source /opt/ros/humble/setup.bash \
    && cd $HOME/suave_ws \
    && sudo apt update \
    && rosdep update \
    && rosdep install --from-paths src --ignore-src -r -y \
    && sudo rm -rf /var/lib/apt/lists/"]

## There is a bug with the default setuptools and packaging versions
RUN USER=ubuntu-user python3 -m pip install setuptools==75.8.2 packaging==24.1 empy==3.3.4 pandas==2.0.2 scipy==1.15.2 numpy==1.23.5

RUN ["/bin/bash", "-c", "source /opt/ros/humble/setup.bash \
    && cd $HOME/suave_ws \
    && colcon build --symlink-install"]

RUN sudo apt autoremove -y && sudo rm -rf /var/lib/apt/lists/

WORKDIR $HOME/suave_ws/
