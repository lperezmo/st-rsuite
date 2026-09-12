/**
 * Keep an RSuite picker popup anchored to its toggle while the page scrolls.
 *
 * RSuite portals every picker popup to `document.body` as `position:
 * absolute`, positions it once when it opens, and only re-anchors on `window`
 * resize or when the popup itself resizes. Nothing tracks the toggle when a
 * scroll container moves it: Streamlit never scrolls the window, it scrolls
 * `section[data-testid="stMain"]` (and inside dialogs, expanders, and other
 * nested scrollers), so the popup stays at its stale viewport coordinates
 * while the toggle moves away. This hook does what MUI's Popper does, on top
 * of RSuite:
 *
 * - While the popup is open, a capturing `scroll` listener on `document`
 *   catches every scroller on the page (scrolls inside the popup itself are
 *   ignored). Each scroll frame recomputes the
 *   popup position from the toggle's current rect and writes it the same way
 *   RSuite's own forced update does: the `--rs-position-x/y` custom
 *   properties and `data-placement` on the popup element.
 * - The configured placement is kept unless the popup no longer fits on that
 *   side of the toggle and would fit on the opposite side; then it flips
 *   (`bottomStart` to `topStart` and back). RSuite's `autoVertical*`
 *   placements are not used for this because they pick whichever side has
 *   more room, which would make the popup jump sides mid-screen even when
 *   both fit.
 * - When the toggle is scrolled fully out of its visible area the popup is
 *   hidden (not closed, so an in-progress range selection survives) and
 *   parked inside the viewport: an absolutely positioned popup left below
 *   the fold would extend the document and give the window a scrollbar
 *   Streamlit never has.
 *
 * Why the position is computed here rather than through the picker's
 * `updatePosition()` handle: for every picker except InputPicker-based ones,
 * RSuite's state-driven position is never applied to the DOM (the popup
 * render ignores it); only the forced DOM write in its resize listeners
 * moves the element. The math below mirrors RSuite's
 * `calcOverlayPosition` for a `document.body` container, so the two writers
 * agree whenever RSuite's own listeners fire.
 *
 * Wire it into a picker with `ref`, `onOpen`, and `onClose`, and keep passing
 * the configured `placement`.
 */
import { RefObject, useCallback, useEffect, useRef, useState } from "react";
import type { PickerHandle } from "rsuite";

/** The picker props the hook drives. Pass them to the RSuite picker. */
export type AnchoredPopupProps = {
  ref: RefObject<PickerHandle>;
  onOpen: () => void;
  onClose: () => void;
};

export type Rect = { top: number; left: number; bottom: number; right: number };
export type Size = { width: number; height: number };

const CLIPPING_OVERFLOW = new Set(["auto", "scroll", "hidden", "clip"]);

/** The viewport minus any window scrollbar gutter. */
function viewport(): Rect {
  return {
    top: 0,
    left: 0,
    bottom: document.documentElement.clientHeight,
    right: document.documentElement.clientWidth,
  };
}

/**
 * The ancestors of `element` that clip their overflow. Computed once per open
 * popup: the DOM around a toggle does not change while its popup is open, and
 * walking it with getComputedStyle on every scroll frame would force style
 * recalculation for nothing.
 */
function clippingAncestors(element: HTMLElement): HTMLElement[] {
  const found: HTMLElement[] = [];
  let node = element.parentElement;
  while (node && node !== document.body) {
    const style = getComputedStyle(node);
    if (
      CLIPPING_OVERFLOW.has(style.overflowY) ||
      CLIPPING_OVERFLOW.has(style.overflowX)
    ) {
      found.push(node);
    }
    node = node.parentElement;
  }
  return found;
}

/**
 * The area of the viewport in which the toggle can actually be seen: the
 * viewport intersected with every ancestor that clips its overflow.
 */
function visibleArea(ancestors: HTMLElement[]): Rect {
  let area = viewport();
  for (const node of ancestors) {
    const rect = node.getBoundingClientRect();
    area = {
      top: Math.max(area.top, rect.top),
      left: Math.max(area.left, rect.left),
      bottom: Math.min(area.bottom, rect.bottom),
      right: Math.min(area.right, rect.right),
    };
  }
  return area;
}

export function isOutside(anchor: Rect, area: Rect): boolean {
  return (
    anchor.bottom <= area.top ||
    anchor.top >= area.bottom ||
    anchor.right <= area.left ||
    anchor.left >= area.right
  );
}

/** `bottomStart` -> `topStart`, `topEnd` -> `bottomEnd`; anything else unchanged. */
export function flipVertical(placement: string): string {
  if (placement.startsWith("bottom")) return "top" + placement.slice(6);
  if (placement.startsWith("top")) return "bottom" + placement.slice(3);
  return placement;
}

/**
 * Whether a popup of `popup.height` should sit on the opposite side of
 * `anchor` from `placement`. Only vertical placements flip, and only when
 * the configured side no longer fits while the other side does.
 */
