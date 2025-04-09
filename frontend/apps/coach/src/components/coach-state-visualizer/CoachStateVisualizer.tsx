import React, { useState, useEffect, useRef } from 'react';
import { CoachStateVisualizerProps, TabName, TabUpdateStatus, ExtractedActions } from './types';
import {
  extractActions,
  renderTabContent,
  getDefaultExpandedSections,
  getTabsConfig,
  detectAllTabChanges,
} from './utils';

/**
 * CoachStateVisualizer Component
 *
 * This component displays the internal state and metadata of the coaching system
 * during test mode. It provides a detailed view into what's happening behind the
 * scenes in the coaching system.
 *
 * Features:
 * - Displays coach state in a tabbed interface
 * - Shows available actions and actions taken
 * - Allows collapsing/expanding sections
 * - Provides syntax highlighting for JSON data
 * - Includes copy to clipboard functionality
 * - Shows indicators when tab content changes
 *
 * @param props.coachState - The current state of the coach
 * @param props.lastResponse - The last API response object containing prompt and other metadata
 */
export const CoachStateVisualizer: React.FC<CoachStateVisualizerProps> = ({
  coachState,
  lastResponse,
}) => {
  const [activeTab, setActiveTab] = useState<TabName>(TabName.STATE);
  const [expandedSections, setExpandedSections] = useState(getDefaultExpandedSections());
  const [tabUpdates, setTabUpdates] = useState<TabUpdateStatus>({});
  const prevStateRef = useRef<null | typeof coachState>(null);
  const prevResponseRef = useRef<undefined | typeof lastResponse>(undefined);
  const prevActionsRef = useRef<null | ExtractedActions>(null);
  const extractedActionsRef = useRef<ExtractedActions>(extractActions(coachState, lastResponse));
  const tabsConfig = getTabsConfig();

  // Toggle section expansion
  const toggleSection = (section: string) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section],
    }));
  };

  // Handle tab click - change active tab and clear update indicator
  const handleTabClick = (tabName: TabName) => {
    setActiveTab(tabName);

    // Clear update indicator for this tab
    if (tabUpdates[tabName]) {
      setTabUpdates(prev => {
        const newUpdates = { ...prev };
        newUpdates[tabName] = false;
        return newUpdates;
      });
    }
  };

  // Detect changes in data when state or response updates
  useEffect(() => {
    // Extract current actions
    const currentActions = extractActions(coachState, lastResponse);
    extractedActionsRef.current = currentActions;

    // Skip first render
    if (prevStateRef.current === null) {
      prevStateRef.current = coachState;
      prevResponseRef.current = lastResponse;
      prevActionsRef.current = currentActions;
      return;
    }

    // Detect changes in each tab's data
    const updates = detectAllTabChanges(
      prevStateRef.current,
      coachState,
      prevResponseRef.current,
      lastResponse,
      prevActionsRef.current,
      currentActions,
      activeTab
    );

    // Only update state if there are actual changes
    let hasAnyUpdates = false;
    Object.values(updates).forEach(value => {
      if (value === true) hasAnyUpdates = true;
    });

    if (hasAnyUpdates) {
      setTabUpdates(prev => ({
        ...prev,
        ...updates,
      }));
    }

    // Store current values for next comparison
    prevStateRef.current = coachState;
    prevResponseRef.current = lastResponse;
    prevActionsRef.current = currentActions;
  }, [coachState, lastResponse, activeTab]); // Remove extractedActions from dependencies

  return (
    <div className="coach-state-visualizer">
      <div className="tabs">
        {tabsConfig.map(tab => (
          <button
            key={tab.name}
            className={`tab ${activeTab === tab.name ? 'active' : ''} ${
              tabUpdates[tab.name] ? 'has-updates' : ''
            }`}
            onClick={() => handleTabClick(tab.name)}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <div className="tab-content">
        {renderTabContent(
          activeTab,
          coachState,
          lastResponse,
          expandedSections,
          toggleSection,
          extractedActionsRef.current
        )}
      </div>
    </div>
  );
};
