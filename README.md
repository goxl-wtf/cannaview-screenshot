# CannaView Screenshot Service

Dedicated screenshot microservice for EasyDis digital display screens using FastAPI + Playwright.

## Why This Service?

Vercel's serverless functions have limitations for browser automation (timeouts, cold starts, environment constraints). This dedicated service running on Render.com provides:

- ✅ **Reliable screenshots** - No serverless limitations
- ✅ **Fast** - Warm browser, no cold starts
- ✅ **Proven** - Uses Playwright (tested successfully)
- ✅ **Cost-effective** - $7/month vs per-screenshot pricing
- ✅ **Full control** - Your infrastructure, your rules

## Features

- FastAPI with automatic OpenAPI docs
- Playwright for reliable browser automation
- API key authentication
- Domain whitelisting for security
- Configurable wait times and selectors
- Health check endpoint for monitoring
- Comprehensive logging

## Quick Start (Local Development)

### Prerequisites

- Docker and Docker Compose
- Git

### Run Locally

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/cannaview-screenshot.git
cd cannaview-screenshot

# Copy environment template
cp .env.example .env

# Edit .env and set your API_KEY

# Build and run with Docker Compose
docker-compose up --build

# Service will be available at http://localhost:8000
# API docs at http://localhost:8000/docs
```

## API Usage

### Take a Screenshot

**Endpoint**: `POST /screenshot`

**Headers**:
```
X-API-Key: your-api-key-here
Content-Type: application/json
```

**Request Body**:
```json
{
  "url": "https://www.easydis.io/screen/67165080bb88c87815c851ad-screen-1",
  "width": 1920,
  "height": 1080,
  "wait_time": 10000,
  "wait_for_selector": "[data-slot='card']",
  "full_page": false
}
```

**Response**:
```json
{
  "success": true,
  "image_base64": "iVBORw0KGgoAAAANS...",
  "metadata": {
    "capture_time_ms": 5234,
    "image_size_bytes": 1234567,
    "url": "https://www.easydis.io/screen/...",
    "dimensions": {
      "width": 1920,
      "height": 1080
    },
    "product_count": 42
  }
}
```

### Health Check

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "healthy",
  "browser": "chromium",
  "uptime_seconds": 3600
}
```

## Deployment to Render.com

### Step 1: Create GitHub Repository

```bash
cd /path/to/cannaview-screenshot
git init
git add .
git commit -m "Initial commit: CannaView Screenshot Service"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/cannaview-screenshot.git
git push -u origin main
```

### Step 2: Deploy on Render.com

1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Render will auto-detect Docker
5. Configure:
   - **Name**: cannaview-screenshot
   - **Plan**: Starter ($7/month)
   - **Environment Variables**:
     - `API_KEY`: Generate a strong random key
     - Other vars are set in `render.yaml`
6. Click "Create Web Service"

### Step 3: Get Service URL

After deployment, you'll get a URL like:
```
https://cannaview-screenshot.onrender.com
```

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `API_KEY` | Authentication key | - | ✅ Yes |
| `ALLOWED_DOMAINS` | Comma-separated allowed domains | easydis.io,www.easydis.io | No |
| `MAX_WAIT_TIME` | Maximum wait time (ms) | 60000 | No |
| `BROWSER_TYPE` | Browser (chromium/firefox/webkit) | chromium | No |
| `HEADLESS` | Run headless | true | No |
| `LOG_LEVEL` | Logging level | INFO | No |

## Integration with EasyDis (Vercel)

Add to your Vercel environment variables:

```
SCREENSHOT_SERVICE_URL=https://cannaview-screenshot.onrender.com
SCREENSHOT_SERVICE_API_KEY=your-api-key-here
```

Then modify `/api/store/screens/[screenId]/screenshot.ts` to call this service instead of using Puppeteer.

## Testing

```bash
# Test the service
curl -X POST http://localhost:8000/screenshot \
  -H "X-API-Key: dev-api-key-change-in-production" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.easydis.io/screen/67165080bb88c87815c851ad-screen-1",
    "width": 1920,
    "height": 1080,
    "wait_time": 10000,
    "wait_for_selector": "[data-slot=\"card\"]"
  }'
```

## Troubleshooting

### Service not starting
- Check logs in Render dashboard
- Verify Playwright dependencies are installed
- Check health endpoint

### Screenshots are blank
- Increase `wait_time`
- Verify `wait_for_selector` exists on page
- Check service logs for errors

### Authentication errors
- Verify API_KEY matches in both services
- Check X-API-Key header is included

## Development

### File Structure

```
cannaview-screenshot/
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Local development
├── requirements.txt        # Python dependencies
├── render.yaml            # Render.com config
└── app/
    ├── main.py            # FastAPI app
    ├── screenshot.py      # Playwright logic
    ├── auth.py            # Authentication
    ├── config.py          # Settings
    └── models.py          # Pydantic models
```

### Adding New Features

The service is designed to be extended. You can add:
- Response caching
- Queue system for bulk screenshots
- Webhook callbacks
- Custom screenshot templates
- PDF generation

## License

MIT

## Support

For issues, contact the EasyDis development team.
