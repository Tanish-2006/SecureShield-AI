import { motion } from "framer-motion";

const variants = {
  primary: "btn btn-primary",
  secondary: "btn btn-secondary",
  ghost: "btn btn-ghost",
  danger: "btn btn-danger",
};

const sizes = {
  sm: "btn-sm",
  md: "",
  lg: "btn-lg",
};

function Button({ children, variant = "primary", size = "md", icon, href, className = "", ...props }) {
  const cls = `${variants[variant] || variants.primary} ${sizes[size] || ""} ${className}`;

  if (href) {
    return (
      <a href={href} className={cls}>
        {icon && <span>{icon}</span>}
        {children}
      </a>
    );
  }

  return (
    <motion.button
      className={cls}
      whileTap={{ scale: 0.97 }}
      {...props}
    >
      {icon && <span>{icon}</span>}
      {children}
    </motion.button>
  );
}

export default Button;
