import React from 'react'
import { Cpu, HardDrive, BatteryCharging, Server } from 'lucide-react'

export default function SystemStats({ stats }) {
  if (!stats) {
    return (
      <div className="stats-tiles">
        <div className="stat-tile">
          <Cpu size={20} color="var(--cyan-bright)" />
          <div className="stat-num">-- %</div>
          <div className="stat-lbl">CPU Usage</div>
        </div>
        <div className="stat-tile">
          <HardDrive size={20} color="var(--cyan-bright)" />
          <div className="stat-num">-- %</div>
          <div className="stat-lbl">RAM Usage</div>
        </div>
        <div className="stat-tile">
          <BatteryCharging size={20} color="var(--cyan-bright)" />
          <div className="stat-num">-- %</div>
          <div className="stat-lbl">Battery</div>
        </div>
        <div className="stat-tile">
          <Server size={20} color="var(--cyan-bright)" />
          <div className="stat-num">ONLINE</div>
          <div className="stat-lbl">OS Status</div>
        </div>
      </div>
    )
  }

  return (
    <div className="stats-tiles">
      <div className="stat-tile">
        <Cpu size={20} color="var(--cyan-bright)" />
        <div className="stat-num">{stats.cpu_percent}%</div>
        <div className="stat-lbl">CPU Load</div>
      </div>
      <div className="stat-tile">
        <HardDrive size={20} color="var(--cyan-bright)" />
        <div className="stat-num">{stats.memory_percent}%</div>
        <div className="stat-lbl">RAM ({stats.memory_used_gb}/{stats.memory_total_gb}GB)</div>
      </div>
      <div className="stat-tile">
        <BatteryCharging size={20} color="var(--gold-accent)" />
        <div className="stat-num">{stats.battery?.percent}%</div>
        <div className="stat-lbl">{stats.battery?.power_plugged ? 'Plugged In' : 'Battery'}</div>
      </div>
      <div className="stat-tile">
        <Server size={20} color="#22c55e" />
        <div className="stat-num" style={{ fontSize: '16px', color: '#22c55e' }}>{stats.os || 'Windows 11'}</div>
        <div className="stat-lbl">Host Telemetry</div>
      </div>
    </div>
  )
}
