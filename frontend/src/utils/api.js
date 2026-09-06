import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 15000
})

export const jarvisApi = {
  sendCommand: (command, speak = true) => api.post('/command', { command, speak }),
  voiceListen: () => api.post('/voice-listen'),
  sendVoiceAudio: (audioBlob, speak = true) => {
    const formData = new FormData()
    formData.append('audio', audioBlob, 'voice_command.wav')
    formData.append('speak', String(speak))
    return api.post('/voice-audio', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  speak: (text) => api.post('/speak', { text }),
  getSystemStatus: () => api.get('/system-status'),
  getQuickActions: () => api.get('/quick-actions')
}

export default api
