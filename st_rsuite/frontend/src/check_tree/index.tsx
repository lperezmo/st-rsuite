import "rsuite/dist/rsuite-no-reset.min.css";
import { createRsuiteRenderer } from "../shared/renderer";
import CheckTreeComponent, {
  CheckTreeState,
  CheckTreeData,
} from "./CheckTree";

export default createRsuiteRenderer<CheckTreeState, CheckTreeData>(
  CheckTreeComponent
);
