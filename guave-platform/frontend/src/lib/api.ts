import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Handle token refresh or redirect to login
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API endpoints
export const productAPI = {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  getAll: (params?: any) => api.get('/products/', { params }),
  getBySlug: (slug: string) => api.get(`/products/${slug}/`),
  getFeatured: () => api.get('/products/featured/'),
  getNewArrivals: () => api.get('/products/new_arrivals/'),
  getBestSelling: () => api.get('/products/best_selling/'),
  getOnSale: () => api.get('/products/on_sale/'),
};

export const categoryAPI = {
  getAll: () => api.get('/categories/'),
  getBySlug: (slug: string) => api.get(`/categories/${slug}/`),
};

export const brandAPI = {
  getAll: () => api.get('/brands/'),
  getBySlug: (slug: string) => api.get(`/brands/${slug}/`),
};