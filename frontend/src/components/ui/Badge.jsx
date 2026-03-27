function Badge({ children, tone = 'neutral' }) {
  const colors = {
    positive: { color: 'var(--positive)', border: 'var(--positive)' },
    negative: { color: 'var(--negative)', border: 'var(--negative)' },
    neutral: { color: 'var(--text-secondary)', border: 'var(--border-subtle)' },
  };
  const toneColors = colors[tone] || colors.neutral;
  return (
    <span
      className="badge"
      style={{
        color: toneColors.color,
        borderColor: toneColors.border,
      }}
    >
      {children}
    </span>
  );
}

export default Badge;