export function shouldFlip(
  placement: string,
  anchor: Rect,
  popupHeight: number,
  area: Rect,
): boolean {
  const fitsBelow = anchor.bottom + popupHeight <= area.bottom;
  const fitsAbove = anchor.top - popupHeight >= area.top;
  if (placement.startsWith("bottom")) return !fitsBelow && fitsAbove;
  if (placement.startsWith("top")) return !fitsAbove && fitsBelow;
  return false;
}

/**
 * Resolve RSuite's `auto*` placements the way its `calcAutoPlacement` does
 * against the viewport: the side with the most free space wins.
 */
export function resolveAutoPlacement(
  placement: string,
  anchor: Rect,
  popup: Size,
  area: Rect,
): string {
  if (!placement.startsWith("auto")) return placement;
  const space = {
    top: anchor.top - area.top - popup.height,
    bottom: area.bottom - anchor.bottom - popup.height,
    left: anchor.left - area.left - popup.width,
    right: area.right - anchor.right - popup.width,
  };
  const best = (keys: (keyof typeof space)[]) =>
    keys.reduce((a, b) => (space[b] > space[a] ? b : a));
  if (placement.startsWith("autoVertical")) {
    return best(["top", "bottom"]) + placement.slice("autoVertical".length);
  }
  if (placement.startsWith("autoHorizontal")) {
    return best(["left", "right"]) + placement.slice("autoHorizontal".length);
  }
  // Plain "auto": main axis is the side with the most room, aligned toward
  // the tighter side on the cross axis (RSuite's AutoPlacement table).
  const main = best(["top", "bottom", "left", "right"]);
  // RSuite's minBy keeps the first entry on a tie, which is the Start side.
  if (main === "left" || main === "right") {
    return main + (space.top <= space.bottom ? "Start" : "End");
  }
  return main + (space.left <= space.right ? "Start" : "End");
}

/**
 * Top-left corner of the popup for `placement`, in viewport coordinates.
 * Mirrors RSuite's `calcOverlayPosition` for a `document.body` container,
 * including its RTL mirroring of the Start/End variants.
 */
export function popupOrigin(
  placement: string,
  anchor: Rect,
  popup: Size,
  rtl: boolean,
): { left: number; top: number } {
  const anchorWidth = anchor.right - anchor.left;
  const anchorHeight = anchor.bottom - anchor.top;
  const startLeft = anchor.left;
  const endLeft = anchor.right - popup.width;
  const centerLeft = anchor.left + (anchorWidth - popup.width) / 2;
  const centerTop = anchor.top + (anchorHeight - popup.height) / 2;
  const endTop = anchor.bottom - popup.height;

  switch (placement) {
    case "bottom":
      return { left: centerLeft, top: anchor.bottom };
    case "bottomStart":
      return { left: rtl ? endLeft : startLeft, top: anchor.bottom };
    case "bottomEnd":
      return { left: rtl ? startLeft : endLeft, top: anchor.bottom };
    case "top":
      return { left: centerLeft, top: anchor.top - popup.height };
    case "topStart":
      return {
        left: rtl ? endLeft : startLeft,
        top: anchor.top - popup.height,
      };
    case "topEnd":
      return {
        left: rtl ? startLeft : endLeft,
        top: anchor.top - popup.height,
      };
    case "left":
      return { left: anchor.left - popup.width, top: centerTop };
    case "leftStart":
      return { left: anchor.left - popup.width, top: anchor.top };
    case "leftEnd":
      return { left: anchor.left - popup.width, top: endTop };
    case "right":
      return { left: anchor.right, top: centerTop };
    case "rightStart":
      return { left: anchor.right, top: anchor.top };
    case "rightEnd":
      return { left: anchor.right, top: endTop };
    default:
      return { left: startLeft, top: anchor.bottom };
  }
}

/** `bottomStart` -> `bottom-start`, matching RSuite's `data-placement`. */
export function kebabPlacement(placement: string): string {
  return placement.replace(/[A-Z]/g, (c) => "-" + c.toLowerCase());
}

/** The popup element of an open picker, or null (RSuite throws when closed). */
function overlayOf(handle: PickerHandle | null): HTMLElement | null {
  if (!handle) return null;
  try {
    return handle.overlay ?? null;
  } catch {
    return null;
  }
}

function clamp(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), Math.max(min, max));
}

