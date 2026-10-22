import { faker } from '@combinatorics/faker';
import type { NavigationItem, ContactChannel } from '@/types/content';

/**
 * Generates a random string that is suitable for use as a SiteName.
 */
export const siteNameArbitrary = faker.string.alphanumeric({ length: 10 });

/**
 * Generates an arbitrary navigation item.
 */
export const navItemArbitrary = () => ({
  label: faker.hacker.word().charAt(0).toUpperCase() + faker.hacker.word().slice(1), // Simple capitalization for display
  href: faker.internet.url(),
  kind: 'route' as const,
});

/**
 * Generates an arbitrary contact channel.
 */
export const contactChannelArbitrary = () => {
  const types: Array<'email' | 'phone' | 'linkedin' | 'website'> = ['email', 'phone', 'linkedin', 'website'];
  const type = faker.helpers.arrayElement(types);
  const label = faker.person.fullName();
  let url: string;
  let isPrimary: boolean;

  switch (type) {
    case 'email':
      url = `${label.toLowerCase().replace(/\s/g, '')}@example.com`;
      isPrimary = faker.datatype.boolean();
      break;
    case 'phone':
      url = `tel:${faker.phone.number()}`;
      isPrimary = faker.datatype.boolean();
      break;
    case 'linkedin':
      url = `https://linkedin.com/in/${label.toLowerCase().replace(/\s/g, '')}`;
      isPrimary = faker.datatype.boolean();
      break;
    case 'website':
      url = `https://www.${faker.internet.domain()}`; 
      isPrimary = faker.datatype.boolean();
      break;
  }
  
  return {
    type, 
    label,
    url,
    isPrimary
  };
};
