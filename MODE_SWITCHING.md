# Waitlist/Launch Mode Switching Guide

This landing page supports two modes that you can easily switch between.

## Modes

### 1. **Waitlist Mode** (Default)
- Shows: Email input field + Submit button
- Button text: "Join Waitlist" / "Присоединиться к списку ожидания"
- Behavior: Collects email addresses and sends them via Resend API
- Use when: App is not ready yet, building hype

### 2. **Launch Mode**
- Shows: Button only (email field hidden)
- Button text: "Get Started" / "Найти бадди"
- Behavior: Redirects users directly to the app
- Use when: App is live and ready for users

## How to Switch Modes

### Edit `.env.local` file:

```bash
# Change this line:
NEXT_PUBLIC_MODE=waitlist    # For waitlist mode
# OR
NEXT_PUBLIC_MODE=launch      # For launch mode
```

### After changing:
1. Save the file
2. Restart your Next.js dev server: `npm run dev`
3. Refresh the browser

## Configuration

All settings are in `.env.local`:

```
RESEND_API_KEY=your_key_here
WAITLIST_TO=levmaysky@gmail.com

# Landing page mode: "waitlist" or "launch"
NEXT_PUBLIC_MODE=waitlist
NEXT_PUBLIC_APP_URL=https://mobile--morningbuddies.us-central1.hosted.app/
```

## How It Works

1. **API Config Endpoint**: `/api/config/route.ts` serves the mode and app URL
2. **Frontend Script**: `public/index.html` fetches config and adjusts behavior
3. **Dynamic Button Text**: Updates based on mode and language (EN/RU)
4. **Form Handler**:
   - Waitlist mode → Submits to `/api/contact`
   - Launch mode → Redirects to app URL

## Testing

### Test Waitlist Mode:
1. Set `NEXT_PUBLIC_MODE=waitlist`
2. Restart server
3. Submit form → Should send email via Resend

### Test Launch Mode:
1. Set `NEXT_PUBLIC_MODE=launch`
2. Restart server
3. Click button → Should redirect to app

## Deployment

For production (Vercel, etc.):
- Set environment variables in your deployment platform
- Different values per environment (staging vs production)
- No need to commit changes to switch modes

## Notes

- Button text automatically translates (EN/RU) based on selected language
- Config loads asynchronously - fallback defaults are set
- Console logs show current mode for debugging
