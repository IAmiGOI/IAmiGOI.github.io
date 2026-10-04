// Tiny BM25 search over the docs chunks. No embeddings, no extra service: deterministic, free and fast enough for ~200 chunks.

const STOP = new Set(('a an the and or but if then so of to in on at by for with from as is are was were be been it its this that these those i you he she we they '
    + 'me my your our do does did can could would should will how what which who why where when there here not no yes about into than also just more most some any').split(' '));

/** lowercase word tokens with a light plural / -ing / -ed strip, stop words removed */
export function tokenize(text) {
    return (String(text).toLowerCase().match(/[a-z0-9]+/g) ?? [])
        .filter(word => word.length > 1 && !STOP.has(word))
        .map(word => word.replace(/(ies)$/, 'y').replace(/(ing|ed|es|s)$/, m => (word.length - m.length >= 3 ? '' : m)));
}

// Words people use for things the docs name differently. Expanded terms count for less than the user's own words.
const SYNONYMS = {
    remember: ['memory', 'summary'], forget: ['summary', 'memory'], context: ['summary'], long: ['summary'], history: ['summary'],
    free: ['cost', 'price', 'pollinations'], cost: ['price'], price: ['cost'], paid: ['cost'],
    picture: ['painter', 'image'], image: ['painter', 'picture'], draw: ['painter', 'picture'], illustration: ['painter'],
    song: ['music'], sound: ['music'], audio: ['music'], soundtrack: ['music'],
    health: ['tracker'], mood: ['tracker'], stats: ['tracker'], clock: ['time'], date: ['time'],
    plugin: ['module'], extension: ['module'], develop: ['module', 'write'], code: ['module', 'write'],
    broken: ['troubleshooting'], error: ['troubleshooting'], fail: ['troubleshooting'], bug: ['troubleshooting'],
};

/** @param {Array<{title:string,text:string}>} chunks */
export function buildIndex(chunks) {
    const docs = chunks.map(chunk => {
        const tokens = [...tokenize(chunk.title), ...tokenize(chunk.title), ...tokenize(chunk.text)];   // the title counts double
        const freq = new Map();
        for (const token of tokens) freq.set(token, (freq.get(token) ?? 0) + 1);
        return { freq, length: tokens.length, boost: chunk.boost ?? 1 };
    });
    const df = new Map();
    for (const doc of docs) for (const token of doc.freq.keys()) df.set(token, (df.get(token) ?? 0) + 1);
    const avg = docs.reduce((sum, doc) => sum + doc.length, 0) / Math.max(1, docs.length);
    return { docs, df, avg, size: docs.length };
}

/** Best `k` chunk indexes for a query, with scores. */
export function search(index, query, k = 5) {
    const own = [...new Set(tokenize(query))];
    if (!own.length) return [];
    const weights = new Map(own.map(term => [term, 1]));
    for (const term of own) for (const alias of tokenize((SYNONYMS[term] ?? []).join(' '))) if (!weights.has(alias)) weights.set(alias, 0.6);
    const terms = [...weights.keys()];
    const k1 = 1.4, b = 0.75;
    const scored = index.docs.map((doc, i) => {
        let score = 0;
        for (const term of terms) {
            const f = doc.freq.get(term);
            if (!f) continue;
            const n = index.df.get(term) ?? 0;
            const idf = Math.log(1 + (index.size - n + 0.5) / (n + 0.5));
            score += weights.get(term) * idf * (f * (k1 + 1)) / (f + k1 * (1 - b + b * doc.length / index.avg));
        }
        return { i, score: score * doc.boost };
    }).filter(item => item.score > 0);
    scored.sort((a, b2) => b2.score - a.score);
    return scored.slice(0, k);
}
