FROM node:23-alpine

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable
RUN pnpm add -D @swc/cli @swc/core
RUN pnpm add next@canary

COPY package.json pnpm-lock.yaml ./
RUN pnpm install

COPY . /front
WORKDIR /front

ENTRYPOINT ["pnpm"]
CMD ["dev"]
