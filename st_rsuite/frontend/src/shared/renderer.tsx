/**
 * Shared renderer utilities for creating v2 component renderers with React.
 *
 * With isolate_styles=False, the component renders directly in the DOM (no
 * Shadow DOM). RSuite styles inject into document.head and popups portal
 * to document.body — both work correctly in this mode.
 */
import {
  FrontendRenderer,
  FrontendRendererArgs,
} from "@streamlit/component-v2-lib";
import { StrictMode, FC } from "react";
import { createRoot, Root } from "react-dom/client";
import { CustomProvider } from "rsuite";
import {
  arEG, caES, csCZ, daDK, deDE, enGB, enUS, esAR, esES, faIR, fiFI, frFR,
  guIN, huHU, itIT, jaJP, kkKZ, koKR, neNP, nlNL, plPL, ptBR, ruRU, svSE,
  thTH, trTR, ukUA, zhCN, zhTW,
} from "rsuite/locales";
import { getStreamlitRsuiteTheme } from "./theme";

// Map Python-side locale strings to RSuite locale objects
const localeMap: Record<string, typeof enUS> = {
  ar_EG: arEG, ca_ES: caES, cs_CZ: csCZ, da_DK: daDK, de_DE: deDE,
  en_GB: enGB, en_US: enUS, es_AR: esAR, es_ES: esES, fa_IR: faIR,
  fi_FI: fiFI, fr_FR: frFR, gu_IN: guIN, hu_HU: huHU, it_IT: itIT,
  ja_JP: jaJP, kk_KZ: kkKZ, ko_KR: koKR, ne_NP: neNP, nl_NL: nlNL,
  pl_PL: plPL, pt_BR: ptBR, ru_RU: ruRU, sv_SE: svSE, th_TH: thTH,
  tr_TR: trTR, uk_UA: ukUA, zh_CN: zhCN, zh_TW: zhTW,
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

// Detect browser locale and map to closest RSuite locale key.
// e.g. "ja-JP" → "ja_JP", "ja" → "ja_JP", "zh-TW" → "zh_TW"
function detectBrowserLocale(): typeof enUS | undefined {
  const tag = navigator?.language;
  if (!tag) return undefined;
  // Try exact match: "ja-JP" → "ja_JP"
  const exact = tag.replace("-", "_");
  if (localeMap[exact]) return localeMap[exact];
  // Try language-only fallback: "ja" → "ja_JP"
  const lang = tag.split("-")[0].toLowerCase();
  const fallbackKey = langFallback[lang];
  return fallbackKey ? localeMap[fallbackKey] : undefined;
}

const browserLocale = detectBrowserLocale();

const reactRoots: WeakMap<FrontendRendererArgs["parentElement"], Root> =
  new WeakMap();

/**
 * Creates a FrontendRenderer that wraps a React component with RSuite CustomProvider.
 * Handles root management, theme injection, and cleanup.
 */
export function createRsuiteRenderer<
  TState extends Record<string, unknown>,
  TData extends Record<string, unknown>,
>(
  Component: FC<{
    data: TData;
    setStateValue: FrontendRendererArgs<TState, TData>["setStateValue"];
  }>
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
    const locale = (data as Record<string, unknown>).locale as string | undefined;
    const rsuiteLocale = locale ? localeMap[locale] : browserLocale;

    reactRoot.render(
      <StrictMode>
        <CustomProvider theme={theme} locale={rsuiteLocale}>
          <Component data={data} setStateValue={setStateValue} />
        </CustomProvider>
      </StrictMode>
    );

    return () => {
      const root = reactRoots.get(parentElement);
      if (root) {
        root.unmount();
        reactRoots.delete(parentElement);
      }
    };
  };
}
