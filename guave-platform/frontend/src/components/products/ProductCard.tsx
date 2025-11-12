// ============================================
// src/components/products/ProductCard.tsx
// ============================================

'use client';

import Link from 'next/link';
import Image from 'next/image';
import { Heart, ShoppingCart, Eye, Star } from 'lucide-react';
import { Product } from '@/types/product';
import { useCartStore } from '@/store/cartStore';
import { useState } from 'react';

interface ProductCardProps {
  product: Product;
}

export function ProductCard({ product }: ProductCardProps) {
  const [isHovered, setIsHovered] = useState(false);
  const addItem = useCartStore((state) => state.addItem);

  const handleAddToCart = (e: React.MouseEvent) => {
    e.preventDefault();
    addItem(product, null, 1);
    // Show toast notification
  };

  return (
    <div 
      className="bg-white rounded-lg shadow-sm hover:shadow-xl transition-all duration-300 group relative overflow-hidden"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <Link href={`/products/${product.slug}`}>
        {/* Product Image */}
        <div className="relative aspect-square overflow-hidden bg-gray-100">
          {product.main_image ? (
            <Image
              src={product.main_image}
              alt={product.name}
              fill
              className="object-cover group-hover:scale-110 transition-transform duration-300"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-gray-400">
              No Image
            </div>
          )}
          
          {/* Badges */}
          <div className="absolute top-2 left-2 flex flex-col gap-2">
            {product.badges?.map((badge) => (
              <span
                key={badge.id}
                className="px-2 py-1 text-xs font-bold rounded"
                style={{
                  backgroundColor: badge.background_color,
                  color: badge.text_color,
                }}
              >
                {badge.text}
              </span>
            ))}
            {product.discount_percentage > 0 && (
              <span className="px-2 py-1 text-xs font-bold bg-red-500 text-white rounded">
                -{product.discount_percentage}%
              </span>
            )}
          </div>

          {/* Stock Status */}
          {product.stock_status === 'out_of_stock' && (
            <div className="absolute inset-0 bg-black/50 flex items-center justify-center">
              <span className="px-4 py-2 bg-red-600 text-white font-bold rounded">
                Out of Stock
              </span>
            </div>
          )}

          {/* Quick Action Buttons */}
          <div className={`absolute top-2 right-2 flex flex-col gap-2 transition-all duration-300 ${
            isHovered ? 'opacity-100 translate-x-0' : 'opacity-0 translate-x-4'
          }`}>
            <button className="w-10 h-10 bg-white rounded-full flex items-center justify-center hover:bg-blue-600 hover:text-white transition shadow-lg">
              <Heart className="w-5 h-5" />
            </button>
            <button className="w-10 h-10 bg-white rounded-full flex items-center justify-center hover:bg-blue-600 hover:text-white transition shadow-lg">
              <Eye className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Product Info */}
        <div className="p-4">
          {/* Brand */}
          {product.brand_name && (
            <div className="text-xs text-gray-500 mb-1">{product.brand_name}</div>
          )}
          
          {/* Product Name */}
          <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2 group-hover:text-blue-600 transition">
            {product.name}
          </h3>

          {/* Rating */}
          <div className="flex items-center gap-2 mb-2">
            <div className="flex items-center">
              {Array.from({ length: 5 }).map((_, i) => (
                <Star
                  key={i}
                  className={`w-4 h-4 ${
                    i < Math.floor(product.average_rating)
                      ? 'fill-yellow-400 text-yellow-400'
                      : 'text-gray-300'
                  }`}
                />
              ))}
            </div>
            <span className="text-sm text-gray-600">({product.review_count})</span>
          </div>

          {/* Price */}
          <div className="flex items-center gap-2 mb-3">
            <span className="text-xl font-bold text-blue-600">
              ${parseFloat(product.price).toFixed(2)}
            </span>
            {product.compare_price && (
              <span className="text-sm text-gray-500 line-through">
                ${parseFloat(product.compare_price).toFixed(2)}
              </span>
            )}
          </div>

          {/* Stock Status Indicator */}
          <div className="mb-3">
            {product.stock_status === 'in_stock' && (
              <span className="text-xs text-green-600 flex items-center gap-1">
                <span className="w-2 h-2 bg-green-600 rounded-full"></span>
                In Stock
              </span>
            )}
            {product.stock_status === 'low_stock' && (
              <span className="text-xs text-orange-600 flex items-center gap-1">
                <span className="w-2 h-2 bg-orange-600 rounded-full"></span>
                Only few left
              </span>
            )}
          </div>

          {/* Add to Cart Button */}
          <button
            onClick={handleAddToCart}
            disabled={product.stock_status === 'out_of_stock'}
            className={`w-full py-2 rounded-lg font-semibold transition ${
              product.stock_status === 'out_of_stock'
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-blue-600 text-white hover:bg-blue-700'
            }`}
          >
            <ShoppingCart className="w-4 h-4 inline mr-2" />
            Add to Cart
          </button>
        </div>
      </Link>
    </div>
  );
}

