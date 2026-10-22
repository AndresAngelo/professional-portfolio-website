// Boilerplate for Root Layout (M4.G6)
import React, { type ReactNode } from 'react';

export default async function RootLayout({ children }: { children: ReactNode }) {
  return <html><body>{children}</body></html>;
}