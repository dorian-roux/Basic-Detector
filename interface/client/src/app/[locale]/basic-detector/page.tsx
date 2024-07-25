// --------------------- //
// BASIC-DETECTOR | PAGE //
// --------------------- //

// Imports //
// - Packages - //
import { useMessages } from 'next-intl';

// - Components - //
import { GetValueFromKeys } from '@/components/basic-detector/hooks/Utils';
import withLayout from '@/components/basic-detector/withLayout';
import Main from '@/components/basic-detector/pages/Main';

// Constant | Landing / Page //
const LandingPage: React.FC = () => {
  const contentMain = GetValueFromKeys(useMessages(), `BasicDetector/Main`);   // Main Content //
  return <Main contentMain={contentMain} />
};

// Export | withLayout //
export default withLayout(LandingPage);