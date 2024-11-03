'use client';

import { useState, useEffect } from 'react';
import { getStock, type Beer, type Order } from '@/lib/api';
import OrderForm from '@/components/OrderForm';
import OrderList from '@/components/OrderList';

export default function Home() {
  const [beers, setBeers] = useState<Beer[]>([]);
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadStock();
  }, []);

  const loadStock = async () => {
    try {
      setLoading(true);
      const stockData = await getStock();
      setBeers(stockData);
    } catch (err) {
      setError('Failed to load stock');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return (
    <div className="flex items-center justify-center min-h-screen">
      Loading...
    </div>
  );

  if (error) return (
    <div className="flex items-center justify-center min-h-screen text-red-500">
      Error: {error}
    </div>
  );

  return (
    <main className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6">Bar Manager</h1>
      
      {/* Stock Section */}
      <section className="mb-8">
        <h2 className="text-2xl font-bold mb-4">Current Stock</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {beers.map((beer) => (
            <div 
              key={beer.name}
              className="p-4 border rounded-lg bg-white shadow"
            >
              <h3 className="font-bold">{beer.name}</h3>
              <p>Price: ${beer.price}</p>
              <p>Available: {beer.quantity}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Order Creation Section */}
      <OrderForm 
        onOrderCreated={(newOrder) => {
          setOrders(prev => [...prev, newOrder]);
        }} 
      />

      {/* Orders List Section */}
      <section>
        <h2 className="text-2xl font-bold mb-4">Orders</h2>
        {orders.length === 0 ? (
          <p className="text-gray-500">No orders yet. Create one to get started!</p>
        ) : (
          <OrderList 
            orders={orders}
            beers={beers}
            onOrderUpdate={(updatedOrder) => {
              setOrders(prev => 
                prev.map(order => 
                  order.id === updatedOrder.id ? updatedOrder : order
                )
              );
            }}
            loadStock={loadStock}
          />
        )}
      </section>
    </main>
  );
}
