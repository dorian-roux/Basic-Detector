// ----------------------- //
// BASIC-DETECTOR | LAYOUT //
// ----------------------- //

// - Imports - //
import { ReactNode } from 'react';
import { getTranslations, unstable_setRequestLocale } from 'next-intl/server';
import TransitionEffect from '@/components/basic-detector/TransitionEffect';

// - Metadata - //
export async function generateMetadata({params: {locale}}: {params: {locale: string}}) {
  const t = await getTranslations({namespace: 'BasicDetector.Metadata', locale, fallback: 'en'});
  return { title: t(`Title`), description: t(`Description`) };
};

// - Layout Function - //
export default async function LocaleLayout({children,params: {locale}}: {children: ReactNode; params: {locale: string}}) {
  unstable_setRequestLocale(locale);
  return (
    <>  
      <link rel="shortcut icon" href="/favicon-basic-detector.ico"/>  {/* Favicon */}
      <TransitionEffect />
      {children}
    </>
  );
};