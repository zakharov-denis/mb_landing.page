import { NextResponse } from 'next/server';
import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { email, timestamp, source, language, userAgent, url } = body;

    if (!email) {
      return NextResponse.json(
        { error: 'Email is required' },
        { status: 400 }
      );
    }

    // Send email notification to levmaysky@gmail.com
    const data = await resend.emails.send({
      from: 'Morning Buddies <onboarding@resend.dev>',
      to: [process.env.WAITLIST_TO || 'levmaysky@gmail.com'],
      subject: '🎉 New Morning Buddies Waitlist Signup!',
      html: `
        <div style="font-family: system-ui, -apple-system, sans-serif; max-width: 600px; margin: 0 auto;">
          <h2 style="color: #6F3CFF;">New Waitlist Signup</h2>

          <table style="width: 100%; border-collapse: collapse;">
            <tr style="border-bottom: 1px solid #eee;">
              <td style="padding: 12px 0; font-weight: 600;">Email:</td>
              <td style="padding: 12px 0;">${email}</td>
            </tr>
            <tr style="border-bottom: 1px solid #eee;">
              <td style="padding: 12px 0; font-weight: 600;">Time:</td>
              <td style="padding: 12px 0;">${timestamp || new Date().toISOString()}</td>
            </tr>
            <tr style="border-bottom: 1px solid #eee;">
              <td style="padding: 12px 0; font-weight: 600;">Language:</td>
              <td style="padding: 12px 0;">${language || 'en'}</td>
            </tr>
            <tr style="border-bottom: 1px solid #eee;">
              <td style="padding: 12px 0; font-weight: 600;">Source:</td>
              <td style="padding: 12px 0;">${source || 'website'}</td>
            </tr>
            ${url ? `
            <tr style="border-bottom: 1px solid #eee;">
              <td style="padding: 12px 0; font-weight: 600;">Page:</td>
              <td style="padding: 12px 0;">${url}</td>
            </tr>
            ` : ''}
          </table>

          <p style="margin-top: 24px; padding-top: 24px; border-top: 1px solid #eee; color: #666; font-size: 14px;">
            Sent from Morning Buddies Landing Page
          </p>
        </div>
      `,
    });

    return NextResponse.json({ success: true, data });
  } catch (error) {
    console.error('Waitlist API error:', error);
    return NextResponse.json(
      { error: 'Failed to send email', details: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}
