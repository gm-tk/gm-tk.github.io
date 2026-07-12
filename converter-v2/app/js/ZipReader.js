/**
 * ZipReader.js
 * ===========================================================================
 * WHAT THIS FILE DOES:
 * Reads a .docx file (which is a standard ZIP archive) entirely in the
 * browser and returns its entries as text, with NO external library.
 *
 * HOW (THE INTERESTING PART):
 * A ZIP file ends with a "central directory" — a table of contents listing
 * every entry's name, compression method, sizes, and where its local header
 * sits. We:
 *   1. find the End Of Central Directory (EOCD) record near the file end,
 *   2. walk the central directory to map entry name → offsets,
 *   3. for a requested entry, jump to its local header, slice out the
 *      compressed bytes, and
 *   4. inflate them with the browser-native DecompressionStream
 *      ("deflate-raw") — the modern API that removes the need for JSZip.
 *
 * WHY NO LIBRARY:
 * The coding standards keep external libraries to an absolute minimum, and
 * docx files written by Word are well-behaved ZIPs (deflate or stored).
 * ~120 lines of commented native code beats a 100 KB dependency the team
 * would have to trust blind.
 *
 * WHEN TO WORK HERE:
 * Only if a writer-supplied docx fails to open. The likely cause would be
 * an exotic compression method (anything other than 0=stored / 8=deflate),
 * which this reader reports loudly rather than mis-reading.
 * ===========================================================================
 */

class ZipReader {

	#view;     // DataView over the whole file
	#bytes;    // Uint8Array over the whole file
	#entries;  // Map: entry name → { offset, compressedSize, size, method }

	/**
	 * @param {ArrayBuffer} buffer - the uploaded file's bytes
	 */
	constructor(buffer) {
		this.#view = new DataView(buffer);
		this.#bytes = new Uint8Array(buffer);
		this.#entries = this.#readCentralDirectory();
	};

	/**
	 * Does the archive contain this entry?
	 * @param {string} name - e.g. "word/document.xml"
	 * @returns {boolean}
	 */
	Has(name) {
		return this.#entries.has(name);
	};

	/**
	 * Extracts one entry and returns its content as a UTF-8 string.
	 *
	 * USAGE:
	 * const xml = await zip.ReadText("word/document.xml");
	 *
	 * @param {string} name - entry path inside the zip
	 * @returns {Promise<string>} decoded text
	 * @throws {Error} when the entry is missing or uses an unknown method
	 */
	async ReadText(name) {
		const entry = this.#entries.get(name);
		if (!entry) throw new Error(`ZipReader: no entry "${name}" in archive`);

		// --- local file header: confirm signature, then skip its variable
		// name/extra fields to find where the data actually starts.
		// Layout (offsets from header start): 26 = name length, 28 = extra
		// length, 30 = name bytes … then the compressed data.
		const sig = this.#view.getUint32(entry.offset, true);
		if (sig !== 0x04034b50) throw new Error(`ZipReader: bad local header for "${name}"`);
		const nameLen = this.#view.getUint16(entry.offset + 26, true);
		const extraLen = this.#view.getUint16(entry.offset + 28, true);
		const dataStart = entry.offset + 30 + nameLen + extraLen;
		const compressed = this.#bytes.subarray(dataStart, dataStart + entry.compressedSize);

		// --- method 0 = stored (no compression): decode directly
		if (entry.method === 0) return new TextDecoder().decode(compressed);

		// --- method 8 = deflate: inflate via the native stream API.
		// "deflate-raw" because ZIP stores raw deflate data (no zlib wrapper).
		if (entry.method === 8) {
			const stream = new Blob([compressed]).stream()
				.pipeThrough(new DecompressionStream("deflate-raw"));
			const buffer = await new Response(stream).arrayBuffer();
			return new TextDecoder().decode(buffer);
		}

		throw new Error(`ZipReader: unsupported compression method ${entry.method} for "${name}"`);
	};

	/**
	 * Finds the EOCD record and walks the central directory.
	 *
	 * WHY SCAN BACKWARDS:
	 * The EOCD sits at the very end of the file but may be followed by a
	 * ZIP comment (up to 65,535 bytes), so we scan back from the end for
	 * its signature 0x06054b50.
	 *
	 * @returns {Map<string, Object>} entry name → location info
	 */
	#readCentralDirectory() {
		const v = this.#view;
		// EOCD is at least 22 bytes; scan backwards for the signature
		let eocd = -1;
		const stop = Math.max(0, v.byteLength - 22 - 65535);
		for (let i = v.byteLength - 22; i >= stop; i--) {
			if (v.getUint32(i, true) === 0x06054b50) { eocd = i; break; }
		}
		if (eocd < 0) throw new Error("ZipReader: not a ZIP file (no end-of-central-directory record)");

		const count = v.getUint16(eocd + 10, true);      // total entries
		let p = v.getUint32(eocd + 16, true);            // central dir offset

		const entries = new Map();
		const decoder = new TextDecoder();
		for (let i = 0; i < count; i++) {
			if (v.getUint32(p, true) !== 0x02014b50) {
				throw new Error("ZipReader: corrupt central directory");
			}
			// central directory entry layout (offsets from entry start):
			// 10 = method, 20 = compressed size, 24 = uncompressed size,
			// 28/30/32 = name/extra/comment lengths, 42 = local header offset
			const method = v.getUint16(p + 10, true);
			const compressedSize = v.getUint32(p + 20, true);
			const size = v.getUint32(p + 24, true);
			const nameLen = v.getUint16(p + 28, true);
			const extraLen = v.getUint16(p + 30, true);
			const commentLen = v.getUint16(p + 32, true);
			const offset = v.getUint32(p + 42, true);
			const name = decoder.decode(this.#bytes.subarray(p + 46, p + 46 + nameLen));

			entries.set(name, { offset, compressedSize, size, method });
			p += 46 + nameLen + extraLen + commentLen;
		}
		return entries;
	};
}

// Node test-harness hook; browsers ignore it.
if (typeof module !== "undefined") module.exports = { ZipReader };
