// ============================================
// src/components/layout/Footer.tsx
// ============================================

import Link from 'next/link';
import { Facebook, Instagram, Twitter, Youtube, Mail, Phone, MapPin } from 'lucide-react';

export function Footer() {
  return (
    <footer className="bg-gray-900 text-gray-300">
      {/* Newsletter Section */}
      <div className="bg-blue-600 py-8">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-4">
              <Mail className="w-12 h-12 text-white" />
              <div>
                <h3 className="text-white text-xl font-bold">Subscribe to Our Newsletter</h3>
                <p className="text-blue-100">Get 20% off your first order and exclusive deals</p>
              </div>
            </div>
            <div className="flex w-full md:w-auto">
              <input
                type="email"
                placeholder="Enter your email address"
                className="px-4 py-3 w-full md:w-80 rounded-l-lg focus:outline-none"
              />
              <button className="px-6 py-3 bg-gray-900 text-white font-semibold rounded-r-lg hover:bg-gray-800 transition">
                Subscribe
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Footer */}
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8">
          {/* Company Info */}
          <div className="lg:col-span-1">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-xl">E</span>
              </div>
              <span className="text-2xl font-bold text-white">ecomall</span>
            </div>
            <p className="text-sm mb-4">
              Your trusted online destination for quality electronics and more. Shop with confidence.
            </p>
            <div className="space-y-2 text-sm">
              <div className="flex items-center gap-2">
                <MapPin className="w-4 h-4" />
                <span>Nairobi, Kenya</span>
              </div>
              <div className="flex items-center gap-2">
                <Phone className="w-4 h-4" />
                <span>+08 9229 8228</span>
              </div>
              <div className="flex items-center gap-2">
                <Mail className="w-4 h-4" />
                <span>support@ecomall.com</span>
              </div>
            </div>
            <div className="flex gap-4 mt-6">
              <Link href="#" className="w-8 h-8 bg-gray-800 rounded-full flex items-center justify-center hover:bg-blue-600 transition">
                <Facebook className="w-4 h-4" />
              </Link>
              <Link href="#" className="w-8 h-8 bg-gray-800 rounded-full flex items-center justify-center hover:bg-blue-600 transition">
                <Instagram className="w-4 h-4" />
              </Link>
              <Link href="#" className="w-8 h-8 bg-gray-800 rounded-full flex items-center justify-center hover:bg-blue-600 transition">
                <Twitter className="w-4 h-4" />
              </Link>
              <Link href="#" className="w-8 h-8 bg-gray-800 rounded-full flex items-center justify-center hover:bg-blue-600 transition">
                <Youtube className="w-4 h-4" />
              </Link>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-white font-bold mb-4">Quick Links</h3>
            <ul className="space-y-2 text-sm">
              <li><Link href="/about" className="hover:text-white transition">About Us</Link></li>
              <li><Link href="/contact" className="hover:text-white transition">Contact Us</Link></li>
              <li><Link href="/track-order" className="hover:text-white transition">Track Order</Link></li>
              <li><Link href="/returns" className="hover:text-white transition">Returns & Refunds</Link></li>
              <li><Link href="/privacy" className="hover:text-white transition">Privacy Policy</Link></li>
              <li><Link href="/terms" className="hover:text-white transition">Terms & Conditions</Link></li>
            </ul>
          </div>

          {/* Customer Service */}
          <div>
            <h3 className="text-white font-bold mb-4">Customer Service</h3>
            <ul className="space-y-2 text-sm">
              <li><Link href="/help" className="hover:text-white transition">Help Center</Link></li>
              <li><Link href="/shipping" className="hover:text-white transition">Shipping Information</Link></li>
              <li><Link href="/payment" className="hover:text-white transition">Payment Methods</Link></li>
              <li><Link href="/warranty" className="hover:text-white transition">Warranty Information</Link></li>
              <li><Link href="/size-guide" className="hover:text-white transition">Size Guide</Link></li>
              <li><Link href="/faq" className="hover:text-white transition">FAQs</Link></li>
            </ul>
          </div>

          {/* My Account */}
          <div>
            <h3 className="text-white font-bold mb-4">My Account</h3>
            <ul className="space-y-2 text-sm">
              <li><Link href="/account" className="hover:text-white transition">Dashboard</Link></li>
              <li><Link href="/account/orders" className="hover:text-white transition">My Orders</Link></li>
              <li><Link href="/account/wishlist" className="hover:text-white transition">My Wishlist</Link></li>
              <li><Link href="/account/addresses" className="hover:text-white transition">Address Book</Link></li>
              <li><Link href="/account/settings" className="hover:text-white transition">Account Settings</Link></li>
              <li><Link href="/logout" className="hover:text-white transition">Logout</Link></li>
            </ul>
          </div>

          {/* Categories */}
          <div>
            <h3 className="text-white font-bold mb-4">Categories</h3>
            <ul className="space-y-2 text-sm">
              <li><Link href="/products?category=laptops" className="hover:text-white transition">Laptops</Link></li>
              <li><Link href="/products?category=smartphones" className="hover:text-white transition">Smartphones</Link></li>
              <li><Link href="/products?category=headphones" className="hover:text-white transition">Headphones</Link></li>
              <li><Link href="/products?category=cameras" className="hover:text-white transition">Cameras</Link></li>
              <li><Link href="/products?category=gaming" className="hover:text-white transition">Gaming</Link></li>
              <li><Link href="/products?category=accessories" className="hover:text-white transition">Accessories</Link></li>
            </ul>
          </div>
        </div>
      </div>

      {/* Footer Bottom */}
      <div className="border-t border-gray-800">
        <div className="container mx-auto px-4 py-6">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <p className="text-sm">
              © 2024 Ecomall. All Rights Reserved.
            </p>
            <div className="flex items-center gap-4">
              <span className="text-sm">We Accept:</span>
              <div className="flex gap-2">
                <div className="w-12 h-8 bg-white rounded flex items-center justify-center text-xs font-bold">VISA</div>
                <div className="w-12 h-8 bg-white rounded flex items-center justify-center text-xs font-bold">MC</div>
                <div className="w-12 h-8 bg-white rounded flex items-center justify-center text-xs font-bold text-blue-600">PayPal</div>
                <div className="w-12 h-8 bg-green-600 rounded flex items-center justify-center text-xs font-bold text-white">M-PESA</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}

export default Footer;