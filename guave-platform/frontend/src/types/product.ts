export interface Product {
  id: string;
  name: string;
  slug: string;
  sku: string;
  category_name: string;
  brand_name: string;
  price: string;
  compare_price: string | null;
  discount_percentage: number;
  stock_status: 'in_stock' | 'low_stock' | 'out_of_stock' | 'pre_order' | 'coming_soon';
  main_image: string | null;
  average_rating: number;
  review_count: number;
  is_featured: boolean;
  is_new: boolean;
  badges: Badge[];
}

export interface ProductDetail extends Product {
  category: Category;
  brand: Brand;
  short_description: string;
  description: string;
  images: ProductImage[];
  specifications: ProductSpecification[];
  variants: ProductVariant[];
  weight: string | null;
  dimensions: string | null;
  views_count: number;
  sales_count: number;
}

export interface Category {
  id: string;
  name: string;
  slug: string;
  description: string;
  image: string | null;
  banner_image: string | null;
  icon: string | null;
  product_count: number;
  children: Category[];
}

export interface Brand {
  id: string;
  name: string;
  slug: string;
  logo: string | null;
  product_count: number;
}

export interface ProductImage {
  id: string;
  image: string;
  alt_text: string;
  is_main: boolean;
  display_order: number;
}

export interface ProductSpecification {
  id: string;
  name: string;
  value: string;
  display_order: number;
}

export interface ProductVariant {
  id: string;
  sku: string;
  attributes: AttributeValue[];
  price: string | null;
  stock_quantity: number;
  image: string | null;
  is_active: boolean;
}

export interface AttributeValue {
  id: string;
  attribute_name: string;
  attribute_type: string;
  value: string;
  color_code: string;
}

export interface Badge {
  id: string;
  name: string;
  badge_type: string;
  text: string;
  background_color: string;
  text_color: string;
  position: string;
}