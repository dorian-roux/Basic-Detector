// ------------------------------------------ //
// COMPONENTS / BASIC-DETECTOR | PAGES / MAIN //
// ------------------------------------------ //

// Client-Side Rendering //
"use client"; 


// Imports //
// - Packages - //
import React, { useEffect, useState } from 'react';
import { useLocale } from 'next-intl';
import { motion } from 'framer-motion';

// - Components - //
import { backendURL } from '@/components/basic-detector/config';
import { GetValueFromKeys } from '@/components/basic-detector/hooks/Utils';
import Core from '@/components/basic-detector/utils/Core';

// - Styles - //
import '@/styles/basic-detector/main.scss';


// Function | Main //
export default function Main({ contentMain }: { contentMain: any }) {
  // States & Variables //
  const locale = useLocale();
  // const [options, setOptions] = useState(Object.keys(GetValueFromKeys(contentMain, 'Options/List')).reduce((acc: any, key: string, index: number) => (acc[key] = index === 0, acc), {}));

  // UseEffect //
  const [weights, setWeights] = useState({}); // Weights for the model
  const [categories, setCategories] = useState([]); // Categories for the model
  useEffect(() => {
    fetch(`${backendURL}/storage/weights`).then(res => res.json()).then(data => setWeights(data));
    fetch(`${backendURL}/storage/${locale}/categories`).then(res => res.json()).then(data => setCategories(data));
  }, []);

  // Constants //
  // - Transform Weights Name to Locale Categories - //
  const transformWeightsToLocaleCtgs = (weights: any, categories: any) => {
    if (Object.keys(weights).length === 0) return {};
    let newWeights: any = {}
    for (const key in weights) {
      newWeights[key] = {...weights[key], 'NAME': categories[key]};
    };
    // Sort the weights by ORDER and Return //
    // return Object.fromEntries(Object.entries(newWeights).sort(([, a], [, b]) => a.ORDER - b.ORDER));
    return Object.fromEntries(
      Object.entries(newWeights).sort(([keyA, a], [keyB, b]) => {
        const weightA = a as {[key: string]: any}
        const weightB = b as {[key: string]: any}
        return weightA.ORDER - weightB.ORDER;
      })
    );
  }
  
  const localeWeights = transformWeightsToLocaleCtgs(weights, categories);

  // Return //
  if (Object.keys(localeWeights).length === 0) return null;
  return (
    <>
      <div id='md-main'>
        <div className='parent-title'>
          <h1>{GetValueFromKeys(contentMain, 'Title')}</h1>
        </div>
        <hr className="divider" />
        <div className='parent-container'>
          <Core contentCore={GetValueFromKeys(contentMain, 'Core')} weights={localeWeights} setWeights={setWeights}/>
        </div>
      </div>
    </>
  );
};