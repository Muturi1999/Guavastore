import { Suspense } from 'react';
import ProductsClient from './ProductsClient';

export default function ProductsPage() {
  return (
    <Suspense fallback={<div className="p-10 text-center">Loading products...</div>}>
      <ProductsClient />
    </Suspense>
  );
}
