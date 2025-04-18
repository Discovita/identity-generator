import { CoachResponse, Action } from '@/types/apiTypes';
import MarkdownRenderer from '@/pages/test/MarkdownRenderer';
import { copyToClipboard } from './dataUtils';

/**
 * Renders a JSON section with collapsible functionality
 *
 * @param title - Section title
 * @param data - JSON data to display
 * @param sectionKey - Unique key for the section
 * @param isExpanded - Whether the section is expanded
 * @param toggleSection - Function to toggle section expansion
 * @returns JSX element for the section
 */
export const renderJsonSection = (
  title: string,
  data: any,
  sectionKey: string,
  isExpanded: boolean,
  toggleSection: (section: string) => void
): JSX.Element | null => {
  if (!data || (Array.isArray(data) && data.length === 0)) return null;

  return (
    <div className="state-section">
      <div className="section-header" onClick={() => toggleSection(sectionKey)}>
        <h3>{title}</h3>
        <div className="section-controls">
          <button
            className="copy-button"
            onClick={e => {
              e.stopPropagation();
              copyToClipboard(data);
            }}
          >
            Copy
          </button>
          <span className={`expand-icon ${isExpanded ? 'expanded' : ''}`}>
            {isExpanded ? '▼' : '▶'}
          </span>
        </div>
      </div>

      {isExpanded && <pre className="json-content">{JSON.stringify(data, null, 2)}</pre>}
    </div>
  );
};

/**
 * Renders actions in a visually appealing way with syntax highlighting
 *
 * @param title - Section title
 * @param actions - Array of actions to display
 * @param sectionKey - Unique key for the section
 * @param isExpanded - Whether the section is expanded
 * @param toggleSection - Function to toggle section expansion
 * @returns JSX element for the section
 */
export const renderActionsSection = (
  title: string,
  actions: Action[],
  sectionKey: string,
  isExpanded: boolean,
  toggleSection: (section: string) => void
): JSX.Element | null => {
  if (!actions || actions.length === 0) return null;

  // Single color for all action types
  const actionColor = 'var(--primary-color)'; // Use the primary color from variables.css

  return (
    <div className="state-section">
      <div className="section-header" onClick={() => toggleSection(sectionKey)}>
        <h3>{title}</h3>
        <div className="section-controls">
          <button
            className="copy-button"
            onClick={e => {
              e.stopPropagation();
              copyToClipboard(actions);
            }}
          >
            Copy
          </button>
          <span className={`expand-icon ${isExpanded ? 'expanded' : ''}`}>
            {isExpanded ? '▼' : '▶'}
          </span>
        </div>
      </div>

      {isExpanded && (
        <div className="actions-container">
          {actions.map((action, index) => (
            <div key={index} className="action-card">
              <div className="action-type" style={{ backgroundColor: actionColor }}>
                {action.type}
              </div>
              <div className="action-params">
                {action.params && action.params.length > 0 ? (
                  <table className="params-table">
                    <thead>
                      <tr>
                        <th>Parameter</th>
                        <th>Value</th>
                      </tr>
                    </thead>
                    <tbody>
                      {action.params.map((param, pIndex) => (
                        <tr key={pIndex}>
                          <td className="param-name">{param.name}</td>
                          <td className="param-value">{JSON.stringify(param.value)}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                ) : (
                  <div className="no-params">No parameters</div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

/**
 * Renders the final prompt using Markdown
 *
 * @param lastResponse - The last API response containing the prompt
 * @param isExpanded - Whether the section is expanded
 * @param toggleSection - Function to toggle section expansion
 * @returns JSX element for the final prompt section
 */
export const renderFinalPrompt = (
  lastResponse: CoachResponse | undefined,
  isExpanded: boolean,
  toggleSection: (section: string) => void
): JSX.Element | null => {
  if (!lastResponse?.final_prompt) return null;

  return (
    <div className="state-section">
      <div className="section-header" onClick={() => toggleSection('prompt')}>
        <h3>Final Prompt</h3>
        <div className="section-controls">
          <button
            className="copy-button"
            onClick={e => {
              e.stopPropagation();
              copyToClipboard(lastResponse.final_prompt);
            }}
          >
            Copy
          </button>
          <span className={`expand-icon ${isExpanded ? 'expanded' : ''}`}>
            {isExpanded ? '▼' : '▶'}
          </span>
        </div>
      </div>

      {isExpanded && (
        <div className="markdown-prompt-content">
          <MarkdownRenderer content={lastResponse.final_prompt} />
        </div>
      )}
    </div>
  );
};

/**
 * Renders an empty state message
 *
 * @param primaryText - Primary text to display
 * @param secondaryText - Optional secondary text
 * @returns JSX element for the empty state
 */
export const renderEmptyState = (primaryText: string, secondaryText?: string): JSX.Element => {
  return (
    <div className="empty-state">
      <p>{primaryText}</p>
      {secondaryText && <p>{secondaryText}</p>}
    </div>
  );
};
