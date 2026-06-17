import { AlertCircle, CheckCircle, AlertTriangle, Info, X } from "lucide-react";

const icons = {
  error: AlertCircle,
  success: CheckCircle,
  warning: AlertTriangle,
  info: Info,
};

function Alert({ type = "info", children, onClose }) {
  const Icon = icons[type] || Info;

  return (
    <div className={`alert alert-${type}`}>
      <Icon size={16} />
      <span style={{ flex: 1 }}>{children}</span>
      {onClose && (
        <button className="toast-close" onClick={onClose}>
          <X size={14} />
        </button>
      )}
    </div>
  );
}

export default Alert;
