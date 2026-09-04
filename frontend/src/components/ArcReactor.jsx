import React from 'react'

export default function ArcReactor({ state = 'idle', statusText = 'JARVIS ONLINE' }) {
  const isListening = state === 'listening'
  const isSpeaking = state === 'speaking'

  const glowColor = isListening ? '#f59e0b' : isSpeaking ? '#22c55e' : '#22d3ee'

  return (
    <div className="arc-reactor-container">
      <svg
        className={`reactor-svg ${isListening ? 'reactor-listening' : isSpeaking ? 'reactor-speaking' : ''}`}
        viewBox="0 0 200 200"
      >
        <defs>
          <radialGradient id="coreGlow" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor={glowColor} stopOpacity="1" />
            <stop offset="60%" stopColor={glowColor} stopOpacity="0.5" />
            <stop offset="100%" stopColor={glowColor} stopOpacity="0" />
          </radialGradient>
        </defs>

        {/* Outer Ring */}
        <circle
          cx="100" cy="100" r="90"
          fill="none" stroke={glowColor} strokeWidth="2" strokeDasharray="6 4"
          opacity="0.6"
        >
          <animateTransform
            attributeName="transform" type="rotate" from="0 100 100" to="360 100 100"
            dur="20s" repeatCount="indefinite"
          />
        </circle>

        {/* Inner Segment Ring */}
        <circle
          cx="100" cy="100" r="75"
          fill="none" stroke={glowColor} strokeWidth="4" strokeDasharray="20 10"
          opacity="0.8"
        >
          <animateTransform
            attributeName="transform" type="rotate" from="360 100 100" to="0 100 100"
            dur="12s" repeatCount="indefinite"
          />
        </circle>

        {/* Glowing Energy Coil Ring */}
        <circle cx="100" cy="100" r="55" fill="none" stroke={glowColor} strokeWidth="6" opacity="0.9" />

        {/* Tri-Node Energy Slots */}
        {[0, 60, 120, 180, 240, 300].map((angle, idx) => {
          const rad = (angle * Math.PI) / 180
          const x1 = 100 + 40 * Math.cos(rad)
          const y1 = 100 + 40 * Math.sin(rad)
          const x2 = 100 + 68 * Math.cos(rad)
          const y2 = 100 + 68 * Math.sin(rad)
          return (
            <line
              key={idx}
              x1={x1} y1={y1} x2={x2} y2={y2}
              stroke={glowColor} strokeWidth="3" opacity="0.8"
            />
          )
        })}

        {/* Core Glowing Orb */}
        <circle cx="100" cy="100" r="30" fill="url(#coreGlow)">
          <animate
            attributeName="r"
            values={isListening ? "28;36;28" : isSpeaking ? "26;34;26" : "28;31;28"}
            dur={isListening ? "0.8s" : isSpeaking ? "0.6s" : "3s"}
            repeatCount="indefinite"
          />
        </circle>

        {/* Center Tri-Triangle Logo */}
        <polygon points="100,82 114,108 86,108" fill="none" stroke="#ffffff" strokeWidth="2" opacity="0.9" />
      </svg>

      <div style={{ marginTop: '18px', textAlign: 'center' }}>
        <div style={{
          fontFamily: 'Orbitron',
          fontSize: '15px',
          fontWeight: 700,
          color: glowColor,
          letterSpacing: '2px',
          textShadow: `0 0 10px ${glowColor}`
        }}>
          {statusText}
        </div>
        <div style={{ fontSize: '12px', color: 'var(--text-muted)', marginTop: '4px', fontFamily: 'Share Tech Mono' }}>
          CORE FREQUENCY: 1.21 GW | INTERFACE ACTIVE
        </div>
      </div>
    </div>
  )
}
