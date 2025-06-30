import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { AxiosResponse } from 'axios';
import App from './App';
import * as api from './lib/api';
import { BottleType } from './types/Bottle';

vi.mock('./lib/api', () => ({
  getUnredeemedBottlesForUser: vi.fn(),
  redeemAllBottlesForUser: vi.fn(),
  addBottle: vi.fn(),
  validateBarcode: vi.fn(),
}));

const mockBottles = [
  {
    id: 1,
    user_id: 1,
    brand: 'Coca-Cola',
    type: BottleType.PLASTIC,
    deposit_value: 0.25,
    barcode: '1234567890',
    added_timestamp: '2024-01-01T00:00:00Z',
    redeemed: false,
  },
  {
    id: 2,
    user_id: 1,
    brand: 'Pepsi',
    type: BottleType.GLASS,
    deposit_value: 0.50,
    barcode: '0987654321',
    added_timestamp: '2024-01-02T00:00:00Z',
    redeemed: false,
  },
];

// helper function to create mock AxiosResponse
function createMockAxiosResponse<T>(data: T): AxiosResponse<T> {
  return {
    data,
    status: 200,
    statusText: 'OK',
    headers: {},
    config: {} as never,
  };
}

describe('App Component - Smoke Tests', () => { 
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders the app title', async () => {
    // mock successful API response
    vi.mocked(api.getUnredeemedBottlesForUser).mockResolvedValue(
      createMockAxiosResponse(mockBottles),
    );

    render(<App />);

    expect(screen.getByText('Bottle Return System')).toBeInTheDocument();
  });

  it('displays loading state initially', () => {
    // mock delayed API response
    vi.mocked(api.getUnredeemedBottlesForUser).mockImplementation(
      () => new Promise(resolve => setTimeout(() => resolve(createMockAxiosResponse([])), 100)),
    );

    render(<App />);

    expect(screen.getByText('Loading your bottles...')).toBeInTheDocument();
  });

  it('displays bottles data after loading', async () => {
    // Mock successful API response
    vi.mocked(api.getUnredeemedBottlesForUser).mockResolvedValue(
      createMockAxiosResponse(mockBottles),
    );

    render(<App />);

    // Wait for loading to complete and bottles to be displayed
    await waitFor(() => {
      expect(screen.queryByText('Loading your bottles...')).not.toBeInTheDocument();
    });

    // check if total value is calculated and displayed correctly
    expect(screen.getByText(/Total Unredeemed Value:/)).toBeInTheDocument();
    expect(screen.getByText('€0.75')).toBeInTheDocument(); // 0.25 + 0.50
  });

  it('displays an error message if API call fails', async () => {
    // mock API failure
    vi.mocked(api.getUnredeemedBottlesForUser).mockRejectedValue(new Error('Network error'));

    render(<App />);

    await waitFor(() => {
      expect(screen.getByText('Failed to load bottles.')).toBeInTheDocument();
    });
  });
});