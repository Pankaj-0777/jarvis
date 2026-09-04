import React, { useRef, useEffect } from 'react'

export default function Terminal({ logs = [] }) {
  const terminalEndRef = useRef(null)

  useEffect(() => {
    terminalEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [logs])

  return (
    <div className="terminal-window">
      <div className="terminal-line terminal-system">
        [SYSTEM INITIALIZED] JARVIS AI Kernel v1.0.0 Online. Listening on audio bus...
      </div>
      {logs.map((log, index) => (
        <div key={index} className="terminal-line">
          {log.type === 'user' && (
            <span className="terminal-user">
              <strong>USER &gt;</strong> {log.text}
            </span>
          )}
          {log.type === 'jarvis' && (
            <span className="terminal-jarvis">
              <strong>JARVIS &gt;</strong> {log.text}
            </span>
          )}
          {log.type === 'system' && (
            <span className="terminal-system">
              <strong>[SYS]</strong> {log.text}
            </span>
          )}
        </div>
      ))}
      <div ref={terminalEndRef} />
    </div>
  )
}
