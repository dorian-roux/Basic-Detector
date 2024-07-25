// ------------------------------------------------------ //
// COMPONENTS / BASIC-DETECTOR | HOOKS / LANGUAGE_CHANGER //
// ------------------------------------------------------ //

// Client-Side Rendering //
"use client"; 


// Imports //
// - Packages - //
import { useTransition} from 'react';
import { useParams } from 'next/navigation';

// - Components - //
import { useRouter, usePathname } from '@/navigation';
import { GetValueFromKeys } from '@/components/basic-detector/hooks/Utils';
import { IcArrowDown } from '@/components/basic-detector/icons/Layout';
import { IcEN, IcES, IcFR } from '@/components/basic-detector/icons/Flags';


// Constants //
// - Language Data - //
const languageData = {
  en : {Name: 'English', Flag: <IcEN className={'w-7 lg:w-6 lg:h-6 sm:w-4 h-auto mr-2 sm:mr-1'}/>},
  es : {Name: 'Español', Flag: <IcES className={'w-7 lg:w-6 lg:h-6 sm:w-4 h-auto mr-2 sm:mr-1'}/>},
  fr : {Name: 'Français', Flag: <IcFR className={'w-7 lg:w-6 lg:h-6 sm:w-4 h-auto mr-2 sm:mr-1'}/>}
};


// Function | Custom Language Changer //
export function LanguageChanger({currentLocale, className} : {currentLocale: string, className: string}){
  // Variables & States //
  const router = useRouter();
  const [isPending, startTransition] = useTransition();
  const pathname = usePathname();
  const params = Object.keys(useParams()).reduce((acc: {[key: string]: string}, key) => { acc[key] = decodeURIComponent(useParams()[key].toString()); return acc; }, {});
  
  // Functions //
  // - Handle Language Change - //
  function handleLangChange(language: string) {
    const nextLocale = language
    startTransition(() => {
      router.replace(
        // @ts-expect-error
        {pathname, params},
        {locale: nextLocale}
      );
    });
  };
    
  // Return //
  return (
    <div className={`${className} relative`}>
      {/* Current Language */}
      <div className={`peer flex items-center font-semibold shadow sm:shadow-none py-2 px-1.5 sm:py-1 border-[1.5px] rounded sm:rounded-none rounded-b-none border-dark dark:border-light`}>
        {currentLocale && GetValueFromKeys(languageData, `${currentLocale.toLocaleLowerCase()}/Flag`)}
        <span className='text-sm lg:text-xs'>{GetValueFromKeys(languageData, `${currentLocale.toLocaleLowerCase()}/Name`)}</span>
        <IcArrowDown className="flex w-6 h-6 sm:w-4 sm:h-4" />
      </div>
      {/* Dropdown Menu */}
      <div className={`peer hidden peer-hover:flex hover:flex absolute w-full`}>
        <div className='border-[1.5px] border-dark dark:border-light dark:shadow-none shadow w-full'>
          {Object.keys(languageData).map((lang, i) => (
            <button key={lang} className={`sm:text-xs font-medium block w-full text-left py-2 px-1.5 sm:py-1 hover:rounded-none bg-light hover:!bg-gray-800 hover:!text-light dark:bg-dark dark:hover:!bg-gray-200 dark:hover:!text-dark ${currentLocale === lang ? 'bg-slate-200 dark:bg-slate-800' : ''} ${i === 0 ? 'rounded-t-[1.5px]' : i === Object.keys(languageData).length - 1 ? 'rounded-b-[1.5px]': ''}`} onClick={() => handleLangChange(lang)}>
              <div className="peer flex items-center font-semibold">
                {lang && GetValueFromKeys(languageData, `${lang.toLocaleLowerCase()}/Flag`)}
                <span className='text-sm lg:text-[13px]'>{GetValueFromKeys(languageData, `${lang.toLocaleLowerCase()}/Name`)}</span>
              </div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};