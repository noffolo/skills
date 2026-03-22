/**
 * Reporter Module - Report generation and formatting
 */

const { loadConfig } = require('../lib/storage');
const { getTimeSlotName } = require('../lib/analyzer');

/**
 * Get category name in Chinese
 */
function getCategoryName(category) {
  const names = {
    work: 'Work',
    study: 'Study',
    exercise: 'Exercise',
    social: 'Social',
    rest: 'Rest',
    entertainment: 'Entertainment',
    chores: 'Chores',
    other: 'Other'
  };
  return names[category] || category;
}

/**
 * Get emoji for category
 */
function getCategoryEmoji(category) {
  const emojis = {
    work: '[W]',
    study: '[S]',
    exercise: '[E]',
    social: '[O]',
    rest: '[R]',
    entertainment: '[G]',
    chores: '[C]',
    other: '[?]'
  };
  return emojis[category] || '[?]';
}

/**
 * Format category breakdown for display
 */
function formatCategoryBreakdown(breakdown) {
  if (!breakdown || breakdown.length === 0) {
    return 'No data';
  }
  
  const totalHours = breakdown.reduce((sum, c) => sum + c.totalDuration, 0);
  
  return breakdown.map(cat => {
    const percentage = totalHours > 0 ? Math.round((cat.totalDuration / totalHours) * 100) : 0;
    const name = getCategoryName(cat.category);
    
    return `${name}: ${cat.totalDuration}h (${percentage}%) | Avg: ${cat.avgDuration}h | Best: ${cat.bestDuration}h | Eff: ${cat.efficiency}%`;
  }).join('\n');
}

/**
 * Format best time slots for display
 */
function formatBestTimeSlots(bestSlots) {
  if (!bestSlots || bestSlots.length === 0) {
    return 'No data';
  }
  
  return bestSlots.map(slot => {
    const name = getCategoryName(slot.category);
    return `${name}: ${slot.slotName} (Eff: ${slot.efficiency}%)`;
  }).join('\n');
}

/**
 * Format suggestions for display
 */
function formatSuggestions(suggestions) {
  if (!suggestions || suggestions.length === 0) {
    return 'No suggestions';
  }
  
  const priorityMarks = { high: '[!]', medium: '[?]', low: '[-]' };
  
  return suggestions.map((s, i) => {
    let text = `${i + 1}. ${priorityMarks[s.priority]} ${s.title}\n   ${s.description}`;
    
    if (s.actionSteps && s.actionSteps.length > 0) {
      text += '\n   Steps:\n';
      s.actionSteps.forEach(step => {
        text += `   - ${step}\n`;
      });
    }
    
    return text;
  }).join('\n');
}

/**
 * Format daily report
 */
function formatDailyReport(report) {
  const date = report.dateRange.start;
  const summary = report.summary;
  
  let md = `# Efficiency Report - ${date}\n`;
  md += `Events: ${summary.totalEvents} | Hours: ${summary.totalHours}h | Completion: ${summary.completionRate}%\n\n`;
  
  md += `## Category Breakdown\n`;
  md += formatCategoryBreakdown(report.categoryBreakdown) + '\n\n';
  
  if (report.bestTimeSlots && report.bestTimeSlots.length > 0) {
    md += `## Best Time Slots\n`;
    md += formatBestTimeSlots(report.bestTimeSlots) + '\n\n';
  }
  
  if (report.suggestions && report.suggestions.length > 0) {
    md += `## Suggestions\n`;
    md += formatSuggestions(report.suggestions) + '\n';
  }
  
  return md;
}

/**
 * Format weekly report
 */
function formatWeeklyReport(report) {
  const { start, end } = report.dateRange;
  const summary = report.summary;
  
  let md = `# Weekly Report: ${start} to ${end}\n`;
  md += `Events: ${summary.totalEvents} | Hours: ${summary.totalHours}h | Daily Avg: ${summary.avgDailyHours}h\n\n`;
  
  md += `## Category Breakdown\n`;
  md += formatCategoryBreakdown(report.categoryBreakdown) + '\n\n';
  
  if (report.bestTimeSlots && report.bestTimeSlots.length > 0) {
    md += `## Best Time Slots\n`;
    md += formatBestTimeSlots(report.bestTimeSlots) + '\n\n';
  }
  
  if (report.suggestions && report.suggestions.length > 0) {
    md += `## Suggestions\n`;
    md += formatSuggestions(report.suggestions) + '\n';
  }
  
  return md;
}

/**
 * Format monthly report
 */
function formatMonthlyReport(report) {
  const { start, end } = report.dateRange;
  const [year, month] = start.split('-');
  const summary = report.summary;
  
  let md = `# Monthly Report: ${year}-${month}\n`;
  md += `Events: ${summary.totalEvents} | Hours: ${summary.totalHours}h | Daily Avg: ${summary.avgDailyHours}h\n\n`;
  
  md += `## Category Breakdown\n`;
  md += formatCategoryBreakdown(report.categoryBreakdown) + '\n\n';
  
  if (report.bestTimeSlots && report.bestTimeSlots.length > 0) {
    md += `## Best Time Slots\n`;
    md += formatBestTimeSlots(report.bestTimeSlots) + '\n\n';
  }
  
  if (report.suggestions && report.suggestions.length > 0) {
    md += `## Suggestions\n`;
    md += formatSuggestions(report.suggestions) + '\n';
  }
  
  return md;
}

/**
 * Format event list
 */
function formatEventList(events) {
  if (!events || events.length === 0) {
    return 'No events';
  }
  
  return events.map(e => {
    const name = getCategoryName(e.category);
    const date = e.startTime.split('T')[0];
    const start = e.startTime.split('T')[1] ? e.startTime.split('T')[1].slice(0, 5) : e.startTime.slice(11, 16);
    const end = e.endTime.split('T')[1] ? e.endTime.split('T')[1].slice(0, 5) : e.endTime.slice(11, 16);
    const status = e.status === 'completed' ? '[OK]' : e.status === 'interrupted' ? '[~]' : '[X]';
    
    return `${date} ${start}-${end} ${name} ${status} ${e.description}`;
  }).join('\n');
}

/**
 * Format schedule output
 */
function formatSchedule(schedule) {
  let md = `# Schedule Suggestion\n\n`;
  md += `Total Duration: ${schedule.totalDuration}h\n\n`;
  
  md += `## Schedule\n\n`;
  
  schedule.schedule.forEach((item, i) => {
    const name = getCategoryName(item.event.category);
    
    md += `${i + 1}. ${item.startTime} - ${item.endTime} ${item.event.description} (${name})\n`;
    md += `   Reason: ${item.reason}\n\n`;
  });
  
  if (schedule.warnings && schedule.warnings.length > 0) {
    md += `## Warnings\n`;
    schedule.warnings.forEach(w => {
      md += `- ${w}\n`;
    });
  }
  
  return md;
}

module.exports = {
  formatDailyReport,
  formatWeeklyReport,
  formatMonthlyReport,
  formatEventList,
  formatSchedule,
  getCategoryName,
  getCategoryEmoji
};