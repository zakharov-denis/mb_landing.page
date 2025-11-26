# Testing Waitlist/Launch Modes

## Current Setup
- `.env.local` has `NEXT_PUBLIC_MODE=launch`
- Need to restart server to apply changes

## Test Checklist

### ✅ Testing LAUNCH Mode

**Setup:**
1. In `.env.local`: `NEXT_PUBLIC_MODE=launch`
2. Restart server: Stop (Ctrl+C) and run `npm run dev`
3. Hard refresh browser (Cmd+Shift+R or Ctrl+Shift+R)

**Expected Behavior:**
- [ ] Email input field is HIDDEN
- [ ] Button is full width
- [ ] Button text in English: "Get Started"
- [ ] Button text in Russian: "Найти бадди"
- [ ] Console shows: `⚙️ Site config loaded: {mode: 'launch', appUrl: '...'}`
- [ ] Console shows: `🔄 Updated button text to: Get Started (mode: launch, lang: en)`
- [ ] Clicking button redirects to: `https://mobile--morningbuddies.us-central1.hosted.app/`
- [ ] NO email submission happens

### ✅ Testing WAITLIST Mode

**Setup:**
1. In `.env.local`: `NEXT_PUBLIC_MODE=waitlist`
2. Restart server: Stop (Ctrl+C) and run `npm run dev`
3. Hard refresh browser (Cmd+Shift+R or Ctrl+Shift+R)

**Expected Behavior:**
- [ ] Email input field is VISIBLE
- [ ] Button text in English: "Join Waitlist"
- [ ] Button text in Russian: "Присоединиться к списку ожидания"
- [ ] Console shows: `⚙️ Site config loaded: {mode: 'waitlist', appUrl: '...'}`
- [ ] Console shows: `🔄 Updated button text to: Join Waitlist (mode: waitlist, lang: en)`
- [ ] Entering email and clicking submits to `/api/contact`
- [ ] Success message: "Thank you! Your message has been sent successfully."
- [ ] Email arrives at `levmaysky@gmail.com` via Resend
- [ ] NO redirect happens

### 🔧 Troubleshooting

**If button text doesn't change:**
- Clear browser cache completely
- Open in incognito/private mode
- Check console for errors
- Verify server restarted after changing `.env.local`

**If email field doesn't hide in launch mode:**
- Check console logs for `updateButtonText` calls
- Inspect element to see if `display: none` is applied
- Try waiting 3-4 seconds after page load

**If mode doesn't change:**
- Verify `.env.local` file saved
- Confirm server was fully stopped and restarted
- Check `/api/config` returns correct mode: `http://localhost:3000/api/config`

## Quick Debug Commands

```bash
# Check what config API returns
curl http://localhost:3000/api/config

# Should return:
# {"mode":"launch","appUrl":"https://mobile--morningbuddies.us-central1.hosted.app/"}
# or
# {"mode":"waitlist","appUrl":"https://mobile--morningbuddies.us-central1.hosted.app/"}
```

## Production Deployment

When deploying to Vercel/Firebase:
1. Add environment variables in deployment settings
2. `NEXT_PUBLIC_MODE=launch` or `waitlist`
3. `NEXT_PUBLIC_APP_URL=https://mobile--morningbuddies.us-central1.hosted.app/`
4. Deploy
5. No code changes needed to switch modes - just update env vars
