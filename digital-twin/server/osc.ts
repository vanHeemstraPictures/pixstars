/**
 * Pixstars Digital Twin — OSC UDP Parser
 *
 * Minimal OSC message parser for receiving messages from the Conductor.
 * Parses OSC 1.0 messages (address + type-tagged arguments).
 */

export interface OSCMessage {
  address: string;
  args: (string | number | boolean)[];
}

/**
 * Parse a raw OSC packet (Buffer/Uint8Array) into an OSCMessage.
 */
export function parseOSC(data: Uint8Array): OSCMessage | null {
  try {
    const view = new DataView(data.buffer, data.byteOffset, data.byteLength);
    let offset = 0;

    // Read address (null-terminated, padded to 4 bytes)
    const address = readString(data, offset);
    offset += alignTo4(address.length + 1);

    // Read type tag string (starts with ',')
    const typeTag = readString(data, offset);
    offset += alignTo4(typeTag.length + 1);

    if (!typeTag.startsWith(",")) {
      return { address, args: [] };
    }

    const types = typeTag.slice(1); // Remove leading ','
    const args: (string | number | boolean)[] = [];

    for (const t of types) {
      switch (t) {
        case "s": {
          const s = readString(data, offset);
          offset += alignTo4(s.length + 1);
          args.push(s);
          break;
        }
        case "i": {
          args.push(view.getInt32(offset, false)); // big-endian
          offset += 4;
          break;
        }
        case "f": {
          args.push(view.getFloat32(offset, false));
          offset += 4;
          break;
        }
        case "T": {
          args.push(true);
          break;
        }
        case "F": {
          args.push(false);
          break;
        }
        default:
          // Skip unknown type
          break;
      }
    }

    return { address, args };
  } catch {
    return null;
  }
}

function readString(data: Uint8Array, offset: number): string {
  let end = offset;
  while (end < data.length && data[end] !== 0) {
    end++;
  }
  return new TextDecoder().decode(data.slice(offset, end));
}

function alignTo4(n: number): number {
  return Math.ceil(n / 4) * 4;
}
