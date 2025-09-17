import { z } from 'zod';

/**
 * Skill weight overrides for exercises in a curated track context
 * Maps skillUuid to weight (0.0 to 1.0)
 */
export const SkillOverridesSchema = z.record(
  z.string(), // skillUuid
  z.number().min(0).max(1) // weight
);

export type SkillOverrides = z.infer<typeof SkillOverridesSchema>;