# Priority 1 Features - Implementation Guide

**Timeline:** 8-12 weeks
**Impact:** Transform ClassyCouture into a competitive platform
**Status:** Ready to implement

---

## Table of Contents

1. [Product Management Interface](#1-product-management-interface)
2. [Order Fulfillment Dashboard](#2-order-fulfillment-dashboard)
3. [Marketing & Abandoned Carts](#3-marketing--abandoned-carts)
4. [Shipping Integration](#4-shipping-integration)
5. [Bulk Operations](#5-bulk-operations)

---

## 1. Product Management Interface

**Impact:** Staff spend 70% of time here
**Timeline:** 2-3 weeks
**Priority:** CRITICAL

### Week 1: Basic Product Grid

#### Frontend Component

Create: `frontend/components/admin/ProductManager.tsx`

```typescript
"use client";

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  Package, Plus, Search, Filter, Grid, List,
  Edit, Trash2, AlertCircle, CheckCircle
} from 'lucide-react';

interface Product {
  id: number;
  name: string;
  price: number;
  discounted_price: number;
  image_url: string;
  inventory: number;
  sku: string;
  category_name: string;
  is_in_stock: boolean;
  on_sale: boolean;
  featured: boolean;
}

export default function ProductManager() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [searchQuery, setSearchQuery] = useState('');
  const [filterCategory, setFilterCategory] = useState('all');
  const [selectedProducts, setSelectedProducts] = useState<number[]>([]);

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:8000/api/products/');
      const data = await response.json();
      const results = data?.data?.results || data?.results || data?.data || data;
      setProducts(Array.isArray(results) ? results : []);
    } catch (error) {
      console.error('Error fetching products:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectProduct = (productId: number) => {
    setSelectedProducts(prev =>
      prev.includes(productId)
        ? prev.filter(id => id !== productId)
        : [...prev, productId]
    );
  };

  const handleSelectAll = () => {
    if (selectedProducts.length === filteredProducts.length) {
      setSelectedProducts([]);
    } else {
      setSelectedProducts(filteredProducts.map(p => p.id));
    }
  };

  const filteredProducts = products.filter(product => {
    const matchesSearch = product.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         product.sku?.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = filterCategory === 'all' || product.category_name === filterCategory;
    return matchesSearch && matchesCategory;
  });

  const categories = [...new Set(products.map(p => p.category_name))];

  if (loading) {
    return (
      <Card>
        <CardContent className="p-8">
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <Card className="border shadow-sm">
        <CardHeader className="border-b bg-white">
          <div className="flex items-center justify-between flex-wrap gap-4">
            <div>
              <CardTitle className="text-xl flex items-center gap-2">
                <Package className="h-5 w-5 text-gray-700" />
                Product Management
              </CardTitle>
              <p className="text-sm text-gray-500 mt-1">
                {products.length} products • {selectedProducts.length} selected
              </p>
            </div>
            <div className="flex gap-2">
              <Button variant="outline" onClick={() => window.location.href = '/admin-dashboard'}>
                Back
              </Button>
              <Button>
                <Plus className="h-4 w-4 mr-2" />
                Add Product
              </Button>
            </div>
          </div>
        </CardHeader>
      </Card>

      {/* Filters & Search */}
      <Card className="border shadow-sm">
        <CardContent className="p-4">
          <div className="flex items-center gap-4 flex-wrap">
            {/* Search */}
            <div className="flex-1 min-w-[300px]">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                <Input
                  type="search"
                  placeholder="Search products by name or SKU..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>

            {/* Category Filter */}
            <select
              value={filterCategory}
              onChange={(e) => setFilterCategory(e.target.value)}
              className="px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">All Categories</option>
              {categories.map(cat => (
                <option key={cat} value={cat}>{cat}</option>
              ))}
            </select>

            {/* View Toggle */}
            <div className="flex gap-1 border rounded-md p-1">
              <button
                onClick={() => setViewMode('grid')}
                className={`p-2 rounded ${viewMode === 'grid' ? 'bg-gray-200' : 'hover:bg-gray-100'}`}
              >
                <Grid className="h-4 w-4" />
              </button>
              <button
                onClick={() => setViewMode('list')}
                className={`p-2 rounded ${viewMode === 'list' ? 'bg-gray-200' : 'hover:bg-gray-100'}`}
              >
                <List className="h-4 w-4" />
              </button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Bulk Actions */}
      {selectedProducts.length > 0 && (
        <Card className="border shadow-sm bg-blue-50">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium">
                {selectedProducts.length} product{selectedProducts.length > 1 ? 's' : ''} selected
              </span>
              <div className="flex gap-2">
                <Button variant="outline" size="sm">Edit Selected</Button>
                <Button variant="outline" size="sm">Update Price</Button>
                <Button variant="outline" size="sm">Change Category</Button>
                <Button variant="destructive" size="sm">Delete Selected</Button>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Products Grid/List */}
      {viewMode === 'grid' ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {filteredProducts.map(product => (
            <Card key={product.id} className="border shadow-sm hover:shadow-md transition-shadow">
              <CardContent className="p-4">
                {/* Checkbox */}
                <div className="flex items-start justify-between mb-3">
                  <input
                    type="checkbox"
                    checked={selectedProducts.includes(product.id)}
                    onChange={() => handleSelectProduct(product.id)}
                    className="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                  <div className="flex gap-1">
                    <button className="p-1 hover:bg-gray-100 rounded">
                      <Edit className="h-4 w-4 text-gray-600" />
                    </button>
                    <button className="p-1 hover:bg-gray-100 rounded">
                      <Trash2 className="h-4 w-4 text-red-600" />
                    </button>
                  </div>
                </div>

                {/* Image */}
                <div className="aspect-square bg-gray-100 rounded-lg mb-3 overflow-hidden">
                  <img
                    src={product.image_url}
                    alt={product.name}
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      e.currentTarget.src = 'https://via.placeholder.com/200?text=No+Image';
                    }}
                  />
                </div>

                {/* Info */}
                <h3 className="font-semibold text-gray-900 mb-1 truncate" title={product.name}>
                  {product.name}
                </h3>

                <p className="text-xs text-gray-500 mb-2">SKU: {product.sku || 'N/A'}</p>

                {/* Price */}
                <div className="flex items-center gap-2 mb-2">
                  {product.on_sale ? (
                    <>
                      <span className="text-lg font-bold text-green-600">
                        ${product.discounted_price.toFixed(2)}
                      </span>
                      <span className="text-sm text-gray-500 line-through">
                        ${product.price.toFixed(2)}
                      </span>
                    </>
                  ) : (
                    <span className="text-lg font-bold text-gray-900">
                      ${product.price.toFixed(2)}
                    </span>
                  )}
                </div>

                {/* Stock */}
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-1">
                    {product.inventory > 0 ? (
                      <>
                        <CheckCircle className="h-4 w-4 text-green-600" />
                        <span className={`text-sm ${product.inventory < 10 ? 'text-orange-600 font-semibold' : 'text-gray-600'}`}>
                          {product.inventory} in stock
                        </span>
                      </>
                    ) : (
                      <>
                        <AlertCircle className="h-4 w-4 text-red-600" />
                        <span className="text-sm text-red-600 font-semibold">Out of stock</span>
                      </>
                    )}
                  </div>
                </div>

                {/* Badges */}
                <div className="flex gap-1 mt-2">
                  {product.featured && (
                    <span className="text-xs bg-purple-100 text-purple-700 px-2 py-1 rounded">
                      Featured
                    </span>
                  )}
                  {product.on_sale && (
                    <span className="text-xs bg-red-100 text-red-700 px-2 py-1 rounded">
                      Sale
                    </span>
                  )}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <Card className="border shadow-sm">
          <CardContent className="p-0">
            <table className="w-full">
              <thead className="bg-gray-50 border-b">
                <tr>
                  <th className="p-4 text-left">
                    <input
                      type="checkbox"
                      checked={selectedProducts.length === filteredProducts.length && filteredProducts.length > 0}
                      onChange={handleSelectAll}
                      className="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                    />
                  </th>
                  <th className="p-4 text-left text-sm font-medium text-gray-700">Product</th>
                  <th className="p-4 text-left text-sm font-medium text-gray-700">SKU</th>
                  <th className="p-4 text-left text-sm font-medium text-gray-700">Price</th>
                  <th className="p-4 text-left text-sm font-medium text-gray-700">Stock</th>
                  <th className="p-4 text-left text-sm font-medium text-gray-700">Category</th>
                  <th className="p-4 text-right text-sm font-medium text-gray-700">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y">
                {filteredProducts.map(product => (
                  <tr key={product.id} className="hover:bg-gray-50">
                    <td className="p-4">
                      <input
                        type="checkbox"
                        checked={selectedProducts.includes(product.id)}
                        onChange={() => handleSelectProduct(product.id)}
                        className="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                      />
                    </td>
                    <td className="p-4">
                      <div className="flex items-center gap-3">
                        <img
                          src={product.image_url}
                          alt={product.name}
                          className="w-12 h-12 rounded object-cover"
                          onError={(e) => {
                            e.currentTarget.src = 'https://via.placeholder.com/48?text=No+Image';
                          }}
                        />
                        <div>
                          <p className="font-medium text-gray-900">{product.name}</p>
                          <div className="flex gap-1 mt-1">
                            {product.featured && (
                              <span className="text-xs bg-purple-100 text-purple-700 px-2 py-0.5 rounded">
                                Featured
                              </span>
                            )}
                            {product.on_sale && (
                              <span className="text-xs bg-red-100 text-red-700 px-2 py-0.5 rounded">
                                Sale
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
                    </td>
                    <td className="p-4 text-sm text-gray-600">{product.sku || 'N/A'}</td>
                    <td className="p-4">
                      {product.on_sale ? (
                        <div>
                          <p className="font-semibold text-green-600">${product.discounted_price.toFixed(2)}</p>
                          <p className="text-xs text-gray-500 line-through">${product.price.toFixed(2)}</p>
                        </div>
                      ) : (
                        <p className="font-semibold text-gray-900">${product.price.toFixed(2)}</p>
                      )}
                    </td>
                    <td className="p-4">
                      <div className="flex items-center gap-1">
                        {product.inventory > 0 ? (
                          <>
                            <CheckCircle className="h-4 w-4 text-green-600" />
                            <span className={`text-sm ${product.inventory < 10 ? 'text-orange-600 font-semibold' : 'text-gray-600'}`}>
                              {product.inventory}
                            </span>
                          </>
                        ) : (
                          <>
                            <AlertCircle className="h-4 w-4 text-red-600" />
                            <span className="text-sm text-red-600 font-semibold">0</span>
                          </>
                        )}
                      </div>
                    </td>
                    <td className="p-4 text-sm text-gray-600">{product.category_name}</td>
                    <td className="p-4 text-right">
                      <div className="flex gap-2 justify-end">
                        <button className="p-2 hover:bg-gray-100 rounded">
                          <Edit className="h-4 w-4 text-gray-600" />
                        </button>
                        <button className="p-2 hover:bg-gray-100 rounded">
                          <Trash2 className="h-4 w-4 text-red-600" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </CardContent>
        </Card>
      )}

      {/* Empty State */}
      {filteredProducts.length === 0 && (
        <Card className="border shadow-sm">
          <CardContent className="p-12 text-center">
            <Package className="h-16 w-16 mx-auto mb-4 text-gray-300" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">No products found</h3>
            <p className="text-gray-500 mb-4">
              {searchQuery || filterCategory !== 'all'
                ? 'Try adjusting your filters'
                : 'Get started by adding your first product'}
            </p>
            <Button>
              <Plus className="h-4 w-4 mr-2" />
              Add Product
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
```

#### Update Admin Dashboard

Edit: `frontend/app/admin-dashboard/page.tsx`

Replace the Products tab placeholder with:

```typescript
{activeTab === "products" && <ProductManager />}
```

Add import at top:

```typescript
import ProductManager from '@/components/admin/ProductManager';
```

---

### Week 2-3: Add Product Form & Image Upload

#### Product Form Component

Create: `frontend/components/admin/ProductForm.tsx`

```typescript
"use client";

import React, { useState, useEffect } from 'react';
import { X, Upload, Loader } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface Category {
  id: number;
  name: string;
}

interface ProductFormProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
  editingProduct?: any | null;
}

export default function ProductForm({
  isOpen,
  onClose,
  onSuccess,
  editingProduct
}: ProductFormProps) {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    price: '',
    image_url: '',
    category: '',
    inventory: '0',
    sku: '',
    on_sale: false,
    discount_percent: '0',
    featured: false,
    new_arrival: false
  });
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    fetchCategories();
    if (editingProduct) {
      setFormData({
        name: editingProduct.name,
        description: editingProduct.description,
        price: editingProduct.price,
        image_url: editingProduct.image_url,
        category: editingProduct.category,
        inventory: editingProduct.inventory,
        sku: editingProduct.sku || '',
        on_sale: editingProduct.on_sale,
        discount_percent: editingProduct.discount_percent || '0',
        featured: editingProduct.featured,
        new_arrival: editingProduct.new_arrival
      });
    }
  }, [editingProduct]);

  const fetchCategories = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/categories/');
      const data = await response.json();
      const results = data?.data?.results || data?.results || data?.data || data;
      setCategories(Array.isArray(results) ? results : []);
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  const handleImageUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Option 1: Use Cloudinary (free tier)
    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('upload_preset', 'your_upload_preset'); // Set in Cloudinary dashboard

    try {
      const response = await fetch(
        'https://api.cloudinary.com/v1_1/your_cloud_name/image/upload',
        {
          method: 'POST',
          body: formData
        }
      );
      const data = await response.json();
      setFormData(prev => ({ ...prev, image_url: data.secure_url }));
    } catch (error) {
      console.error('Error uploading image:', error);
      alert('Error uploading image');
    } finally {
      setUploading(false);
    }

    // Option 2: Use backend file storage (implement later)
    // const formData = new FormData();
    // formData.append('image', file);
    // POST to /api/products/upload-image/
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const url = editingProduct
        ? `http://localhost:8000/api/products/${editingProduct.id}/`
        : 'http://localhost:8000/api/products/';

      const method = editingProduct ? 'PUT' : 'POST';

      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        alert(`Product ${editingProduct ? 'updated' : 'created'} successfully!`);
        onSuccess();
        handleClose();
      } else {
        const error = await response.json();
        alert(`Error: ${JSON.stringify(error)}`);
      }
    } catch (error) {
      console.error('Error saving product:', error);
      alert('Error saving product');
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    setFormData({
      name: '',
      description: '',
      price: '',
      image_url: '',
      category: '',
      inventory: '0',
      sku: '',
      on_sale: false,
      discount_percent: '0',
      featured: false,
      new_arrival: false
    });
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <Card className="w-full max-w-4xl max-h-[90vh] overflow-y-auto m-4">
        <CardHeader className="border-b flex flex-row items-center justify-between">
          <CardTitle>
            {editingProduct ? 'Edit Product' : 'Add New Product'}
          </CardTitle>
          <Button variant="ghost" size="icon" onClick={handleClose}>
            <X className="h-5 w-5" />
          </Button>
        </CardHeader>

        <CardContent className="p-6">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Left Column */}
              <div className="space-y-4">
                {/* Product Name */}
                <div>
                  <label className="block text-sm font-medium mb-2">
                    Product Name <span className="text-red-500">*</span>
                  </label>
                  <Input
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    placeholder="e.g., Classic Black Blazer"
                    required
                  />
                </div>

                {/* Description */}
                <div>
                  <label className="block text-sm font-medium mb-2">Description</label>
                  <textarea
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                    placeholder="Detailed product description..."
                    className="w-full px-3 py-2 border rounded-md min-h-[100px] focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                {/* Price */}
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">
                      Price <span className="text-red-500">*</span>
                    </label>
                    <Input
                      type="number"
                      step="0.01"
                      value={formData.price}
                      onChange={(e) => setFormData({ ...formData, price: e.target.value })}
                      placeholder="0.00"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">Inventory</label>
                    <Input
                      type="number"
                      value={formData.inventory}
                      onChange={(e) => setFormData({ ...formData, inventory: e.target.value })}
                      placeholder="0"
                    />
                  </div>
                </div>

                {/* Category & SKU */}
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">
                      Category <span className="text-red-500">*</span>
                    </label>
                    <select
                      value={formData.category}
                      onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                      className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    >
                      <option value="">Select Category</option>
                      {categories.map(cat => (
                        <option key={cat.id} value={cat.id}>{cat.name}</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">SKU</label>
                    <Input
                      value={formData.sku}
                      onChange={(e) => setFormData({ ...formData, sku: e.target.value })}
                      placeholder="e.g., BLZ-001"
                    />
                  </div>
                </div>

                {/* Sale Settings */}
                <div className="border rounded-lg p-4 space-y-3">
                  <div className="flex items-center gap-2">
                    <input
                      type="checkbox"
                      id="on_sale"
                      checked={formData.on_sale}
                      onChange={(e) => setFormData({ ...formData, on_sale: e.target.checked })}
                      className="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                    />
                    <label htmlFor="on_sale" className="text-sm font-medium">
                      On Sale
                    </label>
                  </div>

                  {formData.on_sale && (
                    <div>
                      <label className="block text-sm font-medium mb-2">
                        Discount Percent
                      </label>
                      <Input
                        type="number"
                        min="0"
                        max="100"
                        value={formData.discount_percent}
                        onChange={(e) => setFormData({ ...formData, discount_percent: e.target.value })}
                        placeholder="0"
                      />
                    </div>
                  )}
                </div>

                {/* Flags */}
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <input
                      type="checkbox"
                      id="featured"
                      checked={formData.featured}
                      onChange={(e) => setFormData({ ...formData, featured: e.target.checked })}
                      className="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                    />
                    <label htmlFor="featured" className="text-sm font-medium">
                      Featured Product
                    </label>
                  </div>

                  <div className="flex items-center gap-2">
                    <input
                      type="checkbox"
                      id="new_arrival"
                      checked={formData.new_arrival}
                      onChange={(e) => setFormData({ ...formData, new_arrival: e.target.checked })}
                      className="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                    />
                    <label htmlFor="new_arrival" className="text-sm font-medium">
                      New Arrival
                    </label>
                  </div>
                </div>
              </div>

              {/* Right Column - Image */}
              <div>
                <label className="block text-sm font-medium mb-2">
                  Product Image <span className="text-red-500">*</span>
                </label>

                {/* Image Preview */}
                {formData.image_url ? (
                  <div className="relative aspect-square bg-gray-100 rounded-lg overflow-hidden mb-3">
                    <img
                      src={formData.image_url}
                      alt="Product preview"
                      className="w-full h-full object-cover"
                    />
                    <button
                      type="button"
                      onClick={() => setFormData({ ...formData, image_url: '' })}
                      className="absolute top-2 right-2 p-2 bg-red-500 text-white rounded-full hover:bg-red-600"
                    >
                      <X className="h-4 w-4" />
                    </button>
                  </div>
                ) : (
                  <div className="aspect-square bg-gray-100 rounded-lg border-2 border-dashed border-gray-300 flex items-center justify-center mb-3">
                    <div className="text-center p-6">
                      <Upload className="h-12 w-12 mx-auto mb-3 text-gray-400" />
                      <p className="text-sm text-gray-600 mb-2">
                        {uploading ? 'Uploading...' : 'Click to upload image'}
                      </p>
                      <p className="text-xs text-gray-500">
                        PNG, JPG up to 5MB
                      </p>
                    </div>
                  </div>
                )}

                {/* Upload Button */}
                <div className="space-y-2">
                  <label className="block">
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleImageUpload}
                      className="hidden"
                      disabled={uploading}
                    />
                    <Button
                      type="button"
                      variant="outline"
                      className="w-full"
                      onClick={(e) => e.currentTarget.previousElementSibling?.click()}
                      disabled={uploading}
                    >
                      {uploading ? (
                        <>
                          <Loader className="h-4 w-4 mr-2 animate-spin" />
                          Uploading...
                        </>
                      ) : (
                        <>
                          <Upload className="h-4 w-4 mr-2" />
                          Upload Image
                        </>
                      )}
                    </Button>
                  </label>

                  <p className="text-xs text-gray-500 text-center">or</p>

                  <Input
                    type="url"
                    value={formData.image_url}
                    onChange={(e) => setFormData({ ...formData, image_url: e.target.value })}
                    placeholder="Enter image URL"
                  />
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-3 pt-4 border-t">
              <Button
                type="submit"
                className="flex-1"
                disabled={loading || uploading}
              >
                {loading ? 'Saving...' : editingProduct ? 'Update Product' : 'Create Product'}
              </Button>
              <Button
                type="button"
                variant="outline"
                onClick={handleClose}
                disabled={loading || uploading}
              >
                Cancel
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
```

#### Backend: Enable Product Creation

Edit: `backend/api/views.py`

```python
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    # Change to ModelViewSet for full CRUD
    pass
```

Change to:

```python
from rest_framework.permissions import IsAdminUser, AllowAny

class ProductViewSet(viewsets.ModelViewSet):  # Changed from ReadOnlyModelViewSet
    """
    ViewSet for Product model with full CRUD operations.
    """
    serializer_class = ProductSerializer

    def get_permissions(self):
        """
        Allow anyone to read, but only admins to create/update/delete
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """Filter products based on query parameters."""
        queryset = Product.objects.select_related('category').prefetch_related('reviews')

        # Filter by featured
        featured = self.request.query_params.get('featured')
        if featured and featured.lower() == 'true':
            queryset = queryset.filter(featured=True)

        # Filter by new arrivals
        new_arrivals = self.request.query_params.get('new_arrivals')
        if new_arrivals and new_arrivals.lower() == 'true':
            queryset = queryset.filter(new_arrival=True)

        # Filter by low stock
        low_stock = self.request.query_params.get('low_stock')
        if low_stock and low_stock.lower() == 'true':
            queryset = queryset.filter(inventory__lte=10, inventory__gt=0)

        # Filter by out of stock
        out_of_stock = self.request.query_params.get('out_of_stock')
        if out_of_stock and out_of_stock.lower() == 'true':
            queryset = queryset.filter(inventory=0)

        # Limit results
        limit = self.request.query_params.get('limit')
        if limit:
            try:
                limit = int(limit)
                queryset = queryset[:limit]
            except ValueError:
                pass

        return queryset
```

---

## 2. Order Fulfillment Dashboard

**Timeline:** 2-3 weeks
**Priority:** CRITICAL

### Kanban Board Interface

Create: `frontend/components/admin/OrderFulfillment.tsx`

```typescript
"use client";

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import {
  ShoppingBag, Clock, Package, Truck, CheckCircle,
  Eye, Printer, Mail, MoreVertical
} from 'lucide-react';

interface Order {
  id: number;
  order_id: string;
  user: number;
  total_price: string;
  status: 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled';
  created_at: string;
  items: any[];
  shipping_address: string;
  phone: string;
  user_email?: string;
}

const STATUS_CONFIG = {
  pending: {
    label: 'Pending',
    icon: Clock,
    color: 'bg-yellow-50 border-yellow-200',
    textColor: 'text-yellow-700',
    iconColor: 'text-yellow-600'
  },
  processing: {
    label: 'Processing',
    icon: Package,
    color: 'bg-blue-50 border-blue-200',
    textColor: 'text-blue-700',
    iconColor: 'text-blue-600'
  },
  shipped: {
    label: 'Shipped',
    icon: Truck,
    color: 'bg-purple-50 border-purple-200',
    textColor: 'text-purple-700',
    iconColor: 'text-purple-600'
  },
  delivered: {
    label: 'Delivered',
    icon: CheckCircle,
    color: 'bg-green-50 border-green-200',
    textColor: 'text-green-700',
    iconColor: 'text-green-600'
  },
  cancelled: {
    label: 'Cancelled',
    icon: CheckCircle,
    color: 'bg-gray-50 border-gray-200',
    textColor: 'text-gray-700',
    iconColor: 'text-gray-600'
  }
};

export default function OrderFulfillment() {
  const [orders, setOrders] = useState<Record<string, Order[]>>({
    pending: [],
    processing: [],
    shipped: [],
    delivered: []
  });
  const [loading, setLoading] = useState(true);
  const [draggedOrder, setDraggedOrder] = useState<Order | null>(null);

  useEffect(() => {
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:8000/api/orders/');
      const data = await response.json();
      const ordersList = data?.data?.results || data?.results || data?.data || data || [];

      // Group orders by status
      const grouped: Record<string, Order[]> = {
        pending: [],
        processing: [],
        shipped: [],
        delivered: []
      };

      ordersList.forEach((order: Order) => {
        if (order.status in grouped) {
          grouped[order.status].push(order);
        }
      });

      setOrders(grouped);
    } catch (error) {
      console.error('Error fetching orders:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDragStart = (order: Order) => {
    setDraggedOrder(order);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };

  const handleDrop = async (e: React.DragEvent, newStatus: string) => {
    e.preventDefault();

    if (!draggedOrder) return;

    // Update order status
    try {
      const response = await fetch(`http://localhost:8000/api/orders/${draggedOrder.id}/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: newStatus }),
      });

      if (response.ok) {
        // Refresh orders
        fetchOrders();

        // Send email notification
        if (newStatus === 'shipped') {
          sendShippingEmail(draggedOrder);
        }
      }
    } catch (error) {
      console.error('Error updating order:', error);
    }

    setDraggedOrder(null);
  };

  const sendShippingEmail = async (order: Order) => {
    // TODO: Implement email sending
    console.log('Sending shipping email for order:', order.order_id);
  };

  const printInvoice = (order: Order) => {
    // TODO: Implement invoice printing
    window.print();
  };

  const sendEmail = (order: Order) => {
    // TODO: Open email client or send email
    window.location.href = `mailto:${order.user_email}?subject=Order ${order.order_id}`;
  };

  if (loading) {
    return (
      <Card>
        <CardContent className="p-8">
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <Card className="border shadow-sm">
        <CardHeader className="border-b bg-white">
          <div className="flex items-center justify-between flex-wrap gap-4">
            <div>
              <CardTitle className="text-xl flex items-center gap-2">
                <ShoppingBag className="h-5 w-5 text-gray-700" />
                Order Fulfillment
              </CardTitle>
              <p className="text-sm text-gray-500 mt-1">
                Drag orders between columns to update status
              </p>
            </div>
            <Button onClick={fetchOrders}>
              Refresh
            </Button>
          </div>
        </CardHeader>
      </Card>

      {/* Kanban Board */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {Object.entries(STATUS_CONFIG).filter(([status]) => status !== 'cancelled').map(([status, config]) => (
          <div key={status}>
            <Card className={`border shadow-sm ${config.color}`}>
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <config.icon className={`h-5 w-5 ${config.iconColor}`} />
                    <h3 className={`font-semibold ${config.textColor}`}>
                      {config.label}
                    </h3>
                  </div>
                  <span className={`text-sm font-medium ${config.textColor}`}>
                    {orders[status]?.length || 0}
                  </span>
                </div>
              </CardHeader>
            </Card>

            {/* Drop Zone */}
            <div
              onDragOver={handleDragOver}
              onDrop={(e) => handleDrop(e, status)}
              className="mt-3 min-h-[400px] space-y-3"
            >
              {orders[status]?.map(order => (
                <Card
                  key={order.id}
                  draggable
                  onDragStart={() => handleDragStart(order)}
                  className="border shadow-sm cursor-move hover:shadow-md transition-shadow"
                >
                  <CardContent className="p-4">
                    {/* Order Header */}
                    <div className="flex items-start justify-between mb-3">
                      <div>
                        <p className="font-semibold text-gray-900">
                          {order.order_id}
                        </p>
                        <p className="text-xs text-gray-500">
                          {new Date(order.created_at).toLocaleDateString()}
                        </p>
                      </div>
                      <div className="dropdown">
                        <button className="p-1 hover:bg-gray-100 rounded">
                          <MoreVertical className="h-4 w-4 text-gray-600" />
                        </button>
                      </div>
                    </div>

                    {/* Order Details */}
                    <div className="space-y-2 mb-3">
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-600">Total:</span>
                        <span className="font-semibold text-gray-900">
                          ${parseFloat(order.total_price).toFixed(2)}
                        </span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-600">Items:</span>
                        <span className="text-gray-900">
                          {order.items?.length || 0}
                        </span>
                      </div>
                    </div>

                    {/* Quick Actions */}
                    <div className="flex gap-1">
                      <button
                        onClick={() => window.location.href = `/admin-dashboard/orders/${order.id}`}
                        className="flex-1 p-2 text-xs border rounded hover:bg-gray-50 flex items-center justify-center gap-1"
                      >
                        <Eye className="h-3 w-3" />
                        View
                      </button>
                      <button
                        onClick={() => printInvoice(order)}
                        className="flex-1 p-2 text-xs border rounded hover:bg-gray-50 flex items-center justify-center gap-1"
                      >
                        <Printer className="h-3 w-3" />
                        Print
                      </button>
                      <button
                        onClick={() => sendEmail(order)}
                        className="flex-1 p-2 text-xs border rounded hover:bg-gray-50 flex items-center justify-center gap-1"
                      >
                        <Mail className="h-3 w-3" />
                        Email
                      </button>
                    </div>
                  </CardContent>
                </Card>
              ))}

              {/* Empty State */}
              {orders[status]?.length === 0 && (
                <div className="p-8 text-center text-gray-400">
                  <config.icon className="h-8 w-8 mx-auto mb-2 opacity-50" />
                  <p className="text-sm">No {config.label.toLowerCase()} orders</p>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
```

#### Update Admin Dashboard

Edit: `frontend/app/admin-dashboard/page.tsx`

Add import:
```typescript
import OrderFulfillment from '@/components/admin/OrderFulfillment';
```

Replace Orders tab placeholder with:
```typescript
{activeTab === "orders" && <OrderFulfillment />}
```

---

## 3. Marketing & Abandoned Carts

**Impact:** 40% of revenue potential
**Timeline:** 3-4 weeks
**Priority:** HIGH

### Week 1: Cart Tracking System

#### Backend: Abandoned Cart Model

Edit: `backend/api/models.py`

Add new model:

```python
class AbandonedCart(models.Model):
    """Track abandoned carts for recovery campaigns."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='abandoned_carts')
    cart_items = models.JSONField(help_text="Snapshot of cart items")
    total_value = models.DecimalField(max_digits=10, decimal_places=2)

    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    last_reminder_sent = models.DateTimeField(null=True, blank=True)
    reminder_count = models.IntegerField(default=0)

    # Recovery
    recovered = models.BooleanField(default=False)
    recovered_at = models.DateTimeField(null=True, blank=True)
    recovery_discount_code = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Abandoned Cart - {self.user.username} (${self.total_value})"
```

Create serializer in `backend/api/serializers.py`:

```python
class AbandonedCartSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    hours_since_abandon = serializers.SerializerMethodField()

    class Meta:
        model = AbandonedCart
        fields = '__all__'

    def get_hours_since_abandon(self, obj):
        from django.utils import timezone
        delta = timezone.now() - obj.created_at
        return int(delta.total_seconds() / 3600)
```

Create viewset in `backend/api/views.py`:

```python
class AbandonedCartViewSet(viewsets.ModelViewSet):
    queryset = AbandonedCart.objects.all()
    serializer_class = AbandonedCartSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get all active abandoned carts (not recovered)."""
        carts = self.queryset.filter(recovered=False)
        serializer = self.get_serializer(carts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def send_reminder(self, request, pk=None):
        """Send recovery email to user."""
        cart = self.get_object()

        # Generate discount code if first reminder
        if cart.reminder_count == 0:
            cart.recovery_discount_code = f"RECOVER{cart.id:05d}"

        # Send email (implement with your email service)
        send_cart_recovery_email(cart)

        cart.last_reminder_sent = timezone.now()
        cart.reminder_count += 1
        cart.save()

        return Response({'status': 'reminder sent'})
```

Register in `backend/api/urls.py`:

```python
router.register(r'abandoned-carts', AbandonedCartViewSet)
```

Run migrations:
```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

---

### Week 2-3: Marketing Dashboard

#### Frontend Component

Create: `frontend/components/admin/MarketingDashboard.tsx`

```typescript
"use client";

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import {
  ShoppingCart, Mail, DollarSign, Users,
  Send, RefreshCw, TrendingUp, Clock
} from 'lucide-react';

interface AbandonedCart {
  id: number;
  user_email: string;
  user_name: string;
  total_value: string;
  cart_items: any[];
  created_at: string;
  reminder_count: number;
  last_reminder_sent: string | null;
  hours_since_abandon: number;
  recovery_discount_code: string;
}

export default function MarketingDashboard() {
  const [abandonedCarts, setAbandonedCarts] = useState<AbandonedCart[]>([]);
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState<number | null>(null);

  useEffect(() => {
    fetchAbandonedCarts();
  }, []);

  const fetchAbandonedCarts = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:8000/api/abandoned-carts/active/');
      const data = await response.json();
      setAbandonedCarts(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Error fetching abandoned carts:', error);
    } finally {
      setLoading(false);
    }
  };

  const sendReminder = async (cartId: number) => {
    setSending(cartId);
    try {
      await fetch(`http://localhost:8000/api/abandoned-carts/${cartId}/send_reminder/`, {
        method: 'POST',
      });
      alert('Recovery email sent!');
      fetchAbandonedCarts();
    } catch (error) {
      console.error('Error sending reminder:', error);
      alert('Error sending email');
    } finally {
      setSending(null);
    }
  };

  // Calculate metrics
  const totalValue = abandonedCarts.reduce((sum, cart) => sum + parseFloat(cart.total_value), 0);
  const avgCartValue = abandonedCarts.length > 0 ? totalValue / abandonedCarts.length : 0;
  const recent24h = abandonedCarts.filter(cart => cart.hours_since_abandon <= 24).length;

  if (loading) {
    return (
      <Card>
        <CardContent className="p-8">
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <Card className="border shadow-sm">
        <CardHeader className="border-b bg-white">
          <div className="flex items-center justify-between flex-wrap gap-4">
            <div>
              <CardTitle className="text-xl flex items-center gap-2">
                <Mail className="h-5 w-5 text-gray-700" />
                Marketing & Cart Recovery
              </CardTitle>
              <p className="text-sm text-gray-500 mt-1">
                Recover abandoned carts and boost revenue
              </p>
            </div>
            <Button onClick={fetchAbandonedCarts}>
              <RefreshCw className="h-4 w-4 mr-2" />
              Refresh
            </Button>
          </div>
        </CardHeader>
      </Card>

      {/* Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card className="border shadow-sm">
          <CardContent className="p-6">
            <div className="flex items-center justify-between mb-2">
              <ShoppingCart className="h-8 w-8 text-orange-600" />
            </div>
            <p className="text-sm text-gray-600 mb-1">Abandoned Carts</p>
            <p className="text-3xl font-bold text-gray-900">{abandonedCarts.length}</p>
          </CardContent>
        </Card>

        <Card className="border shadow-sm">
          <CardContent className="p-6">
            <div className="flex items-center justify-between mb-2">
              <DollarSign className="h-8 w-8 text-green-600" />
            </div>
            <p className="text-sm text-gray-600 mb-1">Potential Revenue</p>
            <p className="text-3xl font-bold text-gray-900">${totalValue.toFixed(0)}</p>
          </CardContent>
        </Card>

        <Card className="border shadow-sm">
          <CardContent className="p-6">
            <div className="flex items-center justify-between mb-2">
              <TrendingUp className="h-8 w-8 text-blue-600" />
            </div>
            <p className="text-sm text-gray-600 mb-1">Avg Cart Value</p>
            <p className="text-3xl font-bold text-gray-900">${avgCartValue.toFixed(2)}</p>
          </CardContent>
        </Card>

        <Card className="border shadow-sm">
          <CardContent className="p-6">
            <div className="flex items-center justify-between mb-2">
              <Clock className="h-8 w-8 text-purple-600" />
            </div>
            <p className="text-sm text-gray-600 mb-1">Last 24 Hours</p>
            <p className="text-3xl font-bold text-gray-900">{recent24h}</p>
          </CardContent>
        </Card>
      </div>

      {/* Abandoned Carts List */}
      <Card className="border shadow-sm">
        <CardHeader className="border-b">
          <CardTitle className="text-lg">Active Abandoned Carts</CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          {abandonedCarts.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 border-b">
                  <tr>
                    <th className="p-4 text-left text-sm font-medium text-gray-700">Customer</th>
                    <th className="p-4 text-left text-sm font-medium text-gray-700">Cart Value</th>
                    <th className="p-4 text-left text-sm font-medium text-gray-700">Items</th>
                    <th className="p-4 text-left text-sm font-medium text-gray-700">Time Since</th>
                    <th className="p-4 text-left text-sm font-medium text-gray-700">Reminders</th>
                    <th className="p-4 text-left text-sm font-medium text-gray-700">Discount Code</th>
                    <th className="p-4 text-right text-sm font-medium text-gray-700">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y">
                  {abandonedCarts.map(cart => (
                    <tr key={cart.id} className="hover:bg-gray-50">
                      <td className="p-4">
                        <div>
                          <p className="font-medium text-gray-900">{cart.user_name}</p>
                          <p className="text-sm text-gray-500">{cart.user_email}</p>
                        </div>
                      </td>
                      <td className="p-4">
                        <p className="font-semibold text-gray-900">${parseFloat(cart.total_value).toFixed(2)}</p>
                      </td>
                      <td className="p-4 text-gray-600">
                        {cart.cart_items?.length || 0} items
                      </td>
                      <td className="p-4">
                        <span className={`text-sm ${
                          cart.hours_since_abandon < 1 ? 'text-green-600' :
                          cart.hours_since_abandon < 24 ? 'text-orange-600' :
                          'text-red-600'
                        }`}>
                          {cart.hours_since_abandon < 1 ? 'Just now' :
                           cart.hours_since_abandon < 24 ? `${cart.hours_since_abandon}h ago` :
                           `${Math.floor(cart.hours_since_abandon / 24)}d ago`}
                        </span>
                      </td>
                      <td className="p-4">
                        <span className="text-sm text-gray-600">
                          {cart.reminder_count} sent
                        </span>
                      </td>
                      <td className="p-4">
                        {cart.recovery_discount_code && (
                          <code className="text-xs bg-gray-100 px-2 py-1 rounded">
                            {cart.recovery_discount_code}
                          </code>
                        )}
                      </td>
                      <td className="p-4 text-right">
                        <Button
                          size="sm"
                          onClick={() => sendReminder(cart.id)}
                          disabled={sending === cart.id}
                        >
                          {sending === cart.id ? (
                            'Sending...'
                          ) : (
                            <>
                              <Send className="h-3 w-3 mr-1" />
                              Send Reminder
                            </>
                          )}
                        </Button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="p-12 text-center">
              <ShoppingCart className="h-16 w-16 mx-auto mb-4 text-gray-300" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">No Abandoned Carts</h3>
              <p className="text-gray-500">Great job! All customers completed checkout.</p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Auto-Recovery Schedule Info */}
      <Card className="border shadow-sm bg-blue-50">
        <CardContent className="p-6">
          <div className="flex items-start gap-4">
            <div className="h-12 w-12 bg-blue-100 rounded-lg flex items-center justify-center flex-shrink-0">
              <Clock className="h-6 w-6 text-blue-600" />
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">Automated Recovery Schedule</h3>
              <div className="space-y-1 text-sm text-gray-700">
                <p>• <strong>1 hour:</strong> First reminder with 10% discount code</p>
                <p>• <strong>24 hours:</strong> Second reminder emphasizing limited stock</p>
                <p>• <strong>72 hours:</strong> Final reminder with 15% discount code</p>
              </div>
              <p className="text-xs text-gray-600 mt-3">
                <strong>Note:</strong> Implement automated cron job in backend to schedule these emails
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
```

#### Update Admin Dashboard

Edit: `frontend/app/admin-dashboard/page.tsx`

Add import:
```typescript
import MarketingDashboard from '@/components/admin/MarketingDashboard';
```

Update Promotions tab:
```typescript
{activeTab === "promotions" && <MarketingDashboard />}
```

---

### Week 4: Automated Email Service

Create: `backend/api/email_service.py`

```python
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

def send_cart_recovery_email(abandoned_cart):
    """Send cart recovery email to customer."""

    # Choose template based on reminder count
    if abandoned_cart.reminder_count == 0:
        subject = "You left something in your cart!"
        template = 'emails/cart_recovery_1.html'
    elif abandoned_cart.reminder_count == 1:
        subject = "Still interested? Items selling fast!"
        template = 'emails/cart_recovery_2.html'
    else:
        subject = "Last chance - Extra 15% off!"
        template = 'emails/cart_recovery_3.html'

    context = {
        'user_name': abandoned_cart.user.username,
        'cart_items': abandoned_cart.cart_items,
        'total_value': abandoned_cart.total_value,
        'discount_code': abandoned_cart.recovery_discount_code,
        'cart_url': f"{settings.FRONTEND_URL}/cart"
    }

    html_message = render_to_string(template, context)

    send_mail(
        subject=subject,
        message='',  # Plain text fallback
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[abandoned_cart.user.email],
        html_message=html_message,
        fail_silently=False,
    )
```

Create email templates in `backend/templates/emails/`:

`cart_recovery_1.html`:
```html
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #f8f9fa; padding: 20px; text-align: center; }
        .content { padding: 20px; }
        .cta-button { background: #007bff; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }
        .discount-code { background: #fff3cd; padding: 15px; margin: 15px 0; border-radius: 5px; font-size: 18px; font-weight: bold; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>ClassyCouture</h1>
        </div>
        <div class="content">
            <h2>Hi {{ user_name }},</h2>
            <p>We noticed you left some items in your cart. Don't worry, we saved them for you!</p>

            <div style="border: 1px solid #ddd; padding: 15px; margin: 20px 0;">
                <h3>Your Cart ({{ cart_items|length }} items)</h3>
                <!-- List cart items here -->
                <p><strong>Total: ${{ total_value }}</strong></p>
            </div>

            <div class="discount-code">
                Use code <strong>{{ discount_code }}</strong> for 10% off!
            </div>

            <a href="{{ cart_url }}" class="cta-button">Complete Your Purchase</a>

            <p style="color: #666; font-size: 14px; margin-top: 30px;">
                This offer is valid for 24 hours.
            </p>
        </div>
    </div>
</body>
</html>
```

---

## 4. Shipping Integration

**Impact:** #1 customer concern
**Timeline:** 3-4 weeks
**Priority:** HIGH

### Week 1-2: Shipping Rate Calculator

#### Backend Integration

Install shipping library:
```bash
pip install easypost  # or shippo/shipstation
```

Add to `backend/requirements.txt`:
```
easypost==6.0.0
```

Create: `backend/api/shipping_service.py`

```python
import easypost
from django.conf import settings

easypost.api_key = settings.EASYPOST_API_KEY

def get_shipping_rates(from_address, to_address, weight, dimensions):
    """Get real-time shipping rates from carriers."""

    shipment = easypost.Shipment.create(
        to_address={
            "street1": to_address['street'],
            "city": to_address['city'],
            "state": to_address['state'],
            "zip": to_address['zip'],
            "country": "US"
        },
        from_address={
            "street1": from_address['street'],
            "city": from_address['city'],
            "state": from_address['state'],
            "zip": from_address['zip'],
            "country": "US"
        },
        parcel={
            "weight": weight,  # in ounces
            "length": dimensions['length'],
            "width": dimensions['width'],
            "height": dimensions['height']
        }
    )

    # Return rates from all carriers
    rates = []
    for rate in shipment.rates:
        rates.append({
            'carrier': rate.carrier,
            'service': rate.service,
            'rate': float(rate.rate),
            'delivery_days': rate.delivery_days,
            'rate_id': rate.id
        })

    return sorted(rates, key=lambda x: x['rate'])

def purchase_shipping_label(rate_id):
    """Purchase shipping label."""
    shipment = easypost.Shipment.retrieve(rate_id)
    shipment.buy(rate=rate_id)

    return {
        'label_url': shipment.postage_label.label_url,
        'tracking_code': shipment.tracking_code
    }
```

Create API endpoint in `backend/api/views.py`:

```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .shipping_service import get_shipping_rates, purchase_shipping_label

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def calculate_shipping(request):
    """Calculate shipping rates for order."""
    data = request.data

    rates = get_shipping_rates(
        from_address=settings.WAREHOUSE_ADDRESS,
        to_address=data['shipping_address'],
        weight=data.get('weight', 16),  # Default 1 lb
        dimensions=data.get('dimensions', {'length': 10, 'width': 8, 'height': 4})
    )

    return Response({'rates': rates})

@api_view(['POST'])
@permission_classes([IsAdminUser])
def generate_label(request):
    """Generate shipping label for order."""
    rate_id = request.data.get('rate_id')

    label_data = purchase_shipping_label(rate_id)

    # Update order with tracking
    order_id = request.data.get('order_id')
    order = Order.objects.get(id=order_id)
    order.tracking_number = label_data['tracking_code']
    order.save()

    return Response(label_data)
```

Register in `backend/api/urls.py`:
```python
urlpatterns = [
    path('shipping/calculate/', calculate_shipping, name='calculate-shipping'),
    path('shipping/generate-label/', generate_label, name='generate-label'),
]
```

---

### Week 3: Shipping Dashboard

Create: `frontend/components/admin/ShippingDashboard.tsx`

```typescript
"use client";

import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Truck, Package, Printer, DollarSign } from 'lucide-react';

interface ShippingRate {
  carrier: string;
  service: string;
  rate: number;
  delivery_days: number;
  rate_id: string;
}

export default function ShippingDashboard({ order }: { order: any }) {
  const [rates, setRates] = useState<ShippingRate[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedRate, setSelectedRate] = useState<string | null>(null);

  const calculateRates = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/shipping/calculate/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          shipping_address: {
            street: order.shipping_address.split(',')[0],
            city: 'New York',  // Parse from order
            state: 'NY',
            zip: '10001'
          },
          weight: order.total_weight || 16
        })
      });
      const data = await response.json();
      setRates(data.rates);
    } catch (error) {
      console.error('Error calculating rates:', error);
    } finally {
      setLoading(false);
    }
  };

  const generateLabel = async () => {
    if (!selectedRate) return;

    try {
      const response = await fetch('http://localhost:8000/api/shipping/generate-label/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          rate_id: selectedRate,
          order_id: order.id
        })
      });
      const data = await response.json();

      // Open label in new window
      window.open(data.label_url, '_blank');
      alert(`Label generated! Tracking: ${data.tracking_code}`);
    } catch (error) {
      console.error('Error generating label:', error);
    }
  };

  return (
    <Card className="border shadow-sm">
      <CardHeader className="border-b">
        <CardTitle className="text-lg flex items-center gap-2">
          <Truck className="h-5 w-5" />
          Shipping Options
        </CardTitle>
      </CardHeader>
      <CardContent className="p-6">
        <Button onClick={calculateRates} disabled={loading} className="mb-4">
          {loading ? 'Calculating...' : 'Get Shipping Rates'}
        </Button>

        {rates.length > 0 && (
          <div className="space-y-3">
            {rates.map(rate => (
              <div
                key={rate.rate_id}
                onClick={() => setSelectedRate(rate.rate_id)}
                className={`p-4 border rounded-lg cursor-pointer hover:bg-gray-50 ${
                  selectedRate === rate.rate_id ? 'border-blue-500 bg-blue-50' : ''
                }`}
              >
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-semibold">{rate.carrier} - {rate.service}</p>
                    <p className="text-sm text-gray-600">
                      Delivery in {rate.delivery_days} days
                    </p>
                  </div>
                  <p className="text-lg font-bold">${rate.rate.toFixed(2)}</p>
                </div>
              </div>
            ))}

            <Button
              onClick={generateLabel}
              disabled={!selectedRate}
              className="w-full mt-4"
            >
              <Printer className="h-4 w-4 mr-2" />
              Generate Shipping Label
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
```

---

## 5. Bulk Operations

**Impact:** Saves hours daily
**Timeline:** 2-3 weeks
**Priority:** HIGH

### Week 1-2: Bulk Update API

#### Backend Endpoint

Add to `backend/api/views.py`:

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

@api_view(['POST'])
@permission_classes([IsAdminUser])
def bulk_update_products(request):
    """
    Bulk update products.

    Body:
    {
        "product_ids": [1, 2, 3],
        "updates": {
            "category": 5,  # Optional
            "featured": true,  # Optional
            "price_adjustment": {
                "type": "percent",  # or "fixed"
                "value": 10  # +10% or +$10
            },
            "inventory_adjustment": {
                "type": "add",  # or "set"
                "value": 50
            }
        }
    }
    """
    product_ids = request.data.get('product_ids', [])
    updates = request.data.get('updates', {})

    if not product_ids:
        return Response({'error': 'No products selected'}, status=400)

    products = Product.objects.filter(id__in=product_ids)
    updated_count = 0

    for product in products:
        # Update category
        if 'category' in updates:
            product.category_id = updates['category']

        # Update flags
        if 'featured' in updates:
            product.featured = updates['featured']
        if 'on_sale' in updates:
            product.on_sale = updates['on_sale']

        # Price adjustment
        if 'price_adjustment' in updates:
            adj = updates['price_adjustment']
            if adj['type'] == 'percent':
                product.price = float(product.price) * (1 + adj['value'] / 100)
            elif adj['type'] == 'fixed':
                product.price = float(product.price) + adj['value']
            elif adj['type'] == 'set':
                product.price = adj['value']

        # Inventory adjustment
        if 'inventory_adjustment' in updates:
            adj = updates['inventory_adjustment']
            if adj['type'] == 'add':
                product.inventory += adj['value']
            elif adj['type'] == 'set':
                product.inventory = adj['value']

        product.save()
        updated_count += 1

    return Response({
        'success': True,
        'updated_count': updated_count,
        'message': f'Successfully updated {updated_count} products'
    })

@api_view(['POST'])
@permission_classes([IsAdminUser])
def bulk_delete_products(request):
    """Bulk delete products."""
    product_ids = request.data.get('product_ids', [])

    if not product_ids:
        return Response({'error': 'No products selected'}, status=400)

    deleted_count, _ = Product.objects.filter(id__in=product_ids).delete()

    return Response({
        'success': True,
        'deleted_count': deleted_count,
        'message': f'Successfully deleted {deleted_count} products'
    })
```

Register in `backend/api/urls.py`:
```python
urlpatterns = [
    path('products/bulk-update/', bulk_update_products, name='bulk-update-products'),
    path('products/bulk-delete/', bulk_delete_products, name='bulk-delete-products'),
]
```

---

### Week 2-3: Bulk Actions UI

Create: `frontend/components/admin/BulkActionsModal.tsx`

```typescript
"use client";

import React, { useState } from 'react';
import { X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface BulkActionsModalProps {
  isOpen: boolean;
  onClose: () => void;
  selectedProducts: number[];
  onSuccess: () => void;
}

export default function BulkActionsModal({
  isOpen,
  onClose,
  selectedProducts,
  onSuccess
}: BulkActionsModalProps) {
  const [action, setAction] = useState<'price' | 'inventory' | 'category' | 'flags'>('price');
  const [priceType, setPriceType] = useState<'percent' | 'fixed' | 'set'>('percent');
  const [priceValue, setPriceValue] = useState('');
  const [inventoryType, setInventoryType] = useState<'add' | 'set'>('add');
  const [inventoryValue, setInventoryValue] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);

    const updates: any = {};

    if (action === 'price') {
      updates.price_adjustment = {
        type: priceType,
        value: parseFloat(priceValue)
      };
    } else if (action === 'inventory') {
      updates.inventory_adjustment = {
        type: inventoryType,
        value: parseInt(inventoryValue)
      };
    }

    try {
      const response = await fetch('http://localhost:8000/api/products/bulk-update/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          product_ids: selectedProducts,
          updates
        })
      });

      if (response.ok) {
        const data = await response.json();
        alert(data.message);
        onSuccess();
        onClose();
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Error updating products');
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <Card className="w-full max-w-2xl m-4">
        <CardHeader className="border-b flex flex-row items-center justify-between">
          <CardTitle>Bulk Update {selectedProducts.length} Products</CardTitle>
          <Button variant="ghost" size="icon" onClick={onClose}>
            <X className="h-5 w-5" />
          </Button>
        </CardHeader>

        <CardContent className="p-6 space-y-6">
          {/* Action Type Selector */}
          <div>
            <label className="block text-sm font-medium mb-2">Update Type</label>
            <div className="grid grid-cols-2 gap-2">
              <button
                onClick={() => setAction('price')}
                className={`p-3 border rounded-lg ${action === 'price' ? 'bg-blue-50 border-blue-500' : ''}`}
              >
                Update Prices
              </button>
              <button
                onClick={() => setAction('inventory')}
                className={`p-3 border rounded-lg ${action === 'inventory' ? 'bg-blue-50 border-blue-500' : ''}`}
              >
                Update Inventory
              </button>
            </div>
          </div>

          {/* Price Update */}
          {action === 'price' && (
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">Price Adjustment Type</label>
                <select
                  value={priceType}
                  onChange={(e) => setPriceType(e.target.value as any)}
                  className="w-full px-3 py-2 border rounded-md"
                >
                  <option value="percent">Percentage (+10% or -10%)</option>
                  <option value="fixed">Fixed Amount (+$5 or -$5)</option>
                  <option value="set">Set Price (=$29.99)</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">
                  {priceType === 'percent' ? 'Percentage' : 'Amount'}
                </label>
                <input
                  type="number"
                  step="0.01"
                  value={priceValue}
                  onChange={(e) => setPriceValue(e.target.value)}
                  placeholder={priceType === 'percent' ? '10' : '5.00'}
                  className="w-full px-3 py-2 border rounded-md"
                />
                <p className="text-sm text-gray-500 mt-1">
                  {priceType === 'percent' && 'Positive for increase, negative for decrease'}
                  {priceType === 'fixed' && 'Positive to add, negative to subtract'}
                  {priceType === 'set' && 'New price for all selected products'}
                </p>
              </div>
            </div>
          )}

          {/* Inventory Update */}
          {action === 'inventory' && (
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">Inventory Adjustment Type</label>
                <select
                  value={inventoryType}
                  onChange={(e) => setInventoryType(e.target.value as any)}
                  className="w-full px-3 py-2 border rounded-md"
                >
                  <option value="add">Add/Subtract Quantity</option>
                  <option value="set">Set Quantity</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Quantity</label>
                <input
                  type="number"
                  value={inventoryValue}
                  onChange={(e) => setInventoryValue(e.target.value)}
                  placeholder="50"
                  className="w-full px-3 py-2 border rounded-md"
                />
              </div>
            </div>
          )}

          {/* Actions */}
          <div className="flex gap-3 pt-4 border-t">
            <Button onClick={handleSubmit} className="flex-1" disabled={loading}>
              {loading ? 'Updating...' : 'Apply Changes'}
            </Button>
            <Button variant="outline" onClick={onClose} disabled={loading}>
              Cancel
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
```

Update `ProductManager.tsx` to use bulk actions - add this to the bulk actions section:

```typescript
const [showBulkModal, setShowBulkModal] = useState(false);

// In the bulk actions card:
<Button
  variant="outline"
  size="sm"
  onClick={() => setShowBulkModal(true)}
>
  Bulk Update
</Button>

// At the end of the component:
<BulkActionsModal
  isOpen={showBulkModal}
  onClose={() => setShowBulkModal(false)}
  selectedProducts={selectedProducts}
  onSuccess={() => {
    fetchProducts();
    setSelectedProducts([]);
  }}
/>
```

---

## CSV Import/Export

Add to `backend/api/views.py`:

```python
import csv
from django.http import HttpResponse

@api_view(['GET'])
@permission_classes([IsAdminUser])
def export_products_csv(request):
    """Export all products to CSV."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'SKU', 'Price', 'Inventory', 'Category', 'Featured', 'On Sale'])

    for product in Product.objects.all():
        writer.writerow([
            product.id,
            product.name,
            product.sku,
            product.price,
            product.inventory,
            product.category.name if product.category else '',
            product.featured,
            product.on_sale
        ])

    return response

@api_view(['POST'])
@permission_classes([IsAdminUser])
def import_products_csv(request):
    """Import products from CSV."""
    csv_file = request.FILES.get('file')

    if not csv_file:
        return Response({'error': 'No file uploaded'}, status=400)

    decoded_file = csv_file.read().decode('utf-8').splitlines()
    reader = csv.DictReader(decoded_file)

    created_count = 0
    updated_count = 0

    for row in reader:
        product_id = row.get('ID')

        # Update existing or create new
        if product_id:
            product, created = Product.objects.update_or_create(
                id=product_id,
                defaults={
                    'name': row['Name'],
                    'sku': row['SKU'],
                    'price': row['Price'],
                    'inventory': row['Inventory'],
                    'featured': row['Featured'].lower() == 'true',
                    'on_sale': row['On Sale'].lower() == 'true'
                }
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

    return Response({
        'success': True,
        'created': created_count,
        'updated': updated_count
    })
```

---

## Implementation Timeline Summary

### Month 1 (Weeks 1-4)
- **Week 1:** Product Manager grid component
- **Week 2:** Product Form with image upload
- **Week 3:** Order Fulfillment Kanban board
- **Week 4:** Cart tracking backend

### Month 2 (Weeks 5-8)
- **Week 5:** Marketing Dashboard UI
- **Week 6:** Automated email service
- **Week 7:** Shipping rate calculator
- **Week 8:** Shipping dashboard

### Month 3 (Weeks 9-12)
- **Week 9:** Bulk update API endpoints
- **Week 10:** Bulk actions UI
- **Week 11:** CSV import/export
- **Week 12:** Testing & refinement

---

## Environment Setup

Add to `backend/.env`:

```bash
# Email Service (use Gmail, SendGrid, or Mailgun)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@classycouture.com

# Shipping Service
EASYPOST_API_KEY=your_easypost_api_key

# Warehouse Address
WAREHOUSE_ADDRESS={"street": "123 Main St", "city": "New York", "state": "NY", "zip": "10001"}

# Frontend URL
FRONTEND_URL=http://localhost:3000

# Cloudinary (for image uploads)
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

---

## Success Metrics

After implementing Priority 1 features:

| Metric | Before | After Target |
|--------|--------|--------------|
| **Staff Efficiency** | 5-10 min per product | <1 min per product |
| **Order Processing** | 30-60 min | <5 min |
| **Cart Recovery** | 0% | 15-20% |
| **Shipping Errors** | Manual mistakes | Near 0% |
| **Bulk Operations** | 1 product/min | 100+ products/min |

**Total Impact:**
- Save 10-15 hours/week in staff time
- Recover $5,000-$10,000/month in abandoned carts
- Reduce shipping errors by 95%
- Process orders 10x faster

---

## Next Steps

1. **Start with Product Management** - Biggest daily impact
2. **Add Order Fulfillment** - Critical for customer satisfaction
3. **Implement Marketing** - Immediate revenue boost
4. **Integrate Shipping** - Professional experience
5. **Enable Bulk Ops** - Staff efficiency multiplier

**Ready to implement? Start with section 1 (Product Management Interface) and work through sequentially.**
