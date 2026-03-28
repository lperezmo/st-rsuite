import "rsuite/dist/rsuite-no-reset.min.css";
import { createRsuiteRenderer } from "../shared/renderer";
import RadioTileComponent, {
  RadioTileState,
  RadioTileData,
} from "./RadioTile";

export default createRsuiteRenderer<RadioTileState, RadioTileData>(
  RadioTileComponent
);
