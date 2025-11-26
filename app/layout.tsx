export const metadata = {
  title: 'Morning Buddies',
  description: 'Morning Buddies — an accountability app that pairs you with a weekly buddy to stay focused, build habits, and achieve goals with simple structure and support.',
  icons: {
    icon: [
      { url: '/favicon.ico' },
      { url: '/favicon.png', sizes: '32x32', type: 'image/png' },
    ],
    apple: [
      { url: '/apple-touch-icon.png', sizes: '180x180', type: 'image/png' },
    ],
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
