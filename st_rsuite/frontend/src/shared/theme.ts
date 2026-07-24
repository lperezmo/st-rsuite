/**
 * Shared theme bridge: Streamlit CSS custom properties → RSuite theme mode.
 *
 * RSuite's CustomProvider accepts a "theme" prop of "light" | "dark" | "high-contrast".
 * We detect Streamlit's dark/light mode and pass the appropriate value.
 */

function getCSSVar(element: Element, name: string, fallback: string): string {
  const val = getComputedStyle(element).getPropertyValue(name).trim();
  return val || fallback;
}

function isDarkBackground(bgColor: string): boolean {
  let r = 0,
    g = 0,
    b = 0;

  const rgbMatch = bgColor.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
  if (rgbMatch) {
    r = parseInt(rgbMatch[1]);
    g = parseInt(rgbMatch[2]);
    b = parseInt(rgbMatch[3]);
  } else if (bgColor.startsWith("#")) {
    const hex = bgColor.replace("#", "");
    const fullHex =
      hex.length === 3
        ? hex
            .split("")
            .map((c) => c + c)
            .join("")
        : hex;
    r = parseInt(fullHex.slice(0, 2), 16);
    g = parseInt(fullHex.slice(2, 4), 16);
    b = parseInt(fullHex.slice(4, 6), 16);
  } else {
    return false;
  }

  const toLinear = (c: number) => {
    const v = c / 255;
    return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
  };
  const lum =
    0.2126 * toLinear(r) + 0.7152 * toLinear(g) + 0.0722 * toLinear(b);
  return lum < 0.5;
}

function detectDarkMode(element: Element): boolean {
  // Streamlit spreads its --st-* custom properties onto a per-component wrapper
  // div, never onto document.documentElement, and CSS custom properties only
  // inherit downward. The component's own element is therefore the only place
  // the variable is readable; reading the document root always yields "".
  const bgVar = getCSSVar(element, "--st-background-color", "");
  if (bgVar) return isDarkBackground(bgVar);

  const bgComputed = getComputedStyle(document.body).backgroundColor;
  if (bgComputed && bgComputed !== "rgba(0, 0, 0, 0)") {
    return isDarkBackground(bgComputed);
  }

  return window.matchMedia("(prefers-color-scheme: dark)").matches;
}

/**
 * RSuite theme mode for Streamlit's current appearance, read from the calling
 * component's own element.
 *
 * Deliberately uncached. The previous module-level cache keyed on a variable
 * read from document.documentElement, which is always empty, so the very first
 * result was pinned for the life of the page and shared by every widget in the
 * bundle: flipping Streamlit's appearance left calendars and popups on the old
 * theme until a hard refresh. Recomputing costs a couple of style reads per
 * render, which is far cheaper than being wrong.
 */
export function getStreamlitRsuiteTheme(element: Element): "light" | "dark" {
  return detectDarkMode(element) ? "dark" : "light";
}
