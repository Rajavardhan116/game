/**
 * Question Generator (Matching backend/game/questions.py)
 */

import { firstNonRepeatingFrequency } from './algorithms';

export interface Question {
  id: string;
  sequence: string;
  difficulty: 'easy' | 'medium' | 'hard' | 'expert';
  options: string[];
  correctAnswer: string;
  timeLimitSeconds: number;
  basePoints: number;
  hint: string;
  category: string;
}

export const CURATED_PUZZLES: Record<string, Array<{ seq: string; hint: string }>> = {
  easy: [
    { seq: "aabbcd", hint: "Look past 'a' and 'b' which both occur in pairs." },
    { seq: "swiss", hint: "'s' appears 3 times. What is the very first letter that only appears once?" },
    { seq: "hello", hint: "Count the 'l's carefully. What about the beginning of the word?" },
    { seq: "letter", hint: "Both 'e' and 't' repeat twice. Check remaining letters in order." },
    { seq: "apple", hint: "'p' is duplicated. Check from left to right." },
    { seq: "speed", hint: "Double 'e' repeats. What unique letter comes first?" },
  ],
  medium: [
    { seq: "programming", hint: "'r', 'g', and 'm' repeat. Scan from left to right for the first singleton." },
    { seq: "character", hint: "'c', 'a', and 'r' repeat. Notice which unique letter appears earliest." },
    { seq: "racecar", hint: "Is 'e' the only letter without a twin?" },
    { seq: "teammate", hint: "Look closely at 't', 'e', 'a', and 'm'." },
    { seq: "success", hint: "'s' and 'c' repeat. Which unique letter comes first?" },
    { seq: "repetition", hint: "'e', 't', and 'i' appear multiple times." },
  ],
  hard: [
    { seq: "aabbccdef", hint: "Multiple unique candidates exist ('d', 'e', 'f'). The rule requires the FIRST one." },
    { seq: "xyzxzywab", hint: "Scan in original order once you filter out all repeating characters." },
    { seq: "abacabadabacaba", hint: "A fractal-like pattern where 'a', 'b', and 'c' repeat heavily." },
    { seq: "abcdeabcdeX", hint: "Every character from a-e repeats twice before the unique character appears." },
    { seq: "112233445A6677", hint: "A sequence containing numbers and letters. Letters follow the same rule!" },
    { seq: "k!k!m@m@q#", hint: "Punctuation characters also follow the frequency rule." },
  ],
  expert: [
    { seq: "aabb", hint: "Every single character repeats. What special option represents this case?" },
    { seq: "x", hint: "A single character sequence. Can a character repeat if it stands alone?" },
    { seq: "abcdefgabcdefg", hint: "Full cycle repeat. Check if any character has a count of 1." },
    { seq: "1234554321", hint: "A numeric palindrome where every number repeats exactly twice." },
    { seq: "z9y8x7w6z9y8x7w6Q", hint: "High-complexity alphanumeric pattern with 1 isolated unique character." },
    { seq: "::::;;;;!!!!", hint: "All punctuation symbols. Are all symbols repeated?" },
  ]
};

export const DIFFICULTY_CONFIG = {
  easy: { timeLimit: 25, basePoints: 100 },
  medium: { timeLimit: 18, basePoints: 150 },
  hard: { timeLimit: 14, basePoints: 200 },
  expert: { timeLimit: 10, basePoints: 300 }
};

export function generateQuestion(difficulty: 'easy' | 'medium' | 'hard' | 'expert', index: number = 1): Question {
  const pool = CURATED_PUZZLES[difficulty] || CURATED_PUZZLES.easy;
  const item = pool[index % pool.length];
  const cfg = DIFFICULTY_CONFIG[difficulty];

  const res = firstNonRepeatingFrequency(item.seq);
  const correctStr = res.result !== null ? res.result : 'None';

  // Build options
  const optionsSet = new Set<string>();
  optionsSet.add(correctStr);

  // Add distinct characters from sequence
  const distinct = Array.from(new Set(item.seq.split('')));
  for (const ch of distinct) {
    if (ch !== correctStr) {
      optionsSet.add(ch);
      if (optionsSet.size >= 4) break;
    }
  }

  // Always consider 'None' as an option
  if (optionsSet.size < 4) optionsSet.add('None');

  const extra = ['z', 'q', 'k', 'm', 'x'];
  for (const ch of extra) {
    if (optionsSet.size >= 4) break;
    optionsSet.add(ch);
  }

  const options = Array.from(optionsSet).slice(0, 4);
  // Shuffle options deterministically
  options.sort(() => Math.sin(index * 997) - 0.5);

  return {
    id: `q_${difficulty}_${index}_${Date.now()}`,
    sequence: item.seq,
    difficulty,
    options,
    correctAnswer: correctStr,
    timeLimitSeconds: cfg.timeLimit,
    basePoints: cfg.basePoints,
    hint: item.hint,
    category: 'curated_puzzle'
  };
}
