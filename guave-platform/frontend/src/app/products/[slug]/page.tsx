'use client';

import React from 'react';
import { useParams } from 'next/navigation';

export default function ProductDetailPage() {
  const params = useParams();
  const { slug } = params;

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Product Detail</h1>
      <p>Showing details for product: <span className="font-semibold">{slug}</span></p>
    </div>
  );
}
