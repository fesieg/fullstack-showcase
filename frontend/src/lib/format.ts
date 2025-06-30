export const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString('de-DE');
};

export const formatCurrency = (amount: number) => {
  return `€${amount.toFixed(2)}`;
};