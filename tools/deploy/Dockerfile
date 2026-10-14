# Always-on copy of the site on any machine with Docker.
# Build and run from the repo root:
#   docker build -f tools/deploy/Dockerfile -t solven-site .
#   docker run -d --restart unless-stopped -p 8080:80 --name solven solven-site
FROM nginx:alpine
COPY tools/deploy/nginx.conf /etc/nginx/conf.d/default.conf
COPY . /usr/share/nginx/html
RUN rm -rf /usr/share/nginx/html/tools \
           /usr/share/nginx/html/BRAND.md \
           /usr/share/nginx/html/CLAUDE.md \
           /usr/share/nginx/html/.git \
           /usr/share/nginx/html/.claude
