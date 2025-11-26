import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json({
    mode: process.env.NEXT_PUBLIC_MODE || 'waitlist',
    appUrl: process.env.NEXT_PUBLIC_APP_URL || 'https://mobile--morningbuddies.us-central1.hosted.app/',
  });
}
