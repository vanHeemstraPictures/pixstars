/**
 * Pixstars Digital Twin — WebSocket Client
 *
 * Connects to the Deno bridge server and dispatches stage events.
 */

export interface StageEvent {
  type: "lamp" | "projection" | "lighting" | "transport" | "cue" | "welcome";
  value: string;
  timestamp: number;
}

export type StageEventHandler = (event: StageEvent) => void;

export class StageWebSocket {
  private ws: WebSocket | null = null;
  private handlers: StageEventHandler[] = [];
  private reconnectTimer: number | null = null;
  private _url: string;

  constructor(url = "ws://localhost:8765") {
    this._url = url;
  }

  connect(): void {
    this.ws = new WebSocket(this._url);

    this.ws.onopen = () => {
      console.log("[WS] Connected to bridge server");
      this.updateConnectionUI(true);
    };

    this.ws.onclose = () => {
      console.log("[WS] Disconnected — reconnecting in 2s...");
      this.updateConnectionUI(false);
      this.reconnectTimer = window.setTimeout(() => this.connect(), 2000);
    };

    this.ws.onerror = () => {
      this.ws?.close();
    };

    this.ws.onmessage = (event) => {
      try {
        const data: StageEvent = JSON.parse(event.data);
        this.updateHUD(data);
        for (const handler of this.handlers) {
          handler(data);
        }
      } catch (e) {
        console.warn("[WS] Failed to parse message:", event.data, e);
      }
    };
  }

  onEvent(handler: StageEventHandler): void {
    this.handlers.push(handler);
  }

  private updateConnectionUI(connected: boolean): void {
    const el = document.getElementById("connection");
    if (el) {
      el.textContent = connected ? "CONNECTED" : "DISCONNECTED";
      el.className = connected ? "connected" : "disconnected";
    }
  }

  private updateHUD(event: StageEvent): void {
    switch (event.type) {
      case "transport": {
        const el = document.getElementById("hudTransport");
        if (el) el.textContent = `Transport: ${event.value}`;
        break;
      }
      case "lamp": {
        const el = document.getElementById("hudLamp");
        if (el) el.textContent = `Lamp: ${event.value}`;
        break;
      }
      case "lighting": {
        const el = document.getElementById("hudLighting");
        if (el) el.textContent = `Lighting: ${event.value}`;
        break;
      }
      case "projection": {
        const el = document.getElementById("hudProjection");
        if (el) el.textContent = `Projection: ${event.value}`;
        break;
      }
      case "cue": {
        const el = document.getElementById("hudCue");
        if (el) el.textContent = `Cue: ${event.value}`;
        break;
      }
    }
  }

  disconnect(): void {
    if (this.reconnectTimer) clearTimeout(this.reconnectTimer);
    this.ws?.close();
  }
}
