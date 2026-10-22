import type { NavEntry } from './nav-entries';
import { usePathname } from 'next/navigation';

/**
 * Finds the index of the navigation entry that matches the current pathname.
 * This assumes a 1:1 relationship between route entries and paths (e.g., '/projects').
 *
 * @param pathname The current URL path provided by usePathname().
 * @param entries Array of all available navigation entries.
 * @returns The index of the matching entry, or -1 if no match is found.
 */
export function getCurrentEntryIndex(pathname: string, entries: readonly NavEntry[]): number {
  for (let i = 0; i < entries.length; i++) {
    const entry = entries[i];
    // Only consider route kind entries for path matching
    if (entry.kind === 'route' && entry.href === pathname) {
      return i;
    }
  }
  return -1;
}