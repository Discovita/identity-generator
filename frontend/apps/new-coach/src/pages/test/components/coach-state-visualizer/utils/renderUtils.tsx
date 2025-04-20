import { CoachResponse, Action } from '@/types/apiTypes';
import MarkdownRenderer from '@/utils/MarkdownRenderer';
import { copyToClipboard } from './dataUtils';
import { Button } from '@/components/ui/button';

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
  data: Record<string, unknown> | unknown[] | null | undefined,
  sectionKey: string,
  isExpanded: boolean,
  toggleSection: (section: string) => void
): JSX.Element | null => {
  if (!data || (Array.isArray(data) && data.length === 0)) return null;

  return (
    <div className="mb-4 border rounded-md overflow-hidden border-gold-600">
      <div
        className="flex justify-between items-center px-4 py-2 bg-gold-200 cursor-pointer transition-colors"
        onClick={() => toggleSection(sectionKey)}
      >
        <h3 className="m-0 text-base font-semibold text-gold-900">{title}</h3>
        <div className="flex items-center gap-2">
          <Button
            className="rounded-md px-2 py-1 text-xs font-medium transition-colors hover:bg-gold-600"
            onClick={e => {
              e.stopPropagation();
              copyToClipboard(data);
            }}
          >
            Copy
          </Button>
          <span className={`text-xs transition-transform ${isExpanded ? '' : 'rotate-[-90deg]'}`}>
            {isExpanded ? '▼' : '▶'}
          </span>
        </div>
      </div>
      {isExpanded && (
        <pre className="m-0 p-3 bg-[#f8f8f8] overflow-x-auto font-mono text-xs text-[#333] whitespace-pre-wrap break-words w-full box-border">
          {JSON.stringify(data, null, 2)}
        </pre>
      )}
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

  return (
    <div className="mb-4 border rounded-md overflow-hidden">
      <div
        className="flex justify-between items-center px-4 py-2 bg-gold-200 cursor-pointer transition-colors"
        onClick={() => toggleSection(sectionKey)}
      >
        <h3 className="m-0 text-base font-semibold text-gold-700">{title}</h3>
        <div className="flex items-center gap-2">
          <Button
            onClick={e => {
              e.stopPropagation();
              copyToClipboard(actions);
            }}
          >
            Copy
          </Button>
          <span className={`text-xs transition-transform ${isExpanded ? '' : 'rotate-[-90deg]'}`}>
            {isExpanded ? '▼' : '▶'}
          </span>
        </div>
      </div>
      {isExpanded && (
        <div className="flex flex-col gap-3 p-4 max-h-[500px] overflow-y-auto">
          {actions.map((action, index) => (
            <div
              key={index}
              className="rounded-md border overflow-hidden bg-white shadow transition-transform hover:-translate-y-0.5 hover:shadow-lg"
            >
              <div className="px-4 py-2 text-white font-semibold text-sm uppercase tracking-wide bg-gold-500">
                {action.type}
              </div>
              <div className="p-3">
                {action.params && action.params.length > 0 ? (
                  <table className="w-full border-collapse text-sm">
                    <thead>
                      <tr>
                        <th className="bg-[#f8f8f8] font-semibold text-[#555] p-2 text-left">
                          Parameter
                        </th>
                        <th className="bg-[#f8f8f8] font-semibold text-[#555] p-2 text-left">
                          Value
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      {action.params.map((param, pIndex) => (
                        <tr key={pIndex}>
                          <td className="font-medium text-[#555] w-2/5 p-2">{param.name}</td>
                          <td className="font-mono bg-[#f9f9f9] p-2 rounded break-words max-w-[60%]">
                            {JSON.stringify(param.value)}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                ) : (
                  <div className="italic text-[#888] text-center p-2">No parameters</div>
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
    <div className="mb-4 border rounded-md overflow-hidden">
      <div
        className="flex justify-between items-center px-4 py-2 bg-gold-200 cursor-pointer transition-colors"
        onClick={() => toggleSection('prompt')}
      >
        <h3 className="m-0 text-base font-semibold text-gold-900">Final Prompt</h3>
        <div className="flex items-center gap-2">
          <Button
            className="bg-gold-500 text-background rounded-md px-2 py-1 text-xs font-medium transition-colors hover:bg-gold-700"
            onClick={e => {
              e.stopPropagation();
              copyToClipboard(lastResponse.final_prompt);
            }}
          >
            Copy
          </Button>
          <span className={`text-xs transition-transform ${isExpanded ? '' : 'rotate-[-90deg]'}`}>
            {isExpanded ? '▼' : '▶'}
          </span>
        </div>
      </div>
      {isExpanded && (
        <div className="p-4 bg-gold-50 overflow-y-auto text-sm leading-[1.5] max-h-[300px]">
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
    <div className="p-6 text-center bg-gold-50 border border-dashed rounded-md text-neutral-400">
      <p className="font-medium mb-2">{primaryText}</p>
      {secondaryText && <p className="mt-1">{secondaryText}</p>}
    </div>
  );
};
