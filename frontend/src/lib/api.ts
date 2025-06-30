import axios from 'axios';
import { Bottle } from '@/types/Bottle';

const API_URL = 'http://localhost:8000/api';
const API_TOKEN = import.meta.env.VITE_API_TOKEN || 'error';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${API_TOKEN}`,
  },
});

export const addBottle = (bottle: Omit<Bottle, 'id' | 'added_timestamp' | 'redeemed' | 'deposit_value'>) => {
  const bottleData = {
    ...bottle,
    redeemed: false,
  };
  return apiClient.post<Bottle>('/bottles/', bottleData);
};

export const getAllBottlesForUser = (userId: number) => {
  return apiClient.get<Bottle[]>(`/bottles/${userId}`);
};

export const getUnredeemedBottlesForUser = (userId: number) => {
  return apiClient.get<Bottle[]>(`/bottles/unredeemed/${userId}`);
};

export const getBalanceForUser = (userId: number) => {
  return apiClient.get<number>(`/bottles/balance/${userId}`);
};

export const redeemAllBottlesForUser = (userId: number) => {
  return apiClient.post<number>(`/bottles/redeem/${userId}`);
};

export const validateBarcode = (barcode: string) => {
  return apiClient.post<boolean>(`/bottles/validate_barcode/${barcode}`);
};
