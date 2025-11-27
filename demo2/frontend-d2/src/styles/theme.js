// Theme tokens for PeerPreview UI
// Clear separation between severity (warm) and track categories (cool)

export const theme = {
  // Accent colors
  accent: {
    teal: '#5BAEB8',       // Primary accent - highlights, selections
    uiBlue: '#65B2E8',     // UI elements - section pills, figure pills
  },

  // Severity colors (warm spectrum)
  severity: {
    major: '#E5484D',      // Red - major issues
    minor: '#FFBE3C',      // Amber - minor issues
    low: '#65B2E8',        // UI Blue - low severity (info)
  },

  // Track categories
  track: {
    rigor: '#3E63DD',      // Blue - structure & reasoning
    clarity: '#8E4EC6',    // Purple - language & style
    counterpoint: '#C75A7A' // Rose - reviewer-style critique
  },

  // Action colors (buttons, interactive elements)
  action: {
    primary: '#5BAEB8',    // Teal accent for primary actions
    secondary: '#A0A0A0',  // Gray for secondary actions
  },

  // Background and neutral colors
  background: {
    primary: '#1D1D1D',
    secondary: '#232323',
    tertiary: '#252525',
    elevated: '#2A2A2A',
  },

  // Border colors
  border: {
    primary: '#2E2E2E',
    secondary: '#3A3A3A',
    hover: '#4A4A4A',
  },

  // Text colors
  text: {
    primary: '#FFFFFF',
    secondary: '#D0D0D0',
    tertiary: '#A0A0A0',
    muted: '#808080',
  }
};

// Helper functions to get colors with opacity
export const withOpacity = (color, opacity) => {
  // Convert hex to rgba
  const r = parseInt(color.slice(1, 3), 16);
  const g = parseInt(color.slice(3, 5), 16);
  const b = parseInt(color.slice(5, 7), 16);
  return `rgba(${r}, ${g}, ${b}, ${opacity})`;
};

// Track color utilities
export const getTrackColor = (track) => {
  const trackMap = {
    'A': theme.track.rigor,
    'B': theme.track.clarity,
    'C': theme.track.counterpoint,
  };
  return trackMap[track] || theme.text.muted;
};

// Severity color utilities
export const getSeverityColor = (severity) => {
  const severityMap = {
    'major': theme.severity.major,
    'high': theme.severity.major,
    'minor': theme.severity.minor,
    'medium': theme.severity.minor,
    'low': theme.severity.low,
  };
  return severityMap[severity] || theme.text.muted;
};
