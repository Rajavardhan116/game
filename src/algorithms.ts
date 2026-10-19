/**
 * Client-Side Algorithmic Engine (Mirroring Python backend/game/algorithms.py)
 */

export interface StepTrace {
  index: number;
  character: string;
  frequency: number;
  isUnique: boolean;
  isFirstUnique: boolean;
}

export interface AlgorithmAnalysis {
  rawSequence: string;
  normalizedSequence: string;
  result: string | null;
  frequencies: Record<string, number>;
  distinctUniqueChars: string[];
  steps: StepTrace[];
  explanation: string;
  freqMethodOperations: number;
  nestedMethodOperations: number;
  bothMethodsMatch: boolean;
  nestedResult: string | null;
}

export function normalizeSequence(seq: string, caseSensitive: boolean = true, ignoreSpaces: boolean = true): string {
  if (!seq) return '';
  let res = seq;
  if (!caseSensitive) res = res.toLowerCase();
  if (ignoreSpaces) res = res.replace(/\s+/g, '');
  return res;
}

export function firstNonRepeatingFrequency(seq: string, caseSensitive: boolean = true, ignoreSpaces: boolean = true): { result: string | null; operations: number; counts: Record<string, number> } {
  const normalized = normalizeSequence(seq, caseSensitive, ignoreSpaces);
  if (!normalized) return { result: null, operations: 0, counts: {} };

  let operations = 0;
  const counts: Record<string, number> = {};

  // Pass 1: Build frequencies (O(n))
  for (let i = 0; i < normalized.length; i++) {
    const ch = normalized[i];
    counts[ch] = (counts[ch] || 0) + 1;
    operations++;
  }

  // Pass 2: Scan left to right (O(n))
  for (let i = 0; i < normalized.length; i++) {
    const ch = normalized[i];
    operations++;
    if (counts[ch] === 1) {
      return { result: ch, operations, counts };
    }
  }

  return { result: null, operations, counts };
}

export function firstNonRepeatingNested(seq: string, caseSensitive: boolean = true, ignoreSpaces: boolean = true): { result: string | null; operations: number } {
  const normalized = normalizeSequence(seq, caseSensitive, ignoreSpaces);
  const n = normalized.length;
  if (n === 0) return { result: null, operations: 0 };

  let operations = 0;
  for (let i = 0; i < n; i++) {
    const candidate = normalized[i];
    let count = 0;
    for (let j = 0; j < n; j++) {
      operations++;
      if (normalized[j] === candidate) {
        count++;
        if (count > 1) break; // early exit optimization
      }
    }
    if (count === 1) {
      return { result: candidate, operations };
    }
  }

  return { result: null, operations };
}

export function explainFirstNonRepeating(seq: string, caseSensitive: boolean = true, ignoreSpaces: boolean = true): AlgorithmAnalysis {
  const normalized = normalizeSequence(seq, caseSensitive, ignoreSpaces);
  const freqRes = firstNonRepeatingFrequency(seq, caseSensitive, ignoreSpaces);
  const nestedRes = firstNonRepeatingNested(seq, caseSensitive, ignoreSpaces);

  const counts = freqRes.counts;
  const distinctUniqueChars: string[] = [];
  const seen = new Set<string>();

  for (let i = 0; i < normalized.length; i++) {
    const ch = normalized[i];
    if (counts[ch] === 1 && !seen.has(ch)) {
      seen.add(ch);
      distinctUniqueChars.push(ch);
    }
  }

  const firstUnique = distinctUniqueChars[0] || null;

  const steps: StepTrace[] = [];
  for (let idx = 0; idx < normalized.length; idx++) {
    const ch = normalized[idx];
    steps.push({
      index: idx,
      character: ch,
      frequency: counts[ch] || 0,
      isUnique: (counts[ch] === 1),
      isFirstUnique: (ch === firstUnique)
    });
  }

  let explanation = '';
  if (firstUnique) {
    const firstIdx = normalized.indexOf(firstUnique);
    explanation = `The first non-repeating character is '${firstUnique}' located at index ${firstIdx}. It occurs exactly 1 time in '${normalized}'.`;
    if (distinctUniqueChars.length > 1) {
      explanation += ` Other unique characters exist (${distinctUniqueChars.slice(1).map(c => `'${c}'`).join(', ')}), but '${firstUnique}' appears first in sequence order.`;
    }
  } else {
    explanation = `No non-repeating character exists in '${normalized}'. Every single character appears 2 or more times. The correct answer is 'None'.`;
  }

  return {
    rawSequence: seq,
    normalizedSequence: normalized,
    result: firstUnique,
    frequencies: counts,
    distinctUniqueChars,
    steps,
    explanation,
    freqMethodOperations: freqRes.operations,
    nestedMethodOperations: nestedRes.operations,
    bothMethodsMatch: (firstUnique === nestedRes.result),
    nestedResult: nestedRes.result
  };
}
