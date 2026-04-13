/**
 * Pixstars Digital Twin — WebSocket Bridge Server (Deno)
 *
 * Receives OSC messages from the Show Conductor on UDP port 9004
 * and forwards them as JSON over WebSocket to all connected browser clients.
 *
 * Usage:
 *   deno run --allow-net digital-twin/server/main.ts
 *   deno run --allow-net digital-twin/server/main.ts --osc-port 9004 --ws-port 8765
 */

import { parseOSC } from "./osc.ts";
import { parseArgs } from "jsr:@std/cli/parse-args";

// ── Config ──────────────────────────────────────────────────────────────────

const args = parseArgs(Deno.args, {
  alias: { o: "osc-port", w: "ws-port" },
});

const OSC_PORT = Number(args["osc-port"] ?? 9004);
const WS_PORT = Number(args["ws-port"] ?? 8765);

// ── WebSocket Clients ───────────────────────────────────────────────────────

const wsClients = new Set<WebSocket>();

function broadcastJSON(data: Record<string, unknown>) {
  const json = JSON.stringify(data);
  for (const ws of wsClients) {
    if (ws.readyState === WebSocket.OPEN) {
      ws.send(json);
    }
  }
}

// ── WebSocket Server (Deno.serve) ───────────────────────────────────────────

Deno.serve({ port: WS_PORT }, (req) => {
  // Handle WebSocket upgrade
  if (req.headers.get("upgrade") === "websocket") {
    const { socket, response } = Deno.upgradeWebSocket(req);

    socket.addEventListener("open", () => {
      wsClients.add(socket);
      console.log(`  [WS] Client connected (${wsClients.size} total)`);

      // Send current state to new client
      socket.send(JSON.stringify({ type: "welcome", message: "Pixstars Digital Twin" }));
    });

    socket.addEventListener("close", () => {
      wsClients.delete(socket);
      console.log(`  [WS] Client disconnected (${wsClients.size} total)`);
    });

    socket.addEventListener("message", (event) => {
      // We don't expect messages from the browser (one-directional)
      console.log(`  [WS] Received from client: ${event.data}`);
    });

    return response;
  }

  // Serve a simple status page for non-WebSocket requests
  return new Response(
    JSON.stringify({
      service: "Pixstars Digital Twin Bridge",
      osc_port: OSC_PORT,
      ws_port: WS_PORT,
      clients: wsClients.size,
    }),
    { headers: { "content-type": "application/json", "access-control-allow-origin": "*" } },
  );
});

// ── OSC UDP Listener ────────────────────────────────────────────────────────

const udpSocket = Deno.listenDatagram({ port: OSC_PORT, transport: "udp" });

console.log("═".repeat(60));
console.log("  PIXSTARS DIGITAL TWIN — WebSocket Bridge");
console.log(`  OSC listener:  UDP port ${OSC_PORT}`);
console.log(`  WebSocket:     ws://localhost:${WS_PORT}`);
console.log("═".repeat(60));

let transportPlaying = false;

for await (const [data, _addr] of udpSocket) {
  try {
    const msg = parseOSC(data);
    if (!msg) continue;

    // Map OSC address to a typed event
    const event = mapOSCToEvent(msg.address, msg.args);
    if (event) {
      console.log(`  [OSC] ${msg.address} ${msg.args.join(" ")} → ${event.type}:${event.value}`);
      broadcastJSON(event as unknown as Record<string, unknown>);
    }
  } catch (err) {
    console.error(`  [OSC ERROR] ${err}`);
  }
}

// ── OSC → JSON Event Mapping ────────────────────────────────────────────────

interface StageEvent {
  type: string;
  value: string;
  timestamp: number;
}


function mapOSCToEvent(
  address: string,
  args: (string | number | boolean)[],
): StageEvent | null {
  const timestamp = Date.now();

  switch (address) {
    case "/lamp/state":
      return { type: "lamp", value: String(args[0] ?? ""), timestamp };

    case "/projection/scene":
      return { type: "projection", value: String(args[0] ?? ""), timestamp };

    case "/lighting/state":
      return { type: "lighting", value: String(args[0] ?? ""), timestamp };

    case "/transport_play":
      transportPlaying = true;
      return { type: "transport", value: "PLAYING", timestamp };

    case "/transport_stop":
      transportPlaying = false;
      return { type: "transport", value: "STOPPED", timestamp };

    case "/toggle_roll":
      transportPlaying = !transportPlaying;
      return { type: "transport", value: transportPlaying ? "PLAYING" : "STOPPED", timestamp };

    case "/transport/state":
      // Explicit transport state from conductor (more reliable than toggle)
      transportPlaying = args[0] === "PLAYING";
      return { type: "transport", value: String(args[0]), timestamp };

    case "/cue/name":
      return { type: "cue", value: String(args[0] ?? ""), timestamp };

    default:
      return null;
  }
}
