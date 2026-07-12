/**
 * ZipWriter.js
 * ===========================================================================
 * WHAT THIS FILE DOES:
 * Builds a downloadable .zip of the conversion outputs entirely in the
 * browser, with no external library. Entries are STORED (no compression):
 * module HTML pages are small, and storing keeps the writer ~80 lines of
 * obvious code instead of a dependency.
 *
 * HOW A STORED ZIP IS LAID OUT (for the next maintainer):
 *   [local header + name + data]  × N entries
 *   [central directory entry]     × N        ← the table of contents
 *   [end-of-central-directory record]
 * Every entry needs a CRC-32 of its data — computed with the classic
 * table-driven algorithm below.
 * ===========================================================================
 */

class ZipWriter {

	// the 256-entry CRC table, built once on first use
	static #crcTable = null;

	/**
	 * Builds a zip Blob from named text files.
	 *
	 * USAGE:
	 * const blob = ZipWriter.Build([{ filename: "a.html", content: "…" }]);
	 *
	 * @param {Object[]} files - [{ filename, content }]
	 * @returns {Blob} application/zip
	 */
	static Build(files) {
		const encoder = new TextEncoder();
		const chunks = [];          // byte chunks in file order
		const central = [];         // central-directory chunks
		let offset = 0;             // running offset of local headers

		for (const f of files) {
			const name = encoder.encode(f.filename);
			const data = encoder.encode(f.content);
			const crc = this.#crc32(data);

			// ---- local file header (30 bytes + name) ---------------------
			const local = new DataView(new ArrayBuffer(30));
			local.setUint32(0, 0x04034b50, true);   // signature
			local.setUint16(4, 20, true);           // version needed
			local.setUint16(6, 0x0800, true);       // UTF-8 names flag
			local.setUint16(8, 0, true);            // method 0 = stored
			local.setUint16(10, 0, true);           // mod time (zero is fine)
			local.setUint16(12, 0, true);           // mod date
			local.setUint32(14, crc, true);
			local.setUint32(18, data.length, true); // compressed = raw (stored)
			local.setUint32(22, data.length, true); // uncompressed
			local.setUint16(26, name.length, true);
			local.setUint16(28, 0, true);           // extra length
			chunks.push(new Uint8Array(local.buffer), name, data);

			// ---- matching central-directory entry (46 bytes + name) ------
			const cd = new DataView(new ArrayBuffer(46));
			cd.setUint32(0, 0x02014b50, true);
			cd.setUint16(4, 20, true);              // version made by
			cd.setUint16(6, 20, true);              // version needed
			cd.setUint16(8, 0x0800, true);
			cd.setUint16(10, 0, true);              // stored
			cd.setUint32(16, crc, true);
			cd.setUint32(20, data.length, true);
			cd.setUint32(24, data.length, true);
			cd.setUint16(28, name.length, true);
			cd.setUint32(42, offset, true);         // where the local header sits
			central.push(new Uint8Array(cd.buffer), name);

			offset += 30 + name.length + data.length;
		}

		// ---- end-of-central-directory record ------------------------------
		const cdSize = central.reduce((n, c) => n + c.length, 0);
		const eocd = new DataView(new ArrayBuffer(22));
		eocd.setUint32(0, 0x06054b50, true);
		eocd.setUint16(8, files.length, true);      // entries on this disk
		eocd.setUint16(10, files.length, true);     // entries total
		eocd.setUint32(12, cdSize, true);
		eocd.setUint32(16, offset, true);           // central dir offset
		chunks.push(...central, new Uint8Array(eocd.buffer));

		return new Blob(chunks, { type: "application/zip" });
	};

	/**
	 * CRC-32 (the ZIP polynomial 0xEDB88320), table-driven.
	 * @param {Uint8Array} data
	 * @returns {number} unsigned 32-bit CRC
	 */
	static #crc32(data) {
		if (!this.#crcTable) {
			this.#crcTable = new Uint32Array(256);
			for (let n = 0; n < 256; n++) {
				let c = n;
				for (let k = 0; k < 8; k++) c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
				this.#crcTable[n] = c >>> 0;
			}
		}
		let crc = 0xFFFFFFFF;
		for (let i = 0; i < data.length; i++) {
			crc = this.#crcTable[(crc ^ data[i]) & 0xFF] ^ (crc >>> 8);
		}
		return (crc ^ 0xFFFFFFFF) >>> 0;
	};
}

// Node test-harness hook; browsers ignore it.
if (typeof module !== "undefined") module.exports = { ZipWriter };
