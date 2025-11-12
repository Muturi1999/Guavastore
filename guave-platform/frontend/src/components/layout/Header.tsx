// // src/components/layout/Header.tsx

// 'use client';

// import { useState, useEffect, SetStateAction } from 'react';
// import Link from 'next/link';
// import Image from 'next/image';
// import { Search, ShoppingCart, Heart, User, Menu, Phone, MapPin } from 'lucide-react';
// import { useCartStore } from '@/store/cartStore';
// import { MegaMenu } from './MegaMenu';
// import { MiniCart } from '../cart/MiniCart';
// import { Input } from '../ui/input';
// import { Button } from '../ui/button';
// // import { Button } from '@/components/ui/button';
// // import { Input } from '@/components/ui/input';

// export function Header() {
//   const [isScrolled, setIsScrolled] = useState(false);
//   const [showMiniCart, setShowMiniCart] = useState(false);
//   const [showMobileMenu, setShowMobileMenu] = useState(false);
//   const [searchQuery, setSearchQuery] = useState('');
  
//   const totalItems = useCartStore((state) => state.getTotalItems());

//   useEffect(() => {
//     const handleScroll = () => {
//       setIsScrolled(window.scrollY > 50);
//     };
//     window.addEventListener('scroll', handleScroll);
//     return () => window.removeEventListener('scroll', handleScroll);
//   }, []);

//   return (
//     <header className="fixed top-0 left-0 right-0 z-50 bg-white shadow-md">
//       {/* Top Bar */}
//       <div className="bg-gray-900 text-white text-sm">
//         <div className="container mx-auto px-4 py-2">
//           <div className="flex items-center justify-between">
//             <div className="flex items-center gap-6">
//               <span className="flex items-center gap-2">
//                 <MapPin className="w-4 h-4" />
//                 Store Locator
//               </span>
//               <span>Track Order</span>
//             </div>
//             <div className="flex items-center gap-6">
//               <span className="flex items-center gap-2">
//                 <Phone className="w-4 h-4" />
//                 +08 9229 8228
//               </span>
//               <select className="bg-transparent border-none text-white">
//                 <option>English</option>
//                 <option>Swahili</option>
//               </select>
//               <select className="bg-transparent border-none text-white">
//                 <option>KES</option>
//                 <option>USD</option>
//               </select>
//             </div>
//           </div>
//         </div>
//       </div>

//       {/* Main Header */}
//       <div className={`transition-all duration-300 ${isScrolled ? 'py-2' : 'py-4'}`}>
//         <div className="container mx-auto px-4">
//           <div className="flex items-center justify-between gap-8">
//             {/* Logo */}
//             <Link href="/" className="flex-shrink-0">
//               <div className="flex items-center gap-2">
//                 <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
//                   <span className="text-white font-bold text-xl">E</span>
//                 </div>
//                 <span className="text-2xl font-bold text-gray-900">ecomall</span>
//               </div>
//             </Link>

//             {/* Search Bar */}
//             <div className="flex-1 max-w-2xl">
//               <div className="relative flex items-center">
//                 <select className="absolute left-0 h-full px-4 border-r border-gray-300 bg-white rounded-l-lg text-sm">
//                   <option>All Categories</option>
//                   <option>Electronics</option>
//                   <option>Fashion</option>
//                   <option>Home & Garden</option>
//                 </select>
//                 <Input
//                   type="text"
//                   placeholder="Search for products..."
//                   value={searchQuery}
//                   onChange={(e: { target: { value: SetStateAction<string>; }; }) => setSearchQuery(e.target.value)}
//                   className="w-full pl-44 pr-12 py-6 border-2 border-gray-300 rounded-lg focus:border-blue-500"
//                 />
//                 <Button className="absolute right-0 h-full px-6 bg-blue-600 hover:bg-blue-700 rounded-r-lg">
//                   <Search className="w-5 h-5" />
//                 </Button>
//               </div>
//             </div>

//             {/* Action Icons */}
//             <div className="flex items-center gap-6">
//               {/* Account */}
//               <Link href="/account" className="flex items-center gap-2 hover:text-blue-600 transition">
//                 <User className="w-6 h-6" />
//                 <div className="hidden lg:block text-sm">
//                   <div className="text-gray-500">My Account</div>
//                   <div className="font-semibold">Login</div>
//                 </div>
//               </Link>

