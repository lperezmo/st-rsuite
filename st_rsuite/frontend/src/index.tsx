/**
 * Single entry for every st-rsuite widget. The Python side registers ONE
 * component (st-rsuite.rsuite) and passes a `kind` discriminator in `data`;
 * this module routes it to the matching React component. One shared bundle
 * means one network fetch and one cached copy of React/RSuite per page,
 * instead of one per widget type.
 */
import "rsuite/dist/rsuite-no-reset.min.css";
import { FC } from "react";
import { createRsuiteRenderer, RendererProps } from "./shared/renderer";
import CarouselComponent from "./carousel/Carousel";
import CheckTreeComponent from "./check_tree/CheckTree";
import CheckTreePickerComponent from "./check_tree_picker/CheckTreePicker";
import DateInputComponent from "./date_input/DateInput";
import DatePickerComponent from "./date_picker/DatePicker";
import DateRangeInputComponent from "./date_range_input/DateRangeInput";
import DateRangePickerComponent from "./date_range_picker/DateRangePicker";
import MultiCascadeTreeComponent from "./multi_cascade_tree/MultiCascadeTree";
import PinInputComponent from "./pin_input/PinInput";
import RadioTileComponent from "./radio_tile/RadioTile";
import TimePickerComponent from "./time_picker/TimePicker";
import TimeRangePickerComponent from "./time_range_picker/TimeRangePicker";
import TimelineComponent from "./timeline/Timeline";

// Keys match the widget module names under st_rsuite/ (the Python side sends
// data.kind = its module name). Each widget keeps its own precise State/Data
// types internally; the registry erases them because the discriminated union
// is only resolvable at runtime.
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const registry: Record<string, FC<any>> = {
  carousel: CarouselComponent,
  check_tree: CheckTreeComponent,
  check_tree_picker: CheckTreePickerComponent,
  date_input: DateInputComponent,
  date_picker: DatePickerComponent,
  date_range_input: DateRangeInputComponent,
  date_range_picker: DateRangePickerComponent,
  multi_cascade_tree: MultiCascadeTreeComponent,
  pin_input: PinInputComponent,
  radio_tile: RadioTileComponent,
  time_picker: TimePickerComponent,
  time_range_picker: TimeRangePickerComponent,
  timeline: TimelineComponent,
};

const Dispatcher: FC<RendererProps> = ({ data, setStateValue }) => {
  const kind = typeof data.kind === "string" ? data.kind : "";
  const Widget = registry[kind];
  if (!Widget) {
    return <div>Unknown st-rsuite widget kind: {kind || String(data.kind)}</div>;
  }
  return <Widget data={data} setStateValue={setStateValue} />;
};

export default createRsuiteRenderer<
  Record<string, unknown>,
  Record<string, unknown>
>(Dispatcher);
