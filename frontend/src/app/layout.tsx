import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Market Mind - Global Stock Screener',
  description: 'Advanced stock screening and fundamental analysis platform',
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
