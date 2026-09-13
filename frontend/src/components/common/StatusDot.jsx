function StatusDot({ label = "Live" }) {
  return (
    <div className="live-status">
      <div className="status-dot-wrapper">
        <div className="status-dot-ring" />
        <div className="status-dot" />
      </div>
      {label}
    </div>
  );
}

export default StatusDot;