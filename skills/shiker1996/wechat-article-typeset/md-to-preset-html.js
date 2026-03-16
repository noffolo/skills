#!/usr/bin/env node
/**
 * 将 Markdown 转换为预设主题 HTML 并保存
 */

import { readFileSync, writeFileSync } from 'fs'
import { getFullHtml } from './lib/utils/markdown.js'

const mdPath = process.argv[2]
const outputPath = process.argv[3]
const themeId = process.argv[4] || 'purple-elegant'
const layoutId = process.argv[5] || 'gradient'

if (!mdPath) {
  console.error('用法：node md-to-preset-html.js <input.md> <output.html> [themeId] [layoutId]')
  process.exit(1)
}

const md = readFileSync(mdPath, 'utf8')
const html = getFullHtml(md, themeId, 'default', layoutId, null, 'vscode-dark')

writeFileSync(outputPath, html, 'utf8')
console.log(`预设主题 HTML 已保存至：${outputPath}`)
