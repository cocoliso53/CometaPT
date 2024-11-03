import { useState } from 'react';
import { addRound, payOrder, type Order, type Beer } from '@/lib/api';

type OrderListProps = {
  orders: Order[];
  beers: Beer[];
  onOrderUpdate: (order: Order) => void;
  loadStock: () => void; // Añadir loadStock a las props
};

export default function OrderList({ orders = [], beers = [], onOrderUpdate, loadStock }: OrderListProps) {
  const [selectedBeers, setSelectedBeers] = useState<{ name: string; quantity: number; }[]>([]);
  const [expandedOrder, setExpandedOrder] = useState<number | null>(null);

  const handleAddRound = async (orderId: number) => {
    if (!selectedBeers.length) return;

    try {
      const updatedOrder = await addRound(orderId, selectedBeers);
      onOrderUpdate(updatedOrder);
      setSelectedBeers([]);
      loadStock(); // Actualizar el stock después de agregar la ronda
    } catch (err) {
      console.error('Failed to add round:', err);
    }
  };

  const handlePayOrder = async (orderId: number) => {
    try {
      const updatedOrder = await payOrder(orderId);
      onOrderUpdate(updatedOrder);
    } catch (err) {
      console.error('Failed to pay order:', err);
    }
  };

  return (
    <div className="space-y-4">
      {orders.map((order) => (
        <div 
          key={order.id}
          className="border rounded-lg p-4 bg-white shadow"
        >
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-xl font-bold">
              Order #{order.id} - {order.paid ? 'Paid' : 'Open'}
            </h3>
            <button
              onClick={() => setExpandedOrder(
                expandedOrder === order.id ? null : order.id
              )}
              className="text-blue-500 hover:text-blue-700"
            >
              {expandedOrder === order.id ? 'Hide Details' : 'Show Details'}
            </button>
          </div>

          {expandedOrder === order.id && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>Subtotal: ${order.subtotal}</div>
                <div>Taxes: ${order.taxes}</div>
                <div>Discounts: ${order.discounts}</div>
                <div className="font-bold">Total: ${order.total}</div>
              </div>

              {!order.paid && (
                <div className="space-y-4 mt-4">
                  <div className="grid grid-cols-2 gap-4">
                    {beers.map((beer) => (
                      <div key={beer.name} className="flex items-center space-x-2">
                        <span>{beer.name}</span>
                        <input
                          type="number"
                          min="0"
                          value={
                            selectedBeers.find(b => b.name === beer.name)?.quantity || 0
                          }
                          onChange={(e) => {
                            const quantity = parseInt(e.target.value) || 0;
                            setSelectedBeers(prev => {
                              const existing = prev.filter(b => b.name !== beer.name);
                              return quantity > 0 
                                ? [...existing, { name: beer.name, quantity }]
                                : existing;
                            });
                          }}
                          className="w-20 px-2 py-1 border rounded"
                        />
                      </div>
                    ))}
                  </div>

                  <div className="flex space-x-4">
                    <button
                      onClick={() => handleAddRound(order.id)}
                      className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
                    >
                      Add Round
                    </button>
                    <button
                      onClick={() => handlePayOrder(order.id)}
                      className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                    >
                      Pay Order
                    </button>
                  </div>
                </div>
              )}

              <div className="mt-4">
                <h4 className="font-bold mb-2">Rounds:</h4>
                {order.rounds?.map((round, index) => (
                  <div key={index} className="border-t pt-2">
                    <div className="text-sm text-gray-600">{round.created}</div>
                    {round.items?.map((item, itemIndex) => (
                      <div key={itemIndex}>
                        {item.quantity}x {item.name}
                      </div>
                    ))}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
