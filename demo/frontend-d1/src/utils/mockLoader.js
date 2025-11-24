/**
 * Mock data loader for demo
 * Simulates API calls by loading static JSON files
 */

export async function loadManuscript() {
  const response = await fetch('/static/manuscript_demo.json')
  return response.json()
}

export async function loadIssues() {
  const response = await fetch('/static/issues_demo.json')
  return response.json()
}

// Simulate processing delay
export function simulateProcessing(ms = 3000) {
  return new Promise(resolve => setTimeout(resolve, ms))
}
