// ---------------------------------------- //
// COMPONENTS / BASIC-DETECTOR | NAVIGATION //
// ---------------------------------------- //

// Client-Side Rendering //
"use client"; 


// Imports //
// - Packages - //
import { usePathname } from 'next/navigation';
import { useLocale } from 'next-intl';

// - Components - //
import { GetValueFromKeys } from '@/components/basic-detector/hooks/Utils';
import { pathnames } from '@/config';
import URLs from '@/assets/basic-detector/URLs.json';


// Functions //
// - Locale URL from Path - //
function GetLocaleInPath(path: string, locale: string){
    const pathURL = GetValueFromKeys(pathnames, `${path}**${locale}`, '**')
    if (pathURL) { return `/${locale}${pathURL}`}
    return ''
}

// - Synthesize Paths - //
export function SynthesizePaths(){
    // Primary Paths //
    const currentURL = usePathname();  // Current URL
    const arrPathname = currentURL.split('/');
    const previousURL = arrPathname.slice(0, -1).join('/'); // Previous URL
    const websiteURL = GetValueFromKeys(URLs, 'WEBSITE');
    const basic_detector_URL = GetValueFromKeys(URLs, 'BASIC_DETECTOR');

    // Return //
    return {
        currentURL: currentURL, previousURL: previousURL,
        websiteURL: websiteURL,
        basic_detector_URL:  GetLocaleInPath(basic_detector_URL, useLocale()) || basic_detector_URL
    };
};