FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js for n8n
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Install n8n globally
RUN npm install -g n8n

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create directory for logs
RUN mkdir -p logs

# Expose n8n port
EXPOSE 5678

# Set environment variables
ENV N8N_HOST=0.0.0.0
ENV N8N_PORT=5678
ENV PYTHONUNBUFFERED=1

# Create startup script
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
echo "Starting AI Meeting Automation..."\n\
\n\
# Start n8n in background\n\
echo "Starting n8n..."\n\
n8n start &\n\
N8N_PID=$!\n\
\n\
# Wait for n8n to start\n\
sleep 10\n\
\n\
# Import workflow if it exists\n\
if [ -f "n8n-workflow.json" ]; then\n\
    echo "Workflow file found, ready for import"\n\
fi\n\
\n\
# Keep container running\n\
echo "Services started. Container ready."\n\
wait $N8N_PID\n\
' > /app/start.sh && chmod +x /app/start.sh

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:5678/healthz || exit 1

# Start the application
CMD ["/app/start.sh"]
