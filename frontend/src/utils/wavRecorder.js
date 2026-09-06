export class WavRecorder {
  constructor() {
    this.audioContext = null
    this.mediaStream = null
    this.processor = null
    this.input = null
    this.pcmData = []
    this.sampleRate = 16000
    this.isRecording = false
  }

  async start() {
    this.pcmData = []
    this.mediaStream = await navigator.mediaDevices.getUserMedia({
      audio: {
        channelCount: 1,
        echoCancellation: true,
        noiseSuppression: true
      }
    })

    this.audioContext = new (window.AudioContext || window.webkitAudioContext)({
      sampleRate: this.sampleRate
    })
    this.sampleRate = this.audioContext.sampleRate

    this.input = this.audioContext.createMediaStreamSource(this.mediaStream)
    this.processor = this.audioContext.createScriptProcessor(4096, 1, 1)

    this.processor.onaudioprocess = (e) => {
      if (!this.isRecording) return
      const channel = e.inputBuffer.getChannelData(0)
      this.pcmData.push(new Float32Array(channel))
    }

    this.input.connect(this.processor)
    this.processor.connect(this.audioContext.destination)
    this.isRecording = true
  }

  async stop() {
    this.isRecording = false

    if (this.processor) {
      try { this.processor.disconnect() } catch (e) {}
      this.processor = null
    }
    if (this.input) {
      try { this.input.disconnect() } catch (e) {}
      this.input = null
    }
    if (this.mediaStream) {
      this.mediaStream.getTracks().forEach(track => track.stop())
      this.mediaStream = null
    }
    if (this.audioContext && this.audioContext.state !== 'closed') {
      try { await this.audioContext.close() } catch (e) {}
    }

    const totalLength = this.pcmData.reduce((acc, b) => acc + b.length, 0)
    if (totalLength === 0) return null

    const merged = new Float32Array(totalLength)
    let offset = 0
    for (const chunk of this.pcmData) {
      merged.set(chunk, offset)
      offset += chunk.length
    }

    return this.encodeWAV(merged, this.sampleRate)
  }

  encodeWAV(samples, sampleRate) {
    const buffer = new ArrayBuffer(44 + samples.length * 2)
    const view = new DataView(buffer)

    /* RIFF identifier */
    this.writeString(view, 0, 'RIFF')
    /* file length */
    view.setUint32(4, 36 + samples.length * 2, true)
    /* RIFF type */
    this.writeString(view, 8, 'WAVE')
    /* format chunk identifier */
    this.writeString(view, 12, 'fmt ')
    /* format chunk length */
    view.setUint32(16, 16, true)
    /* sample format (PCM) */
    view.setUint16(20, 1, true)
    /* channel count (1) */
    view.setUint16(22, 1, true)
    /* sample rate */
    view.setUint32(24, sampleRate, true)
    /* byte rate */
    view.setUint32(28, sampleRate * 2, true)
    /* block align */
    view.setUint16(32, 2, true)
    /* bits per sample */
    view.setUint16(34, 16, true)
    /* data chunk identifier */
    this.writeString(view, 36, 'data')
    /* data chunk length */
    view.setUint32(40, samples.length * 2, true)

    let offset = 44
    for (let i = 0; i < samples.length; i++, offset += 2) {
      const s = Math.max(-1, Math.min(1, samples[i]))
      view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7FFF, true)
    }

    return new Blob([view], { type: 'audio/wav' })
  }

  writeString(view, offset, string) {
    for (let i = 0; i < string.length; i++) {
      view.setUint8(offset + i, string.charCodeAt(i))
    }
  }
}
