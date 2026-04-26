#!/usr/bin/env bash
# Promtail setup script — installs and configures Promtail as a systemd service.
# Usage: sudo bash setup.sh <LOKI_URL>
# Example: sudo bash setup.sh http://34.123.45.67:3100

set -euo pipefail

PROMTAIL_VERSION="3.0.0"
LOKI_URL="${1:?Usage: $0 <LOKI_URL>}"
CONFIG_DIR="/etc/promtail"
BINARY="/usr/local/bin/promtail"

echo "=== Installing Promtail v${PROMTAIL_VERSION} ==="

# Download binary
ARCH=$(dpkg --print-architecture)
DOWNLOAD_URL="https://github.com/grafana/loki/releases/download/v${PROMTAIL_VERSION}/promtail-linux-${ARCH}.zip"
TMPDIR=$(mktemp -d)
cd "${TMPDIR}"

echo "Downloading from ${DOWNLOAD_URL}..."
curl -fsSL -o promtail.zip "${DOWNLOAD_URL}"
unzip -q promtail.zip
chmod +x promtail-linux-${ARCH}
mv promtail-linux-${ARCH} "${BINARY}"

echo "Binary installed at ${BINARY}"

# Create config directory
mkdir -p "${CONFIG_DIR}"

# Write config file with LOKI_URL substituted
HOSTNAME=$(hostname)
cat > "${CONFIG_DIR}/config.yml" <<EOF
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: ${LOKI_URL}/loki/api/v1/push

scrape_configs:
  - job_name: syslog
    static_configs:
      - targets: [localhost]
        labels:
          job: local-server
          host: ${HOSTNAME}
          env: production
          __path__: /var/log/syslog

  - job_name: authlog
    static_configs:
      - targets: [localhost]
        labels:
          job: local-server
          host: ${HOSTNAME}
          env: production
          __path__: /var/log/auth.log

  - job_name: kernlog
    static_configs:
      - targets: [localhost]
        labels:
          job: local-server
          host: ${HOSTNAME}
          env: production
          __path__: /var/log/kern.log

  - job_name: docker
    static_configs:
      - targets: [localhost]
        labels:
          job: local-server
          host: ${HOSTNAME}
          env: production
          __path__: /var/lib/docker/containers/*/*-json.log
    pipeline_stages:
      - docker: {}
EOF

echo "Config written to ${CONFIG_DIR}/config.yml"

# Create systemd service
cat > /etc/systemd/system/promtail.service <<EOF
[Unit]
Description=Promtail Log Agent
Documentation=https://grafana.com/docs/loki/latest/clients/promtail/
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=${BINARY} -config.file=${CONFIG_DIR}/config.yml
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

echo "Systemd service created"

# Enable and start
systemctl daemon-reload
systemctl enable promtail.service
systemctl start promtail.service

# Cleanup
rm -rf "${TMPDIR}"

echo ""
echo "=== Promtail Setup Complete ==="
systemctl status promtail.service --no-pager || true
echo ""
echo "Logs push to: ${LOKI_URL}"
echo "Check status: sudo systemctl status promtail"
echo "View logs:    sudo journalctl -u promtail -f"