export function useAnchoredPopup(placement: string): AnchoredPopupProps {
  const ref = useRef<PickerHandle>(null);
  const [open, setOpen] = useState(false);

  // The current open session's scheduler, so the per-render effect below can
  // poke it without re-subscribing anything.
  const scheduleRef = useRef<(() => void) | null>(null);

  const onOpen = useCallback(() => setOpen(true), []);
  const onClose = useCallback(() => setOpen(false), []);

  // A Streamlit rerun re-renders the component without any scroll or resize,
  // yet content above the toggle may have grown or shrunk and moved it. No
  // dependency list: re-check after every render while open. One
  // getBoundingClientRect per rerun.
  useEffect(() => {
    scheduleRef.current?.();
  });

  useEffect(() => {
    if (!open) return;
    let frame = 0;
    let observed: HTMLElement | null = null;
    let ancestors: HTMLElement[] = [];
    let lastWrite = { x: "", y: "", placement: "" };
    let retries = 0;

    const schedule = () => {
      if (!frame) frame = requestAnimationFrame(update);
    };
    scheduleRef.current = schedule;

    // Scrolling inside the popup (a time column, a long listbox) does not
    // move the toggle; skip those instead of re-measuring on every tick.
    const onScroll = (event: Event) => {
      if (
        observed &&
        event.target instanceof Node &&
        observed.contains(event.target)
      ) {
        return;
      }
      schedule();
    };

    // RSuite keeps its own writers: a ResizeObserver on the popup and the
    // window resize listener both re-position from the configured placement
    // and the trigger's current rect. They agree with this hook except when
    // the popup is flipped or parked, so watch the attributes they write and
    // re-apply after any write that is not ours.
    // Both observers run after layout and before paint, so correcting
    // synchronously here (rather than on the next frame) means RSuite's write
    // never reaches the screen. Our own write only re-triggers the mutation
    // callback, which then sees its own values and stops.
    const updateNow = () => {
      if (frame) cancelAnimationFrame(frame);
      update();
    };
    const resizeObserver = new ResizeObserver(updateNow);
    const mutationObserver = new MutationObserver(() => {
      if (!observed) return;
      const same =
        observed.style.getPropertyValue("--rs-position-x") === lastWrite.x &&
        observed.style.getPropertyValue("--rs-position-y") === lastWrite.y &&
        (observed.dataset.placement ?? "") === lastWrite.placement;
      if (!same) updateNow();
    });

    const observe = (anchor: HTMLElement, overlay: HTMLElement) => {
      if (observed === overlay) return;
      resizeObserver.disconnect();
      mutationObserver.disconnect();
      resizeObserver.observe(overlay);
      resizeObserver.observe(anchor);
      mutationObserver.observe(overlay, {
        attributes: true,
        attributeFilter: ["style", "data-placement"],
      });
      observed = overlay;
      ancestors = clippingAncestors(anchor);
    };

    const update = () => {
      frame = 0;
      const handle = ref.current;
      const anchor = handle?.root;
      const overlay = overlayOf(handle);
      // The popup mounts in the same commit that fires onOpen, but be
      // tolerant of a late mount: retry for a few frames, then give up until
      // the next scroll or resize.
      if (!anchor || !overlay) {
        if (retries++ < 30) schedule();
        return;
      }
      retries = 0;
      // Below RSuite's xs breakpoint (576px) the picker renders a full-screen
      // drawer instead of an anchored popup; the same element ref is still
      // populated, but positioning it would displace the drawer's content.
      if (
        overlay.dataset.breakpoint === "xs" ||
        getComputedStyle(overlay).position !== "absolute"
      ) {
        return;
      }
      observe(anchor, overlay);

      const anchorRect = anchor.getBoundingClientRect();
      const area = visibleArea(ancestors);
      const popup = {
        width: overlay.offsetWidth,
        height: overlay.offsetHeight,
      };
      const rtl = document.dir === "rtl";

      let resolved = resolveAutoPlacement(placement, anchorRect, popup, area);
      if (shouldFlip(resolved, anchorRect, popup.height, area)) {
        resolved = flipVertical(resolved);
      }
      let { left, top } = popupOrigin(resolved, anchorRect, popup, rtl);

      const hidden = isOutside(anchorRect, area);
      if (hidden) {
        // Park it inside the viewport so it cannot extend the document.
        const view = viewport();
        left = clamp(left, 0, view.right - popup.width);
        top = clamp(top, 0, view.bottom - popup.height);
      }
      overlay.style.visibility = hidden ? "hidden" : "";

      // Same writes as RSuite's forced update, in document coordinates.
      lastWrite = {
        x: `${left + window.scrollX}px`,
        y: `${top + window.scrollY}px`,
        placement: kebabPlacement(resolved),
      };
      overlay.style.setProperty("--rs-position-x", lastWrite.x);
      overlay.style.setProperty("--rs-position-y", lastWrite.y);
      overlay.dataset.placement = lastWrite.placement;
    };

    document.addEventListener("scroll", onScroll, {
      capture: true,
      passive: true,
    });
    window.addEventListener("resize", schedule);
    schedule();

    return () => {
      scheduleRef.current = null;
      document.removeEventListener("scroll", onScroll, true);
      window.removeEventListener("resize", schedule);
      resizeObserver.disconnect();
      mutationObserver.disconnect();
      if (frame) cancelAnimationFrame(frame);
    };
  }, [open, placement]);

  return { ref, onOpen, onClose };
}
