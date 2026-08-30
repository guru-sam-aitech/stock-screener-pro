import React from 'react';
import AIAnalytics from '../components/AIAnalytics';

/**
 * AI Analytics Page
 * Wrapper component for the AI Analytics dashboard
 * Can be used with React Router or similar routing libraries
 */
const AIAnalyticsPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl font-bold text-gray-900">AI Analytics</h1>
          <p className="mt-2 text-sm text-gray-600">
            Advanced AI-powered stock analysis and insights
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <AIAnalytics />
      </main>
    </div>
  );
};

export default AIAnalyticsPage;
