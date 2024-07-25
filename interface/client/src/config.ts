import Paths from '@/locales/paths.json'


export const locales = ['en', 'es', 'fr'] as const;

export const pathnames = {
    ...Paths,
};

export const localePrefix = undefined;
export type AppPathnames = keyof typeof pathnames;

