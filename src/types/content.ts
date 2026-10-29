export interface ContactChannel {
  type: 'email' | 'phone' | 'linkedin' | 'website' | string;
  label: string;
  url: string;
  isPrimary?: boolean;
}

export interface NavigationItem {
  label: string;
  href: string;
  kind: 'route' | 'anchor' | string;
}

export interface SiteConfig {
  name?: string;
  title?: string;
  introduction?: string;
  location?: string;
  availability?: boolean;
  contactChannels: ContactChannel[];
  navigation?: NavigationItem[];
  [key: string]: unknown;
}
