/**
 * Shared theme bridge: Streamlit CSS custom properties → RSuite theme.
 *
 * Two things cross the bridge. RSuite's CustomProvider accepts a "theme" prop of
 * "light" | "dark" | "high-contrast", which Streamlit's background decides; and
 * RSuite's primary color ramp, which Streamlit's --st-primary-color decides.
 */

function getCSSVar(element: Element, name: string, fallback: string): string {
  const val = getComputedStyle(element).getPropertyValue(name).trim();
  return val || fallback;
}

function parseColorChannels(color: string): [number, number, number] | null {
  const value = color.trim();

  const rgbMatch = value.match(/^rgba?\(\s*([\d.]+)[\s,]+([\d.]+)[\s,]+([\d.]+)/i);
  if (rgbMatch) {
    return [Number(rgbMatch[1]), Number(rgbMatch[2]), Number(rgbMatch[3])];
  }

  const hex = value.startsWith("#") ? value.slice(1) : "";
  const full =
    hex.length === 3
      ? hex
          .split("")
          .map((c) => c + c)
          .join("")
      : hex;
  if (!/^[0-9a-f]{6}$/i.test(full)) {
    return null;
  }
  return [
    parseInt(full.slice(0, 2), 16),
    parseInt(full.slice(2, 4), 16),
    parseInt(full.slice(4, 6), 16),
  ];
}

function isDarkBackground(bgColor: string): boolean {
  const channels = parseColorChannels(bgColor);
  if (!channels) {
    return false;
  }

  const toLinear = (c: number) => {
    const v = c / 255;
    return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
  };
  const [r, g, b] = channels;
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
 *
 * Reading fresh is enough because Streamlit re-invokes a component's renderer
 * when the appearance changes, so a render always follows the flip and there is
 * nothing to subscribe to. Checked by hand on 1.51 (Settings dialog) and 1.55
 * (menu icons): with no interaction beyond the appearance control itself,
 * document.body went from rs-theme-light to rs-theme-dark. A watcher here would
 * be dead weight. The e2e counterpart is
 * test_rsuite_theme_follows_a_streamlit_appearance_change.
 */
export function getStreamlitRsuiteTheme(element: Element): "light" | "dark" {
  return detectDarkMode(element) ? "dark" : "light";
}

/**
 * RSuite draws every accent from a ten stop primary ramp, so bridging one
 * Streamlit color means producing the whole ramp rather than a single value.
 *
 * Each stop is a fraction of the distance from the base color's lightness to
 * white (positive) or to black (negative). The fractions are RSuite's own light
 * ramp solved against its 500 stop, #3498ff at l=60: its 50 sits at l=97, which
 * is 0.925 of the way from 60 to 100, and its 900 sits at l=30, which is 0.5 of
 * the way from 60 to 0. Feeding this table #3498ff therefore reproduces
 * RSuite's ramp, and feeding it anything else keeps the same relative contrast.
 *
 * Fractions rather than fixed offsets because the base color is whatever the
 * app configured. A light primary such as #a78bfa (l=76) has only 24 points of
 * headroom, so RSuite's own +37 point step would clamp its top three stops to
 * plain white and collapse the hover states that use them.
 *
 * The 500 stop is exactly the configured color. It is not snapped onto RSuite's
 * lightness, so the accent an app asked for is the accent it gets.
 */
const PRIMARY_RAMP_LIGHTNESS_FRACTIONS: ReadonlyArray<[string, number]> = [
  ["50", 0.925],
  ["100", 0.75],
  ["200", 0.575],
  ["300", 0.375],
  ["400", 0.2],
  ["500", 0],
  ["600", -1 / 12],
  ["700", -0.2],
  ["800", -1 / 3],
  ["900", -0.5],
];

function rgbToHsl(
  r: number,
  g: number,
  b: number
): [number, number, number] {
  const red = r / 255;
  const green = g / 255;
  const blue = b / 255;
  const max = Math.max(red, green, blue);
  const min = Math.min(red, green, blue);
  const lightness = (max + min) / 2;

  if (max === min) {
    return [0, 0, lightness * 100];
  }

  const delta = max - min;
  const saturation =
    lightness > 0.5 ? delta / (2 - max - min) : delta / (max + min);

  let hue: number;
  if (max === red) {
    hue = (green - blue) / delta + (green < blue ? 6 : 0);
  } else if (max === green) {
    hue = (blue - red) / delta + 2;
  } else {
    hue = (red - green) / delta + 4;
  }

  return [(hue / 6) * 360, saturation * 100, lightness * 100];
}

function hslToHex(h: number, s: number, l: number): string {
  const saturation = s / 100;
  const lightness = l / 100;
  const chroma = (1 - Math.abs(2 * lightness - 1)) * saturation;
  const secondary = chroma * (1 - Math.abs(((h / 60) % 2) - 1));
  const offset = lightness - chroma / 2;

  const sector = Math.floor(((h % 360) + 360) % 360 / 60);
  const [r, g, b] = (
    [
      [chroma, secondary, 0],
      [secondary, chroma, 0],
      [0, chroma, secondary],
      [0, secondary, chroma],
      [secondary, 0, chroma],
      [chroma, 0, secondary],
    ] as const
  )[sector];

  const channel = (value: number) =>
    Math.round((value + offset) * 255)
      .toString(16)
      .padStart(2, "0");
  return `#${channel(r)}${channel(g)}${channel(b)}`;
}

// The last --st-primary-color a ramp was written for. Only ever set to a value
// that produced a ramp, so an empty or unparseable read cannot pin the cache
// the way the old document.documentElement read pinned the theme mode.
let appliedPrimary = "";

/**
 * Point RSuite's primary ramp at Streamlit's primary color.
 *
 * Without this, every accent RSuite draws (a selected day, a checked box, a
 * highlighted option) is RSuite's stock blue no matter what the app configured,
 * so a themed app renders its own widgets in one color and its st-rsuite
 * widgets in another.
 *
 * The ramp is written to documentElement and to body, and it needs both.
 *
 * RSuite does not read the ramp where it paints; it derives semantic properties
 * from it, such as ``--rs-bg-active: var(--rs-primary-500)``. A var() in a
 * declaration resolves against the element the declaration sits on, so the
 * scope that matters is where RSuite declares those, and the two themes differ.
 * The light theme declares them on ``:root``, which is documentElement, so a
 * ramp written only to body leaves them resolving against RSuite's stock blue
 * and nothing in light mode changes color. The dark theme redeclares them under
 * ``.rs-theme-dark``, the class CustomProvider puts on body, and that rule also
 * redeclares the ramp, so a ramp written only to documentElement is overridden
 * there. An inline style beats any selector on the same element, so writing
 * both covers both.
 *
 * The component's own element is not an option for either: RSuite portals its
 * popups (calendars, picker menus) to body, so a scope inside the component
 * would style a toggle and miss the menu it opens.
 *
 * One ramp for the page is correct rather than a limitation: Streamlit has a
 * single primary color per appearance, and the appearance is global too.
 */
export function applyStreamlitPrimaryPalette(element: Element): void {
  const primary = getCSSVar(element, "--st-primary-color", "");
  if (!primary || primary === appliedPrimary) {
    return;
  }

  const channels = parseColorChannels(primary);
  if (!channels) {
    return;
  }

  const [hue, saturation, lightness] = rgbToHsl(...channels);
  const scopes = [document.documentElement, document.body];
  for (const [stop, fraction] of PRIMARY_RAMP_LIGHTNESS_FRACTIONS) {
    const shade =
      fraction > 0
        ? lightness + fraction * (100 - lightness)
        : lightness + fraction * lightness;
    const shadeHex = hslToHex(hue, saturation, shade);
    for (const scope of scopes) {
      scope.style.setProperty(`--rs-primary-${stop}`, shadeHex);
    }
  }
  appliedPrimary = primary;
}
