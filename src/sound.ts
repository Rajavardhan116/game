/**
 * Web Audio API retro arcade sound synthesizer
 */

class SoundSynthesizer {
  private ctx: AudioContext | null = null;
  public enabled: boolean = true;

  private initCtx() {
    if (!this.ctx && typeof window !== 'undefined') {
      const AudioCtx = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
      if (AudioCtx) {
        this.ctx = new AudioCtx();
      }
    }
    if (this.ctx && this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
  }

  private playTone(freq: number, type: OscillatorType, startOffset: number, duration: number, gainVal: number) {
    if (!this.enabled) return;
    this.initCtx();
    if (!this.ctx) return;

    try {
      const now = this.ctx.currentTime + startOffset;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();

      osc.type = type;
      osc.frequency.setValueAtTime(freq, now);

      gain.gain.setValueAtTime(gainVal, now);
      gain.gain.exponentialRampToValueAtTime(0.0001, now + duration);

      osc.connect(gain);
      gain.connect(this.ctx.destination);

      osc.start(now);
      osc.stop(now + duration);
    } catch {
      // Audio autoplay policy catch
    }
  }

  public play(type: 'correct' | 'incorrect' | 'game_over' | 'level_up' | 'achievement' | 'click' | 'tick') {
    if (!this.enabled) return;

    if (type === 'click') {
      this.playTone(600, 'sine', 0, 0.04, 0.1);
    } else if (type === 'tick') {
      this.playTone(850, 'triangle', 0, 0.03, 0.06);
    } else if (type === 'correct') {
      this.playTone(523.25, 'sine', 0, 0.1, 0.18);      // C5
      this.playTone(659.25, 'sine', 0.08, 0.12, 0.22); // E5
      this.playTone(783.99, 'sine', 0.16, 0.22, 0.26); // G5
    } else if (type === 'incorrect') {
      this.playTone(220.0, 'sawtooth', 0, 0.15, 0.22);
      this.playTone(174.6, 'sawtooth', 0.12, 0.22, 0.22);
    } else if (type === 'level_up') {
      this.playTone(440.0, 'square', 0, 0.08, 0.12);
      this.playTone(554.37, 'square', 0.08, 0.08, 0.12);
      this.playTone(659.25, 'square', 0.16, 0.08, 0.12);
      this.playTone(880.0, 'square', 0.24, 0.28, 0.16);
    } else if (type === 'achievement') {
      this.playTone(659.25, 'sine', 0, 0.09, 0.18);
      this.playTone(830.61, 'sine', 0.08, 0.09, 0.18);
      this.playTone(987.77, 'sine', 0.16, 0.09, 0.18);
      this.playTone(1318.5, 'sine', 0.24, 0.25, 0.22);
    } else if (type === 'game_over') {
      this.playTone(392.0, 'triangle', 0, 0.18, 0.25);
      this.playTone(329.6, 'triangle', 0.16, 0.18, 0.25);
      this.playTone(261.6, 'triangle', 0.32, 0.18, 0.25);
      this.playTone(196.0, 'triangle', 0.48, 0.35, 0.3);
    }
  }
}

export const sound = new SoundSynthesizer();
