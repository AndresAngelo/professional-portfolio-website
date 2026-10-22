import type { SiteConfig } from '@/types/content';
import { ButtonProps, cx } from '@/components/ui/cx'; // Assuming ButtonProps and cx are available

/**
 * Filters a list of contact channels to determine the renderable primary channel.
 * 
* This logic is critical for the SiteHeader component to maintain clean state boundaries.
 * @param contactChannels The full array of contact channels defined in SiteConfig.navigation.
 * @returns An object containing { renderableChannels: Array<ContactChannel>, primaryChannel: ContactChannel | undefined }.
 */
export function getRenderableChannels(contactChannels: SiteConfig['contactChannels']) {
  const renderableChannels = contactChannels.filter((channel) => {
    // Only filter out channels that are invalid or incomplete (simple check)
    return !!channel.label && !!channel.url;
  });

  const primaryChannel = renderableChannels.find((channel) => channel.isPrimary);

  return { renderableChannels, primaryChannel };
}