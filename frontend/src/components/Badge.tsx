import type { ReactNode } from "react";

type BadgeVariant = "type" | "tech" | "phase";

interface BadgeProps {
  variant: BadgeVariant;
  children: ReactNode;
}

const VARIANT_CLASS: Record<BadgeVariant, string> = {
  type: "badge-type",
  tech: "badge-tech",
  phase: "badge-phase",
};

/** Coloured pill used to label a project's type / technology / dev-process
 *  phase. Each variant has its own colour. */
export function Badge({ variant, children }: BadgeProps) {
  return <span className={`badge ${VARIANT_CLASS[variant]}`}>{children}</span>;
}

export default Badge;
