import "rsuite/dist/rsuite-no-reset.min.css";
import { createRsuiteRenderer } from "../shared/renderer";
import MultiCascadeTreeComponent, {
  MultiCascadeTreeState,
  MultiCascadeTreeData,
} from "./MultiCascadeTree";

export default createRsuiteRenderer<MultiCascadeTreeState, MultiCascadeTreeData>(
  MultiCascadeTreeComponent
);
