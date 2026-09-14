/**
 * Shared fixtures for the equation tests — a tiny XML reader so the OMML in
 * those tests can be written the way Word actually emits it, rather than as
 * hand-built node literals. Loaded by tests/test-runner.js BEFORE the test
 * files, so both the LaTeX and the MathML suites can use it.
 *
 * Test-only: the shipped converters walk real DOM nodes; these plain objects
 * just present the same duck-typed surface (childNodes / nodeType / localName /
 * textContent / getAttribute / getAttributeNS).
 */

'use strict';

var OM_NS = {
    m: 'http://schemas.openxmlformats.org/officeDocument/2006/math',
    w: 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
};

function omText(node) {
    if (node.nodeType === 3) { return node.data; }
    var out = '';
    for (var i = 0; i < node.childNodes.length; i++) { out += omText(node.childNodes[i]); }
    return out;
}

function omDecode(s) {
    return s.replace(/&lt;/g, '<').replace(/&gt;/g, '>')
        .replace(/&quot;/g, '"').replace(/&amp;/g, '&');
}

function omElement(raw) {
    var head = raw.match(/^([^\s/>]+)([\s\S]*)$/);
    var qname = head[1];
    var attrsRaw = head[2] || '';
    var colon = qname.indexOf(':');
    var prefix = colon === -1 ? '' : qname.slice(0, colon);
    var local = colon === -1 ? qname : qname.slice(colon + 1);

    var attrs = {};
    var re = /([\w:.-]+)\s*=\s*"([^"]*)"/g;
    var a;
    while ((a = re.exec(attrsRaw)) !== null) { attrs[a[1]] = omDecode(a[2]); }

    var el = {
        nodeType: 1,
        localName: local,
        namespaceURI: OM_NS[prefix] || null,
        childNodes: [],
        getAttribute: function (name) {
            return Object.prototype.hasOwnProperty.call(attrs, name) ? attrs[name] : null;
        },
        getAttributeNS: function (ns, name) {
            for (var key in attrs) {
                if (!Object.prototype.hasOwnProperty.call(attrs, key)) { continue; }
                var c = key.indexOf(':');
                var p = c === -1 ? '' : key.slice(0, c);
                var l = c === -1 ? key : key.slice(c + 1);
                if (l === name && (OM_NS[p] || null) === ns) { return attrs[key]; }
            }
            return null;
        }
    };
    Object.defineProperty(el, 'textContent', { get: function () { return omText(el); } });
    return el;
}

/** Parse a small XML string into a DOM-shaped node tree. */
function omXml(xml) {
    var root = { nodeType: 1, localName: '#root', childNodes: [] };
    var stack = [root];
    var i = 0;

    function pushText(t) {
        if (t === '') { return; }
        stack[stack.length - 1].childNodes.push({ nodeType: 3, data: omDecode(t) });
    }

    while (i < xml.length) {
        var lt = xml.indexOf('<', i);
        if (lt === -1) { pushText(xml.slice(i)); break; }
        if (lt > i) { pushText(xml.slice(i, lt)); }

        var gt = xml.indexOf('>', lt);
        var raw = xml.slice(lt + 1, gt);

        if (raw.charAt(0) === '/') {
            stack.pop();
        } else if (raw.charAt(raw.length - 1) === '/') {
            stack[stack.length - 1].childNodes.push(omElement(raw.slice(0, -1)));
        } else {
            var el = omElement(raw);
            stack[stack.length - 1].childNodes.push(el);
            stack.push(el);
        }
        i = gt + 1;
    }
    return root.childNodes[0];
}

/** Wrap run text in the OMML a Word equation run actually produces. */
function omRun(text) {
    return '<m:r><w:rPr><w:rFonts w:ascii="Cambria Math"/></w:rPr><m:t>' + text + '</m:t></m:r>';
}

function omConvert(xml) {
    return new OmmlToMathml().convert(omXml(xml));
}

var OM_MATH_OPEN = '<math xmlns="http://www.w3.org/1998/Math/MathML">';

// ---------------------------------------------------------------------------

