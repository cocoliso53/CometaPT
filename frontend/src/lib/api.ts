const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export type Beer = {
  name: string;
  price: number;
  quantity: number;
}

export type Order = {
  id: number;
  created: string;
  paid: boolean;
  subtotal: number;
  taxes: number;
  discounts: number;
  total: number;
  rounds: Round[];
}

export type Round = {
  created: string;
  items: { name: string; quantity: number; }[];
}

// API call functions
export const getStock = async (): Promise<Beer[]> => {
  const response = await fetch(`${API_URL}/stock`);
  const data = await response.json();
  return data.beers;
};

export const createOrder = async (): Promise<Order> => {
  const response = await fetch(`${API_URL}/orders`, {
    method: 'POST'
  });
  return response.json();
};

export const addRound = async (orderId: number, items: { name: string; quantity: number; }[]): Promise<Order> => {
  const response = await fetch(`${API_URL}/orders/${orderId}/rounds`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ items }),
  });
  return response.json();
};

export const payOrder = async (orderId: number): Promise<Order> => {
  const response = await fetch(`${API_URL}/orders/${orderId}/pay`, {
    method: 'POST'
  });
  return response.json();
};