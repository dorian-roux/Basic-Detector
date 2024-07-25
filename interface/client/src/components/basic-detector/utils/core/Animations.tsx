// ------------------------------------------------------- //
// COMPONENTS / BASIC-DETECTOR | UTILS / CORE / ANIMATIONS //
// ------------------------------------------------------- //

// Client-Side Rendering //
"use client"; 


// Imports //
// - Packages - //
import React from 'react';

// - Styles - //
import '@/styles/basic-detector/utils/animations.scss';


// Constant | Animated Circle //
export const AnimatedCircle = ({ text }: { text: string }) => {
    return (
        <div className="a-circle">
            <div className="child">
                <div className="text-ctnr">{text}</div>
                <div className="item-ctnr"><div className="circle"/></div>
            </div>
        </div>
    );
};

// Constant | Animated Progress Bar //
export const AnimatedProgressBar = ({ text, progress }: { text: string, progress: number }) => {
    return (
        <div className="a-prgs-bar">
            <div className="text-ctnr">{text.replace('**', `${progress}`)}</div>
            <div className='item-ctnr'>
                <div className={`inner ${progress === 100 ? '!rounded-r' : '!rounded-r-none'}`}  style={{width: `${progress}%` }}>
                    {progress}%
                </div>        
            </div>
        </div>
    );
};