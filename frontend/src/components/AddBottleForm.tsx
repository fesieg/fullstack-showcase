import React, { useState } from 'react';
import { Plus, X } from 'lucide-react';
import { BottleType } from '../types/Bottle';
import { addBottle, validateBarcode } from '../lib/api';
import './AddBottleForm.scss';

interface AddBottleFormProps {
  userId: number;
  onBottleAdded: () => void;
}

export const AddBottleForm: React.FC<AddBottleFormProps> = ({ userId, onBottleAdded }) => {
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    brand: '',
    type: BottleType.PLASTIC,
    barcode: '',
  });
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsSubmitting(true);

    if (!formData.brand.trim() || !formData.barcode.trim()) {
      setError('Brand and barcode are required.');
      setIsSubmitting(false);
      return;
    }

    try {
      // barcode validation
      const barcodeCheck = await validateBarcode(formData.barcode);
      if (!barcodeCheck.data) {
        setError('This barcode already exists.');
        setIsSubmitting(false);
        return;
      }

      await addBottle({
        user_id: userId,
        brand: formData.brand.trim(),
        type: formData.type,
        barcode: formData.barcode.trim(),
      });
      
      setFormData({ brand: '', type: BottleType.PLASTIC, barcode: '' });
      setShowForm(false);
      onBottleAdded();
      
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    } catch (err: any) {
      setError(err.response?.status === 409 ? 'Barcode already exists.' : 'Failed to add bottle.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const closeForm = () => {
    setShowForm(false);
    setError(null);
    setFormData({ brand: '', type: BottleType.PLASTIC, barcode: '' });
  };

  return (
    <div className="add-bottle-section">
      <button className="add-bottle-btn" onClick={() => setShowForm(true)} disabled={showForm}>
        <Plus className="add-bottle-btn__icon" />
        Add New Bottle
      </button>

      {showForm && (
        <div className="modal" onClick={closeForm}>
          <form className="form" onClick={(e) => e.stopPropagation()} onSubmit={handleSubmit}>
            <div className="form__header">
              <h3>Add New Bottle</h3>
              <button type="button" onClick={closeForm}><X /></button>
            </div>

            {error && <div className="form__error">{error}</div>}

            <input
              type="text"
              placeholder="Brand"
              value={formData.brand}
              onChange={(e) => setFormData({ ...formData, brand: e.target.value })}
              required
            />

            <input
              type="text"
              placeholder="Barcode"
              value={formData.barcode}
              onChange={(e) => setFormData({ ...formData, barcode: e.target.value })}
              required
            />

            <select
              value={formData.type}
              onChange={(e) => setFormData({ ...formData, type: e.target.value as BottleType })}
            >
              {Object.values(BottleType).map(type => (
                <option key={type} value={type}>
                  {type.charAt(0).toUpperCase() + type.slice(1)}
                </option>
              ))}
            </select>

            <div className="form__actions">
              <button type="button" onClick={closeForm}>Cancel</button>
              <button type="submit" disabled={isSubmitting}>
                {isSubmitting ? 'Adding...' : 'Add Bottle'}
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
};