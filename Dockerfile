FROM ghcr.io/kas-lab/suave-headless:1.6.0 AS base

RUN wget https://dlcdn.apache.org/maven/maven-3/3.9.16/binaries/apache-maven-3.9.16-bin.tar.gz -P /tmp && \
    sudo tar -xf /tmp/apache-maven-3.9.16-bin.tar.gz -C /opt && \
    sudo ln -sf /opt/apache-maven-3.9.16/bin/mvn /usr/local/bin/mvn && \
    rm /tmp/apache-maven-3.9.16-bin.tar.gz

RUN pip3 install jpype1

## Import extra dependencies into the existing suave_ws (suave already present → skip-existing)
COPY --chown=ubuntu-user:ubuntu-user suave_tactical_retreat.repos $HOME/suave_ws/suave_tactical_retreat.repos
ARG DEPS_CACHE_BUSTER
RUN echo "deps-buster=${DEPS_CACHE_BUSTER}" > /dev/null && \
    vcs import --skip-existing --input $HOME/suave_ws/suave_tactical_retreat.repos $HOME/suave_ws/src

## Copy suave_tactical_retreat source
COPY --chown=ubuntu-user:ubuntu-user . $HOME/suave_ws/src/suave_tactical_retreat/
COPY --chown=ubuntu-user:ubuntu-user --chmod=0755 \
    scripts/run_suave_runner.sh $HOME/suave_ws/run_suave_runner.sh

RUN ["/bin/bash", "-c", "source /opt/ros/humble/setup.bash \
    && cd $HOME/suave_ws \
    && sudo apt update \
    && rosdep update \
    && rosdep install --from-paths src --ignore-src -r -y \
    && sudo rm -rf /var/lib/apt/lists/"]

## There is a bug with the default setuptools and packaging versions
RUN USER=ubuntu-user python3 -m pip install setuptools==75.8.2 packaging==24.1 empy==3.3.4 pandas==2.0.2 scipy==1.15.2 numpy==1.23.5

WORKDIR $HOME/suave_ws/
RUN sudo apt autoremove -y && sudo rm -rf /var/lib/apt/lists/

FROM base AS built

RUN ["/bin/bash", "-c", "source /opt/ros/humble/setup.bash \
    && cd $HOME/suave_ws \
    && colcon build --symlink-install"]
