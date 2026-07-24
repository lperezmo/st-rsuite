/**
 * Teach React 18's JSX types about the `inert` HTML attribute.
 *
 * `inert` is what makes a visually disabled wrapper actually non-interactive:
 * it removes the subtree from the tab order and from hit testing, where
 * `pointer-events: none` blocks the mouse alone. React 19 types it natively;
 * @types/react 18 does not, and this package still targets React 18.
 *
 * Typed as a string (use `inert=""` for on, `undefined` for off) because React
 * 18's DOM layer passes unknown attributes through verbatim only for string
 * values; a boolean would log "Received `true` for a non-boolean attribute".
 */
import "react";

declare module "react" {
  interface HTMLAttributes<T> {
    inert?: string | undefined;
  }
}
