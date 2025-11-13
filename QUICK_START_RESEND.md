# Quick Start: Resend Webhook Implementation

## Prerequisites
- ✅ Next.js project structure exists
- ✅ Resend package installed (`resend@^3.0.0`)
- ✅ Existing waitlist API route at `/app/api/waitlist/route.ts`

## Quick Implementation Steps

### 1. Create Contact API Endpoint

Create file: `/app/api/contact/route.ts`

```typescript
import { NextResponse } from 'next/server';
import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);

export async function POST(request: Request) {
  try {
    const contentType = request.headers.get('content-type');
    const body = contentType?.includes('application/json')
      ? await request.json()
      : Object.fromEntries(await request.formData());

    const { name, email, message, comment, rating, formType } = body;

    if (!email) {
      return NextResponse.json({ error: 'Email is required' }, { status: 400 });
    }

    const isReview = formType === 'review' || rating || comment;
    const subject = isReview 
      ? '⭐ New Morning Buddies Review Submission'
      : '📧 New Morning Buddies Contact Form Message';

    await resend.emails.send({
      from: 'Morning Buddies <onboarding@resend.dev>',
      to: [process.env.CONTACT_TO || 'levmaysky@gmail.com'],
      replyTo: email,
      subject: subject,
      html: `
        <h2>${isReview ? 'New Review' : 'New Contact Message'}</h2>
        ${name ? `<p><strong>Name:</strong> ${name}</p>` : ''}
        <p><strong>Email:</strong> ${email}</p>
        ${rating ? `<p><strong>Rating:</strong> ${'⭐'.repeat(parseInt(rating))}</p>` : ''}
        ${comment || message ? `<p><strong>Message:</strong> ${comment || message}</p>` : ''}
      `,
    });

    return NextResponse.json({ success: true });
  } catch (error) {
    console.error('Contact API error:', error);
    return NextResponse.json(
      { error: 'Failed to send email' },
      { status: 500 }
    );
  }
}
```

### 2. Set Environment Variables

Create `.env.local`:
```bash
RESEND_API_KEY=re_xxxxxxxxxxxxxxxxxxxxx
CONTACT_TO=levmaysky@gmail.com
```

Add to Vercel environment variables (if deploying).

### 3. Update HTML Form Handler

Add to `page.html` (before closing `</body>` tag):

```javascript
<script>
async function handleFormSubmit(event) {
    event.preventDefault();
    const form = event.currentTarget;
    const formData = new FormData(form);
    
    const data = {
        formType: form.classList.contains('review-form') ? 'review' : 'contact',
        ...Object.fromEntries(formData.entries())
    };

    try {
        const response = await fetch('/api/contact', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        
        if (response.ok) {
            alert('Thank you! Your message has been sent.');
            form.reset();
        } else {
            throw new Error('Submission failed');
        }
    } catch (error) {
        alert('Error submitting form. Please try again.');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', handleFormSubmit);
    });
});
</script>
```

### 4. Test Locally

```bash
npm run dev
# Visit http://localhost:3000
# Test form submission
```

### 5. Deploy to Vercel

```bash
# Install Vercel CLI (if not installed)
npm i -g vercel

# Deploy
vercel

# Add environment variables in Vercel dashboard
# Update API URL in HTML form handler
```

## API Endpoint URLs

- **Local**: `http://localhost:3000/api/contact`
- **Vercel**: `https://your-project.vercel.app/api/contact`
- **Production**: Update with your production domain

## Form Data Format

**Contact Form:**
```json
{
  "formType": "contact",
  "email": "user@example.com",
  "message": "Hello, I have a question..."
}
```

**Review Form:**
```json
{
  "formType": "review",
  "name": "John Doe",
  "email": "user@example.com",
  "comment": "Great app!",
  "rating": "5"
}
```

## Troubleshooting

**Error: "Failed to send email"**
- Check `RESEND_API_KEY` is set correctly
- Verify Resend account is active
- Check Vercel function logs

**Error: "Email is required"**
- Ensure form has `name="email"` field
- Check form data is being sent correctly

**CORS Error**
- Ensure API and HTML are on same domain (Vercel)
- Or configure CORS headers in API route

## Next Steps

1. Verify domain in Resend dashboard
2. Update `from` field with verified domain
3. Add rate limiting
4. Add spam protection (reCAPTCHA)
5. Set up email templates