//               {/* Wishlist */}
//               <Link href="/wishlist" className="relative hover:text-blue-600 transition">
//                 <Heart className="w-6 h-6" />
//                 <span className="absolute -top-2 -right-2 bg-blue-600 text-white text-xs w-5 h-5 flex items-center justify-center rounded-full">
//                   0
//                 </span>
//               </Link>

//               {/* Cart */}
//               <div 
//                 className="relative cursor-pointer hover:text-blue-600 transition"
//                 onMouseEnter={() => setShowMiniCart(true)}
//                 onMouseLeave={() => setShowMiniCart(false)}
//               >
//                 <div className="flex items-center gap-2">
//                   <div className="relative">
//                     <ShoppingCart className="w-6 h-6" />
//                     <span className="absolute -top-2 -right-2 bg-blue-600 text-white text-xs w-5 h-5 flex items-center justify-center rounded-full">
//                       {totalItems}
//                     </span>
//                   </div>
//                   <div className="hidden lg:block text-sm">
//                     <div className="text-gray-500">My Cart</div>
//                     <div className="font-semibold">$0.00</div>
//                   </div>
//                 </div>
//                 {showMiniCart && <MiniCart />}
//               </div>

//               {/* Mobile Menu Toggle */}
//               <button 
//                 className="lg:hidden"
//                 onClick={() => setShowMobileMenu(!showMobileMenu)}
//               >
//                 <Menu className="w-6 h-6" />
//               </button>
//             </div>
//           </div>
//         </div>
//       </div>

//       {/* Navigation */}
//       <div className="bg-gray-50 border-t border-gray-200">
//         <div className="container mx-auto px-4">
//           <div className="flex items-center justify-between">
//             {/* Categories Menu */}
//             <div className="relative">
//               <Button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-none">
//                 <Menu className="w-5 h-5 mr-2" />
//                 Shop Categories
//               </Button>
//             </div>

//             {/* Main Navigation */}
//             <nav className="hidden lg:flex items-center gap-8">
//               <Link href="/" className="py-4 hover:text-blue-600 transition font-medium">
//                 Home
//               </Link>
//               <div className="relative group">
//                 <button className="py-4 hover:text-blue-600 transition font-medium flex items-center gap-1">
//                   Laptops
//                   <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
//                     <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
//                   </svg>
//                 </button>
//                 <MegaMenu />
//               </div>
//               <Link href="/products?category=smartphones" className="py-4 hover:text-blue-600 transition font-medium">
//                 Smartphone
//               </Link>
//               <Link href="/products?category=headphones" className="py-4 hover:text-blue-600 transition font-medium">
//                 Headphones
//               </Link>
//               <Link href="/products?category=camera" className="py-4 hover:text-blue-600 transition font-medium">
//                 Camera
//               </Link>
//             </nav>

//             {/* Special Menu Items */}
//             <div className="hidden lg:flex items-center gap-4">
//               <Link 
//                 href="/flash-sale" 
//                 className="flex items-center gap-2 text-red-600 font-semibold hover:text-red-700 transition"
//               >
//                 <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
//                   <path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 1 0 001.414 1.414l.707-.707zM18 10a1 1 0 01-1 1h-1a1 1 0 110-2h1a1 1 0 011 1zM5.05 6.464A1 1 0 106.464 5.05l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM5 10a1 1 0 01-1 1H3a1 1 0 110-2h1a1 1 0 011 1zM8 16v-1h4v1a2 2 0 11-4 0zM12 14c.015-.34.208-.646.477-.859a4 4 0 10-4.954 0c.27.213.462.519.476.859h4.002z" />
//                 </svg>
//                 Flash Sale
//               </Link>
//               <Link 
//                 href="/deals" 
//                 className="px-4 py-2 bg-yellow-400 text-gray-900 font-semibold rounded-lg hover:bg-yellow-500 transition"
//               >
//                 Today&apos;s Deal
//                 <span className="ml-2 px-2 py-1 bg-red-600 text-white text-xs rounded-full">HOT</span>
//               </Link>
//             </div>
//           </div>
//         </div>
//       </div>
//     </header>
//   );
// }
// export default Header;

'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Menu, Search, ShoppingCart, User, Heart, ChevronDown } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { useCartStore } from '@/store/cartStore';

