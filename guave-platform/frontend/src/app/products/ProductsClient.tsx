'use client';

import { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import { productAPI, categoryAPI, brandAPI } from '@/lib/api';
import { Product, Category, Brand } from '@/types/product';
import { ProductCard } from '@/components/products/ProductCard';
import { ChevronDown, Grid, List, SlidersHorizontal } from 'lucide-react';

export default function ProductsClient() {
  const searchParams = useSearchParams();
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [brands, setBrands] = useState<Brand[]>([]);
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [sortBy, setSortBy] = useState('default');
  const [priceRange, setPriceRange] = useState([0, 5000]);
  const [selectedCategories, setSelectedCategories] = useState<string[]>([]);
  const [selectedBrands, setSelectedBrands] = useState<string[]>([]);
  const [showFilters, setShowFilters] = useState(true);

  const categoryParam = searchParams.get('category') || '';
  const brandParam = searchParams.get('brand') || '';

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const params = {
          category: categoryParam,
          brand: brandParam,
          ordering:
            sortBy === 'price_asc'
              ? 'price'
              : sortBy === 'price_desc'
              ? '-price'
              : '-created_at',
        };

        const [productsRes, categoriesRes, brandsRes] = await Promise.all([
          productAPI.getAll(params),
          categoryAPI.getAll(),
          brandAPI.getAll(),
        ]);

        setProducts(productsRes.data.results || productsRes.data);
        setCategories(categoriesRes.data);
        setBrands(brandsRes.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [categoryParam, brandParam, sortBy]);

  return (
    <div className="min-h-screen bg-gray-50 pt-32">
      <div className="container mx-auto px-4 py-8">
        <div className="text-sm text-gray-600 mb-6">
          Home / Products {categoryParam && `/ ${categoryParam}`}
        </div>

        {/* Sidebar and Main Content */}
        <div className="flex gap-8">
          {/* Sidebar Filters */}
          {showFilters && (
            <aside className="w-64 flex-shrink-0">
              <div className="bg-white rounded-lg p-6 sticky top-32">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="font-bold text-lg">Filters</h2>
                  <button className="text-blue-600 text-sm">Clear All</button>
                </div>
                {/* Add your filters JSX here */}
              </div>
            </aside>
          )}

          {/* Main Products Grid */}
          <main className="flex-1">
            {loading ? (
              <div className="grid grid-cols-4 gap-6">
                {Array.from({ length: 12 }).map((_, i) => (
                  <div key={i} className="bg-white h-96 rounded-lg animate-pulse" />
                ))}
              </div>
            ) : (
              <div className={`grid ${viewMode === 'grid' ? 'grid-cols-4' : 'grid-cols-1'} gap-6`}>
                {products.map((product) => (
                  <ProductCard key={product.id} product={product} />
                ))}
              </div>
            )}
          </main>
        </div>
      </div>
    </div>
  );
}
