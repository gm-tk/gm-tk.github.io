import io, sys
# ROUND 340 — the url-only fence (LinkVideoUrlOnly) on both seams; run from app/js; LF preserved (newline="")
p='MediaBuilder.js'; s=io.open(p,encoding='utf-8',newline='').read()
assert '\r\n' not in s
old_b = r'''			const ba = String(nx.blackAfter ?? "");
			const url = nx.block?.links?.[0]?.target ?? (ba.match(_re)?.[0] ?? "");
			if (!url || !host.test(url)) return null;
			if (ba.replace(/https?:\/\/[^\s\]]+/g, "").replace(/\*/g, "").trim()) return null;   // a titled link stays a link
			return { item: nx, url };'''
new_b = r'''			const ba = String(nx.blackAfter ?? "");
			const url = nx.block?.links?.[0]?.target ?? (ba.match(_re)?.[0] ?? "");
			if (!url || !host.test(url)) return null;
			if (!this.LinkVideoUrlOnly(nx)) return null;   // a titled / prose link stays a link
			return { item: nx, url };'''
assert s.count(old_b)==1, s.count(old_b)
s=s.replace(old_b,new_b)
anchor = r'''	/**
	 * ROUND 340 (seam B) — the next unconsumed item after a url-less media element, when it is a'''
helper = r'''	/**
	 * ROUND 340 — the url-only test shared by both seams: the link item's WHOLE PARAGRAPH (its
	 * docx block) carries no visible words once the red tag spans, the urls and the bold
	 * markers are removed — the measurement's `words 0` (gold EMBED 0.90). `blackAfter` alone
	 * is NOT enough: a trailing "[link] URL" after a prose sentence ("If you need help reading
	 * the bar chart then click on this link to watch a video [link] https://…" — HPRE203,
	 * TEFUN07, XDLS908) has an empty blackAfter but 18–31 visible words before the tag, and
	 * the gold anchors that phrase inline (the prose form the class excludes, gold ANCHOR).
	 */
	static LinkVideoUrlOnly(it) {
		const RED = /\u{1f534}\[RED TEXT\][\s\S]*?\[\/RED TEXT\]\u{1f534}/gu;
		const src = it?.block?.text != null ? String(it.block.text) : String(it?.blackAfter ?? "");
		return !src.replace(RED, " ").replace(/https?:\/\/[^\s\]\)"<>]+/g, " ").replace(/\*/g, "").trim();
	};

'''
assert s.count(anchor)==1
s=s.replace(anchor, helper+anchor)
io.open(p,'w',encoding='utf-8',newline='').write(s)
p='ContentConverter.js'; s=io.open(p,encoding='utf-8',newline='').read()
assert '\r\n' not in s
old_a = r'''			// elements.external_link_video_embed; env LINKVID_OFF. The url-only test is the
			// same `!labelText` the r76 rule uses; MediaBuilder.media over the item alone
			// reads the url from its block link / own line and drops that line (the r80
			// title-drop), so nothing but the embed ships.
			if (MediaBuilder.LinkVideoEmbedOn(tpl) && isExtLink && !labelText
				&& MediaBuilder.LinkVideoHost(tpl).test(url)) {'''
new_a = r'''			// elements.external_link_video_embed; env LINKVID_OFF. The url-only test is the
			// r76 `!labelText` AND MediaBuilder.LinkVideoUrlOnly — the whole paragraph block
			// has no visible words (a trailing tag after a prose sentence has an empty
			// blackAfter but is the gold's inline ANCHOR — HPRE203 / TEFUN07 / XDLS908, found
			// by the 416-module probe); MediaBuilder.media over the item alone reads the url
			// from its block link / own line and drops that line (the r80 title-drop), so
			// nothing but the embed ships.
			if (MediaBuilder.LinkVideoEmbedOn(tpl) && isExtLink && !labelText
				&& MediaBuilder.LinkVideoUrlOnly(it)
				&& MediaBuilder.LinkVideoHost(tpl).test(url)) {'''
assert s.count(old_a)==1
s=s.replace(old_a,new_a)
io.open(p,'w',encoding='utf-8',newline='').write(s)
print("patched")