export function Header() {
  const [isScrolled, setIsScrolled] = useState(false);
  const [showCategories, setShowCategories] = useState(false);
  const totalItems = useCartStore((state) => state.getTotalItems());

  useEffect(() => {
    const handleScroll = () => setIsScrolled(window.scrollY > 50);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-white shadow-sm">
      {/* Top Bar */}
      <div className="bg-gray-900 text-gray-200 text-sm">
        <div className="container mx-auto flex justify-between items-center px-4 py-2">
          <div>Free shipping on orders over KES 5,000</div>
          <div className="flex items-center gap-4">
            <Link href="#" className="hover:text-white">Track Order</Link>
            <Link href="#" className="hover:text-white">Help</Link>
          </div>
        </div>
      </div>

      {/* Main Header */}
      <div className={`transition-all duration-300 ${isScrolled ? 'py-3' : 'py-5'}`}>
        <div className="container mx-auto px-4 flex items-center justify-between gap-8">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2">
            <div className="w-10 h-10 bg-blue-600 text-white font-bold text-lg flex items-center justify-center rounded-lg">
              E
            </div>
            <span className="text-2xl font-bold text-gray-900">Ecomall</span>
          </Link>

          {/* Search */}
          <div className="flex-1 max-w-2xl relative">
            <Input
              type="text"
              placeholder="Search for products..."
              className="w-full pl-4 pr-12 py-3 border-2 border-gray-200 rounded-lg focus:border-blue-500"
            />
            <Button className="absolute right-1 top-1 bottom-1 bg-blue-600 hover:bg-blue-700 rounded-md px-4">
              <Search className="w-5 h-5 text-white" />
            </Button>
          </div>

          {/* Icons */}
          <div className="flex items-center gap-6">
            <Link href="/account" className="flex items-center gap-2 hover:text-blue-600">
              <User className="w-5 h-5" />
              <span className="hidden md:block text-sm">Account</span>
            </Link>
            <Link href="/wishlist" className="relative hover:text-blue-600">
              <Heart className="w-5 h-5" />
              <span className="absolute -top-2 -right-2 bg-red-600 text-white text-xs w-4 h-4 flex items-center justify-center rounded-full">0</span>
            </Link>
            <Link href="/cart" className="relative hover:text-blue-600">
              <ShoppingCart className="w-5 h-5" />
              {totalItems > 0 && (
                <span className="absolute -top-2 -right-2 bg-blue-600 text-white text-xs w-4 h-4 flex items-center justify-center rounded-full">
                  {totalItems}
                </span>
              )}
            </Link>
          </div>
        </div>
      </div>

      {/* Bottom Nav */}
      <nav className="bg-gray-100 border-t border-gray-200 relative">
        <div className="container mx-auto px-4 flex items-center justify-between">
          {/* Categories Dropdown */}
          <div
            className="relative"
            onMouseEnter={() => setShowCategories(true)}
            onMouseLeave={() => setShowCategories(false)}
          >
            <button className="flex items-center gap-2 bg-blue-600 text-white px-5 py-3 rounded-t-md hover:bg-blue-700 transition">
              <Menu className="w-5 h-5" />
              Shop Categories
              <ChevronDown className="w-4 h-4" />
            </button>

            {/* Dropdown */}
            {showCategories && (
              <div className="absolute left-0 top-full bg-white shadow-lg border w-64 rounded-b-md py-3 z-40">
                {['Electronics', 'Fashion', 'Home & Garden', 'Sports', 'Health & Beauty', 'Toys', 'Automotive'].map((cat, i) => (
                  <Link
                    key={i}
                    href={`/products?category=${cat.toLowerCase().replace(/\s+/g, '-')}`}
                    className="block px-5 py-2 text-gray-700 hover:bg-gray-100 hover:text-blue-600 transition"
                  >
                    {cat}
                  </Link>
                ))}
              </div>
            )}
          </div>

          {/* Main Links */}
          <div className="hidden lg:flex items-center gap-8">
            {['Home', 'Deals', 'New Arrivals', 'Best Sellers', 'Contact'].map((item, i) => (
              <Link
                key={i}
                href={`/${item.toLowerCase().replace(/\s+/g, '-')}`}
                className="py-4 text-gray-700 font-medium hover:text-blue-600 transition"
              >
                {item}
              </Link>
            ))}
          </div>
        </div>
      </nav>
    </header>
  );
}

export default Header;
