// --------------- //
// LOCALE | LAYOUT //
// --------------- //

// - Imports - //
import { ReactNode } from 'react';
import { getTranslations, unstable_setRequestLocale } from 'next-intl/server';

// - Metadata - //
export async function generateMetadata({params: {locale}}: {params: {locale: string}}) {
  const t = await getTranslations({namespace: 'Metadata', locale, fallback: 'fr'});
  const keys = ['NotFound'];
  return {
    title: t(`${keys.join('.')}.Title`),
    description: t(`${keys.join('.')}.Description`)
  };
}

// - Layout Function - //
export default async function LocaleRootLayout({children,params: {locale}}: {children: ReactNode; params: {locale: string}}) {
  unstable_setRequestLocale(locale);
  return (
    <>
      {children}
    </>
  );
};