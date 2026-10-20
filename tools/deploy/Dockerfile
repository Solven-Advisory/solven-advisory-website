# Always-on copy of the site on any machine with Docker.
# Build and run from the repo root:
#   docker build -f tools/deploy/Dockerfile -t solven-site .
#   docker run -d --restart unless-stopped -p 8080:80 --name solven solven-site
FROM nginx:alpine
COPY tools/deploy/nginx.conf /etc/nginx/conf.d/default.conf
# Only the built site, as on Vercel (run tools/build_site_v5.py --prod first)
COPY public/ /usr/share/nginx/html
