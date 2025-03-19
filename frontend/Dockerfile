FROM node:23-slim

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable
RUN pnpm add -D @swc/cli @swc/core

COPY . /front
WORKDIR /front

COPY package.json pnpm-lock.yaml ./
RUN pnpm install
RUN pnpm add next@canary

ENTRYPOINT ["pnpm"]
CMD ["dev"]
