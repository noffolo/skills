// AudioWorklet processor — matches NuwaAI demo: 16kHz input, 100ms chunks (1600 samples)
class AudioProcessor extends AudioWorkletProcessor {
  static get parameterDescriptors() { return []; }

  constructor() {
    super();
    this.buffer = new Float32Array(6400);
    this.bufferIndex = 0;
    this.chunkSize = 1600; // 16kHz * 100ms
    this.port.onmessage = (e) => {
      if (e.data.type === 'reset' || e.data === 'stop') {
        this.bufferIndex = 0;
      }
    };
  }

  process(inputs) {
    const input = inputs[0];
    if (input.length > 0) {
      const channelData = input[0];
      for (let i = 0; i < channelData.length; i++) {
        if (this.bufferIndex < this.buffer.length) {
          this.buffer[this.bufferIndex++] = channelData[i];
        }
      }

      while (this.bufferIndex >= this.chunkSize) {
        const pcmData = new Int16Array(this.chunkSize);
        for (let i = 0; i < this.chunkSize; i++) {
          pcmData[i] = Math.max(-32768, Math.min(32767, this.buffer[i] * 32768));
        }

        this.port.postMessage({ type: 'audioData', data: pcmData.buffer }, [pcmData.buffer]);

        const remaining = this.bufferIndex - this.chunkSize;
        for (let i = 0; i < remaining; i++) {
          this.buffer[i] = this.buffer[this.chunkSize + i];
        }
        this.bufferIndex = remaining;
      }
    }
    return true;
  }
}

registerProcessor('pcm-processor', AudioProcessor);
