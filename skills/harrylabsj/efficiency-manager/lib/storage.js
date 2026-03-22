/**
 * Storage Module - Local data persistence
 */

const fs = require('fs');
const path = require('path');

// Simple UUID v4 generator (no external dependency)
function uuidv4() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0;
    const v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

const STORAGE_DIR = path.join(process.env.HOME, '.openclaw', 'efficiency-manager');
const DATA_DIR = path.join(STORAGE_DIR, 'data');
const EVENTS_FILE = path.join(DATA_DIR, 'events.json');
const CONFIG_FILE = path.join(STORAGE_DIR, 'config.json');

// Default categories with best durations (in hours)
const DEFAULT_CATEGORIES = {
  work: { name: '工作', bestDuration: 1.8 },
  study: { name: '学习', bestDuration: 1.0 },
  exercise: { name: '运动', bestDuration: 0.75 },
  social: { name: '社交', bestDuration: 1.5 },
  rest: { name: '休息', bestDuration: 0.5 },
  entertainment: { name: '娱乐', bestDuration: 1.2 },
  chores: { name: '家务', bestDuration: 1.0 },
  other: { name: '其他', bestDuration: 1.0 }
};

const DEFAULT_CONFIG = {
  dayStartTime: '06:00',
  dayEndTime: '23:00',
  reportTime: '22:00',
  categories: DEFAULT_CATEGORIES,
  benchmarkSource: 'local'
};

/**
 * Initialize storage directories and files
 */
function initStorage() {
  if (!fs.existsSync(STORAGE_DIR)) {
    fs.mkdirSync(STORAGE_DIR, { recursive: true });
  }
  if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
  }
  if (!fs.existsSync(EVENTS_FILE)) {
    fs.writeFileSync(EVENTS_FILE, JSON.stringify([], null, 2));
  }
  if (!fs.existsSync(CONFIG_FILE)) {
    fs.writeFileSync(CONFIG_FILE, JSON.stringify(DEFAULT_CONFIG, null, 2));
  }
}

/**
 * Load all events with optional query filters
 * @param {Object} query - Query filters
 * @param {string} query.category - Filter by category
 * @param {string} query.date - Filter by date (YYYY-MM-DD)
 * @param {string} query.startDate - Start date for range
 * @param {string} query.endDate - End date for range
 * @returns {Array} Filtered events
 */
function loadEvents(query = {}) {
  initStorage();
  try {
    const data = fs.readFileSync(EVENTS_FILE, 'utf8');
    let events = JSON.parse(data);

    if (query.category) {
      events = events.filter(e => e.category === query.category);
    }

    if (query.date) {
      const targetDate = query.date;
      events = events.filter(e => {
        const eventDate = e.startTime.split('T')[0];
        return eventDate === targetDate;
      });
    }

    if (query.startDate && query.endDate) {
      events = events.filter(e => {
        const eventDate = e.startTime.split('T')[0];
        return eventDate >= query.startDate && eventDate <= query.endDate;
      });
    }

    return events.sort((a, b) => new Date(b.startTime) - new Date(a.startTime));
  } catch (e) {
    console.error('Failed to load events:', e.message);
    return [];
  }
}

/**
 * Save an event (create or update)
 * @param {Object} eventData - Event data
 * @returns {Object} Saved event
 */
function saveEvent(eventData) {
  initStorage();
  const events = loadEvents();

  const now = new Date().toISOString();
  const event = {
    id: eventData.id || uuidv4(),
    description: eventData.description,
    category: eventData.category,
    startTime: eventData.startTime,
    endTime: eventData.endTime,
    status: eventData.status || 'completed',
    notes: eventData.notes || '',
    tags: eventData.tags || [],
    createdAt: eventData.createdAt || now,
    updatedAt: now
  };

  const existingIndex = events.findIndex(e => e.id === event.id);
  if (existingIndex >= 0) {
    events[existingIndex] = { ...events[existingIndex], ...event, updatedAt: now };
  } else {
    events.push(event);
  }

  fs.writeFileSync(EVENTS_FILE, JSON.stringify(events, null, 2));
  return event;
}

/**
 * Delete an event by ID
 * @param {string} id - Event ID
 * @returns {boolean} Success
 */
function deleteEvent(id) {
  initStorage();
  const events = loadEvents();
  const filtered = events.filter(e => e.id !== id);

  if (filtered.length === events.length) {
    return false;
  }

  fs.writeFileSync(EVENTS_FILE, JSON.stringify(filtered, null, 2));
  return true;
}

/**
 * Delete all events
 */
function deleteAllEvents() {
  initStorage();
  fs.writeFileSync(EVENTS_FILE, JSON.stringify([], null, 2));
}

/**
 * Load user configuration
 * @returns {Object} User config
 */
function loadConfig() {
  initStorage();
  try {
    const data = fs.readFileSync(CONFIG_FILE, 'utf8');
    return { ...DEFAULT_CONFIG, ...JSON.parse(data) };
  } catch (e) {
    return DEFAULT_CONFIG;
  }
}

/**
 * Save user configuration
 * @param {Object} config - Config to save
 */
function saveConfig(config) {
  initStorage();
  const current = loadConfig();
  const merged = { ...current, ...config };
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(merged, null, 2));
}

/**
 * Get event by ID
 * @param {string} id - Event ID
 * @returns {Object|null} Event
 */
function getEventById(id) {
  const events = loadEvents();
  return events.find(e => e.id === id) || null;
}

/**
 * Get events by date range
 * @param {string} startDate - Start date (YYYY-MM-DD)
 * @param {string} endDate - End date (YYYY-MM-DD)
 * @returns {Array} Events
 */
function getEventsByDateRange(startDate, endDate) {
  return loadEvents({ startDate, endDate });
}

/**
 * Get dates that have events (for a month)
 * @param {number} year - Year
 * @param {number} month - Month (1-12)
 * @returns {Array} Dates with events
 */
function getEventDates(year, month) {
  const startDate = `${year}-${String(month).padStart(2, '0')}-01`;
  const endDate = `${year}-${String(month).padStart(2, '0')}-31`;
  const events = getEventsByDateRange(startDate, endDate);
  const dates = [...new Set(events.map(e => e.startTime.split('T')[0]))];
  return dates.sort();
}

module.exports = {
  initStorage,
  loadEvents,
  saveEvent,
  deleteEvent,
  deleteAllEvents,
  loadConfig,
  saveConfig,
  getEventById,
  getEventsByDateRange,
  getEventDates,
  DEFAULT_CATEGORIES,
  DEFAULT_CONFIG
};