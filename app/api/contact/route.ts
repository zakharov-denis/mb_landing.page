import { NextResponse } from 'next/server';
import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);

export async function POST(request: Request) {
  try {
    // Parse request body - handles both JSON and form-data
    const contentType = request.headers.get('content-type');
    let body;
    
    if (contentType?.includes('application/json')) {
      body = await request.json();
    } else {
      // Handle form-data
      const formData = await request.formData();
      body = Object.fromEntries(formData.entries());
    }

    const { name, email, message, comment, rating, formType, Name, Email, Comment, Message, Location } = body;

    // Normalize field names (handle both camelCase and PascalCase from Framer forms)
    const normalizedName = name || Name || '';
    const normalizedEmail = email || Email || '';
    const normalizedMessage = message || Message || '';
    const normalizedComment = comment || Comment || '';
    const normalizedRating = rating || Location || '';

    // Validate required fields
    if (!normalizedEmail) {
      return NextResponse.json(
        { error: 'Email is required' },
        { status: 400 }
      );
    }

    // Determine form type
    const isReview = formType === 'review' || normalizedRating || normalizedComment;
    const subject = isReview 
      ? '⭐ New Morning Buddies Review Submission'
      : '📧 New Morning Buddies Contact Form Message';
    
    const recipientEmail = process.env.CONTACT_TO || process.env.WAITLIST_TO || 'levmaysky@gmail.com';

    // Send email notification
    const emailData = await resend.emails.send({
      from: 'Morning Buddies <onboarding@resend.dev>',
      to: [recipientEmail],
      replyTo: normalizedEmail,
      subject: subject,
      html: `
        <div style="font-family: system-ui, -apple-system, sans-serif; max-width: 600px; margin: 0 auto;">
          <h2 style="color: #6F3CFF;">${isReview ? 'New Review Submission' : 'New Contact Form Message'}</h2>

          <table style="width: 100%; border-collapse: collapse;">
            ${normalizedName ? `
            <tr style="border-bottom: 1px solid #eee;">
              <td style="padding: 12px 0; font-weight: 600; width: 150px;">Name:</td>
              <td style="padding: 12px 0;">${normalizedName}</td>
            </tr>
            ` : ''}
            <tr style="border-bottom: 1px solid #eee;">
              <td style="padding: 12px 0; font-weight: 600;">Email:</td>
              <td style="padding: 12px 0;">${normalizedEmail}</td>
            </tr>
            ${normalizedRating ? `
            <tr style="border-bottom: 1px solid #eee;">
              <td style="padding: 12px 0; font-weight: 600;">Rating:</td>
              <td style="padding: 12px 0;">${'⭐'.repeat(parseInt(normalizedRating))} (${normalizedRating}/5)</td>
            </tr>
            ` : ''}
            ${normalizedComment || normalizedMessage ? `
            <tr style="border-bottom: 1px solid #eee;">
              <td style="padding: 12px 0; font-weight: 600; vertical-align: top;">${isReview ? 'Comment' : 'Message'}:</td>
              <td style="padding: 12px 0;">${normalizedComment || normalizedMessage}</td>
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

${normalizedName ? `Name: ${normalizedName}` : ''}
Email: ${normalizedEmail}
${normalizedRating ? `Rating: ${'⭐'.repeat(parseInt(normalizedRating))} (${normalizedRating}/5)` : ''}
${normalizedComment || normalizedMessage ? `${isReview ? 'Comment' : 'Message'}: ${normalizedComment || normalizedMessage}` : ''}
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

