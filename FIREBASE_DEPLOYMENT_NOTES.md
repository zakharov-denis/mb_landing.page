# Firebase Deployment - Important Notes

## ✅ Deployment Successful

**Hosting URL**: https://banya-na-griga.web.app

## ⚠️ Important: API Routes Won't Work

Firebase Hosting only serves **static files**. The API routes (`/api/contact` and `/api/waitlist`) are Next.js serverless functions and **cannot run on Firebase Hosting**.

### Current Situation

- ✅ Static HTML (`page.html`) is deployed to Firebase Hosting
- ❌ API routes (`/app/api/contact/route.ts` and `/app/api/waitlist/route.ts`) are NOT deployed
- ❌ Form submissions will fail because `/api/contact` doesn't exist on Firebase

## Solution: Deploy API Routes to Vercel

### Step 1: Deploy Next.js API to Vercel

1. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Deploy to Vercel:
   ```bash
   vercel
   ```

3. Follow prompts to link project

4. Get your Vercel deployment URL (e.g., `https://your-app.vercel.app`)

### Step 2: Set Environment Variables in Vercel

1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Add:
   - `RESEND_API_KEY`: Your Resend API key
   - `CONTACT_TO`: Email for contact forms
   - `WAITLIST_TO`: Email for waitlist signups

### Step 3: Update API URL in page.html

Update line 906 in `page.html`:

```javascript
// Change from:
const apiUrl = '/api/contact';

// To:
const apiUrl = 'https://your-vercel-app.vercel.app/api/contact';
```

Or use environment detection:

```javascript
const apiUrl = window.location.hostname.includes('firebase')
    ? 'https://your-vercel-app.vercel.app/api/contact'
    : '/api/contact'; // For local development
```

### Step 4: Redeploy to Firebase

After updating the API URL:

```bash
firebase deploy --only hosting
```

## Alternative: Use Firebase Functions

If you prefer to keep everything on Firebase, you can:

1. Set up Firebase Functions
2. Convert Next.js API routes to Firebase Functions
3. Update `firebase.json` to include functions configuration
4. Deploy functions with `firebase deploy --only functions`

This is more complex but keeps everything on Firebase.

## Quick Fix for Testing

For immediate testing, you can temporarily update the API URL in `page.html` to point to a deployed Vercel instance, then redeploy to Firebase.

## Files Deployed to Firebase

- ✅ `page.html` - Main landing page
- ✅ `blog/` - Blog pages
- ✅ Other static assets
- ❌ `app/` - Next.js API routes (not deployed, needs Vercel)
- ❌ `node_modules/` - Excluded
- ❌ `package.json` - Excluded

## Next Steps

1. Deploy API routes to Vercel
2. Update API URL in `page.html`
3. Redeploy to Firebase
4. Test form submissions
5. Verify emails are received


