function Input({ label, error, className = "", ...props }) {
  return (
    <div className="form-group">
      {label && <label className="form-label">{label}</label>}
      <input className={`form-input ${className}`} {...props} />
      {error && <div className="form-error">{error}</div>}
    </div>
  );
}

function Textarea({ label, error, className = "", ...props }) {
  return (
    <div className="form-group">
      {label && <label className="form-label">{label}</label>}
      <textarea className={`form-textarea ${className}`} {...props} />
      {error && <div className="form-error">{error}</div>}
    </div>
  );
}

function Select({ label, error, children, className = "", ...props }) {
  return (
    <div className="form-group">
      {label && <label className="form-label">{label}</label>}
      <select className={`form-select ${className}`} {...props}>
        {children}
      </select>
      {error && <div className="form-error">{error}</div>}
    </div>
  );
}

export { Input, Textarea, Select };
