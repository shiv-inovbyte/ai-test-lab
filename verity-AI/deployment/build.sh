#!/bin/bash

# Verity AI Docker Build and Deploy Script

set -e

echo "🚀 Building Verity AI Docker Image..."

# Navigate to deployment directory
cd "$(dirname "$0")"

# Build the Docker image from parent directory context
echo "📦 Building Docker image..."
docker build -f Dockerfile -t verity-ai:latest ..

echo "✅ Docker image built successfully!"

# Check if we should run the container
read -p "🤔 Do you want to start the container now? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🏃‍♂️ Starting Verity AI container..."
    
    # Check if OPENAI_API_KEY is set
    if [ -z "$OPENAI_API_KEY" ]; then
        echo "⚠️  Warning: OPENAI_API_KEY environment variable is not set."
        echo "   The /maintenance-advice endpoint will not work without it."
        echo "   You can set it with: export OPENAI_API_KEY='your-key-here'"
        echo ""
    fi
    
    # Stop any existing container
    docker stop verity-ai 2>/dev/null || true
    docker rm verity-ai 2>/dev/null || true
    
    # Start new container
    docker run -d \
        --name verity-ai \
        -p 6000:6000 \
        -e OPENAI_API_KEY="${OPENAI_API_KEY}" \
        verity-ai:latest
    
    echo "🎉 Verity AI is running!"
    echo "📊 Health check: http://localhost:6000/health"
    echo "🔮 Prediction API: http://localhost:6000/predict"
    echo "🔧 Maintenance API: http://localhost:6000/maintenance-advice"
    echo ""
    echo "📋 Container logs: docker logs -f verity-ai"
    echo "🛑 Stop container: docker stop verity-ai"
fi

echo "✨ Done!"