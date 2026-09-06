import React from 'react'
import { Monitor, Terminal, Volume2, CloudSun, Clock, Chrome, Code, Play, Music } from 'lucide-react'

export default function QuickActions({ onTriggerAction }) {
  const actions = [
    { label: 'Play YouTube', command: 'play', icon: Play },
    { label: 'Spotify Music', command: 'play music on spotify', icon: Music },
    { label: 'Google Chrome', command: 'open chrome', icon: Chrome },
    { label: 'VS Code', command: 'open code', icon: Code },
    { label: 'Calculator', command: 'open calculator', icon: Monitor },
    { label: 'CMD Terminal', command: 'open cmd', icon: Terminal },
    { label: 'System Stats', command: 'system stats', icon: Monitor },
    { label: 'Live Weather', command: 'weather', icon: CloudSun },
    { label: 'Volume Up', command: 'volume up', icon: Volume2 },
    { label: 'Volume Down', command: 'volume down', icon: Volume2 },
    { label: 'Check Time', command: 'what time is it', icon: Clock }
  ]

  return (
    <div className="action-grid">
      {actions.map((act, index) => {
        const IconComponent = act.icon
        return (
          <button
            key={index}
            className="btn-hud"
            onClick={() => onTriggerAction(act.command)}
          >
            <IconComponent size={15} color="var(--cyan-bright)" />
            {act.label}
          </button>
        )
      })}
    </div>
  )
}
