// ----------------------------------------- //
// COMPONENTS / BASIC-DETECTOR | WITH_LAYOUT //
// ----------------------------------------- //


// Imports //
// - Packages - //
import { useMessages } from 'next-intl';
import React, { ComponentType } from 'react';

// - Components - //
import { GetValueFromKeys } from '@/components/basic-detector/hooks/Utils';
import Header from '@/components/basic-detector/pages/layout/Header';
import Footer from '@/components/basic-detector/pages/layout/Footer';


// Function | with Layout //
export default function withLayout<Props extends object>(PageComponent: ComponentType<Props>): React.FC<Props> {
    // Constant | With Layout // 
    const WithLayout: React.FC<Props> = (props) => {
        // - Content Layout - //
        const contentLayout = GetValueFromKeys(useMessages(), `BasicDetector/Layout`);

        // - Return - //
        return (
            <>
                <Header contentHeader={ GetValueFromKeys(contentLayout, 'Header')}/>
                <main className='flex flex-grow px-4 sm:px-2'><PageComponent {...props}/></main>
                <Footer contentFooter={ GetValueFromKeys(contentLayout, 'Footer') } />
            </>
        );
    };

    // Return //
    return WithLayout;
};