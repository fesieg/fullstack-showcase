import { BottleWine } from 'lucide-react';
import './App.scss';
import { useEffect, useState } from 'react';
import { Bottle } from './types/Bottle';
import { getUnredeemedBottlesForUser, redeemAllBottlesForUser } from './lib/api';
import { BottleTable } from './components/BottleTable';
import { formatCurrency } from './lib/format';
import { BottleBalanceSection } from './components/BottleBalanceSection';
import { AddBottleForm } from './components/AddBottleForm';

// harcoded user id for dev purposes
const USER_ID = 1;

function App() {
  const [unredeemedBottles, setUnredeemedBottles] = useState<Bottle[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchBottles = async () => {
    try {
      setIsLoading(true);
      const response = await getUnredeemedBottlesForUser(USER_ID);
      setUnredeemedBottles(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load bottles.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchBottles();
  }, []);

  const redeemAllAndNotify = () => {
    redeemAllBottlesForUser(USER_ID)
      .then(response => {
        alert(`Successfully redeemed all bottles for a total of ${formatCurrency(response.data)}`);
        fetchBottles();
      })
      .catch(err => {
        setError('Failed to redeem bottles.');
        console.error(err);
      });
  };

  return (
    <div className="app-container">
      <div className="app-container__header">
        <h1 className="app-container__title">
          Bottle Return System 
          <BottleWine className="bottle-icon" />
        </h1>
      </div>

      <BottleBalanceSection bottles={unredeemedBottles} redeemAll={redeemAllAndNotify} />
      
      <AddBottleForm onBottleAdded={fetchBottles} userId={USER_ID} />
      
      {isLoading && <p>Loading your bottles...</p>}
      {error && <p className="error-message">{error}</p>}
      {!isLoading && !error && (
        <BottleTable bottles={unredeemedBottles} />
      )}
    </div>
  );
}

export default App;