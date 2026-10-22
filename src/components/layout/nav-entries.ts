// Defines the structure for a single navigation entry.

import type { SiteConfig } from '@/types/content';

/**
 * @typedef {'route' | 'anchor'} NavKind
 */

export interface NavEntry {
  label: string; // Display name in the nav bar
  href: string; // The destination path or hash
  kind: NavKind; // Determines if it's a full route or an on-page anchor
}
