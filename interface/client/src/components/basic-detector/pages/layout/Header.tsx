// ----------------------------------------------------- //
// COMPONENTS / BASIC-DETECTOR | PAGES / LAYOUT / HEADER //
// ----------------------------------------------------- //

// Client-Side Rendering //
"use client"; 

// Imports //
// - Packages - //
import React, { useState } from 'react'
import { useLocale } from 'next-intl'
import { motion } from 'framer-motion'
import Image from 'next/image';

// - Components - //
import { SynthesizePaths } from '@/components/basic-detector/Navigation';
import UseThemeSwitcher from '@/components/basic-detector/hooks/UseThemeSwitcher'
import { LanguageChanger } from '@/components/basic-detector/hooks/LanguageChanger';
import { pushToURL } from '@/components/basic-detector/hooks/Utils';
import { IcSun, IcMoon } from '@/components/basic-detector/icons/Layout';
import LogoMD from '@/assets/basic-detector/logo.png';

// - Styles - //
import '@/styles/basic-detector/layout.scss';


// Function | Header //
export default function Header({contentHeader}: {contentHeader: any}) {
    // States & Variables //
    const { basic_detector_URL } = SynthesizePaths();  // Paths
    const [mode, setMode] = UseThemeSwitcher();

    // Return //
    return (
        <>
        <header id="md-header">
            <div className='parent-container'>
                <nav className='navigation-container'>  {/* Left Side */}
                    <motion.div className='parent-logo-container' whileHover={{y: -2}} whileTap={{scale: 0.9}}>
                        <button onClick={() => pushToURL(basic_detector_URL)} className='btn-logo'>
                            <Image src={LogoMD} alt="Logo - Games Basketball"/>
                        </button>
                    </motion.div> 
                </nav>
                <nav className='navigation-container'>   {/* Right Side */}  
                    <div className='parent-theme-container'>
                        <div className='flex justify-end items-center my-2'>
                            <button className="btn-theme" onClick={() => setMode(mode === "light" ? "dark" : "light")}>
                                <div id="switch-toggle" className= {`${mode == "light" ? 'bg-yellow-500 -translate-x-2' : 'bg-gray-700 translate-x-full'}`}>
                                    {mode==='light' ? <IcSun className='ic'/> : <IcMoon className='ic'/>}
                                </div>
                            </button>
                        </div>
                    </div>
                    <LanguageChanger currentLocale={useLocale()} className='parent-lang-container'/>
                </nav>
            </div>  
    </header>
        </>
    );
};