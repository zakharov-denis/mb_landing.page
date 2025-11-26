#!/usr/bin/env python3

# Read the file
with open('page.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Make.com webhook with Resend API
old_fetch = '''                // Send to Make.com webhook
                console.log('Fetching Make.com webhook...');
                const response = await fetch('https://hook.us2.make.com/hlw6p8jd43pdboxnlsknelk7t1gt5qpb', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload)
                });

                console.log('Make.com response status:', response.status);
                console.log('Make.com response ok:', response.ok);

                if (!response.ok) {
                    const errorText = await response.text();
                    console.error('Make.com error response:', errorText);
                    throw new Error(`Make.com webhook responded with status ${response.status}: ${errorText}`);
                }

                let responseData;
                try {
                    responseData = await response.json();
                    console.log('Make.com response data:', responseData);
                } catch (e) {
                    console.log('Make.com response is not JSON (this is OK)');
                }'''

new_fetch = '''                // Send to Resend API via Next.js route
                console.log('Sending to Resend API...');
                const response = await fetch('/api/waitlist', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload)
                });

                console.log('Resend API response status:', response.status);
                console.log('Resend API response ok:', response.ok);

                if (!response.ok) {
                    const errorText = await response.text();
                    console.error('Resend API error response:', errorText);
                    throw new Error(`Resend API responded with status ${response.status}: ${errorText}`);
                }

                const responseData = await response.json();
                console.log('Resend API response data:', responseData);'''

content = content.replace(old_fetch, new_fetch)

# Write back
with open('page.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Updated frontend to use Resend API!")
print("\nChanges:")
print("  • Replaced Make.com webhook URL with /api/waitlist")
print("  • Updated console logs to reference Resend API")
print("  • Kept all existing payload structure")
