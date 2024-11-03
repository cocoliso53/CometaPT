import { createOrder, type Order } from '@/lib/api';

type OrderFormProps = {
  onOrderCreated?: (order: Order) => void; 
};

export default function OrderForm({ onOrderCreated }: OrderFormProps) {
  const handleCreateOrder = async () => {
    try {
      const newOrder = await createOrder();
      if (onOrderCreated) {
        onOrderCreated(newOrder);
      } else {
        console.warn('onOrderCreated callback is not provided');
      }
    } catch (error) {
      console.error('Failed to create order:', error);
    }
  };

  return (
    <div className="mb-8">
      <button
        onClick={handleCreateOrder}
        className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
      >
        Create New Order
      </button>
    </div>
  );
}
