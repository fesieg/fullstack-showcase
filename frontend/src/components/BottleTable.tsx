import React from 'react';
import { Bottle } from '@/types/Bottle';
import './BottleTable.scss';
import { formatCurrency, formatDate } from '@/lib/format';

interface BottleTableProps {
  bottles: Bottle[];
}

export const BottleTable: React.FC<BottleTableProps> = ({ bottles }) => {
  return (
    <div className="bottle-table">
      <h2 className="bottle-table__title">Your Unredeemed Bottles</h2>
      
      {bottles.length === 0 ? (
        <p className="bottle-table__empty">You have no unredeemed bottles.</p>
      ) : (
        <table className="bottle-table__table">
          <thead className="bottle-table__header">
            <tr className="bottle-table__row bottle-table__row--header">
              <th className="bottle-table__cell bottle-table__cell--header">Brand</th>
              <th className="bottle-table__cell bottle-table__cell--header">Type</th>
              <th className="bottle-table__cell bottle-table__cell--header">Value</th>
              <th className="bottle-table__cell bottle-table__cell--header">Barcode</th>
              <th className="bottle-table__cell bottle-table__cell--header">Added</th>
            </tr>
          </thead>
          <tbody className="bottle-table__body">
            {bottles.map((bottle) => (
              <tr key={bottle.id} className="bottle-table__row">
                <td className="bottle-table__cell">{bottle.brand}</td>
                <td className="bottle-table__cell bottle-table__cell--type">
                  {bottle.type}
                </td>
                <td className="bottle-table__cell bottle-table__cell--deposit">
                  {formatCurrency(bottle.deposit_value)}
                </td>
                <td className="bottle-table__cell bottle-table__cell--barcode">
                  {bottle.barcode}
                </td>
                <td className="bottle-table__cell bottle-table__cell--date">
                  {formatDate(bottle.added_timestamp)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};