# Use official Node image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files first (for caching)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy rest of the project
COPY . .

# Build TypeScript
RUN npm run build

# Set production mode
ENV NODE_ENV=production

# Start MCP server
CMD ["node", "dist/index.js"]
