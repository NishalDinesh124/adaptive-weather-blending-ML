function Metric({ icon: Icon, label, value, confidence }) {
  return (
    <div className="metric">
      <div className="metric-icon">
        <Icon size={16} />
      </div>

      <span>{label}</span>
      <strong>{value}</strong>

      {confidence && (
        <small>Confidence {confidence}</small>
      )}
    </div>
  );
}

export default Metric;