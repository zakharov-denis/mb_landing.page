export const metadata = {
  title: 'Morning Buddies',
  description: 'Morning Buddies — an accountability app that pairs you with a weekly buddy to stay focused, build habits, and achieve goals with simple structure and support.',
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
