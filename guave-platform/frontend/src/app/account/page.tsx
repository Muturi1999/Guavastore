// src/app/account/page.tsx
'use client';

import React from 'react';
import Link from 'next/link';

export default function AccountPage() {
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">My Account</h1>
      <p>Welcome to your account dashboard.</p>

      <ul className="mt-4 space-y-2">
        <li>
          <Link href="/account/orders" className="text-blue-600 hover:underline">
            My Orders
          </Link>
        </li>
        <li>
          <Link href="/account/wishlist" className="text-blue-600 hover:underline">
            Wishlist
          </Link>
        </li>
        <li>
          <Link href="/account/settings" className="text-blue-600 hover:underline">
            Account Settings
          </Link>
        </li>
      </ul>
    </div>
  );
}
