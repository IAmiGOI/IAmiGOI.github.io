// Per-IP and global limits as one pure decision, so the same code runs in the Durable Object and in tests.

/**
 * @param {{ stamps: number[], day: string, count: number }} state  recent request times (ms), the current UTC day and its count
 * @param {number} now  ms since epoch
 * @param {{ burst: number, windowMs: number, daily: number }} limits  `burst` per `windowMs`, `daily` per UTC day (0 = unlimited)
 * @returns {{ allowed: boolean, scope?: 'minute' | 'day', retryAfter?: number, state: object, remainingToday: number }}
 */
export function decide(state, now, { burst, windowMs = 60_000, daily }) {
    const day = new Date(now).toISOString().slice(0, 10);
    const stamps = (state?.stamps ?? []).filter(stamp => now - stamp < windowMs);
    const count = state?.day === day ? state.count : 0;

    if (daily > 0 && count >= daily) {
        const tomorrow = Date.parse(day + 'T00:00:00Z') + 86_400_000;
        return { allowed: false, scope: 'day', retryAfter: Math.ceil((tomorrow - now) / 1000), state: { stamps, day, count }, remainingToday: 0 };
    }
    if (burst > 0 && stamps.length >= burst) {
        return { allowed: false, scope: 'minute', retryAfter: Math.max(1, Math.ceil((stamps[0] + windowMs - now) / 1000)), state: { stamps, day, count }, remainingToday: daily > 0 ? daily - count : -1 };
    }
    stamps.push(now);
    return { allowed: true, state: { stamps, day, count: count + 1 }, remainingToday: daily > 0 ? daily - count - 1 : -1 };
}
