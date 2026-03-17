import { apiRequest, formatJson, handleError } from "./api-client.js";

// ── 股票筛选 ──────────────────────────────────────────

export async function stock_filter({ filters = {}, page = 1, page_size = 20, sort_field, sort_order } = {}) {
  try {
    const body = { filters, page, pageSize: page_size };
    if (sort_field) body.sortField = sort_field;
    if (sort_order) body.sortOrder = sort_order;
    const data = await apiRequest("/stocks/filter", { method: "POST", body });
    const result = data.data || data;
    return formatJson({
      total: result.total || 0,
      count: (result.list || []).length,
      page,
      page_size,
      stocks: result.list || [],
      has_more: (result.total || 0) > page * page_size,
    });
  } catch (e) { return handleError(e); }
}

export async function stock_filter_options() {
  try {
    const data = await apiRequest("/stocks/filters/options");
    return formatJson(data.data || data);
  } catch (e) { return handleError(e); }
}

export async function stock_search({ keyword, limit = 10 }) {
  try {
    const data = await apiRequest("/stocks/search", { params: { keyword, limit } });
    return formatJson(data.data || data);
  } catch (e) { return handleError(e); }
}

export async function stock_detail({ code }) {
  try {
    const data = await apiRequest(`/stocks/${code}`);
    return formatJson(data.data || data);
  } catch (e) { return handleError(e); }
}

// ── 热门因子 ──────────────────────────────────────────

export async function hot_factor_list() {
  try {
    const data = await apiRequest("/hot-factors");
    return formatJson(data.data || data);
  } catch (e) { return handleError(e); }
}

export async function hot_factor_create({ name, factors }) {
  try {
    const data = await apiRequest("/hot-factors", { method: "POST", body: { name, factors } });
    return formatJson(data.data || data);
  } catch (e) { return handleError(e); }
}

export async function hot_factor_update({ preset_id, name, factors }) {
  try {
    const body = {};
    if (name != null) body.name = name;
    if (factors != null) body.factors = factors;
    const data = await apiRequest(`/hot-factors/${preset_id}`, { method: "PUT", body });
    return formatJson(data.data || data);
  } catch (e) { return handleError(e); }
}

export async function hot_factor_delete({ preset_id }) {
  try {
    const data = await apiRequest(`/hot-factors/${preset_id}`, { method: "DELETE" });
    return formatJson(data.data || data);
  } catch (e) { return handleError(e); }
}

export async function hot_factor_use({ preset_id }) {
  try {
    const data = await apiRequest(`/hot-factors/${preset_id}/use`, { method: "POST" });
    return formatJson(data.data || data);
  } catch (e) { return handleError(e); }
}

export async function hot_factor_sort({ preset_ids }) {
  try {
    const data = await apiRequest("/hot-factors/sort", { method: "PUT", body: { preset_ids } });
    return formatJson(data.data || data);
  } catch (e) { return handleError(e); }
}

// ── Jiuyan 数据 ──────────────────────────────────────

export async function jiuyan_stock_analysis({ stock_code }) {
  try {
    const data = await apiRequest("/jiuyan/stock-analysis", { params: { stock_code } });
    return formatJson(data.data || data);
  } catch (e) { return handleError(e); }
}

export async function jiuyan_stock_theme({ stock_code }) {
  try {
    const data = await apiRequest("/jiuyan/stock-theme", { params: { stock_code } });
    return formatJson(data.data || data);
  } catch (e) { return handleError(e); }
}

export async function jiuyan_articles({ article_ids }) {
  try {
    const data = await apiRequest("/jiuyan/articles", { params: { article_ids } });
    return formatJson(data.data || data);
  } catch (e) { return handleError(e); }
}

// ── 抖音热点 ──────────────────────────────────────────

export async function douyin_hotspot_list({ page = 1, page_size = 20 } = {}) {
  try {
    const data = await apiRequest("/douyin/hotspots", { params: { page, page_size } });
    return formatJson(data.data || data);
  } catch (e) { return handleError(e); }
}

export async function douyin_hotspot_detail({ aweme_id }) {
  try {
    const data = await apiRequest(`/douyin/hotspots/${aweme_id}`);
    return formatJson(data.data || data);
  } catch (e) { return handleError(e); }
}
