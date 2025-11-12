// 'use client';

// import { FC } from 'react';
// import Link from 'next/link';
// import { useCartStore } from '@/store/cartStore';
// import { Button } from '@/components/ui/button';

// export const MiniCart: FC = () => {
//   const cartItems = useCartStore((state) => state.items);
//   const totalItems = useCartStore((state) => state.getTotalItems());
//   const totalPrice = useCartStore((state) => state.getTotalPrice());

//   if (cartItems.length === 0) {
//     return (
//       <div className="absolute right-0 mt-2 w-80 bg-white border shadow-lg rounded-lg p-4 z-50">
//         <p className="text-center text-gray-500">Your cart is empty.</p>
//       </div>
//     );
//   }

//   return (
//     <div className="absolute right-0 mt-2 w-80 bg-white border shadow-lg rounded-lg p-4 z-50">
//       <h3 className="text-lg font-semibold mb-4">My Cart ({totalItems})</h3>
//       <ul className="divide-y divide-gray-200 max-h-64 overflow-y-auto">
//         {cartItems.map((item) => (
//           <li key={item.id} className="flex justify-between py-2">
//             <div>
//               <p className="font-medium">{item.name}</p>
//               <p className="text-sm text-gray-500">
//                 {item.quantity} x ${item.price.toFixed(2)}
//               </p>
//             </div>
//             <p className="font-semibold">${(item.quantity * item.price).toFixed(2)}</p>
//           </li>
//         ))}
//       </ul>
//       <div className="mt-4 flex justify-between items-center font-semibold text-gray-900">
//         <span>Total:</span>
//         <span>${totalPrice.toFixed(2)}</span>
//       </div>
//       <div className="mt-4 flex gap-2">
//         <Link href="/cart" className="flex-1">
//           <Button className="w-full bg-blue-600 hover:bg-blue-700 text-white">
//             View Cart
//           </Button>
//         </Link>
//         <Link href="/checkout" className="flex-1">
//           <Button className="w-full bg-green-600 hover:bg-green-700 text-white">
//             Checkout
//           </Button>
//         </Link>
//       </div>
//     </div>
//   );
// };

'use client';

import { FC } from 'react';
import Link from 'next/link';
import { useCartStore } from '@/store/cartStore';
import { Button } from '@/components/ui/button';

export const MiniCart: FC = () => {
  const cartItems = useCartStore((state) => state.items);
  const totalItems = useCartStore((state) => state.getTotalItems());
  const totalPrice = useCartStore((state) => state.getTotalPrice());

  if (cartItems.length === 0) {
    return (
      <div className="absolute right-0 mt-2 w-80 bg-white border shadow-lg rounded-lg p-4 z-50">
        <p className="text-center text-gray-500">Your cart is empty.</p>
      </div>
    );
  }

  return (
    <div className="absolute right-0 mt-2 w-80 bg-white border shadow-lg rounded-lg p-4 z-50">
      <h3 className="text-lg font-semibold mb-4">My Cart ({totalItems})</h3>
      <ul className="divide-y divide-gray-200 max-h-64 overflow-y-auto">
        {cartItems.map((item) => (
          <li key={item.id} className="flex justify-between py-2">
            <div>
              <p className="font-medium">{item.product.name}</p>
              <p className="text-sm text-gray-500">
                {item.quantity} x ${item.price.toFixed(2)}
              </p>
            </div>
            <p className="font-semibold">${(item.quantity * item.price).toFixed(2)}</p>
          </li>
        ))}
      </ul>
      <div className="mt-4 flex justify-between items-center font-semibold text-gray-900">
        <span>Total:</span>
        <span>${totalPrice.toFixed(2)}</span>
      </div>
      <div className="mt-4 flex gap-2">
        <Link href="/cart" className="flex-1">
          <Button className="w-full bg-blue-600 hover:bg-blue-700 text-white">
            View Cart
          </Button>
        </Link>
        <Link href="/checkout" className="flex-1">
          <Button className="w-full bg-green-600 hover:bg-green-700 text-white">
            Checkout
          </Button>
        </Link>
      </div>
    </div>
  );
};
