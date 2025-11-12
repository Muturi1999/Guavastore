// import { Product, ProductVariant } from '@/types/product';
// import { create } from 'zustand';
// import { persist } from 'zustand/middleware';

// interface CartItem {
//   [x: string]: ReactNode;
// //   [x: string]: ReactNode;
//   id: string;
//   product: Product;
//   variant: ProductVariant | null;
//   quantity: number;
//   price: number;
// }

// interface CartStore {
//   items: CartItem[];
//   addItem: (product: Product, variant: ProductVariant | null, quantity: number) => void;
//   removeItem: (itemId: string) => void;
//   updateQuantity: (itemId: string, quantity: number) => void;
//   clearCart: () => void;
//   getTotalItems: () => number;
//   getTotalPrice: () => number;
// }

// export const useCartStore = create<CartStore>()(
//   persist(
//     (set, get) => ({
//       items: [],
      
//       addItem: (product, variant, quantity) => {
//         const items = get().items;
//         const existingItemIndex = items.findIndex(
//           item => item.product.id === product.id && 
//           item.variant?.id === variant?.id
//         );

//         if (existingItemIndex > -1) {
//           // Update quantity if item exists
//           const newItems = [...items];
//           newItems[existingItemIndex].quantity += quantity;
//           set({ items: newItems });
//         } else {
//           // Add new item
//           const newItem: CartItem = {
//             id: `${product.id}-${variant?.id || 'no-variant'}`,
//             product,
//             variant,
//             quantity,
//             price: parseFloat(variant?.price || product.price),
//           };
//           set({ items: [...items, newItem] });
//         }
//       },

//       removeItem: (itemId) => {
//         set({ items: get().items.filter(item => item.id !== itemId) });
//       },

//       updateQuantity: (itemId, quantity) => {
//         const items = get().items;
//         const itemIndex = items.findIndex(item => item.id === itemId);
//         if (itemIndex > -1) {
//           const newItems = [...items];
//           newItems[itemIndex].quantity = quantity;
//           set({ items: newItems });
//         }
//       },

//       clearCart: () => set({ items: [] }),

//       getTotalItems: () => {
//         return get().items.reduce((total, item) => total + item.quantity, 0);
//       },

//       getTotalPrice: () => {
//         return get().items.reduce((total, item) => {
//           return total + (item.price * item.quantity);
//         }, 0);
//       },
//     }),
//     {
//       name: 'cart-storage',
//     }
//   )
// );

import { Product, ProductVariant } from '@/types/product';
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface CartItem {
  id: string;
  product: Product;
  variant: ProductVariant | null;
  quantity: number;
  price: number;
}

interface CartStore {
  items: CartItem[];
  addItem: (product: Product, variant: ProductVariant | null, quantity: number) => void;
  removeItem: (itemId: string) => void;
  updateQuantity: (itemId: string, quantity: number) => void;
  clearCart: () => void;
  getTotalItems: () => number;
  getTotalPrice: () => number;
}

export const useCartStore = create<CartStore>()(
  persist(
    (set, get) => ({
      items: [],

      addItem: (product, variant, quantity) => {
        const items = get().items;
        const existingItemIndex = items.findIndex(
          item => item.product.id === product.id && item.variant?.id === variant?.id
        );

        if (existingItemIndex > -1) {
          const newItems = [...items];
          newItems[existingItemIndex].quantity += quantity;
          set({ items: newItems });
        } else {
          const newItem: CartItem = {
            id: `${product.id}-${variant?.id || 'no-variant'}`,
            product,
            variant,
            quantity,
            price: parseFloat(variant?.price || product.price),
          };
          set({ items: [...items, newItem] });
        }
      },

      removeItem: (itemId) => {
        set({ items: get().items.filter(item => item.id !== itemId) });
      },

      updateQuantity: (itemId, quantity) => {
        const items = get().items;
        const itemIndex = items.findIndex(item => item.id === itemId);
        if (itemIndex > -1) {
          const newItems = [...items];
          newItems[itemIndex].quantity = quantity;
          set({ items: newItems });
        }
      },

      clearCart: () => set({ items: [] }),

      getTotalItems: () => {
        return get().items.reduce((total, item) => total + item.quantity, 0);
      },

      getTotalPrice: () => {
        return get().items.reduce((total, item) => total + (item.price * item.quantity), 0);
      },
    }),
    {
      name: 'cart-storage',
    }
  )
);
