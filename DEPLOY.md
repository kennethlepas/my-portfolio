# Deployment Guide (Vercel)

This portfolio is ready to be deployed to [Vercel](https://vercel.com).

## Prerequisites
- A Vercel account.
- [Vercel CLI](https://vercel.com/docs/cli) installed (optional but recommended).

## Deployment Steps

1. **Connect to Vercel**: 
   - You can connect your GitHub repository directly to Vercel for automatic deployments.
   - Alternatively, run `vercel` in the project root.

2. **Environment Variables**:
   In the Vercel Dashboard, go to **Settings > Environment Variables** and add:
   - `ADMIN_PASSWORD`: Your secret admin password (defaults to `admin123`).
   - `DATABASE_URL`: (Optional) If you want to use a persistent database like Vercel Postgres. If not provided, it will use the bundled `portfolio.db` (read-only).

3. **Database Note**:
   - Vercel's filesystem is **read-only**. 
   - Any changes made via the `/admin` dashboard while using SQLite (`portfolio.db`) will **not persist** across redeployments.
   - **Recommendation**: For full functionality, connect a **Vercel Postgres** database and set the `DATABASE_URL` environment variable.

## Local Testing
To test the production configuration locally:
```bash
export ADMIN_PASSWORD=your_secure_password
python app.py
```

## Files Prepared
- `vercel.json`: Routing and runtime configuration.
- `requirements.txt`: Updated with production dependencies.
- `app.py`: Updated to support environment variables.
