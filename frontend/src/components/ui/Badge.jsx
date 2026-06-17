const severityMap = {
  CRITICAL: "badge-critical",
  HIGH: "badge-high",
  MEDIUM: "badge-medium",
  LOW: "badge-low",
};

function Badge({ children, variant = "", severity, className = "" }) {
  const cls = severity ? severityMap[severity] || "" : variant ? `badge-${variant}` : "";
  return <span className={`badge ${cls} ${className}`}>{children}</span>;
}

export { Badge, severityMap };
