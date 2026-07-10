# ========================================================
# STAGE 1: Build & Dependency Isolation
# ========================================================
FROM python:3.11-slim-bookworm AS builder

# Disable Python writing .pyc files to disk (reduces container size)
ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1

WORKDIR /build

# Securely install dependencies into a local user space
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt


# ========================================================
# STAGE 2: Hardened Runtime Execution
# ========================================================
FROM python:3.11-slim-bookworm AS runner

# Install 'tini' to handle process signals (SIGTERM) properly as PID 1
RUN apt-get update && apt-get install -y --no-install-recommends tini && \
  rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 🔒 Senior Security: Establish an unprivileged system service worker
RUN groupadd -g 10001 appgroup && \
  useradd -u 10001 -g appgroup -s /sbin/nologin -c "Docker Application User" appuser

# Copy packages from builder stage and assign explicit ownership
COPY --from=builder /root/.local /home/appuser/.local
COPY --chown=appuser:appgroup src/ /app/src/

# Update execution PATH for the unprivileged user
ENV PATH=/home/appuser/.local/bin:$PATH \
  ENV=production \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1

# Drop privileges to the non-root user
USER 10001:10001

EXPOSE 5000

# Use tini to transparently pass lifecycle signals to our application
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["python", "src/app.py"]
