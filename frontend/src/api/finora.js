import axios from 'axios';

const client = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  timeout: 10000,
});

export const postTax = (payload) => client.post('/tax', payload);
export const postInvest = (payload) => client.post('/invest', payload);
