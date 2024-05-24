import { IWidget } from "@comfy-main-web/types/litegraph.js";
type SelectOnOptions = "focus" | "click" | "dblclick" | "mousedown" | "mouseup" | "select";
type WidgetType = "text" | "number" | "toggle" | "customtext" | "combo" // There are others

/**
 * Represents the options for a widget.
 */
export interface WidgetOptions extends Record<string, any> {
  /**
   * A function that returns the current value of the widget.
   * Will effectively override the default getValue function of the created widget.
   */
  getValue: () => any;

  /**
   * A function that sets the value of the widget.
   * Will effectively override the default setValue function of the created widget.
   * 
   * @param value - The value to set.
   */
  setValue?: (value: any) => void;

  /**
   * A callback function that is called when the value of the widget changes.
   * @param value - The new value of the widget.
   */
  callback?: (value: any) => void;

  /**
   * Determines whether the widget should be hidden when zooming out.
   */
  hideOnZoomOut?: boolean;

  /**
   * Determines whether the widget should be hidden when zooming in.
   */
  hideOnZoom?: boolean;

  /**
   * Which events should trigger the widget to be selected.
   */
  selection?: SelectOnOptions[];

  /**
   * The maximum value allowed for the widget if it is a number.
   */
  max?: integer;

  /**
   * The minimum value allowed for the widget if it is a number.
   */
  min?: integer;

  /**
   * The precision of the widget's value if it is a floating point number.
   */
  precision?: number;

  /**
   * The number of decimal places to round the widget's value to if it 
   * is a floating point number.
   */
  round?: number;

  /**
   * The step size for incrementing or decrementing the widget's value
   * if it is a number and a slider.
   */
  step?: number;

  /**
   * If the widget is a boolean, whether it is True.
   * 
   */
  on?: string;

  /**
   * If the widget is a boolean, whether it is False.
   */
  off?: string;
}

export interface ComfyWidget extends IWidget {
  onRemove?: () => void;
  getValue: () => any; // Set in options, calls options.getValue
  setValue?: (value: any) => void; // Set in options, calls options.setValue

  value?: any;
  options: WidgetOptions;
  last_y?: number;
  computedHeight?: number;
  element?: HTMLElement;
  inputEl?: HTMLInputElement;
}

export type ComfyWidgetUIWrapper = {
  widget: ComfyWidget;
  minHeight?: number;
  minWidth?: number;
};
