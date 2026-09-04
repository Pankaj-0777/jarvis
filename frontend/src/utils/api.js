import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 12000
})

export const jarvisApi = {
  sendCommand: (command, speak = true) => api.post('/command', { command, speak }),
  voiceListen: () => api.post('/voice-listen'),
  speak: (text) => api.post('/speak', { text }),
  getSystemStatus: () => api.get('/system-status'),
  getQuickActions: () => api.get('/quick-actions')
}

export default api
