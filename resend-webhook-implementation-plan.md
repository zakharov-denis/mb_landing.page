# Resend Webhook Implementation Plan

## Overview
Implement a serverless endpoint using Resend to handle form submissions from the landing page. The project already has a Next.js API route for waitlist (`/app/api/waitlist/route.ts`), so we'll extend this pattern for contact/review forms.

## Current State
- ✅ Next.js project structure exists
- ✅ Resend package installed (`resend@^3.0.0`)
- ✅ Waitlist API endpoint exists at `/app/api/waitlist/route.ts`
- ✅ Environment variable setup needed for `RESEND_API_KEY`
- ⚠️ HTML form (`page.html`) currently uses Framer's form handling
- ⚠️ Project is hosted on Firebase (static), but has Next.js setup

## Implementation Steps

### Step 1: Create Contact/Review API Endpoint

**File:** `/app/api/contact/route.ts`

Create a new API route that handles contact form submissions (name, email, message) and review submissions (name, comment, rating).

```typescript
import { NextResponse } from 'next/server';
import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);

export async function POST(request: Request) {
  try {
    // Parse form data (handles both JSON and form-data)
    const contentType = request.headers.get('content-type');
    let body;
    
    if (contentType?.includes('application/json')) {
      body = await request.json();
    } else {
      // Handle form-data
      const formData = await request.formData();
      body = Object.fromEntries(formData.entries());
    }

    const { name, email, message, comment, rating, formType } = body;

    // Validate required fields based on form type
    if (!email) {
      return NextResponse.json(
        { error: 'Email is required' },
        { status: 400 }
      );
    }

    // Determine form type and set appropriate subject/content
    const isReview = formType === 'review' || rating || comment;
    const subject = isReview 
      ? '⭐ New Morning Buddies Review Submission'
      : '📧 New Morning Buddies Contact Form Message';
    
    const recipientEmail = process.env.CONTACT_TO || process.env.WAITLIST_TO || 'levmaysky@gmail.com';

    // Send email notification
    const emailData = await resend.emails.send({
      from: 'Morning Buddies <onboarding@resend.dev>', // Update with verified domain
      to: [recipientEmail],
      replyTo: email,
      subject: subject,
      html: `
        <div style="font-family: system-ui, -apple-system, sans-serif; max-width: 600px; margin: 0 auto;">
          <h2 style="color: #6F3CFF;">${isReview ? 'New Review Submission' : 'New Contact Form Message'}</h2>

          <table style="width: 100%; border-collapse: collapse;">
            ${name ? `
            <tr style="border-bottom: 1px solid #eee;">
              <td style="padding: 12px 0; font-weight: 600; width: 150px;">Name:</td>
              <td style="padding: 12px 0;">${name}</td>
            </tr>
            ` : ''}
            <tr style="border-bottom: 1px solid #eee;">
              <td style="padding: 12px 0; font-weight: 600;">Email:</td>
              <td style="padding: 12px 0;">${email}</td>
            </tr>
            ${rating ? `
            <tr style="border-bottom: 1px solid #eee;">
              <td style="padding: 12px 0; font-weight: 600;">Rating:</td>
              <td style="padding: 12px 0;">${'⭐'.repeat(parseInt(rating))} (${rating}/5)</td>
            </tr>
            ` : ''}
            ${comment || message ? `
            <tr style="border-bottom: 1px solid #eee;">
              <td style="padding: 12px 0; font-weight: 600; vertical-align: top;">${isReview ? 'Comment' : 'Message'}:</td>
              <td style="padding: 12px 0;">${comment || message}</td>
            </tr>
            ` : ''}
            <tr style="border-bottom: 1px solid #eee;">
              <td style="padding: 12px 0; font-weight: 600;">Time:</td>
              <td style="padding: 12px 0;">${new Date().toISOString()}</td>
            </tr>
          </table>

          <p style="margin-top: 24px; padding-top: 24px; border-top: 1px solid #eee; color: #666; font-size: 14px;">
            Sent from Morning Buddies Landing Page
          </p>
        </div>
      `,
      text: `
${isReview ? 'New Review Submission' : 'New Contact Form Message'}

