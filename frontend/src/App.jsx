import React, { useState, useEffect, useRef } from 'react'
import { Mic, MicOff, Send, Cpu, Volume2, ShieldCheck, Zap, Radio } from 'lucide-react'
import ArcReactor from './components/ArcReactor'
import Terminal from './components/Terminal'
import SystemStats from './components/SystemStats'
import QuickActions from './components/QuickActions'
import { jarvisApi } from './utils/api'
import { WavRecorder } from './utils/wavRecorder'

export default function App() {
  const [commandInput, setCommandInput] = useState('')
  const [reactorState, setReactorState] = useState('idle') // 'idle' | 'listening' | 'speaking'
  const [statusText, setStatusText] = useState('JARVIS ONLINE')
  const [logs, setLogs] = useState([
    { type: 'system', text: '[JARVIS AI Kernel v1.0.0 Online. Standing by for directives.]' }
  ])
  const [systemStats, setSystemStats] = useState(null)
  const [voiceEnabled, setVoiceEnabled] = useState(true)
  const [isRecording, setIsRecording] = useState(false)

  const recorderRef = useRef(null)
  const autoStopTimerRef = useRef(null)

  const fetchStats = async () => {
    try {
      const res = await jarvisApi.getSystemStatus()
      if (res.data?.data) {
        setSystemStats(res.data.data)
      }
    } catch (err) {
      console.warn('System status check offline', err)
    }
  }

  useEffect(() => {
    fetchStats()
    const interval = setInterval(fetchStats, 5000)
    return () => clearInterval(interval)
  }, [])

  const handleSendCommand = async (cmdText = commandInput) => {
    if (!cmdText || !cmdText.trim()) return

    const textToSubmit = cmdText.trim()
    setCommandInput('')

    // Append to terminal
    setLogs(prev => [...prev, { type: 'user', text: textToSubmit }])
    setReactorState('speaking')
    setStatusText('PROCESSING COMMAND...')

    try {
      const res = await jarvisApi.sendCommand(textToSubmit, voiceEnabled)
      if (res.data?.data) {
        const jarvisReply = res.data.data.response
        setLogs(prev => [...prev, { type: 'jarvis', text: jarvisReply }])
        if (res.data.data.action_executed) {
          setLogs(prev => [...prev, { type: 'system', text: `Action Executed: ${res.data.data.action_details}` }])
        }
      }
    } catch (err) {
      setLogs(prev => [...prev, { type: 'system', text: 'Error connecting to JARVIS backend core.' }])
    } finally {
      setTimeout(() => {
        setReactorState('idle')
        setStatusText('JARVIS ONLINE')
      }, 1500)
    }
  }

  const stopAndProcessRecording = async () => {
    if (autoStopTimerRef.current) {
      clearTimeout(autoStopTimerRef.current)
      autoStopTimerRef.current = null
    }

    if (!recorderRef.current || !isRecording) return

    setIsRecording(false)
    setReactorState('speaking')
    setStatusText('TRANSCRIBING AUDIO BUS...')
    setLogs(prev => [...prev, { type: 'system', text: 'Transcribing voice buffer...' }])

    try {
      const wavBlob = await recorderRef.current.stop()
      recorderRef.current = null

      if (!wavBlob) {
        setLogs(prev => [...prev, { type: 'system', text: 'No audio captured.' }])
        setReactorState('idle')
        setStatusText('JARVIS ONLINE')
        return
      }

      const res = await jarvisApi.sendVoiceAudio(wavBlob, voiceEnabled)

      if (res.data?.heard_text) {
        setLogs(prev => [...prev, { type: 'user', text: res.data.heard_text }])
        if (res.data?.data?.response) {
          setLogs(prev => [...prev, { type: 'jarvis', text: res.data.data.response }])
        }
        if (res.data?.data?.action_executed) {
          setLogs(prev => [...prev, { type: 'system', text: `Action Executed: ${res.data.data.action_details}` }])
        }
      } else {
        setLogs(prev => [
          ...prev,
          { type: 'system', text: res.data?.message || 'Could not understand audio. Please try speaking clearly.' }
        ])
      }
    } catch (err) {
      console.error('Voice transcription error:', err)
      setLogs(prev => [...prev, { type: 'system', text: 'Audio transcription error or server unreachable.' }])
    } finally {
      setTimeout(() => {
        setReactorState('idle')
        setStatusText('JARVIS ONLINE')
      }, 1200)
    }
  }

  const handleToggleVoice = async () => {
    if (isRecording) {
      await stopAndProcessRecording()
      return
    }

    try {
      const recorder = new WavRecorder()
      recorderRef.current = recorder
      await recorder.start()

      setIsRecording(true)
      setReactorState('listening')
      setStatusText('RECORDING MICROPHONE BUFFER...')
      setLogs(prev => [
        ...prev,
        { type: 'system', text: '🎙️ Microphone listening. Speak your command now...' }
      ])

      // Auto-stop after 4 seconds of speech
      autoStopTimerRef.current = setTimeout(() => {
        stopAndProcessRecording()
      }, 4200)
    } catch (err) {
      console.error('Microphone capture error:', err)
      setLogs(prev => [
        ...prev,
        { type: 'system', text: 'Microphone access denied. Please click the camera/mic icon in your browser URL bar to allow microphone access.' }
      ])
      setIsRecording(false)
      setReactorState('idle')
      setStatusText('JARVIS ONLINE')
    }
  }

  return (
    <div className="jarvis-container">
      {/* Top Header */}
      <header className="hud-header">
        <div className="hud-title">
          <Zap color="var(--cyan-bright)" size={28} />
          JARVIS HUD
        </div>
        <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
          <button
            className="btn-hud"
            onClick={() => setVoiceEnabled(!voiceEnabled)}
            style={{ borderColor: voiceEnabled ? 'var(--cyan-bright)' : 'var(--red-alert)' }}
          >
            <Volume2 size={16} color={voiceEnabled ? 'var(--cyan-bright)' : 'var(--red-alert)'} />
            Voice Output: {voiceEnabled ? 'ON' : 'OFF'}
          </button>
          <span className="hud-status-badge">
            ● SYSTEM ACTIVE
          </span>
        </div>
      </header>

      {/* Main Grid */}
      <div className="hud-grid">
        {/* Left Column: ARC Reactor & Controls */}
        <div className="hud-panel" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
          <div>
            <div className="panel-title">
              <ShieldCheck size={18} />
              ARC Core Energy Visualizer
            </div>
            <ArcReactor state={reactorState} statusText={statusText} />
          </div>

          <div style={{ marginTop: '24px', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '16px' }}>
            <button
              className={`btn-mic ${isRecording ? 'listening' : ''}`}
              onClick={handleToggleVoice}
              style={{
                background: isRecording ? 'rgba(239, 68, 68, 0.25)' : undefined,
                borderColor: isRecording ? '#ef4444' : undefined
              }}
            >
              <Mic size={18} style={{ marginRight: '8px', verticalAlign: 'middle', animation: isRecording ? 'pulse 1s infinite' : 'none' }} />
              {isRecording ? '🔴 Recording... Click to Process' : '🎙️ Activate Voice Command'}
            </button>

            <form
              onSubmit={(e) => { e.preventDefault(); handleSendCommand(); }}
              className="command-input-group"
              style={{ width: '100%' }}
            >
              <input
                type="text"
                className="hud-input"
                placeholder="Type command (e.g. 'weather in tokyo', 'open chrome', 'system stats')..."
                value={commandInput}
                onChange={(e) => setCommandInput(e.target.value)}
              />
              <button type="submit" className="btn-hud" style={{ background: 'var(--cyan-bright)', color: '#030712' }}>
                <Send size={16} />
              </button>
            </form>
          </div>
        </div>

        {/* Right Column: Terminal & HUD Metrics */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          <div className="hud-panel">
            <div className="panel-title">
              <Cpu size={18} />
              System Telemetry HUD
            </div>
            <SystemStats stats={systemStats} />
          </div>

          <div className="hud-panel" style={{ flex: 1 }}>
            <div className="panel-title">
              Terminal Log Transcript
            </div>
            <Terminal logs={logs} />
          </div>

          <div className="hud-panel">
            <div className="panel-title">
              Quick HUD Automation Shortcuts
            </div>
            <QuickActions onTriggerAction={(cmd) => handleSendCommand(cmd)} />
          </div>
        </div>
      </div>
    </div>
  )
}
