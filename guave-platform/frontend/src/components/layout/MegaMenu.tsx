'use client';

import Link from 'next/link';

export function MegaMenu() {
  const laptopCategories = [
    {
      title: 'By Brand',
      items: ['Apple', 'Dell', 'HP', 'Lenovo', 'ASUS', 'Acer'],
    },
    {
      title: 'By Category',
      items: ['Gaming', 'Business', 'Ultrabooks', '2-in-1', 'Budget', 'Premium'],
    },
    {
      title: 'By Screen Size',
      items: ['13 inch', '14 inch', '15 inch', '16 inch', '17 inch'],
    },
    {
      title: 'Accessories',
      items: ['Laptop Bags', 'Stands', 'Keyboards', 'Mice', 'USB Hubs'],
    },
  ];

  return (
    <div className="absolute left-0 top-full w-full bg-white shadow-lg border-t border-gray-200 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300 z-50">
      <div className="container mx-auto px-4 py-6">
        <div className="grid grid-cols-4 gap-8">
          {laptopCategories.map((cat, i) => (
            <div key={i}>
              <h3 className="font-bold text-gray-900 mb-3 text-sm uppercase tracking-wide">
                {cat.title}
              </h3>
              <ul className="space-y-2">
                {cat.items.map((item, idx) => (
                  <li key={idx}>
                    <Link
                      href={`/products?category=${item.toLowerCase().replace(/\s+/g, '-')}`}
                      className="text-gray-700 hover:text-blue-600 transition text-sm block"
                    >
                      {item}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* Optional Featured Section */}
        <div className="mt-6 bg-gray-50 p-4 rounded-lg flex justify-between items-center">
          <div>
            <h4 className="font-semibold text-gray-900">Featured Laptop</h4>
            <p className="text-sm text-gray-600">MacBook Pro 16&quot; M3 Max</p>
          </div>
          <Link
            href="/products/macbook-pro-16"
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition"
          >
            Shop Now
          </Link>
        </div>
      </div>
    </div>
  );
}

export default MegaMenu;
