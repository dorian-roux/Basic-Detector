import {notFound} from 'next/navigation';
import {getRequestConfig} from 'next-intl/server';
import {locales} from './config';

export default getRequestConfig(async ({locale}) => {
  // Validate that the incoming `locale` parameter is valid
  if (!locales.includes(locale as any)) notFound();

  const messages = {
    Metadata: (await import(`@/locales/${locale}/metadata.json`)).default,
    BasicDetector: {
      Metadata: (await import(`@/locales/${locale}/basic-detector/metadata.json`)).default,
      Layout: (await import(`@/locales/${locale}/basic-detector/layout.json`)).default,
      Main: (await import(`@/locales/${locale}/basic-detector/main.json`)).default,
    },
  };
  return {
    messages
  }
});
