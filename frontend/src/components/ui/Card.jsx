import { motion } from "framer-motion";

function Card({ children, className = "", hover = true, ...props }) {
  return (
    <motion.div
      className={`glass-card ${className}`}
      whileHover={hover ? { y: -2, transition: { duration: 0.2 } } : undefined}
      {...props}
    >
      {children}
    </motion.div>
  );
}

function CardHeader({ children, className = "" }) {
  return <div className={`glass-card-header ${className}`}>{children}</div>;
}

export { Card, CardHeader };
