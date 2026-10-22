export type MobileState = 'collapsed' | 'expanded';

/**
 * Reducer function for managing the mobile navigation toggle state.
 * @param state The current state ('collapsed' or 'expanded').
 * @param action The action dispatched (e.g., 'TOGGLE', 'ESCAPE', 'LINK_ACTIVATED', 'ROUTE_CHANGED').
 * @returns The new state.
 */
export function disclosureReducer(state: MobileState, action: any): MobileState {
  switch (action.type) {
    case 'TOGGLE':
      return state === 'collapsed' ? 'expanded' : 'collapsed';
    case 'LINK_ACTIVATED':
    case 'ROUTE_CHANGED':
    case 'ESCAPE': // Escape key handles collapse, but explicitly handling it here is clearer.
      return 'collapsed';
    default:
      return state;
  }
}