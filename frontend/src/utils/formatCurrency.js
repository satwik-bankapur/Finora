export function formatCurrency(value) {
  const num = Number(value) || 0;
  return `₹${num.toLocaleString('en-IN')}`;
}

export function formatPercent(value, digits = 1) {
  const num = Number(value) || 0;
  return `${num.toFixed(digits)}%`;
}
