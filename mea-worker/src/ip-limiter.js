import { DurableObject } from 'cloudflare:workers';
import { decide } from './limits.js';

/** One instance per hashed IP (and one for the whole site). Holds the counters; the decision itself is `decide()`. */
export class IpLimiter extends DurableObject {
    async check(limits) {
        const state = (await this.ctx.storage.get('state')) ?? { stamps: [], day: '', count: 0 };
        const result = decide(state, Date.now(), limits);
        await this.ctx.storage.put('state', result.state);
        return { allowed: result.allowed, scope: result.scope, retryAfter: result.retryAfter, remainingToday: result.remainingToday };
    }
}
