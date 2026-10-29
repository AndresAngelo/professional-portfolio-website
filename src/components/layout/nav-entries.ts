import type { SiteConfig } from '@/types/content';

export type NavKind = 'route' | 'anchor';

export interface NavEntry {
  label: string;
  href: string;
  kind: NavKind;
}

export const getNavEntries = (config?: SiteConfig): NavEntry[] => {
  return [];
};
