FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies with improved reliability
# Clean npm cache and increase timeout to handle network issues
RUN npm cache clean --force && \
    npm config set fetch-retry-mintimeout 20000 && \
    npm config set fetch-retry-maxtimeout 120000 && \
    npm ci --prefer-offline --no-audit || \
    (rm -rf node_modules package-lock.json && npm install --no-audit)

# Copy application code
COPY . .

# Build the application
RUN npm run build

# Production image
FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install production dependencies only with improved reliability
RUN npm cache clean --force && \
    npm config set fetch-retry-mintimeout 20000 && \
    npm config set fetch-retry-maxtimeout 120000 && \
    npm ci --production --prefer-offline --no-audit || \
    (rm -rf node_modules && npm install --production --no-audit)

# Copy built application from builder
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/next.config.js ./

# Create public directory (Next.js expects it even if empty)
RUN mkdir -p ./public

# Expose port
EXPOSE 3000

# Start the application
CMD ["npm", "start"]
