/**
 * SCI-FI WEB AUDIO & TACTICAL VOICE SYNTHESIZER
 * Zero external audio files required - synthesizes futuristic sound effects in real-time.
 */

const SFXEngine = {
    audioCtx: null,
    soundEnabled: true,
    voiceEnabled: true,

    init() {
        // Initialize Web Audio Context on first user interaction
        const initAudio = () => {
            if (!this.audioCtx) {
                const AudioContext = window.AudioContext || window.webkitAudioContext;
                if (AudioContext) {
                    this.audioCtx = new AudioContext();
                }
            }
            window.removeEventListener('click', initAudio);
        };
        window.addEventListener('click', initAudio);
    },

    toggleSound() {
        this.soundEnabled = !this.soundEnabled;
        return this.soundEnabled;
    },

    /**
     * Synthesize Sci-Fi UI Click Beep
     */
    playClick() {
        if (!this.soundEnabled || !this.audioCtx) return;

        try {
            const osc = this.audioCtx.createOscillator();
            const gain = this.audioCtx.createGain();

            osc.type = 'sine';
            osc.frequency.setValueAtTime(800, this.audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(1200, this.audioCtx.currentTime + 0.05);

            gain.gain.setValueAtTime(0.12, this.audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, this.audioCtx.currentTime + 0.05);

            osc.connect(gain);
            gain.connect(this.audioCtx.destination);

            osc.start();
            osc.stop(this.audioCtx.currentTime + 0.05);
        } catch (e) {
            // Audio context gesture restrictions
        }
    },

    /**
     * Synthesize Alert / Warning Ping
     */
    playAlert() {
        if (!this.soundEnabled || !this.audioCtx) return;

        try {
            const osc = this.audioCtx.createOscillator();
            const gain = this.audioCtx.createGain();

            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(440, this.audioCtx.currentTime);
            osc.frequency.linearRampToValueAtTime(880, this.audioCtx.currentTime + 0.15);

            gain.gain.setValueAtTime(0.15, this.audioCtx.currentTime);
            gain.gain.linearRampToValueAtTime(0.01, this.audioCtx.currentTime + 0.15);

            osc.connect(gain);
            gain.connect(this.audioCtx.destination);

            osc.start();
            osc.stop(this.audioCtx.currentTime + 0.15);
        } catch (e) {
            // Audio context gesture restrictions
        }
    },

    /**
     * Tactical Web Speech Voice Announcement
     */
    speak(text) {
        if (!this.voiceEnabled || !('speechSynthesis' in window)) return;

        window.speechSynthesis.cancel(); // stop current
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 1.05;
        utterance.pitch = 0.9;
        utterance.volume = 0.7;

        // Try to pick an English voice
        const voices = window.speechSynthesis.getVoices();
        const engVoice = voices.find(v => v.lang.includes('en'));
        if (engVoice) utterance.voice = engVoice;

        window.speechSynthesis.speak(utterance);
    }
};
