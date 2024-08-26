# Build the image with a specific Alpine version:
# docker build --build-arg ALPINE_VERSION=3.14 -t my-image:tag .
ARG ALPINE_VERSION=3.20

FROM alpine:${ALPINE_VERSION}

# Install Python and pip
RUN apk add --no-cache python3 py3-pip

# Set up Python environment
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Expose port 80 for Nginx (which will be installed by our script)
EXPOSE 80

# Set up entrypoint script
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]

# Default command (can be overridden)
CMD ["python3", "scripts/manage_sites.py"]
