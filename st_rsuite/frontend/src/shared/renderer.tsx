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
import { getStreamlitRsuiteTheme } from "./theme";

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

    reactRoot.render(
      <StrictMode>
        <CustomProvider theme={theme}>
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
