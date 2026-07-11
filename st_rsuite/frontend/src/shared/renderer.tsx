/**
 * Shared renderer utilities for creating v2 component renderers with React.
 *
 * With isolate_styles=False, the component renders directly in the DOM (no
 * Shadow DOM). RSuite styles inject into document.head and popups portal
 * to document.body — both work correctly in this mode.
 *
 * Locales load lazily: each RSuite locale is its own chunk (see build.mjs),
 * so a page downloads only the locale it actually renders. The first paint of
 * a localized widget goes out with RSuite's built-in English strings and
 * re-renders when the locale chunk arrives.
 */
import {
  FrontendRenderer,
  FrontendRendererArgs,
} from "@streamlit/component-v2-lib";
import { ComponentProps, StrictMode, FC } from "react";
import { createRoot, Root } from "react-dom/client";
import { CustomProvider } from "rsuite";
import { getStreamlitRsuiteTheme } from "./theme";

type RsuiteLocale = ComponentProps<typeof CustomProvider>["locale"];

// Map Python-side locale strings to lazy locale imports. Static literal paths
// keep each locale statically analyzable so Rollup emits one chunk per locale.
const localeLoaders: Record<string, () => Promise<{ default: RsuiteLocale }>> =
  {
    ar_EG: () => import("rsuite/locales/ar_EG"),
    ca_ES: () => import("rsuite/locales/ca_ES"),
    cs_CZ: () => import("rsuite/locales/cs_CZ"),
    da_DK: () => import("rsuite/locales/da_DK"),
    de_DE: () => import("rsuite/locales/de_DE"),
    en_GB: () => import("rsuite/locales/en_GB"),
    en_US: () => import("rsuite/locales/en_US"),
    es_AR: () => import("rsuite/locales/es_AR"),
    es_ES: () => import("rsuite/locales/es_ES"),
    fa_IR: () => import("rsuite/locales/fa_IR"),
    fi_FI: () => import("rsuite/locales/fi_FI"),
    fr_FR: () => import("rsuite/locales/fr_FR"),
    gu_IN: () => import("rsuite/locales/gu_IN"),
    hu_HU: () => import("rsuite/locales/hu_HU"),
    it_IT: () => import("rsuite/locales/it_IT"),
    ja_JP: () => import("rsuite/locales/ja_JP"),
    kk_KZ: () => import("rsuite/locales/kk_KZ"),
    ko_KR: () => import("rsuite/locales/ko_KR"),
    ne_NP: () => import("rsuite/locales/ne_NP"),
    nl_NL: () => import("rsuite/locales/nl_NL"),
    pl_PL: () => import("rsuite/locales/pl_PL"),
    pt_BR: () => import("rsuite/locales/pt_BR"),
    ru_RU: () => import("rsuite/locales/ru_RU"),
    sv_SE: () => import("rsuite/locales/sv_SE"),
    th_TH: () => import("rsuite/locales/th_TH"),
    tr_TR: () => import("rsuite/locales/tr_TR"),
    uk_UA: () => import("rsuite/locales/uk_UA"),
    zh_CN: () => import("rsuite/locales/zh_CN"),
    zh_TW: () => import("rsuite/locales/zh_TW"),
  };

// Fallback from language code to default locale for that language
const langFallback: Record<string, string> = {
  ar: "ar_EG", ca: "ca_ES", cs: "cs_CZ", da: "da_DK", de: "de_DE",
  en: "en_US", es: "es_ES", fa: "fa_IR", fi: "fi_FI", fr: "fr_FR",
  gu: "gu_IN", hu: "hu_HU", it: "it_IT", ja: "ja_JP", kk: "kk_KZ",
  ko: "ko_KR", ne: "ne_NP", nl: "nl_NL", pl: "pl_PL", pt: "pt_BR",
  ru: "ru_RU", sv: "sv_SE", th: "th_TH", tr: "tr_TR", uk: "uk_UA",
  zh: "zh_CN",
};

/**
 * Resolve the locale key to load: an explicit key from Python wins, otherwise
 * the browser locale maps to the closest RSuite key.
 * e.g. "ja-JP" → "ja_JP", "ja" → "ja_JP", "zh-TW" → "zh_TW"
 */
function resolveLocaleKey(explicit: string | undefined): string | undefined {
  if (explicit) return localeLoaders[explicit] ? explicit : undefined;
  const tag = navigator?.language;
  if (!tag) return undefined;
  // Try exact match: "ja-JP" → "ja_JP"
  const exact = tag.replace("-", "_");
  if (localeLoaders[exact]) return exact;
  // Try language-only fallback: "ja" → "ja_JP"
  const lang = tag.split("-")[0].toLowerCase();
  const fallbackKey = langFallback[lang];
  return fallbackKey && localeLoaders[fallbackKey] ? fallbackKey : undefined;
}

// Locales already fetched this page; shared across every widget instance.
const loadedLocales = new Map<string, RsuiteLocale>();

const reactRoots: WeakMap<FrontendRendererArgs["parentElement"], Root> =
  new WeakMap();

/** Props the wrapped React component receives from the renderer. */
export type RendererProps<
  TState extends Record<string, unknown> = Record<string, unknown>,
  TData extends Record<string, unknown> = Record<string, unknown>,
> = {
  data: TData;
  setStateValue: FrontendRendererArgs<TState, TData>["setStateValue"];
};

/**
 * Creates a FrontendRenderer that wraps a React component with RSuite CustomProvider.
 * Handles root management, theme injection, locale loading, and cleanup.
 */
export function createRsuiteRenderer<
  TState extends Record<string, unknown>,
  TData extends Record<string, unknown>,
>(
  Component: FC<RendererProps<TState, TData>>
): FrontendRenderer<TState, TData> {
  return (args) => {
    const { data, parentElement, setStateValue } = args;

    const rootElement = parentElement.querySelector(".react-root");
    if (!rootElement) {
      throw new Error("React root element (.react-root) not found");
    }

    let reactRoot = reactRoots.get(parentElement);
    if (!reactRoot) {
      reactRoot = createRoot(rootElement);
      reactRoots.set(parentElement, reactRoot);
    }

    const theme = getStreamlitRsuiteTheme();
    const explicit = (data as Record<string, unknown>).locale as
      | string
      | undefined;
    const localeKey = resolveLocaleKey(explicit);

    const renderTree = () => {
      const locale = localeKey ? loadedLocales.get(localeKey) : undefined;
      reactRoot!.render(
        <StrictMode>
          <CustomProvider theme={theme} locale={locale}>
            <Component data={data} setStateValue={setStateValue} />
          </CustomProvider>
        </StrictMode>
      );
    };

    if (localeKey && !loadedLocales.has(localeKey)) {
      localeLoaders[localeKey]().then((mod) => {
        loadedLocales.set(localeKey, mod.default);
        // Skip the re-render if this instance unmounted while the chunk loaded.
        if (reactRoots.get(parentElement) === reactRoot) renderTree();
      });
    }

    renderTree();

    return () => {
      const root = reactRoots.get(parentElement);
      if (root) {
        root.unmount();
        reactRoots.delete(parentElement);
      }
    };
  };
}
