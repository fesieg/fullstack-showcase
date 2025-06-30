import { formatCurrency } from '@/lib/format';
import { Bottle } from '@/types/Bottle';
import React, { useMemo } from 'react';
import './BottleBalanceSection.scss';

export const BottleBalanceSection: React.FC<{bottles: Bottle[], redeemAll: () => void}> = ({ bottles, redeemAll }) => {

  const totalUnreedemedValue = useMemo(() => {
    return bottles.reduce((total, bottle) => total + bottle.deposit_value, 0);
  }, [bottles]);

  return <div className="balance-section">
    <div className="balance-section__value">
            Total Unredeemed Value: <strong>{formatCurrency(totalUnreedemedValue)}</strong>
    </div>
    <button 
      className="balance-section__redeem-btn" 
      onClick={() => redeemAll()} 
      disabled={!bottles?.length}
    >
              Redeem {bottles.length} Bottles
    </button>
  </div>;
};