/**
 * The main class required to set up an Ace instance in the browser.
 */
export interface Ace {
  /**
   * Provides access to require in packed noconflict mode
   * @param moduleName
   */
  require(moduleName: string): any;

  /**
   * Embeds the Ace editor into the DOM, at the element provided by `el`.
   * @param el Either the id of an element, or the element itself
   */
  edit(el: string): Editor;

  /**
   * Embeds the Ace editor into the DOM, at the element provided by `el`.
   * @param el Either the id of an element, or the element itself
   */
  edit(el: HTMLElement): Editor;

  /**
   * Creates a new [[EditSession]], and returns the associated [[Document]].
   * @param text {:textParam}
   * @param mode {:modeParam}
   */
  createEditSession(text: Document, mode: TextMode): IEditSession;

  /**
   * Creates a new [[EditSession]], and returns the associated [[Document]].
   * @param text {:textParam}
   * @param mode {:modeParam}
   */
  createEditSession(text: string, mode: TextMode): IEditSession;
}
