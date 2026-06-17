import { Inbox } from "lucide-react";

function EmptyState({ icon, title, description, action }) {
  const Icon = icon || Inbox;

  return (
    <div className="empty-state">
      <div className="empty-state-icon">
        <Icon size={28} />
      </div>
      <h3>{title}</h3>
      <p>{description}</p>
      {action}
    </div>
  );
}

export default EmptyState;
