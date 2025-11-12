
// ============================================
// src/app/page.tsx - Homepage
// ============================================

'use client';

import { useState, useEffect } from 'react';
import { productAPI } from '@/lib/api';
import { Product } from '@/types/product';
import { ProductCard } from '@/components/products/ProductCard';
import { ChevronLeft, ChevronRight, TruckIcon, RotateCcw, Headphones, ShieldCheck } from 'lucide-react';

export default function HomePage() {
  const [featuredProducts, setFeaturedProducts] = useState<Product[]>([]);
  const [newArrivals, setNewArrivals] = useState<Product[]>([]);
  const [bestSelling, setBestSelling] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const [featured, newArr, best] = await Promise.all([
          productAPI.getFeatured(),
          productAPI.getNewArrivals(),
          productAPI.getBestSelling(),
        ]);
        
        setFeaturedProducts(featured.data);
        setNewArrivals(newArr.data);
        setBestSelling(best.data);
      } catch (error) {
        console.error('Error fetching products:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Slider */}
      <section className="bg-gradient-to-r from-blue-900 to-blue-700 text-white">
        <div className="container mx-auto px-4 py-20">
          <div className="grid md:grid-cols-2 gap-8 items-center">
            <div>
              <span className="text-yellow-400 font-semibold mb-2 block">EXCLUSIVE OFFER</span>
              <h1 className="text-5xl font-bold mb-4">
                iPhone 15 Pro Max<br />
                On Sale At<br />
                <span className="text-yellow-400">35% Off</span>
              </h1>
              <p className="text-blue-100 mb-6 text-lg">
                Limited time offer. Don&apos;t miss out on this amazing deal!
              </p>
              <button className="px-8 py-4 bg-yellow-400 text-blue-900 font-bold rounded-lg hover:bg-yellow-300 transition text-lg">
                Shop Now
              </button>
            </div>
            <div className="relative">
              <div className="aspect-square bg-blue-800/50 rounded-full flex items-center justify-center">
                <div className="text-6xl">📱</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* USP Section */}
      <section className="bg-white py-8 shadow-sm">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                <TruckIcon className="w-6 h-6 text-blue-600" />
              </div>
              <div>
                <h3 className="font-bold text-gray-900">Free Delivery</h3>
                <p className="text-sm text-gray-600">On orders over $100</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0">
                <RotateCcw className="w-6 h-6 text-green-600" />
              </div>
              <div>
                <h3 className="font-bold text-gray-900">7 Days Return</h3>
                <p className="text-sm text-gray-600">Money back guarantee</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-orange-100 rounded-full flex items-center justify-center flex-shrink-0">
                <Headphones className="w-6 h-6 text-orange-600" />
              </div>
              <div>
                <h3 className="font-bold text-gray-900">24/7 Support</h3>
                <p className="text-sm text-gray-600">Dedicated support</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center flex-shrink-0">
                <ShieldCheck className="w-6 h-6 text-purple-600" />
              </div>
              <div>
                <h3 className="font-bold text-gray-900">Secure Payment</h3>
                <p className="text-sm text-gray-600">100% protected</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Category Grid */}
      <section className="py-12">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
            {['Smartphones', 'Laptops', 'Headphones', 'Cameras', 'Gaming', 'Smartwatches'].map((category) => (
              <div key={category} className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition cursor-pointer group">
                <div className="w-16 h-16 bg-blue-100 rounded-full mx-auto mb-4 flex items-center justify-center group-hover:bg-blue-600 transition">
                  <span className="text-3xl">📱</span>
                </div>
                <h3 className="text-center font-semibold text-gray-900">{category}</h3>
                <p className="text-center text-sm text-gray-600">120+ products</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Products */}
      <section className="py-12 bg-white">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between mb-8">
            <h2 className="text-3xl font-bold text-gray-900">Featured Products</h2>
            <div className="flex gap-4">
              <button className="px-6 py-2 rounded-lg hover:bg-blue-600 hover:text-white transition">Recent</button>
              <button className="px-6 py-2 rounded-lg hover:bg-blue-600 hover:text-white transition">Best Selling</button>
              <button className="px-6 py-2 rounded-lg hover:bg-blue-600 hover:text-white transition">Top Rated</button>
              <button className="px-6 py-2 rounded-lg hover:bg-blue-600 hover:text-white transition">On Sale</button>
            </div>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
            {loading ? (
              Array.from({ length: 10 }).map((_, i) => (
                <div key={i} className="bg-gray-200 h-80 rounded-lg animate-pulse" />
              ))
            ) : (
              featuredProducts.map((product) => (
                <ProductCard key={product.id} product={product} />
              ))
            )}
          </div>
        </div>
      </section>

      {/* Flash Sale Banner */}
      <section className="py-12">
        <div className="container mx-auto px-4">
          <div className="bg-gradient-to-r from-red-600 to-pink-600 rounded-2xl p-8 text-white relative overflow-hidden">
            <div className="relative z-10">
              <h2 className="text-4xl font-bold mb-4">⚡ Flash Sale</h2>
              <p className="text-xl mb-6">Limited time offer - Up to 50% off</p>
              <div className="flex gap-4 mb-6">
                <div className="bg-white text-red-600 rounded-lg p-4 text-center">
                  <div className="text-3xl font-bold">12</div>
                  <div className="text-sm">Hours</div>
                </div>
                <div className="bg-white text-red-600 rounded-lg p-4 text-center">
                  <div className="text-3xl font-bold">34</div>
                  <div className="text-sm">Minutes</div>
                </div>
                <div className="bg-white text-red-600 rounded-lg p-4 text-center">
                  <div className="text-3xl font-bold">56</div>
                  <div className="text-sm">Seconds</div>
                </div>
              </div>
              <button className="px-8 py-3 bg-white text-red-600 font-bold rounded-lg hover:bg-gray-100 transition">
                Shop Flash Sale
              </button>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}