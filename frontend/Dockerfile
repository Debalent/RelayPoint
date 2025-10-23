# RelayPoint Elite - Frontend Production Container
# Multi-stage build for optimized React production deployment

FROM node:18-alpine as builder

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies with production optimizations
RUN npm ci --only=production --silent

# Copy source code
COPY . .

# Build application
RUN npm run build

# Production stage with nginx
FROM nginx:alpine as production

# Install security updates
RUN apk update && apk upgrade && apk add --no-cache curl

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy built application from builder stage
COPY --from=builder /app/build /usr/share/nginx/html

# Create nginx user and set permissions
RUN addgroup -g 1001 -S relaypoint && \
    adduser -S relaypoint -u 1001 -G relaypoint && \
    chown -R relaypoint:relaypoint /usr/share/nginx/html && \
    chown -R relaypoint:relaypoint /var/cache/nginx && \
    chown -R relaypoint:relaypoint /var/log/nginx && \
    chown -R relaypoint:relaypoint /etc/nginx/conf.d

# Switch to non-root user
USER relaypoint

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000 || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]