${name ? `Name: ${name}` : ''}
Email: ${email}
${rating ? `Rating: ${'⭐'.repeat(parseInt(rating))} (${rating}/5)` : ''}
${comment || message ? `${isReview ? 'Comment' : 'Message'}: ${comment || message}` : ''}
Time: ${new Date().toISOString()}
      `.trim(),
    });

    return NextResponse.json({ success: true, data: emailData });
  } catch (error) {
    console.error('Contact API error:', error);
    return NextResponse.json(
      { 
        error: 'Failed to send email', 
        details: error instanceof Error ? error.message : 'Unknown error' 
      },
      { status: 500 }
    );
  }
}
```

### Step 2: Set Up Environment Variables

**File:** `.env.local` (for local development)

```bash
RESEND_API_KEY=re_xxxxxxxxxxxxxxxxxxxxx
CONTACT_TO=levmaysky@gmail.com
WAITLIST_TO=levmaysky@gmail.com
```

**For Vercel Deployment:**
1. Go to Vercel project settings
2. Navigate to Environment Variables
3. Add:
   - `RESEND_API_KEY`: Your Resend API key
   - `CONTACT_TO`: Email address to receive contact form submissions
   - `WAITLIST_TO`: Email address to receive waitlist submissions

**For Resend Setup:**
1. Sign up at [resend.com](https://resend.com)
2. Get API key from dashboard
3. Verify domain (optional but recommended for production)
4. Update `from` field in API route with verified domain

### Step 3: Update HTML Form to Use New Endpoint

**File:** `page.html`

Update the form submission handler to send data to the new API endpoint.

**Option A: Update existing form handler (if exists)**
- Find form submission JavaScript
- Update `fetch` URL to point to `/api/contact` (or full URL if deployed)
- Send form data as JSON or FormData

**Option B: Add new form handler**
Add JavaScript to handle form submissions:

```javascript
// Form submission handler
async function handleFormSubmit(event) {
    event.preventDefault();
    event.stopPropagation();
    event.stopImmediatePropagation();

    const form = event.currentTarget;
    const submitButton = form.querySelector('[type="submit"]');
    const originalButtonText = submitButton ? submitButton.textContent : null;

    // Show loading state
    if (submitButton) {
        submitButton.disabled = true;
        submitButton.dataset.originalText = originalButtonText || '';
        const loadingLabel = submitButton.getAttribute('data-loading-label') || 'Sending...';
        submitButton.textContent = loadingLabel;
        submitButton.setAttribute('aria-busy', 'true');
    }

    // Collect form data
    const formData = new FormData(form);
    const formType = form.classList.contains('framer-1kym45d') ? 'review' : 'contact';
    
    // Convert FormData to object
    const data = {
        formType: formType,
        ...Object.fromEntries(formData.entries())
    };

    // Determine API endpoint URL
    // For production: use full URL (e.g., https://yourdomain.com/api/contact)
    // For local development: use relative URL (/api/contact)
    const apiUrl = window.location.hostname === 'localhost' 
        ? '/api/contact' 
        : 'https://your-vercel-app.vercel.app/api/contact';

    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        
        // Show success message
        showThankYouModal();
        form.reset();
    } catch (error) {
        console.error('Form submission failed:', error);
        alert('We could not submit the form. Please try again later.');
    } finally {
        // Restore button state
        if (submitButton) {
            submitButton.disabled = false;
            submitButton.removeAttribute('aria-busy');
            if (submitButton.dataset.originalText !== undefined) {
                submitButton.textContent = submitButton.dataset.originalText;
                delete submitButton.dataset.originalText;
            }
        }
    }
}

// Attach event listeners to forms
document.addEventListener('DOMContentLoaded', () => {
    // Find all forms (adjust selector based on your form classes)
    const forms = document.querySelectorAll('form.framer-1kym45d, form.framer-rf4jiv');
    forms.forEach(form => {
        form.addEventListener('submit', handleFormSubmit);
    });
});
```

### Step 4: Update Form HTML Structure

**File:** `page.html`

Ensure forms have proper structure:

```html
<!-- Contact Form -->
<form class="framer-rf4jiv" method="POST">
    <input type="hidden" name="formType" value="contact">
    <label>
        <input type="email" name="email" placeholder="Email" required>
    </label>
    <label>
        <textarea name="message" placeholder="Message" required></textarea>
    </label>
    <button type="submit">Submit</button>
</form>

<!-- Review Form -->
<form class="framer-1kym45d" method="POST">
    <input type="hidden" name="formType" value="review">
    <label>
        <input type="text" name="name" placeholder="Name" required>
    </label>
    <label>
        <textarea name="comment" placeholder="Leave your review" required></textarea>
    </label>
    <label>
        <select name="rating" required>
            <option value="">Select rating</option>
            <option value="1">1 ⭐</option>
            <option value="2">2 ⭐⭐</option>
            <option value="3">3 ⭐⭐⭐</option>
            <option value="4">4 ⭐⭐⭐⭐</option>
            <option value="5">5 ⭐⭐⭐⭐⭐</option>
        </select>
    </label>
    <button type="submit">Submit</button>
</form>
```

### Step 5: Deployment Strategy

**Option A: Deploy API to Vercel (Recommended)**
1. Push code to GitHub
2. Connect repository to Vercel
3. Set environment variables in Vercel dashboard
4. Deploy API routes
5. Update HTML form to use Vercel API URL

**Option B: Keep Static HTML on Firebase, API on Vercel**
1. Deploy Next.js API routes to Vercel
2. Keep `page.html` on Firebase Hosting
3. Update form handler in HTML to point to Vercel API URL
4. Configure CORS if needed (Vercel handles this automatically for same-origin requests)

**Option C: Full Next.js Deployment**
1. Convert `page.html` to Next.js page component
2. Deploy entire Next.js app to Vercel
3. Use Next.js API routes for form handling

### Step 6: Testing

**Local Testing:**
1. Start Next.js dev server: `npm run dev`
2. Test API endpoint: `curl -X POST http://localhost:3000/api/contact -H "Content-Type: application/json" -d '{"email":"test@example.com","message":"Test message"}'
3. Test form submission from HTML page
4. Verify emails are received

**Production Testing:**
1. Deploy to Vercel
2. Test form submission from production site
3. Verify emails are received
4. Check Vercel function logs for errors

### Step 7: Error Handling & Validation

**Add to API route:**
- Email validation
- Rate limiting (optional, using Vercel Edge Config or Upstash)
- Spam protection (optional, using reCAPTCHA or similar)
- Input sanitization
- CORS headers (if needed)

**Add to HTML form:**
- Client-side validation
- Error message display
- Success message display
- Loading states
- Retry logic

### Step 8: Monitoring & Logging

**Vercel Functions:**
- Monitor function logs in Vercel dashboard
- Set up alerts for errors
- Track function execution time and costs

**Resend:**
- Monitor email delivery in Resend dashboard
- Set up webhooks for delivery events (optional)
- Track email open rates (optional)

## Files to Create/Modify

### New Files:
- `/app/api/contact/route.ts` - Contact/Review form API endpoint
- `.env.local` - Local environment variables (gitignored)
- `.env.example` - Example environment variables (committed)

### Modified Files:
- `page.html` - Update form submission handler
- `package.json` - Verify Resend dependency (already installed)
- `vercel.json` - Optional: configure Vercel settings
- `.gitignore` - Ensure `.env.local` is ignored

## Checklist

- [ ] Create `/app/api/contact/route.ts`
- [ ] Set up Resend account and get API key
- [ ] Add environment variables to `.env.local`
- [ ] Update HTML form submission handler
- [ ] Test locally with Next.js dev server
- [ ] Deploy API to Vercel
- [ ] Add environment variables to Vercel
- [ ] Update HTML form to use Vercel API URL
- [ ] Test form submission in production
- [ ] Verify emails are received
- [ ] Set up error monitoring
- [ ] Document API endpoint for team

## Next Steps After Implementation

1. **Domain Verification**: Verify domain in Resend for better deliverability
2. **Email Templates**: Create branded email templates
3. **Auto-reply**: Set up auto-reply emails to form submitters
4. **Database**: Store submissions in database (optional)
5. **Analytics**: Track form submission metrics
6. **A/B Testing**: Test different form layouts and messaging

## Notes

- The waitlist endpoint (`/app/api/waitlist/route.ts`) already exists and can be used as a reference
- Resend has a free tier (3,000 emails/month)
- Vercel has a free tier for serverless functions
- Consider using Vercel's Edge Functions for faster response times
- For production, use a verified domain in Resend's `from` field
- Consider adding rate limiting to prevent spam
- Add reCAPTCHA or similar for spam protection if needed

