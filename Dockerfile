# Super JinX Panel: PasarGuard + Xray core + nginx in one Railway service (port 8080)
FROM pasarguard/node:latest AS node

FROM pasarguard/panel:latest AS python-seal
RUN apt-get update && apt-get install -y --no-install-recommends build-essential python3-dev \
 && python -m pip install --no-cache-dir Cython==3.1.8 setuptools==80.10.2 wheel==0.48.0 python-minifier==3.4.0
COPY bootstrap.py genpaths.py entrypoint.sh healthcheck.sh /protected/
COPY tools/build_native.py /tmp/build_native.py
RUN python /tmp/build_native.py /protected/bootstrap.py /protected/genpaths.py

FROM pasarguard/panel:latest

RUN apt-get update && apt-get install -y --no-install-recommends nginx openssl ca-certificates curl \
 && rm -rf /var/lib/apt/lists/* /etc/nginx/sites-enabled/default

# node binary + xray core + geo files (static Go binaries, run fine on debian)
COPY --from=node /app/main /opt/pg-node/main
COPY --from=node /usr/local/bin/xray /usr/local/bin/xray
COPY --from=node /usr/local/share/xray /usr/local/share/xray

COPY nginx.conf.template /etc/nginx/nginx.conf.template
COPY ws.inc /etc/nginx/ws.inc
COPY jinx-ui.js /etc/nginx/jinx-ui.js
COPY --from=python-seal /protected/launchers/entrypoint.sh /entrypoint.sh
COPY --from=python-seal /protected/runtime/ /code/
COPY sub.html /code/custom_templates/subscription/index.html
COPY sub.html /etc/jinx/sub.html
COPY --from=python-seal /protected/launchers/healthcheck.sh /usr/local/bin/jinx-healthcheck
# strip Windows line endings (safe if files were edited on a phone/PC), then make executable
RUN sed -i "s/\r$//" /code/bootstrap.py /code/genpaths.py /etc/nginx/nginx.conf.template /etc/nginx/ws.inc /etc/nginx/jinx-ui.js \
 && chmod +x /entrypoint.sh /opt/pg-node/main /usr/local/bin/xray /usr/local/bin/jinx-healthcheck

ENV PORT=8080 \
    UVICORN_HOST=127.0.0.1 \
    UVICORN_PORT=8000 \
    UVICORN_PROXY_HEADERS=True \
    UVICORN_FORWARDED_ALLOW_IPS=127.0.0.1 \
    SQLALCHEMY_DATABASE_URL=sqlite+aiosqlite:////var/lib/pasarguard/db.sqlite3 \
    CUSTOM_TEMPLATES_DIRECTORY=/code/custom_templates/ \
    SUBSCRIPTION_PAGE_TEMPLATE=subscription/index.html \
    SUBSCRIPTION_PATH=sub \
    XRAY_EXECUTABLE_PATH=/usr/local/bin/xray \
    XRAY_ASSETS_PATH=/usr/local/share/xray

EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s CMD jinx-healthcheck || exit 1
ENTRYPOINT ["/entrypoint.sh"]
