export enum BottleType {
    PLASTIC = 'plastic',
    GLASS = 'glass',
    METAL = 'metal',
}

export interface Bottle {
    id?: number;
    user_id: number;
    type: BottleType;
    brand: string;
    deposit_value: number;
    barcode: string;
    added_timestamp: string; // ISO 8601 format
    redeemed: boolean;
}
