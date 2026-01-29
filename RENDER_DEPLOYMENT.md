# Render Deployment Guide for Shivkumar Kirana Store

This guide explains how to deploy your Flask app on **Render** using GitHub.

## Prerequisites

1. **GitHub Account** - Push your code here
2. **Render Account** - https://render.com (free tier available)
3. **PostgreSQL Database** - Render provides free PostgreSQL

## Step-by-Step Deployment

### Step 1: Prepare Your Repository

#### 1.1 Initialize Git (if not done)
```bash
cd shivkumar
git init
git add .
git commit -m "Initial commit - Shivkumar Kirana Store"
```

#### 1.2 Create GitHub Repository
1. Go to https://github.com/new
2. Create repository name: `shivkumar-kirana`
3. Click "Create repository"

#### 1.3 Push Code to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/shivkumar-kirana.git
git branch -M main
git push -u origin main
```

### Step 2: Create Render Account

1. Go to https://render.com
2. Click "Sign up" (use GitHub for easy login)
3. Authorize Render to access your GitHub account

### Step 3: Create PostgreSQL Database on Render

1. Go to **Dashboard** → Click **New +**
2. Select **PostgreSQL**
3. **Configuration**:
   - **Name**: `shivkumar-db`
   - **Database**: `kirana_db`
   - **User**: `postgres`
   - **Region**: Select closest to you
   - **PostgreSQL Version**: 15
   - **Plan**: Free

4. Click **Create Database**
5. Wait for it to be created (5-10 minutes)
6. Copy the **External Database URL** (it looks like: `postgresql://...`)
7. Save this for later ⭐

### Step 4: Create Web Service on Render

1. Go to **Dashboard** → Click **New +**
2. Select **Web Service**
3. Select **Deploy existing repository**

#### Connection
- Click "Connect account" → GitHub
- Select repository: `shivkumar-kirana`
- Click "Connect"

#### Configuration
- **Name**: `shivkumar-kirana`
- **Environment**: `Python 3`
- **Build Command**: 
  ```
  pip install -r requirements.txt && python -m flask db upgrade
  ```
- **Start Command**: 
  ```
  gunicorn app:app
  ```
- **Region**: Same as database
- **Plan**: Free

#### Environment Variables
Click **Add Environment Variable** and add these:

```
FLASK_ENV = production

SECRET_KEY = your_random_secret_key_here

DATABASE_URL = postgresql://postgres:PASSWORD@HOST:5432/kirana_db

ADMIN_USERNAME = admin

ADMIN_PASSWORD = your_strong_password
```

**Replace these with actual values:**
- `PASSWORD` - from your Render PostgreSQL database
- `HOST` - from your Render PostgreSQL database
- `SECRET_KEY` - Generate one: https://www.random.org/passwords/
- `ADMIN_PASSWORD` - Your chosen password

4. Click **Create Web Service**

### Step 5: Verify Deployment

1. Wait for build to complete (3-5 minutes)
2. Check logs for errors
3. Once deployed, click the URL to visit your site
4. Login to admin panel: `/admin`

## 🚀 Deployment Complete!

Your app is now live! 

- **Website**: `https://your-app-name.onrender.com`
- **Admin Panel**: `https://your-app-name.onrender.com/admin`

## 📝 Environment Variables Reference

| Variable | Example | Required |
|----------|---------|----------|
| `FLASK_ENV` | production | ✅ |
| `SECRET_KEY` | abc123xyz789... | ✅ |
| `DATABASE_URL` | postgresql://... | ✅ |
| `ADMIN_USERNAME` | admin | ✅ |
| `ADMIN_PASSWORD` | MyPassword123 | ✅ |

## 🔄 Updating Your App

Every time you push to GitHub:

```bash
git add .
git commit -m "Your changes"
git push origin main
```

Render will automatically rebuild and redeploy! 🎉

## ⚠️ Important Notes

1. **Free Tier Limits**:
   - Spin-down after 15 minutes of inactivity
   - Limited to 0.5GB RAM
   - Upgrade to paid plan for production use

2. **Database**:
   - Free PostgreSQL sleeps after inactivity
   - 90-day auto-deletion if not used

3. **Security**:
   - Never commit `.env` file to GitHub
   - Change default admin password
   - Use strong SECRET_KEY

## 🆘 Troubleshooting

### App won't deploy
- Check build logs in Render dashboard
- Verify all environment variables are set
- Check requirements.txt is correct

### Database connection error
- Verify DATABASE_URL is correct
- Check PostgreSQL service is running
- Restart the web service

### Admin login fails
- SSH into Render and run: `python create_admin.py`
- Or reset credentials in environment variables

### App keeps spinning down
- Upgrade to Paid plan
- Or use background jobs to keep it alive

## 📞 Support

- Render Docs: https://render.com/docs
- Flask Docs: https://flask.palletsprojects.com/
- PostgreSQL Docs: https://www.postgresql.org/docs/

---

Happy Deployment! 🚀
