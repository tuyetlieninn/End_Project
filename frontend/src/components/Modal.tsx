import type { ReactNode } from "react";

interface ModalProps {
  open: boolean;
  title: string;
  children: ReactNode;
  onClose: () => void;
  confirmLabel: string;
  onConfirm: () => void;
  confirmDisabled?: boolean;
  /** "destructive" (red) for delete-style confirmations,
   *  "tertiary" (green) for non-destructive confirmations like export. */
  confirmVariant?: "destructive" | "tertiary";
}

/** Generic confirm modal. */
export function Modal({
  open,
  title,
  children,
  onClose,
  confirmLabel,
  onConfirm,
  confirmDisabled = false,
  confirmVariant = "destructive",
}: ModalProps) {
  if (!open) {
    return null;
  }

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div
        className="modal-panel"
        role="dialog"
        aria-modal="true"
        onClick={(event) => event.stopPropagation()}
      >
        <p className="modal-title">{title}</p>
        <div className="modal-body">{children}</div>
        <div className="modal-actions">
          <button type="button" className="button-secondary" onClick={onClose}>
            キャンセル
          </button>
          <button
            type="button"
            className={confirmVariant === "tertiary" ? "button-tertiary" : "button-destructive"}
            onClick={onConfirm}
            disabled={confirmDisabled}
          >
            {confirmLabel}
          </button>
        </div>
      </div>
    </div>
  );
}

export default Modal;
